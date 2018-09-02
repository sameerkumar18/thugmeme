import requests

cookies = {
    'sid': '9km2g0pf887qujruiq53mftvl7',
    'is_user': '1',
    'fcap_2810': '%7B%22fcap%22%3A1%2C%22expire%22%3A1516731064%7D',
    'adblock': 'off',
    'webfont-loaded': 'true',
    'convert_count': '1',
    'hl': 'en',
    'is_old_user': '1',
    'user_converts_count': '1',
    'ap_provider': '0',
    'ap_shown': '1',
    'fcap_2864': '%7B%22fcap%22%3A3%2C%22expire%22%3A1516731112%7D',
    'noprpkedvhozafiwrcnt': '1',
    'noprpkedvhozafiwrexp': 'Tue, 23 Jan 2018 18:12:32 GMT',
    'fcap_2819': '%7B%22fcap%22%3A2%2C%22expire%22%3A1516731064%7D',
    'fcap_2820': '%7B%22fcap%22%3A1%2C%22expire%22%3A1516731306%7D',
    'fcap_2720': '%7B%22fcap%22%3A3%2C%22expire%22%3A1516731064%7D',
    'fcap_2812': '%7B%22fcap%22%3A2%2C%22expire%22%3A1516731196%7D',
    'fcap_2611': '%7B%22fcap%22%3A3%2C%22expire%22%3A1516731064%7D',
    'fcap_2896': '%7B%22fcap%22%3A1%2C%22expire%22%3A1516731319%7D',
}

headers = {
    'Origin': 'http://2conv.com',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9,la;q=0.8,hi;q=0.7',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Cache-Control': 'max-age=0',
    'Referer': 'http://2conv.com/',
    'Connection': 'keep-alive',
    'DNT': '1',
}

data = [
  ('url', 'http://www.youtube.com/watch?v=v5w-0H-hq6E'),
  ('format', '1'),
  ('service', 'youtube'),
]

r = response = requests.post('http://2conv.com/convert/', headers=headers, data=data)
print(r,r.text)
