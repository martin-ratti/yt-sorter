<div align="center">

# 🎵 YTSorter - YouTube Music Manager

<img src="https://img.shields.io/badge/Estado-Producción-success?style=for-the-badge&logo=check&logoColor=white" alt="Estado Badge"/>
<img src="https://img.shields.io/badge/Versión-2.3.0-blue?style=for-the-badge" alt="Version Badge"/>

<br/>

<a href="https://github.com/martin-ratti" target="_blank" style="text-decoration: none;">
    <img src="https://img.shields.io/badge/👤%20Martín%20Ratti-martin--ratti-000000?style=for-the-badge&logo=github&logoColor=white" alt="Martin"/>
</a>

<br/>

<p>
    <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python Badge"/>
    <img src="https://img.shields.io/badge/API-YTMusic-FF0000?style=for-the-badge&logo=youtube&logoColor=white" alt="YTMusic Badge"/>
    <img src="https://img.shields.io/badge/GUI-CustomTkinter-2B2B2B?style=for-the-badge&logo=tkinter&logoColor=white" alt="CustomTkinter Badge"/>
    <img src="https://img.shields.io/badge/Platform-Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white" alt="Windows Badge"/>
</p>

</div>

---

## 🎯 Objetivo y Alcance

**YTSorter** es una aplicación de escritorio avanzada diseñada para gestionar y ordenar masivamente playlists de **YouTube Music**. Su prioridad es la seguridad de los datos y la flexibilidad del usuario.

A diferencia de otras herramientas, YTSorter **nunca modifica tus playlists originales**. En su lugar, analiza la lista, permite previsualizar el nuevo orden y genera una *nueva* playlist ordenada en tu cuenta (ej. *"Mi Lista [Ordenada]"*), garantizando que nunca pierdas tu curaduría original.

---

## ⚙️ Stack Tecnológico & Arquitectura

El proyecto implementa **Clean Architecture** para asegurar un código mantenible y modular.

| Capa / Componente | Tecnología / Ruta | Descripción |
| :--- | :--- | :--- |
| **Interface (GUI)** | `src/interface/`<br>_(CustomTkinter)_ | Maneja la UI moderna (Dark Mode), hilos de ejecución para no congelar la ventana y feedback visual de progreso. |
| **Core (Dominio)** | `src/core/`<br>_(Python Puro)_ | Contiene la lógica pura de ordenamiento (Entidades `Track` y algoritmos de normalización de texto). |
| **Infrastructure** | `src/infrastructure/`<br>_(ytmusicapi)_ | Implementación de la comunicación con YouTube Music, manejo de sesión (`auth.json`) y subida por lotes. |
| **Empaquetado** | PyInstaller | Script de compilación automatizado (`build_exe.py`) para generar un ejecutable portable. |

---

## 🚀 Características Principales

* **🔑 Autenticación Inteligente:** Sistema de login capaz de parsear y limpiar automáticamente los *Request Headers* crudos del navegador.
* **🛡️ Modo Seguro (Non-Destructive):** Crea copias ordenadas sin tocar la lista fuente.
* **👁️ Previsualización en Vivo:** Tabla interactiva que muestra el "Antes y Después" con indicadores de desplazamiento (▲ ▼) antes de confirmar.
* **🎛️ Criterios de Ordenamiento:**
    * **Artista / Álbum / Título:** Con normalización de caracteres (ignora acentos/mayúsculas).
    * **Duración:** De corta a larga.
    * **Shuffle:** Aleatoriedad real.
    * **Inverso:** Opción Z-A disponible para todos los criterios.
* **💾 Persistencia de Sesión:** Guarda el token de acceso localmente (`auth.json`) para evitar re-autenticarse cada vez.

---

## 🔑 Guía de Conexión (Setup Inicial)

Para que la aplicación pueda leer y crear playlists en tu cuenta, necesita una "cookie" válida.

> **🔒 Nota de Privacidad:** Los datos de sesión se guardan únicamente en tu archivo local `auth.json`. **Nunca** se envían a servidores externos.

1.  Abre **[music.youtube.com](https://music.youtube.com)** en tu navegador (Chrome/Edge/Firefox).
2.  Abre las Herramientas de Desarrollador (**F12** o Click Derecho -> Inspeccionar) y ve a la pestaña **Network**.
3.  Navega por la web (haz clic en "Biblioteca" o "Inicio") hasta que veas aparecer peticiones en la lista.
4.  Busca una petición llamada `browse` (o `guide`).
5.  Haz clic en ella, busca la sección **"Request Headers"** (a la derecha), copia todo el bloque de texto y pégalo en YTSorter.

---

## 🛠️ Modo de Uso

```text
/YTSorter
├── YTSorter.exe       <-- La aplicación
├── auth.json          <-- Tu sesión (se crea al loguearse)
└── assets/            <-- Fuentes e iconos
````

1.  **Conectar:** Pega tus headers y haz clic en "Conectar".
2.  **Seleccionar:** Elige una playlist de tu biblioteca en el menú desplegable.
3.  **Configurar:** Elige el criterio (ej. *Artista*) y si deseas invertir el orden.
4.  **Analizar:** Presiona "Re-Analizar" para descargar la metadata y ver la previsualización.
5.  **Confirmar:** Si te gusta el resultado, presiona "Confirmar y Crear Playlist".

-----

## ❓ Solución de Problemas (Troubleshooting)

**Error: "No se pudo autenticar" o la sesión expiró.**
Las cookies de Google/YouTube caducan con el tiempo o si cierras sesión en el navegador.

1.  Elimina el archivo `auth.json`.
2.  Abre la aplicación.
3.  Repite el paso de **Guía de Conexión** para generar un token fresco.

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

## ⚖️ Créditos y Disclaimer

Desarrollado por **Martín Ratti**.

*Este proyecto es una herramienta de terceros y no está afiliado, asociado, autorizado, respaldado ni conectado oficialmente de ninguna manera con YouTube, Google LLC, ni ninguna de sus subsidiarias o afiliadas. Úsalo bajo tu propia responsabilidad.*
