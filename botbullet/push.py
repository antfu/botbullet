
from .utils import IndexedDict


class FakeDevice:

    def __init__(self, device_iden):
        self.device_iden = device_iden


class Push(dict):

    def __init__(self, d, bullet):
        super().__init__(d)
        self.bullet = bullet
        self.iden = self.get('iden', None)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(
                r"'IndexedDict' object has no attribute '%s'" % key)

    def reply(self, body, title='', *args, **kwargs):
        target_device = None
        source_device = None
        target_device_iden = self.get('target_device_iden', None)
        source_device_iden = self.get('source_device_iden', None)
        if target_device_iden:
            target_device = FakeDevice(target_device_iden)
        if source_device_iden:
            source_device = FakeDevice(source_device_iden)

        push = self.bullet.push_note(title, body, *args,
                                     **kwargs,
                                     device=source_device,
                                     source_device=target_device)

        return Push(push, self.bullet)

    def dismiss(self):
        return self.bullet.dismiss_push(self.iden)

    def delete(self):
        return self.bullet.delete_push(self.iden)
