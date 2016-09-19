from botbullet import Module


class HelloModel(Module):

    def __init__(self):
        super().__init__('hello')

    def handler(self, body, push):
        push.reply('Hello, ' + push.sender_name + '!')

export = HelloModel
