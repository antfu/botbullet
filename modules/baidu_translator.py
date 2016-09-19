from botbullet import Module


class TranslatorModule(Module):

    def __init__(self):
        super().__init__('trans')

    def handler(self, body, push):
        translated, action = baidu_translate(body)
        if not action:
            translated = '# Translate failed'
        push.reply(translated)

export = TranslatorModule

import requests
import urllib
import json
import hashlib
import random
from pprint import pprint

BAIDU_TRANS_API_APPID = '20160919000028921'
BAIDU_TRANS_API_KEY = 'inOmkEzClYvvseJEfDV8'
BAIDU_TRANS_API_URL = 'http://api.fanyi.baidu.com/api/trans/vip/translate?appid={appid}&q={source}&from={fromlang}&to={tolang}&salt={salt}&sign={sign}'

def baidu_translate(source, fromlang='auto', tolang='en'):
    quoted_source = urllib.request.quote(source)
    salt = str(random.randint(32768, 65536))
    appid = BAIDU_TRANS_API_APPID
    secret_key = BAIDU_TRANS_API_KEY
    # get sign
    sign = appid + source + salt + secret_key
    sign = hashlib.md5(sign.encode()).hexdigest()

    url = BAIDU_TRANS_API_URL.format(appid=appid, source=quoted_source, fromlang=fromlang, tolang=tolang, salt=salt, sign=sign)
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

    return translated, action
