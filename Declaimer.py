"""
本模块封装了百度语音合成的API
用法：Declaimer(接口配置).txt2audio(要合成的文本, 文件名，存放生成语音文件的目录)
"""
import json
import os
from urllib.request import urlopen
from urllib.request import Request
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.parse import quote_plus


class Declaimer(object):
    def __init__(self, api_key='cBsa0QM3saNOw4iWTYNVLLym', secret_key='V4hKTpOWQx1i7rLx5jO3uafdf12IWmWy',
                 cuid='b74e98ca87974ed48c3c3a49105ec222', pre=5, spd=5, pit=5, vol=5, fmt='mp3'):
        """
        :param text: 合成的文本，使用UTF-8编码。小于2048个中文字或者英文数字。（文本在百度服务器内转换为GBK后，长度必须小于4096字节）
        :param api_key:
        :param secret_key:
        :param cuid:用户唯一标识，用来计算UV值。建议填写能区分用户的机器 MAC 地址或 IMEI 码，长度为60字符以内
        :param pre:发音人选择, 0为普通女声，1为普通男生，3为情感合成-度逍遥，4为情感合成-度丫丫，默认为普通女声
        :param spd:语速，取值0-15，默认为5中语速
        :param pit:取值0-15，默认为5中语调
        :param vol:音量，取值0-9，默认为5中音量
        :param fmt:下载的文件格式, 'mp3' , 'pcm-16k'  , 'pcm-8k' ,  'wav '
        """
        self.FORMAT = fmt if fmt in ['mp3', 'pcm-16k', 'pcm-8k', 'wav'] else 'mp3'
        self.VOL = vol if vol in range(1, 9) else 5
        self.PIT = pit if pit in range(1, 15) else 5
        self.SPD = spd if spd in range(1, 15) else 5
        self.PER = pre if pre in range(0, 6) else 0
        self.API_KEY = api_key
        self.SECRET_KEY = secret_key
        self.CUID = cuid
        try:
            self.fetch_token()
        except TokenError:
            self.txt2audio = lambda text=None, filename=None, basedir=None: None

    def fetch_token(self):
        token_url = 'http://openapi.baidu.com/oauth/2.0/token'
        scope = 'audio_tts_post'  # 有此scope表示有tts能力，没有请在网页里勾选

        params = {'grant_type': 'client_credentials',
                  'client_id': self.API_KEY,
                  'client_secret': self.SECRET_KEY}
        post_data = urlencode(params)
        post_data = post_data.encode('utf-8')
        req = Request(token_url, post_data)
        try:
            f = urlopen(req, timeout=5)
            result_str = f.read()
        except URLError as err:
            print('token http response http code : ' + str(err.code))
            result_str = err.read()

        result_str = result_str.decode()

        result = json.loads(result_str)

        if ('access_token' in result.keys() and 'scope' in result.keys()):
            if not scope in result['scope'].split(' '):
                raise TokenError('scope is not correct')
            self.token = result['access_token']
        else:
            raise TokenError(
                'MAYBE API_KEY or SECRET_KEY not correct: access_token or scope not found in token response')

    def txt2audio(self, text, filename, basedir='./audio/'):
        # 构造API请求
        TTS_URL = 'http://tsn.baidu.com/text2audio'
        params = {'tok': self.token, 'tex': quote_plus(text), 'per': self.PER, 'spd': self.SPD, 'pit': self.PIT,
                  'vol': self.VOL, 'aue': self.FORMAT, 'cuid': self.CUID,
                  'lan': 'zh', 'ctp': 1}  # lan ctp 固定参数
        data = urlencode(params)
        req = Request(TTS_URL, data.encode('utf-8'))

        # 获取音频文件
        has_error = False
        try:
            f = urlopen(req)
            self.result_str = f.read()
            has_error = ('Content-Type' not in f.headers.keys() or f.headers['Content-Type'].find('audio/') < 0)
        except URLError as err:
            print('asr http response http code : ' + str(err.code))
            self.result_str = err.read()
            has_error = True

        # 创建资源文件夹
        if not os.path.exists(basedir):
            os.mkdir(basedir)

        # 写入文件
        save_file = filename + "_error.txt" if has_error else filename + '.' + self.FORMAT
        with open(os.path.join(basedir, save_file), 'wb') as of:
            of.write(self.result_str)
        if has_error:
            result_str = str(self.result_str, 'utf-8')
            print("tts api  error:" + result_str)
        # 报告结果
        print("{filename} saved as {path}:".format(filename=filename, path=basedir + save_file))


class TokenError(Exception):
    pass


if __name__ == '__main__':
    decl = Declaimer()
    decl.txt2audio('中文分词，是一门高深莫测的技术。不论对于人类，还是对于AI。', filename='first')
    decl.txt2audio('土地，快告诉俺老孙，俺的金箍棒在哪？大圣，您的金箍，棒就棒在特别适合您的发型。', filename='second')
