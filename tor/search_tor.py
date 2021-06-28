# You need install:
# $ pip install requests
# $ pip install requests[socks]

import requests
proxies = {
    'http': 'socks5://127.0.0.1:9050',
    'https': 'socks5://127.0.0.1:9050'
}

url = 'https://ifconfig.me/ip'
response = requests.get(url)
print("Ip pública real: " + response.text)
response = requests.get(url, proxies=proxies)
print("Ip usando Tor:" + response.text)
