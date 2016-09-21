import warnings
import sys
import traceback
import importlib
from pprint import pprint

from .botbullet import Botbullet
from .module import Module
from .errors import *

DEFAULT_DEVICE_NAME = 'Botbullet'


class Bot:

    def __init__(self, api_token, device_name=None, module_configs=None, debug=False):
        self.api_token = api_token
        self.bullet = Botbullet(api_token)
        self.device_name = device_name or DEFAULT_DEVICE_NAME
        self.device = self.bullet.get_or_create_device(self.device_name)
        self.modules = {}
        self.modules_info = {}
        self.debug = debug
        self.module_configs = module_configs
        self.pushes_in_session = []
        self.immerse_func = None

    def start(self):
        self.bullet.listen_pushes_asynchronously(
            callback=lambda *args: self.callback(*args))

    def stop(self):
        if self.bullet:
            self.bullet.stop_listening()

    def clear_session(self):
        for push in self.pushes_in_session:
            self.bullet.delete_push(push['iden'])
        self.pushes_in_session = []


    def unuse(self):
        self.modules = {}

    def use(self, module, module_key=None, override=False):
        module_key = module_key or module.name
        if not override and module_key in self.modules.keys():
            raise ModuleConflictError
        module.bot = self

        self.modules[module_key] = module

        if module.alias:
            for alias in module.alias:
                self.modules[alias] = module

    def __load_module(self, module, override=False):
        clses = module.export
        if not isinstance(clses, list):
            clses = [clses]
        cls_obj = {}

        for cls in clses:
            configures = self.module_configs.get_set(cls.name, {})
            instance = cls(bot=self, configures=configures)
            cls_obj[cls.name] = {"cls": cls, "instance": instance}
            self.use(instance, override=override)

        return cls_obj

    def use_module(self, name, module):
        module_obj = {'module': module}
        module_obj['class'] = self.__load_module(module)

        def reload():
            del(module_obj['class'])
            importlib.reload(module)
            module_obj['class'] = self.__load_module(module, override=True)

        module_obj['reload'] = reload
        self.modules_info[name] = module_obj

    def load_modules(self, module_list):
        for module_name in module_list:
            try:
                print('Loading module', module_name, '... ', end='')
                module = importlib.import_module('modules.' + module_name)
                self.use_module(module_name, module)

            except Exception as e:
                print('Failed  <', str(e), '>')
                if self.debug:
                    traceback.print_exc(file=sys.stdout)
            else:
                print('OK')

    def reload_modules(self):
        self.immerse_func = None
        self.unuse()
        for name, obj in self.modules_info.items():
            try:
                print('Reloading module', name, '... ', end='')
                obj['reload']()

            except Exception as e:
                print('Failed  <', str(e), '>')
                if self.debug:
                    traceback.print_exc(file=sys.stdout)
            else:
                print('OK')

    def reply(self, body, title='', *args, **kwargs):
        push = self.bullet.push_note(
            title=title, body=body, *args, **kwargs, source_device=self.device)
        self.pushes_in_session.append(push)

    def immerse(self, func):
        if self.debug:
            print('Function {} is immersing'.format(str(func)))
        self.immerse_func = func

    def call(self, func, body, push):
        try:
            func(body, push)
        except Exception:
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def callback(self, push):
        direction = push.direction
        if direction == 'self':
            target_device_iden = push.target_device_iden

            # Only get messages sent to Bot
            if target_device_iden == self.device.device_iden:
                self.pushes_in_session.append(push)
                if self.debug:
                    print('[to Bot] ', end='')
                body = push.get('body', '').strip()

                # If there is a function taking the control of bot
                if self.immerse_func:
                    func = self.immerse_func
                    self.immerse_func = None
                    self.call(func, body, push)

                else:
                    if not body:
                        return
                    key = body.split(' ')[0].lower()
                    body = ' '.join(body.split(' ')[1:])

                    if key in self.modules.keys():
                        module = self.modules[key]
                        self.call(module.handler, body, push)

                    # There is no matched modules, start CoR
                    else:
                        # TODO
                        pass

        elif direction == 'incoming':
            if self.debug:
                print('[Incoming] ', end='')
        elif direction == 'outcoming':
            pass
        else:
            if self.debug:
                print('Unexcepted direction', direction)

        if self.debug:
            try:
                print('> {}: {}'.format(push['sender_name'], push['body']))
                pprint(push)
            except:
                pass

    def __del__(self):
        self.stop()
