from botbullet import Module

# Create a custom module
class HelloModule(Module):
    # Set the command of this module to 'hello'
    name = 'hello'
    # Set alias
    alias = ['hey', 'hi']

    # Handle incoming pushes which start with 'hello' command
    def handler(self, body, push):
        # Reply to sender
        push.reply('Hello, ' + push.sender_name + '!')

# Export this module
export = HelloModule
