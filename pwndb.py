import re
import requests
from bs4 import BeautifulSoup


URL_PWNDB_ONION = "http://pwndb2am4tzkvold.onion/"
USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36"


def buscar_brechas(usuario_email='', dominio_email=''):
    session = requests.session()
    session.proxies = {'http': 'socks5h://127.0.0.1:9050', 'https': 'socks5h://127.0.0.1:9050'}
    headers = {
        'User-Agent': USER_AGENT,
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'luser': usuario_email,
        'domain': dominio_email,
        'luseropr': '0',
        'domainopr': '0',
        'submitform': 'em'
    }
    try:
        response = session.post(URL_PWNDB_ONION, data, headers=headers)
        html = response.text
        return parsear_resultado(html)
    except Exception as e:
        print("Error al conectarse con pwndb: ", str(e))
        return None


def parsear_resultado(html):
    lista = []
    soup = BeautifulSoup(html, 'html.parser')
    pre_tag = soup.find_all('pre', attrs={'class': None})[0]

    pattern_users = re.compile(r'\d*\n?Array\n?\(\n?(.*)\n?(.*)\n?(.*)\n?(.*)\n?\)')
    pattern_id = re.compile(r'\[id\] =&gt; (.*)', re.IGNORECASE)
    pattern_luser = re.compile(r'\[luser\] =&gt; (.*)', re.IGNORECASE)
    pattern_domain = re.compile(r'\[domain\] =&gt; (.*)', re.IGNORECASE)
    pattern_password = re.compile(r'\[password\] =&gt; (.*)', re.IGNORECASE)
    matches_users = pattern_users.findall(str(pre_tag), re.IGNORECASE|re.MULTILINE|re.I)
    for match_user in matches_users[1:]:
        linea_id = match_user[0].strip()
        linea_luser = match_user[1].strip()
        linea_domain = match_user[2].strip()
        linea_password = match_user[3].strip()

        id = pattern_id.findall(linea_id)[0]
        luser = pattern_luser.findall(linea_luser)[0]
        domain = pattern_domain.findall(linea_domain)[0]
        password = pattern_password.findall(linea_password)[0]
        lista.append({
            'id': id,
            'luser': luser,
            'domain': domain,
            'password': password,
            'email': "%s@%s" % (luser, domain)
        })
    return lista


if __name__ == '__main__':
    import sys
    import pprint
    email = sys.argv[1]
    usuario, dominio = email.split("@")

    lista = buscar_brechas(usuario, dominio)

    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(lista)
