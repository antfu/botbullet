import os
import json
import importlib
from shutil import copy2 as copy
from codecs import open
from botbullet import Bot, IndexedDict

if os.name == 'nt':
    os.system('chcp 65001')

def load_configs(path, default_path):
    if not os.path.exists(path):
        copy(default_path, path)

    with open(path, 'r', 'utf-8') as f:
        configs = json.loads(f.read())
        return IndexedDict(configs)

def run():
    configs = load_configs('configs.json','configs_default.json')
    bot = Bot(configs.api_token, debug=configs.get('debug',False))
    modules = {}

    for module_name in configs.modules:
        module = importlib.import_module('modules.'+module_name)
        cls = module.export
        instance = cls()
        bot.use(instance)
        modules[module_name] = {"module":module, "cls": cls, "instance": instance}

    bot.start()
    input('Start: ')
    bot.stop()

if __name__ == '__main__':
    run()
