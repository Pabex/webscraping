"""
URL de prueba:
https://www.lavoz.com.ar/

Selector de prueba:
"#top > section.block.block-main.is-first-section > div > article > div.card-content.is-overlay > div > div > h1 > a"

Ejemplo de ejecución:
python3 main.py "https://www.lavoz.com.ar/" "#top > section.block.block-main.is-first-section > div > article > div.card-content.is-overlay > div > div > h1 > a"
"""

import requests
import re
from bs4 import BeautifulSoup
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("url")
parser.add_argument("selector")
args = parser.parse_args()

print("\nScrapeando la url:")
print("\t" + args.url)
print("\nBuscando el selector:")
print("\t" + args.selector)

url = args.url
selector = args.selector

response = requests.get(url)

bs = BeautifulSoup(response.text, "html.parser")

articles = bs.select(selector)

found = False
for article in articles:
    print("\nResultado encontrado")
    print(article.text)
    print("=============================================================")
    found = True

if not found:
    print("\nNo se encontraron resultados")

