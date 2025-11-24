# 🎵 YouTube Music Sorter

Herramienta de escritorio moderna (GUI) escrita en Python para ordenar playlists extensas de YouTube Music que la interfaz web no permite gestionar eficientemente.

## 🚀 Características

* **GUI Moderna:** Interfaz oscura basada en CustomTkinter, inspirada en la estética de YouTube Music.
* **Clean Architecture:** Código modular, mantenible y escalable.
* **No destructivo:** Nunca modifica tu lista original; crea una nueva lista llamada *Original [Sorted]*.
* **Criterios de Orden:**
    * Artista
    * Título
    * Álbum
    * Duración
* **Soporte Masivo:** Probado con playlists de +400 canciones.

## 🛠️ Instalación

1.  **Clonar el repositorio:**
    \\\ash
    git clone https://github.com/martin-ratti/yt-sorter.git
    cd yt-sorter
    \\\

2.  **Crear entorno virtual e instalar dependencias:**
    \\\ash
    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    # Linux/Mac
    source venv/bin/activate
    
    pip install -r requirements.txt
    \\\

3.  **Ejecutar:**
    \\\ash
    python main.py
    \\\

## 🔑 Cómo obtener los Headers (Autenticación)

Para que el script funcione, necesita permiso para acceder a tu cuenta. Esto se hace copiando las credenciales de tu navegador (solo una vez):

1.  Abre [YouTube Music](https://music.youtube.com) en Chrome o Firefox (asegúrate de estar logueado).
2.  Abre las **Herramientas de Desarrollador** (F12) y ve a la pestaña **Network** (Red).
3.  Navega un poco por la web (ej. haz clic en 'Biblioteca').
4.  En la lista de peticiones de Network, busca una que empiece por \rowse\ (filtra por 'XHR' si es necesario).
5.  Haz clic derecho sobre ella -> **Copy** -> **Copy request headers**.
6.  Pega ese texto en la caja de texto de la aplicación y pulsa **Conectar Cuenta**.

## 🏗️ Arquitectura

El proyecto sigue los principios de **Clean Architecture**:
* \src/core\: Entidades y lógica de negocio pura (Ordenamiento).
* \src/infrastructure\: Implementación de la API de YouTube (ytmusicapi).
* \src/interface\: Interfaz gráfica (CustomTkinter).

---
Desarrollado con 🐍 Python.
