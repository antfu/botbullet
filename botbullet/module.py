
class FakeDevice:
    def __init__(self, device_iden):
        self.device_iden = device_iden

class Module:
    def __init__(self, name):
        self.name = name.lower().strip()
        self.bot = None

    def reply(self, *args, **kwargs):
        device = None
        source_device_iden = self.push.get('source_device_iden', '')
        if source_device_iden:
            device = FakeDevice(source_device_iden)
        self.bot.reply(*args, **kwargs, device=device)

    def monopolize(self):
        self.bot.monopolize(self)

    def handler(self, body, push, event_obj, monopolize=False):
        pass

    def help(self):
        pass
