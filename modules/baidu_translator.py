from botbullet import Module


class TranslatorModule(Module):

    def __init__(self, **kwargs):
        super().__init__(name='trans', alias=['t'], **kwargs)
        self.appid = self.configures.get_set('appid',  '20160919000028921')
        self.appkey = self.configures.get_set('appkey', 'inOmkEzClYvvseJEfDV8')

    def translate(self, body, **kwargs):
        return baidu_translate(body, self.appid, self.appkey, **kwargs)

    def handler(self, body, push):
        title = ''
        plices = body.strip().split(' ')
        tolang = 'en'
        if len(plices) >= 3 and plices[-2].lower() == 'to' and plices[-1].lower() in TOLANGS:
            tolang = plices[-1].lower()
            body = ' '.join(plices[:-2])
        translated, action, _from, _to = self.translate(body, tolang=tolang)
        if not action:
            translated = '# Translate failed'
        elif _from and _to:
            title = _from.upper() + ' ⇀ ' + _to.upper()
        push.reply(translated, title=title)

export = TranslatorModule

import requests
import urllib
import json
import hashlib
import random
from pprint import pprint

BAIDU_TRANS_API_URL = 'http://api.fanyi.baidu.com/api/trans/vip/translate?appid={appid}&q={source}&from={fromlang}&to={tolang}&salt={salt}&sign={sign}'
TOLANGS = ['zh', 'en', 'yue', 'wyw', 'jp', 'kor', 'fra', 'spa', 'th', 'ara',
           'ru', 'pt', 'de', 'it', 'el', 'nl', 'pl', 'bul', 'est', 'dan', 'fin',
           'cs', 'rom', 'slo', 'swe', 'hu', 'cht']


def baidu_translate(source, appid, apikey, fromlang='auto', tolang='en'):
    quoted_source = urllib.request.quote(source)
    salt = str(random.randint(32768, 65536))
    # get sign
    sign = appid + source + salt + apikey
    sign = hashlib.md5(sign.encode()).hexdigest()

    url = BAIDU_TRANS_API_URL.format(
        appid=appid, source=quoted_source, fromlang=fromlang, tolang=tolang, salt=salt, sign=sign)
    # request
    r = requests.get(url)
    data = json.loads(r.text)

    translated = ''
    action = True
    if 'dst' in data.keys():
        translated = data['dst']
    elif 'trans_result' in data.keys():
        translated = '\n'.join([x['dst'] for x in data['trans_result']])
    else:
        # Failed to get result
        translated = source
        action = False

    print(data)
    _from = data.get('from', '')
    _to = data.get('to', '')

    return translated, action, _from, _to
