# Ruta_trabajo
Sistema en Raspberry Pi que, cada día a las 12:30 PM, envía por Telegram la ruta más rápida al trabajo entre tres opciones usando OpenRouteService. Evalúa duración y distancia, elige la mejor ruta y notifica. Automatizado con crontab, funciona sin pantalla. Puede mejorarse con tráfico en tiempo real.

🧠 Resumen del Proyecto: Ruta más corta al trabajo con Raspberry Pi

Este proyecto usa una Raspberry Pi para ejecutar diariamente un script en Python que calcula la ruta más rápida al trabajo entre tres opciones predefinidas (Lago de Guadalupe, Arboledas, Atizapán), y envía la información por Telegram a las 12:30 PM.

🧩 Características clave:

Tecnologías usadas:

Raspberry Pi (sin pantalla)

Python

OpenRouteService API (para calcular rutas)

Telegram Bot API (para enviar notificaciones)

crontab (para ejecución diaria automática)

Rutas predefinidas:

Casa → Trabajo, pasando por 3 puntos intermedios posibles

Se evalúan duración y distancia de cada ruta

Mensaje enviado (ejemplo):

🚗 Ruta más rápida: Arboledas  
🕒 Duración estimada: 10 min  
📏 Distancia: 7.2 km

⚙️ Automatización:

Script se ejecuta cada día a las 12:30 PM vía crontab

Archivos principales: ruta_trabajo.py y .env (para guardar claves)

🔧 Estado actual:

Funciona correctamente

Usa estimaciones de tiempo, sin tráfico en tiempo real

💡 Mejoras futuras:

Integrar Google Maps API para tráfico en tiempo real

Crear interfaz web o app de control remoto

Guardar historial de rutas

Ejecutar automáticamente al encender la Raspberry
