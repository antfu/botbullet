
class Module:
    def __init__(self, name, alias=None, help=None, helps=None, bot=None, configures=None):
        self.name = name.lower().strip()
        self.bot = None
        self.help = help or ''
        self.helps = helps or {}
        self.bot = bot
        self.alias = alias
        self.configures = configures

    def immerse(self, func):
        return self.bot.immerse(func)

    def handler(self, body, push):
        pass
