import os
import requests
import time

SHOPIFY_URL = os.getenv("SHOPIFY_URL")
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

productos_previos = set()

def obtener_productos():
    try:
        r = requests.get(SHOPIFY_URL)
        data = r.json()
        return {(p['id'], p['title'], p['handle']) for p in data['products']}
    except Exception as e:
        print("Error al obtener productos:", e)
        return set()

def enviar_discord(titulo, url):
    data = {
        "content": f"🛍️ **Nuevo producto en la tienda!**\n**{titulo}**\n🔗 {url}"
    }
    try:
        requests.post(DISCORD_WEBHOOK_URL, json=data)
    except Exception as e:
        print("Error al enviar a Discord:", e)

print("Iniciando monitoreo...")

while True:
    productos = obtener_productos()
    nuevos = [p for p in productos if p[0] not in [pp[0] for pp in productos_previos]]

    for producto in nuevos:
        _, titulo, handle = producto
        url = f"https://udiscover.mx/products/{handle}"
        enviar_discord(titulo, url)

    productos_previos = productos
    time.sleep(5)
