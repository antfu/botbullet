from botbullet import Module

class BaseModule(Module):
    def __init__(self):
        super().__init__('bot')

    def handler(self, body, push):
        if body == 'modules':
            push.reply('\n'.join(self.bot.modules.keys()), title="Modules")
        elif body == 'clear':
            push.clear_session()

export = BaseModule
