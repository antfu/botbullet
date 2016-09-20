import os
import json
import importlib
import sys
import signal
import traceback
from shutil import copy2 as copy
from codecs import open
from botbullet import Bot, IndexedDict
from biconfigs import BiConfigs, BiDict

default_configs = {
    "api_token": "",
    "modules": ["base", "hello", "eval"],
    "debug": False
}
configs_path = 'configs.json'

if os.name == 'nt':
    os.system('chcp 65001')

class App:
    def __init__(self, api_token, name='Botbullet', configures=None, debug=False):
        self.api_token = api_token
        self.name = name
        self.bot = None
        self.configs = configures
        self.debug = debug

        if not self.configs:
            self.configs = BiConfigs(configs_path, default_value=default_configs)

        if not isinstance(self.configs, BiDict):
            raise TypeError("configures should be biconfigs.BiDict")

        self.module_configs = self.configs.get_set('modules_configs', {})


    def connect(self):
        self.bot = Bot(self.api_token, debug=self.debug, module_configs=self.module_configs)

    def load_modules(self):
        self.bot.load_modules(self.configs.modules)

    def use_module(self, modules):
        if not isinstance(modules, list):
            modules = [modules]

        for m in modules:
            pass

    def start(self):
        if not self.bot:
            self.connect()
        self.bot.start()

    def stop(self):
        if self.bot:
            self.bot.stop()

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

    app = App(api_token, configures=configs, debug=debug)
    print('Connecting...')
    app.connect()

    def signal_handler(signal, frame):
        #print('You pressed Ctrl+C!')
        app.stop()
        print('Exit.')
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    app.load_modules()
    app.start()

    print('Listening pushes... (Press Enter to stop the program)')
    input()
    print('Stoping...')
    app.stop()
    print('Exit.')

if __name__ == '__main__':
    run()
