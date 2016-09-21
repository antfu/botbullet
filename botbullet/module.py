
class Module:
    def __init__(self, bot=None, configures=None):
        class_dict = self.__class__.__dict__
        self.name = class_dict['name'].lower().strip()
        self.alias = class_dict.get('alias',None)
        self.help = class_dict.get('help','')
        self.helps = class_dict.get('helps',[])

        self.bot = bot
        self.configures = configures

        self.init()

    def init(self):
        pass

    def immerse(self, func):
        return self.bot.immerse(func)

    def handler(self, body, push):
        pass
