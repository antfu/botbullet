import warnings
from botbullet import Botbullet
from model import Model
from pprint import pprint

DEFAULT_DEVICE_NAME = 'Botbullet'


class Bot:

    def __init__(self, api_token, device_name=None, debug=False):
        self.api_token = api_token
        self.bullet = Botbullet(api_token)
        self.device_name = device_name or DEFAULT_DEVICE_NAME
        self.device = self.bullet.get_or_create_device(self.device_name)
        self.models = {}
        self.debug = debug
        self.pushes_in_session = []
        self.monopolizing = None
        self.bullet.listen_pushes_asynchronously(
            callback=lambda *args: self.callback(*args))

    def clear_session(self):
        for push in self.pushes_in_session:
            self.bullet.delete_push(push['iden'])
        self.pushes_in_session = []

    def use(self, model, model_key=None):
        model_key = model_key or model.name
        if model_key in self.models.keys():
            warnings.warn("duplicated", FutureWarning)
        model.bot = self
        self.models[model_key] = model

    def reply(self, body, title='', *args, **kwargs):
        kwargs['body'] = body
        kwargs['title'] = title
        push = self.bullet.push_note(*args, **kwargs, source_device=self.device)
        self.pushes_in_session.append(push)

    def monopolize(self, model):
        if self.debug:
            print('Model {} is monopolizing'.format(str(model)))
        self.monopolizing = model

    def callback(self, push, event_obj):
        direction = push.get('direction', None)
        if direction == 'self':
            target_device_iden = push.get('target_device_iden', None)
            if target_device_iden == self.device.device_iden:
                self.pushes_in_session.append(push)
                if self.debug:
                    print('[to Bot] ', end='')
                body = push.get('body', '').strip()
                # If there is a model taking control of the bot
                if self.monopolizing:
                    model = self.monopolizing
                    # Remove monopolizing
                    self.monopolizing = None
                    model.handler(body, push, event_obj, monopolize=True)
                else:
                    key = body.split(' ')[0].lower()
                    body = ' '.join(body.split(' ')[1:])
                    if key in self.models.keys():
                        self.models[key].handler(body, push, event_obj)

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
        self.bullect and self.bullect.stop_listening()
