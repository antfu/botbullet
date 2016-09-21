from .bot import Bot
from biconfigs import BiConfigs, BiDict

default_configs = {
    "api_token": "",
    "modules": ["base", "hello"],
    "debug": False
}
configs_path = 'configs.json'

def InitConfigs(filepath=None):
    if not filepath:
        filepath = configs_path
    return BiConfigs(filepath, default_value=default_configs)

class App:
    def __init__(self, api_token, name='Botbullet', configures=None, debug=False):
        self.api_token = api_token
        self.name = name
        self.bot = None
        self.configs = configures
        self.debug = debug
        self.connected = False
        self.listening = False

        if not self.configs:
            self.configs = BiConfigs(configs_path, default_value=default_configs)

        if not isinstance(self.configs, BiDict):
            raise TypeError("configures should be biconfigs.BiDict")

        self.module_configs = self.configs.get_set('modules_configs', {})


    def connect(self):
        if self.connected:
            return
        self.bot = Bot(self.api_token, debug=self.debug, module_configs=self.module_configs)
        self.connected = True

    def load_modules(self):
        self.bot.load_modules(self.configs.modules)

    def use_module(self, modules):
        if not isinstance(modules, list):
            modules = [modules]

        for m in modules:
            self.bot.use(m)

    def listen(self):
        if not self.bot:
            self.connect()
        self.bot.start()
        self.listening = True

    def stop(self):
        if self.connected and self.listening and self.bot:
            self.bot.stop()
            self.listening = False
