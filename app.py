import os
import json
import importlib
from shutil import copy2 as copy
from codecs import open
from botbullet import Bot, IndexedDict
from bilateral_configs_py import BilateralConfigs

default_configs = {
    "api_token": "",
    "modules": ["base", "hello", "eval"],
    "debug": False
}
configs_path = 'configs.json'

if os.name == 'nt':
    os.system('chcp 65001')


def load_configs(path, default_path):
    if not os.path.exists(path):
        copy(default_path, path)

    with open(path, 'r', 'utf-8') as f:
        configs = json.loads(f.read())
        return IndexedDict(configs)


def run():
    print('Starting Botbullet...')
    configs = BilateralConfigs(configs_path, default_value=default_configs)
    debug = configs.get('debug', False)
    if not configs.get('api_token', None):
        print('[!] Missing Pushbullet API token, please enter it:')
        api_token = input().strip()
        if not api_token:
            print('Exit')
            return
        configs['api_token'] = api_token

    print('Connecting...')
    bot = Bot(configs.api_token, debug=debug)
    modules = {}

    for module_name in configs.modules:
        try:
            if debug:
                print('Loading module', module_name, '... ', end='')
            module = importlib.import_module('modules.' + module_name)
            cls = module.export
            instance = cls()
            bot.use(instance)
            modules[module_name] = {"module": module,
                                    "cls": cls, "instance": instance}
        except Exception as e:
            if debug:
                print('Failed  <', str(e), '>')
        else:
            if debug:
                print('OK')

    bot.start()
    print('Success! Listening pushes... (Press Enter to stop the program)')
    input()
    print('Stoping...')
    bot.stop()
    print('Exit.')

if __name__ == '__main__':
    run()
