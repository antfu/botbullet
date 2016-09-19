from botbullet import Module

class BaseModule(Module):
    def __init__(self):
        super().__init__('bot')

    def handler(self, body, push, event_obj, monopolize=False):
        if body == 'modules':
            self.bot.reply('\n'.join(self.bot.modules.keys()), title="Modules")
        elif body == 'clear':
            self.bot.clear_session()
