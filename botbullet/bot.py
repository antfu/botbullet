import warnings
from pprint import pprint

from .botbullet import Botbullet
from .module import Module
from .errors import *

DEFAULT_DEVICE_NAME = 'Botbullet'


class Bot:

    def __init__(self, api_token, device_name=None, debug=False):
        self.api_token = api_token
        self.bullet = Botbullet(api_token)
        self.device_name = device_name or DEFAULT_DEVICE_NAME
        self.device = self.bullet.get_or_create_device(self.device_name)
        self.modules = {}
        self.debug = debug
        self.pushes_in_session = []
        self.monopolizing = None

    def start(self):
        self.bullet.listen_pushes_asynchronously(
            callback=lambda *args: self.callback(*args))

    def stop(self):
        if self.bullect:
            self.bullect.stop_listening()

    def clear_session(self):
        for push in self.pushes_in_session:
            self.bullet.delete_push(push['iden'])
        self.pushes_in_session = []

    def use(self, module, module_key=None, override=False):
        module_key = module_key or module.name
        if not override and module_key in self.modules.keys():
            raise ModuleConflictError
        module.bot = self
        self.modules[module_key] = module

    def reply(self, body, title='', *args, **kwargs):
        kwargs['body'] = body
        kwargs['title'] = title
        push = self.bullet.push_note(*args, **kwargs, source_device=self.device)
        self.pushes_in_session.append(push)

    def monopolize(self, module):
        if self.debug:
            print('module {} is monopolizing'.format(str(module)))
        self.monopolizing = module

    def callback(self, push, event_obj):
        direction = push.get('direction', None)
        if direction == 'self':
            target_device_iden = push.get('target_device_iden', None)
            if target_device_iden == self.device.device_iden:
                self.pushes_in_session.append(push)
                if self.debug:
                    print('[to Bot] ', end='')
                body = push.get('body', '').strip()
                # If there is a module taking control of the bot
                if self.monopolizing:
                    module = self.monopolizing
                    # Remove monopolizing
                    self.monopolizing = None
                    module.handler(body, push, event_obj, monopolize=True)
                else:
                    key = body.split(' ')[0].lower()
                    body = ' '.join(body.split(' ')[1:])
                    if key in self.modules.keys():
                        self.modules[key].handler(body, push, event_obj)

        elif direction == 'incoming':
            print('[Incoming] ', end='')
        elif direction == 'outcoming':
            pass
        else:
            print('Unexcepted direction', direction)

        if self.debug:
            print('> {}: {}'.format(push.sender_name, push.body))
            pprint(push)

    def __del__(self):
        self.stop()
