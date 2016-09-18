

class Model:
    def __init__(self, name):
        self.name = name.lower().strip()
        self.bot = None

    def monopolize(self):
        self.bot.monopolize(self)

    def handler(self, body, push, event_obj, monopolize=False):
        pass

    def help(self):
        pass
