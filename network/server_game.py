from random import choice as random_choice
from common_things.global_clock import ROUND_CLOCK
from world_arena.base.arena_cell_obj import ArenaCellObject
from settings.network_settings.network_settings import GAME_TICK_RATE, END_ROUND_TIME, \
    TIME_TO_START_ROUND, WAIT_FOR_PLAYERS_TIME
from settings.network_settings.network_constants import *
from time import time, sleep
from player_and_spells.player.player_object import NetworkPlayerObject
import json
from _thread import start_new_thread


class ServerGame:
    """Part which processing all game logic"""

    TICK_RATE = GAME_TICK_RATE

    def __init__(self, max_number_of_rounds, time_for_round, teams,
                 cell_data, server, players_connections,
                 logger, players_objects):
        self.logger = logger

        self.ARENA = ArenaCellObject(data=cell_data, server_instance=True)
        self.server = server
        self.players_connections: dict = players_connections
        self.players_objects: dict = players_objects

        self.max_number_of_rounds = max_number_of_rounds
        self.round = 0
        self.time_for_round = time_for_round
        self.clock = ROUND_CLOCK

        self.teams = teams
        self.teams_scores = {team: 0 for team in self.teams if team != 'spectator'}
        self.scores_to_win = max_number_of_rounds // 2 + 1  # needed rounds to win, if 10 rounds -> 6 to win

        self.teams_names = self.server.team_names

        self.end_of_round_time = False

        self.teams_spawn_positions = {}
        self.prepare_spawn_positions()
        self.used_spawn_pos = set()

        self.clock.set_time(time=WAIT_FOR_PLAYERS_TIME)

        self.stages = {
            'round': self.ROUND,
            'prepare_to_round': self.PREPARING_TO_ROUND,
            'finish': self.FINISH_GAME,
            'waiting_for_players': self.WAITING_FOR_PLAYERS,
            'round_finished': self.ROUND_FINISHED,
        }

        self.current_stage = 'waiting_for_players'

        self.data_which_sending_to_players = {}
        self.updated_players_data_dict = {}

    def run_game(self):
        self.logger.info('Sever Game loop started.')
        update_delay = 1 / self.TICK_RATE
        self.logger.info(f'Tick rate {self.TICK_RATE}. Time per frame: {update_delay}')

        next_update = -1
        while self.server.alive:
            t = time()
            if t > next_update:
                next_update = t + update_delay
                self.clock.update(update_delay)
                self.stages[self.current_stage]()
            elif next_update - t - 0.05 > 0.01:
                sleep(next_update - t - 0.05)

        self.logger.info("Game cycle stopped")

    def WAITING_FOR_PLAYERS(self):
        self.ARENA.update()
        self.data_which_sending_to_players.clear()

        self.get_players_response_and_update_players(revise_after_death=True)

        self.data_which_sending_to_players[PLAYERS_DATA] = self.updated_players_data_dict
        self.data_which_sending_to_players[WAITING_PLAYERS] = True
        self.update_data_which_sending_by_common_data()

        self.update_data_which_sending_by_server_actions()

        self.send_updated_data_to_all_players()

        if self.clock.time > 0:
            if self.server.all_players_connected:
                self.current_stage = 'round'
            else:
                self.server.do_not_accept_connections = 0
                self.data_which_sending_to_players[SERVER_MESSAGE] = 'Not all players connected'
                self.send_updated_data_to_all_players()
                self.server.stop_server()

    def PREPARING_TO_ROUND(self):
        self.round += 1
        self.end_of_round_time = False

        self.used_spawn_pos.clear()

        for player in self.players_objects.copy().values():
            while 1:
                pos = random_choice(self.teams_spawn_positions[player.team])
                if pos not in self.used_spawn_pos:
                    self.used_spawn_pos.add(pos)
                    player.position = pos
                    player.spawn_position = pos
                    player.health_points = player.full_health_points
                    break

        self.clock.set_time(TIME_TO_START_ROUND)

        self.current_stage = 'round'

    def ROUND(self):
        self.ARENA.update()
        self.get_players_response_and_update_players(players_disabled=self.clock.time < 0)
        self.data_which_sending_to_players = self.updated_players_data_dict
        self.update_data_which_sending_by_server_actions()
        self.update_data_which_sending_by_common_data()

        dead_teams = self.get_dead_teams()

        if self.end_of_round_time and self.clock.time >= 0:
            # finish of round, last update
            if len(self.teams) - len(dead_teams) == 1:
                winner_team = tuple(dead_teams)[0]
                self.logger.info(f"TEAM {winner_team.upper()} WON")

            elif len(dead_teams) == 0:
                self.data_which_sending_to_players[ROUND_WINNER] = 'DRAW'
                self.logger.info(f"DRAW")

            self.current_stage = 'round_finished'

        else:
            if len(self.teams) - len(dead_teams) <= 1 or self.clock.time > self.time_for_round:
                self.clock.set_time(END_ROUND_TIME)
                self.end_of_round_time = True

        self.send_updated_data_to_all_players()

    def get_dead_teams(self):
        teams_health_points = {team: 0 for team in self.teams}
        for player in self.players_objects.values():
            teams_health_points[player.team] += player.health_points

        return [team for team, health_points in teams_health_points.items() if health_points < 0]

    def update_data_which_sending_by_common_data(self):
        self.data_which_sending_to_players[SERVER_TIME] = self.clock()
        self.data_which_sending_to_players[TEAM_SCORES] = tuple(self.teams_scores.values())
        self.data_which_sending_to_players[CURRENT_ROUND] = f"{self.round}/{self.max_number_of_rounds}"
        self.data_which_sending_to_players[DELETE_OBJECTS] = self.ARENA.dead_objects
        self.data_which_sending_to_players[ADD_OBJECTS] = self.ARENA.new_objects

    def update_data_which_sending_by_server_actions(self):
        if self.server.server_actions:
            self.data_which_sending_to_players[SERVER_ACTION] = self.server.server_actions.copy()
            self.server.server_actions.clear()

    def get_players_response_and_update_players(self, players_disabled=False, revise_after_death=False):
        for player_hash, player in self.players_objects.copy().items():
            try:
                new_player_data = self.players_connections[player_hash].recv(2048).decode()
            except Exception as e:
                self.server.disconnect_player(player_hash)
                self.logger.error(f'Failed to get info from {player_hash}: \n\t{e}')
            else:
                if new_player_data:
                    if "}{" in new_player_data:
                        new_player_data = f"{'{'}{new_player_data.split('}{')[-1]}"

                new_player_data = self.server.str_to_json(new_player_data)

                if player.alive:
                    player.angle = new_player_data.get(ANGLE)
                    commands = () if players_disabled else new_player_data.get('keyboard', ())
                    mouse_data = (0, 0, 0) if players_disabled else new_player_data.get('mouse_data', ((0, 0, 0),))[0]
                    player_action = player.update(commands=commands,
                                                  mouse_buttons=mouse_data,
                                                  mouse_pos=new_player_data.get('mouse_data', (1, (0, 0)))[1])

                    self.updated_players_data_dict[player_hash] = {
                        POSITION: player.position,
                        ANGLE: player.angle,
                        PLAYER_ACTION: player_action,
                        DAMAGED: player.damaged,
                        DEAD: player.dead,
                        HEALTH_POINTS: player.health_points,
                        PLAYER_SKIN: self.server.players_simple_data[player_hash][PLAYER_SKIN]
                    }
                else:
                    if revise_after_death:
                        player.position = player.spawn_position
                        player.hp = player.full_health_points

                    player_action = player.update()
                    self.updated_players_data_dict[player_hash] = {
                        POSITION: player.position,
                        ANGLE: player.angle,
                        PLAYER_ACTION: player_action,
                        DAMAGED: player.damaged,
                        DEAD: player.dead,
                        REVISE: revise_after_death,
                    }

    def ROUND_FINISHED(self):
        if self.round != self.max_number_of_rounds:
            self.current_stage = 'prepare_to_round'
        else:
            self.current_stage = 'finish'

    def FINISH_GAME(self):
        self.server.stop_server()

    def send_updated_data_to_all_players(self):
        start_new_thread(self.__send_updated_data_to_all_players, (self.data_which_sending_to_players.copy(),
                                                                   self.players_connections.copy(),
                                                                   self.logger,
                                                                   self.server))

    @staticmethod
    def __send_updated_data_to_all_players(data_which_sending_to_players, players_connections, logger, server):
        data = json.dumps(data_which_sending_to_players).encode()
        for player_hash, connection in players_connections.copy().items():
            try:
                connection.send(data)
            except Exception as e:
                logger.info(f"Failed to send data to {player_hash}: {e}")
                server.disconnect_player(player_hash)

    def prepare_spawn_positions(self):
        number_of_players_in_team = self.server.max_number_of_players // 2 + 1
        arena_x_size = arena_y_size = self.ARENA._size
        player_size = self.server.player_size
        arena_y_half_size = arena_y_size // 2

        for team_name in self.teams_names:
            self.teams_spawn_positions[team_name] = []

        for team, dx_position in (('red', player_size * 2), ('blue', arena_x_size - player_size * 2)):
            # for 3 players position_k is [-2, -1, 0, 1, 2]
            for position_k in range(-(number_of_players_in_team // 2 + 1), number_of_players_in_team // 2 + 2):
                self.teams_spawn_positions[team].append(
                    (dx_position, arena_y_half_size + int(player_size * position_k)))

    def get_spawn_position(self, team):
        while 1:
            position = random_choice(self.teams_spawn_positions[team])
            if position not in self.used_spawn_pos:
                self.used_spawn_pos.add(position)
                return position

    def __del__(self):
        self.server.stop_server()
        self.logger.info(f'Game server was closed.')
