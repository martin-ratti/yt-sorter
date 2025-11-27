<div align="center">

# 🎵 YTSorter - YouTube Music Manager

<img src="https://img.shields.io/badge/Estado-Producción-success?style=for-the-badge&logo=check&logoColor=white" alt="Estado Badge"/>
<img src="https://img.shields.io/badge/Versión-2.3.0-blue?style=for-the-badge" alt="Version Badge"/>
<img src="https://img.shields.io/badge/Licencia-MIT-green?style=for-the-badge" alt="License Badge"/>

<br/>

<a href="https://github.com/martin-ratti" target="_blank" style="text-decoration: none;">
    <img src="https://img.shields.io/badge/👤%20Martín%20Ratti-martin--ratti-000000?style=for-the-badge&logo=github&logoColor=white" alt="Martin"/>
</a>

<br/>

<p>
    <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python Badge"/>
    <img src="https://img.shields.io/badge/Arquitectura-Clean%20Arch-orange?style=for-the-badge&logo=expertsexchange&logoColor=white" alt="Clean Arch Badge"/>
    <img src="https://img.shields.io/badge/GUI-CustomTkinter-2B2B2B?style=for-the-badge&logo=tkinter&logoColor=white" alt="CustomTkinter Badge"/>
    <img src="https://img.shields.io/badge/API-ytmusicapi-FF0000?style=for-the-badge&logo=youtube&logoColor=white" alt="YTMusic Badge"/>
    <img src="https://img.shields.io/badge/Build-PyInstaller-0054a6?style=for-the-badge&logo=pypi&logoColor=white" alt="PyInstaller Badge"/>
</p>

</div>

---

## 🎯 Objetivo y Alcance

**YTSorter** es una aplicación de escritorio diseñada para empoderar a los usuarios de **YouTube Music**. Su función principal es permitir el ordenamiento masivo y personalizado de playlists, una funcionalidad que la plataforma nativa no ofrece de forma nativa.

La filosofía central es **"Non-Destructive"**: La aplicación nunca modifica tus playlists originales. En su lugar, lee la lista, aplica el ordenamiento deseado en memoria y crea una **nueva playlist** en tu cuenta (ej. *"Mi Lista [Ordenada]"*), garantizando la seguridad de tu curaduría.

---

## 🏛️ Arquitectura y Diseño

El proyecto implementa una arquitectura modular para separar la lógica de presentación, las reglas de negocio (ordenamiento) y la comunicación externa.

### Diagrama de Componentes

| Capa | Componente | Responsabilidad |
| :--- | :--- | :--- |
| **Interface** | `src/interface/gui.py` | Gestiona la ventana, el diálogo de login (`AuthDialog`) y la visualización de progreso. |
| **Core** | `src/core/entities.py` | Define qué es un `Track` y contiene la lógica de normalización de texto para el ordenamiento (ignorar acentos, mayúsculas). |
| **Infrastructure** | `src/infrastructure/yt_service.py` | Encapsula la librería `ytmusicapi`. Maneja la sesión, recuperación de librerías y creación de playlists. |

-----

## 🚀 Características Principales

  * **🛡️ Modo Seguro:** Algoritmo de "Solo Lectura" en las fuentes. Tus playlists originales están a salvo.
  * **🔑 Autenticación Flexible:** Sistema capaz de parsear y limpiar automáticamente los *Request Headers* crudos copiados del navegador.
  * **👁️ Previsualización en Vivo:** Tabla interactiva para verificar el nuevo orden antes de confirmar la creación en YouTube.
  * **🎛️ Criterios Avanzados:**
      * **Smart Sort:** Normalización Unicode (tildes, emojis) para un orden alfabético real.
      * **Opciones:** Por Artista, Álbum, Título, Duración, Shuffle y Orden Inverso.
  * **💾 Persistencia:** Guarda el token de sesión localmente (`auth.json`) para no requerir login en cada uso.

-----

## 🔑 Guía de Conexión (Setup Inicial)

Para acceder a tu cuenta, la aplicación necesita una "cookie" de sesión válida. Esto se hace una sola vez.

> **🔒 Privacidad:** Los datos se guardan en `auth.json` en tu PC. **Nunca** se envían a servidores de terceros.

1.  Abre **[music.youtube.com](https://music.youtube.com)** en tu navegador (Chrome/Edge/Firefox).
2.  Abre las Herramientas de Desarrollador (**F12** o Click Derecho -\> Inspeccionar) y ve a la pestaña **Network**.
3.  Navega por la web (clic en "Biblioteca") hasta ver tráfico en la lista.
4.  Busca una petición llamada `browse` (o `guide`).
5.  En los detalles de la petición, busca **"Request Headers"**, copia todo el bloque de texto y pégalo en la ventana de login de YTSorter.

-----

## 🛠️ Modo de Uso

```text
/YTSorter
├── YTSorter.exe       <-- La aplicación
├── auth.json          <-- Tu sesión (se crea al loguearse)
└── assets/            <-- Fuentes e iconos
```

1.  **Conectar:** Pega tus headers si es la primera vez.
2.  **Seleccionar:** Elige una playlist de tu biblioteca en el menú desplegable.
3.  **Configurar:** Elige el criterio (ej. *Artista*) y si deseas invertir el orden.
4.  **Analizar:** Presiona "Re-Analizar" para descargar la metadata y ver la previsualización.
5.  **Confirmar:** Si te gusta el resultado, presiona "Confirmar y Crear Playlist".

-----

## ❓ Solución de Problemas (Troubleshooting)

**Error: "No se pudo autenticar" o la sesión expiró.**
Las cookies de Google caducan eventualmente.

1.  Cierra la aplicación.
2.  Elimina el archivo `auth.json`.
3.  Repite el paso de **Guía de Conexión** para generar credenciales frescas.

-----

## 🧑‍💻 Setup para Desarrolladores

Si deseas modificar el código o compilar tu propia versión:

### 1\. Configuración del Entorno

```bash
# Clonar repositorio
git clone [https://github.com/martin-ratti/yt-sorter.git](https://github.com/martin-ratti/yt-sorter.git)

# Crear entorno virtual
python -m venv venv
.\venv\Scripts\activate  # Windows

# Instalar dependencias
pip install -r requirements.txt
```

### 2\. Ejecución en Desarrollo

```bash
python main.py
```

### 3\. Compilación (.exe)

El proyecto incluye un script de construcción automatizado:

```bash
python build_exe.py
```

*Esto generará el archivo `YTSorter.exe` en la carpeta `dist/` incluyendo todos los assets necesarios.*

-----

## ⚖️ Disclaimer

Desarrollado por **Martín Ratti**.

*Este proyecto es una herramienta de terceros y no está afiliado, asociado, autorizado, respaldado ni conectado oficialmente de ninguna manera con YouTube, Google LLC, ni ninguna de sus subsidiarias o afiliadas. Úsalo bajo tu propia responsabilidad.*
