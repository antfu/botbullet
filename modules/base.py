from botbullet import Module


class BaseModule(Module):
    name = 'bot'

    def __init__(self, **kwargs):
        super().__init__('bot', **kwargs)

    def handler(self, body, push):
        if body == 'clear':
            push.clear_session()
        elif body == 'clear all':
            self.bot.bullet.delete_pushes()


class MoudlesModule(Module):
    name = 'modules'

    def __init__(self, **kwargs):
        super().__init__('modules', **kwargs)

    def handler(self, body, push):
        if body == '':
            push.reply('\n'.join(self.bot.modules.keys()), title="Modules")
        elif body == 'reload':
            self.bot.reload_modules()
            push.reply('Modules Reload Finished')

export = [BaseModule, MoudlesModule]
