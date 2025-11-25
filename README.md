
-----

# 🎵 YTSorter

**Una aplicación de escritorio potente y segura para ordenar playlists masivas de YouTube Music con control total.**

[Aquí va una captura de pantalla de la aplicación funcionando]

-----

## ✨ Características

  * **🔑 Autenticación Inteligente:** Pega tus headers y la app filtrará automáticamente lo necesario (Cookies, Auth) para conectar de forma segura, guardando tu sesión para el futuro.
  * **🛡️ Modo Seguro y Anti-Duplicados:** Detecta y elimina canciones repetidas antes de procesar. Utiliza un sistema de subida "lento y seguro" para evitar bloqueos por parte de Google.
  * **👁️ Previsualización en Tiempo Real:** "Trust but Verify". Revisa exactamente cómo quedará tu lista (con indicadores de subida/bajada) antes de crearla.
  * **🎛️ Criterios Avanzados:** Ordena por Artista (normalizando acentos), Título, Álbum, Duración o Aleatorio real. Incluye opción de invertir orden (Z-A).
  * **📦 Portable:** Código listo para ser empaquetado como un ejecutable `.exe` independiente.

-----

## 🚀 Cómo Instalar y Usar

Esta aplicación está diseñada para ejecutarse con Python. Sigue estos pasos sencillos:

### 1\. Preparar el Entorno

1.  **Clona el repositorio:**

    ```bash
    git clone https://github.com/martin-ratti/yt-sorter.git
    cd yt-sorter
    ```

2.  **Crea un entorno virtual e instala dependencias:**

    ```bash
    # Crear entorno
    python -m venv venv

    # Activar (Windows)
    .\venv\Scripts\Activate

    # Instalar librerías
    pip install -r requirements.txt
    ```

### 2\. Ejecutar la Aplicación

Simplemente corre el archivo principal:

```bash
python main.py
```

### 3\. (Opcional) Crear tu propio Ejecutable (.exe)

Si prefieres tener la aplicación como un archivo único para no abrir la terminal:

1.  Asegúrate de instalar PyInstaller: `pip install pyinstaller`.
2.  Ejecuta el script de construcción incluido:
    ```bash
    python build_exe.py
    ```
3.  Encontrarás tu `YTSorter.exe` en la carpeta `/dist`.

-----

## 🔑 Guía de Conexión (Solo primera vez)

Para gestionar tus listas, la aplicación necesita permiso temporal.

1.  Abre YouTube Music en tu navegador (F12 -\> Network).
2.  Copia el bloque de "Request Headers" de cualquier petición (ej. `browse`).
3.  Pégalo en la app y dale a "Conectar".

> La app guardará un archivo local `auth.json` para que no tengas que repetir este paso.

-----

## ⚠️ Seguridad ante todo

Esta herramienta **NUNCA** modifica ni borra tus playlists originales.

  * Siempre crea una **nueva playlist** llamada `Nombre Original [Sorted by X]`.
  * Esto garantiza que, pase lo que pase, tus datos originales estén a salvo. Tú decides cuándo borrar la lista vieja.

> 💡 Nota: El proceso de subida puede tardar unos minutos en listas largas (+400 canciones) debido a las pausas de seguridad para evitar errores de la API.

-----

## 🤝 Cómo Contribuir

¡Las ideas son bienvenidas\! Si quieres añadir un nuevo criterio de ordenamiento:

1.  **Fork y Clona:** Clona el repo en tu máquina.
2.  **Añade la Lógica:** Modifica `src/core/entities.py` para agregar tu criterio en `sort_tracks`.
3.  **Actualiza la UI:** Agrega el RadioButton en `src/interface/gui.py`.
4.  **Pull Request:** Envía tus cambios para integrarlos.

-----

## 🧩 Tecnologías Utilizadas

  * Python 3.10+ 🐍
  * CustomTkinter (Interfaz Moderna)
  * ytmusicapi (API Wrapper)
  * PyInstaller (Empaquetado)

-----

## 📜 Licencia

Este proyecto es de código abierto. Úsalo bajo tu propia responsabilidad. No está afiliado oficialmente con Google ni YouTube.

-----

Hecho con ❤️ por **[Martín Ratti](https://www.google.com/search?q=https://github.com/martin-ratti)**
