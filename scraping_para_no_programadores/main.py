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

# Reemplazo nth-child por nth-of-type.
selector = selector.replace("nth-child", "nth-of-type")

response = requests.get(url)

bs = BeautifulSoup(response.text, "html.parser")

elements = bs.select(selector)

found = False
for element in elements:
    print("\nResultado encontrado")
    print(element.text)
    print("=============================================================")
    found = True

if not found:
    print("\nNo se encontraron resultados")

