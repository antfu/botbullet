import os
import json
import importlib
import sys
import signal
import traceback
from shutil import copy2 as copy
from codecs import open
from botbullet import Bot, IndexedDict
from biconfigs import BiConfigs

default_configs = {
    "api_token": "",
    "modules": ["base", "hello", "eval"],
    "debug": False
}
configs_path = 'configs.json'

if os.name == 'nt':
    os.system('chcp 65001')

def run():
    print('Starting Botbullet...')
    configs = BiConfigs(configs_path, default_value=default_configs)
    modules_configs = configs.get_set('modules_configs', {})
    debug = configs.get_set('debug', False)
    api_token = configs.get('api_token', None)
    if not api_token:
        print('[!] Missing Pushbullet API token, please enter it:')
        api_token = input().strip()
        if not api_token:
            print('Exit')
            return
        configs['api_token'] = api_token

    print('Connecting...')
    bot = Bot(api_token, debug=debug)
    modules = {}

    bot.load_modules(configs.modules, modules_configs)

    def signal_handler(signal, frame):
        #print('You pressed Ctrl+C!')
        bot.stop()
        print('Exit.')
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)


    bot.start()
    print('Success! Listening pushes... (Press Enter to stop the program)')
    input()
    print('Stoping...')
    bot.stop()
    print('Exit.')

if __name__ == '__main__':
    run()
