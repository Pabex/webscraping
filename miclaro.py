import requests
import re
from bs4 import BeautifulSoup
from time import sleep, time

######### SETTINGS ##########
USUARIO_CLARO = ""
CLAVE_CLARO = ""

SEGUNDOS_TIMEOUT = 10

lineas = [{
    "nombre": "",
    "linea": ""
}
]
#############################


URL = "https://miclaro.claro.com.ar/web/guest/bienvenido?p_p_id=58&p_p_lifecycle=1&p_p_state=normal&p_p_mode=view&p_p_col_id=column-1&p_p_col_count=1&saveLastPath=0&_58_doActionAfterLogin=false&_58_struts_action=%2Flogin%2Flogin"

data = {
    "_login_usuario": USUARIO_CLARO,
    "_login_password": CLAVE_CLARO,
    "remember-me": True
}

session = requests.session()
session.get("https://miclaro.claro.com.ar/web/guest/bienvenido", timeout=SEGUNDOS_TIMEOUT)
sleep(1)
response = session.post(URL, data)
html = BeautifulSoup(response.text, "html.parser")

resultados = []
hay_cuenta_sin_sms = False
for linea in lineas:
    timestamp = int(time())
    dic_resultado = {}
    dic_resultado["nombre"] = linea["nombre"]
    dic_resultado["linea"] = linea["linea"]
    try:
        session.get("https://miclaro.claro.com.ar/web/guest/verLinea/?linea=" + linea["linea"], timeout=SEGUNDOS_TIMEOUT)
        session.get("https://miclaro.claro.com.ar/c/portal/logout?cambioDeLinea=si&_=" + str(timestamp), timeout=SEGUNDOS_TIMEOUT)
        session.get("https://miclaro.claro.com.ar/web/guest/bienvenido?lineaALogear=" + linea["linea"] +"&tokenUMS=&autovinculacion=&cantidadDescubiertasIniciadas=", timeout=SEGUNDOS_TIMEOUT)
        response = session.get("https://miclaro.claro.com.ar/web/guest/mi-consumo", timeout=SEGUNDOS_TIMEOUT)
        html_consumo = BeautifulSoup(response.text, "html.parser")
        div_credito = html_consumo.find("div", class_="credito credito-pp-pa")
        if div_credito:
            div_credito_info = div_credito.find("div", class_="credito-info")
            div_txt_izq = div_credito_info.find("div", class_="txt-izq")
            credito = div_txt_izq.find("p", class_="txt-negrita").string

            div_txt_der = div_credito_info.find("div", class_="txt-der")
            vencimiento = div_txt_der.find("p", class_="txt-negrita").string

            dic_resultado['credito'] = credito
            dic_resultado['vencimiento'] = vencimiento
    except Exception as e:
        print("Error al obtener datos de linea %s" % linea["linea"], e)

    resultados.append(dic_resultado)

print("Línea\tNúmero\tCrédito\tVencimiento")
for r in resultados:
    linea = r['nombre']
    numero = r['linea']
    numero = numero[:-3] + "*"*3
    saldo = r['credito']
    vencimiento = r['vencimiento']
    print("%s\t%s\t%s\t%s" % (linea, numero, saldo, vencimiento))
