import sys
import os
import signal
from termcolor import cprint

try:
    import botbullet
except ImportError:
    try:
        sys.path.insert(0, os.path.abspath('.'))
        import botbullet
    except ImportError:
        try:
            sys.path.insert(0, os.path.abspath('..'))
            import botbullet
        except ImportError:
            print('Unable to import "botbullet", did you install it?')

from botbullet import App, InitConfigs

if __name__ == '__main__':
    import atexit
    def exit_handler():
        app.stop()
        print('Exit.')
    atexit.register(exit_handler)

    # Change charset to utf-8 for windows cmd
    if os.name == 'nt':
        os.system('chcp 65001')

    cprint('Starting Botbullet...','cyan')
    configs = InitConfigs(os.path.join(os.path.dirname(__file__),'configs.json'))
    modules_configs = configs.get_set('modules_configs', {})
    debug = configs.get_set('debug', False)
    api_token = configs.get('api_token', None)
    if not api_token:
        cprint('[!] Missing Pushbullet API token, please enter it:','yellow')
        api_token = input().strip()
        if not api_token:
            cprint('Exit','yellow')
            sys.exit()
        configs['api_token'] = api_token

    app = App(api_token, configures=configs, debug=debug)
    cprint('Connecting...','yellow')
    app.connect()

    def signal_handler(signal, frame):
        #print('You pressed Ctrl+C!')
        cprint('Stoping...','yellow')
        app.stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    app.load_modules()
    app.listen()

    cprint('Listening pushes...', 'green')
    cprint('(Press Enter to stop the program)', 'blue')
    input()
    cprint('Stoping...','yellow')
    app.stop()
