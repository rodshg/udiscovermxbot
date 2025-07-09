import requests
import time

SHOP_URL = "https://umg-mexico.myshopify.com/products.json"  # Cambia esto por tu tienda
URL_CORTA = "https://udiscover.mx"
WEBHOOK_URL = "https://discord.com/api/webhooks/1392530963690557581/0B3R64vLKqciWbLdFapc-CMfoapMakVAAnYLQ60b0EXDKt9CUdXdPdFfdF_-QojMXizS"       # Pega aquí tu webhook

seen_products = set()

def fetch_products():
    try:
        response = requests.get(SHOP_URL)
        response.raise_for_status()
        return response.json().get("products", [])
    except Exception as e:
        print(f"Error al obtener productos: {e}")
        return []

def send_to_discord(product):
    data = {
        "content": f"🛍️ **Nuevo producto detectado!**\n"
                   f"**{product['title']}**\n"
                   f"{product['vendor']}\n"
                   f"{product['handle']}\n"
                   f"https://{URL_CORTA.split('//')[1].split('/')[0]}/products/{product['handle']}"
    }
    try:
        requests.post(WEBHOOK_URL, json=data)
    except Exception as e:
        print(f"Error enviando a Discord: {e}")

def monitor():
    global seen_products
    while True:
        products = fetch_products()
        for product in products:
            if product["id"] not in seen_products:
                seen_products.add(product["id"])
                send_to_discord(product)
        time.sleep(1)

if __name__ == "__main__":
    print("👀 Empezando a monitorear...")
    monitor()
