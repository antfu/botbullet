from model import Model

class BaseModel(Model):
    def __init__(self):
        super().__init__('bot')

    def handler(self, body, push, event_obj, monopolize=False):
        if body == 'models':
            self.bot.reply('\n'.join(bot.models.keys()), title="Models")
        elif body == 'clear':
            self.bot.clear_session()
