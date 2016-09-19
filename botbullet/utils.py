
class IndexedDict(dict):
    '''
    Simple dict but support access as x.y style.
    '''

    def __init__(self, d=None, **kw):
        super(IndexedDict, self).__init__(**kw)
        if d:
            for k, v in d.items():
                self[k] = IndexedDict(v) if isinstance(v, dict) else v

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(
                r"'IndexedDict' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value
