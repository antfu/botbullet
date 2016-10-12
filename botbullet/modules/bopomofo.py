from botbullet import Module
from bopomofo import to_bopomofo

class BpmfModule(Module):
    name = 'bpmf'

    def handler(self, body, push):
        push.reply(to_bopomofo(body))

export = BpmfModule
