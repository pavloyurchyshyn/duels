DEFAULT_PORT = 5555

HOST_ADDRESS = {
    'ip': '',
    'port': '',
}


def update_host_address(text):
    text = text.split(':')
    HOST_ADDRESS['ip'] = text[0]
    HOST_ADDRESS['port'] = text[1]

