import inspect
import time
import types
from threading import Thread
from pprint import pprint

import pushbullet
from pushbullet import Pushbullet
from .utils import IndexedDict
from .errors import *

class BotbulletThread(Thread):

    def __init__(self, switch=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.switch = switch

    def stop(self):
        self.switch[0] = False

    def __repr__(self):
        return '<BotbulletThread({})>'.format('Alive' if self.switch[0] else 'Stopped')


class Botbullet(Pushbullet):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.listening_thread = None

    def get_device_by_iden(self, device_iden):
        for device in self.devices:
            if device.device_iden == device_iden:
                return device
        return None

    def get_or_create_device(self, name):
        try:
            return self.get_device(name)
        except pushbullet.InvalidKeyError:
            return self.new_device(name)

    def listen_pushes(self, callback=None, modified_after=None, filter=None, sleep_interval=2, switch=None, log=None, debug=False):
        def noop(*args):
            pass

        log = log or print
        last_time = modified_after or time.time()
        callback = callback or noop
        # This allows stopping listening from outer scope
        switch = switch or [True]

        debug and log('Pushes listening Start.')
        while True:
            pushes = self.get_pushes(modified_after=last_time)
            if filter:
                pushes = filter(pushes)
            if len(pushes):
                length = len(pushes)
                debug and log('{} pushes received.'.format(length))
                for i in range(length):
                    event_obj = IndexedDict(
                        {'listening': True, 'remain_pushes': length - i - 1, 'sender': self})
                    push = IndexedDict(pushes[i])
                    callback(push, event_obj)
                    if not event_obj['listening']:
                        switch[0] = False  # Escape the listening loop
            if not switch[0]:
                debug and log('Pushes listening end.')
                return
            last_time = time.time()
            time.sleep(sleep_interval)

    def listen_pushes_asynchronously(self, *args, **kwargs):
        switch = [True]

        kwargs['switch'] = switch
        thread = BotbulletThread(switch=switch, target=self.listen_pushes, args=args, kwargs=kwargs)

        if self.listening_thread and self.listening_thread.is_alive():
            raise ThreadAlreadyExistsError('Thread already exists. You may want to execute "stop_listening" first.')
        self.listening_thread = thread
        thread.start()
        return thread

    def stop_listening(self):
        if self.listening_thread:
            if self.listening_thread.is_alive():
                self.listening_thread.stop()
            self.listen_threads = None

    def __del__(self):
        self.stop_listening()
