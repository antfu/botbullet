from botbullet import Module

DEFAULT_TOLANG = 'en'


class TranslatorModule(Module):
    name = 'trans'
    alias = ['t', 'translate']

    def init(self):
        self.appid = self.configures.get_set('appid',  '20160919000028921')
        self.appkey = self.configures.get_set('appkey', 'inOmkEzClYvvseJEfDV8')
        self.tolang = DEFAULT_TOLANG

    def translate(self, body, **kwargs):
        return baidu_translate(body, self.appid, self.appkey, **kwargs)

    def body_normalize(self, body):
        body = body.strip()
        plices = body.strip().split(' ')
        tolang = self.tolang
        if len(plices) >= 2 and plices[-2].lower() == 'to' and plices[-1].lower() in TOLANGS:
            tolang = plices[-1].lower()
            body = ' '.join(plices[:-2])

        return body, tolang

    def translate_and_reply(self, body, push, tolang=None, display_title=True):
        tolang = tolang or self.tolang
        translated, action, _from, _to = self.translate(body, tolang=tolang)
        if not action:
            translated = '# Translate failed'
        elif _from and _to:
            title = _from.upper() + ' ⇀ ' + _to.upper()
        push.reply(translated, title=title)

    def immerse_handler(self, body, push):
        if body.strip().lower() == '#exit':
            push.reply(title='Translator', body='Exiting Immerse Mode.')
            return

        self.translate_and_reply(body, push, display_title=False)
        self.immerse(self.immerse_handler)

    def handler(self, body, push):
        title = ''
        body, tolang = self.body_normalize(body)
        if not body:
            self.tolang = tolang
            self.immerse(self.immerse_handler)
            push.reply(title='Immerse Mode',
                       body='Translating to {}.\n'.format(self.tolang.upper())
                       + 'You can send "#exit" to exit immerse mode.')
        self.translate_and_reply(body, push, tolang)

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

    # print(data)
    _from = data.get('from', '')
    _to = data.get('to', '')

    return translated, action, _from, _to
