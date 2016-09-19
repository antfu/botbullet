from botbullet import Module

# Create a custom module
class HelloModule(Module):
    def __init__(self, **kwargs):
        # Set the command of this module to 'hello'
        super().__init__('hello', **kwargs)

    # Handle incoming pushes which start with 'hello' command
    def handler(self, body, push):
        # Reply to sender
        push.reply('Hello, ' + push.sender_name + '!')

# Export this module
export = HelloModule
