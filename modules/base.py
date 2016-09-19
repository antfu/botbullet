from botbullet import Module

class BaseModule(Module):
    def __init__(self, **kwargs):
        super().__init__('bot', **kwargs)

    def handler(self, body, push):
        if body == 'modules':
            push.reply('\n'.join(self.bot.modules.keys()), title="Modules")
        elif body == 'clear':
            push.clear_session()
        elif body == 'clear all':
            self.bot.bullet.delete_pushes()
        elif body == 'reload':
            self.bot.reload_modules()
            push.reply('Reload finished',title='Bot')


export = BaseModule
