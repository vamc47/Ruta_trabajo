import os
import requests

# 📌 Claves de API (mejor guardarlas en variables de entorno)
import os
from dotenv import load_dotenv

# Cargar variables del archivo .env
load_dotenv(dotenv_path="key.env")

# Obtener las variables de entorno
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

print("Google API Key:", GOOGLE_API_KEY)
print("Telegram Token:", TELEGRAM_TOKEN)
print("Telegram Chat ID:", TELEGRAM_CHAT_ID)

# Aquí seguiría tu lógica con las variables ya cargadas...


# Coordenadas base (lat, lon)
lat_casa, lon_casa = 19.596333, -99.243361
lat_trabajo, lon_trabajo = 19.539957, -99.215272

rutas = {
    "Lago de Guadalupe": (19.578206, -99.211629),
    "Arboledas": (19.559017, -99.218337),
    "Atizapán": (19.549000, -99.238792)
}


import requests

def obtener_duracion_google(origen, destino, waypoint):
    url = "https://maps.googleapis.com/maps/api/directions/json"
    params = {
        "origin": f"{origen[0]},{origen[1]}",
        "destination": f"{destino[0]},{destino[1]}",
        "waypoints": f"{waypoint[0]},{waypoint[1]}",
        "departure_time": "now",  # IMPORTANTE
        "mode": "driving",
        "traffic_model": "best_guess",
        "alternatives": "true",
        "key": GOOGLE_API_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()
    
    try:
        leg = data["routes"][0]["legs"][0]
        # Intentar obtener duration_in_traffic, si no está usar duration normal
        if "duration_in_traffic" in leg:
            duracion_seg = leg["duration_in_traffic"]["value"]
        else:
            duracion_seg = leg["duration"]["value"]
        
        duracion_min = duracion_seg / 60
        distancia_km = leg["distance"]["value"] / 1000
        
        return round(duracion_min), round(distancia_km, 1)
    except (IndexError, KeyError) as e:
        print(f"Error al obtener duración para ruta: {waypoint}")
        print(data)
        print(f"Detalle error: {e}")
        return None, None


def enviar_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": mensaje, "parse_mode": "Markdown"}
    resp = requests.post(url, data=data)
    return resp.ok

if __name__ == "__main__":
    tiempos = {}
    for nombre, punto in rutas.items():
        duracion, distancia = obtener_duracion_google(
            (lat_casa, lon_casa), (lat_trabajo, lon_trabajo), punto)
        if duracion is not None:
            tiempos[nombre] = (duracion, distancia)

    if not tiempos:
        enviar_telegram("❌ No se pudo calcular ninguna ruta con Google Maps.")
        exit()

    ruta_mas_rapida = min(tiempos, key=lambda k: tiempos[k][0])
    duracion_rapida, distancia_rapida = tiempos[ruta_mas_rapida]

    mensaje = (f"🚗 *Ruta más rápida:* {ruta_mas_rapida}\n"
               f"🕒 Duración estimada: {duracion_rapida} min\n"
               f"📏 Distancia: {distancia_rapida} km\n\n"
               "🛣️ *Otras rutas:*")

    for nombre, (duracion, distancia) in tiempos.items():
        if nombre != ruta_mas_rapida:
            mensaje += f"\n- {nombre}: {duracion} min, {distancia} km"

    if enviar_telegram(mensaje):
        print("✅ Mensaje enviado correctamente")
    else:
        print("❌ No se pudo enviar mensaje")
