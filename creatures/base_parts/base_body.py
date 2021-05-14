from abc import abstractmethod


class Body:
    def __init__(self, head, l_hands, r_hands, legs, back):
        self.head = head
        self._l_hands = l_hands
        self._r_hands = r_hands
        self._legs = legs
        self.back = back

        self.dead_parts = []

    @abstractmethod
    def update(self):
        self._update()

    def _update(self):
        for part in (self.head, self.back):
            if not part.alive:
                self.dead_parts.append(part)
            else:
                part.change_position()
        # if arm on 0 index -> to dead list
        for part in (self._l_hands, self._r_hands, self._legs):
            if part and not part[0].alive:
                self.dead_parts.append(part.pop(0))

    def l_hand(self):
        return self._l_hands[0]

    def r_hand(self):
        return self._r_hands[0]

    def legs(self):
        return self._legs[0]
