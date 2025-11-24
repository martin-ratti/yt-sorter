# 🎵 YouTube Music Sorter (YTSorter)

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Status](https://img.shields.io/badge/Status-Stable-green)

Una herramienta de escritorio robusta para ordenar playlists masivas de YouTube Music que la interfaz web no permite gestionar. Diseñada para detectar duplicados, evadir límites de API y ordenar por metadatos reales.

## ✨ Características Clave

* **🛡️ Auditoría de Duplicados:** Analiza la playlist antes de procesarla y elimina automáticamente canciones repetidas (clones exactos).
* **🐢 Modo "Slow & Safe":** Sube canciones en lotes pequeños con pausas inteligentes para evitar que Google bloquee la operación por "spam".
* **💾 Sesión Persistente:** Guarda tu autenticación localmente (`auth.json`) para que no tengas que copiar las cookies cada vez.
* **🎨 Interfaz Moderna:** GUI oscura basada en CustomTkinter.
* **📊 Feedback en Tiempo Real:** Log detallado del proceso en pantalla.

## 🚀 Instalación y Uso

### Opción A: Usar el Ejecutable (Windows)
1. Descarga el archivo `YTSorter.exe` desde la carpeta `dist`.
2. Ejecútalo. No requiere Python instalado.

### Opción B: Ejecutar desde Código Fuente
1. Clonar el repositorio:
   ```bash
   git clone [https://github.com/martin-ratti/yt-sorter.git](https://github.com/martin-ratti/yt-sorter.git)
   cd yt-sorter