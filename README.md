<h1 align="center">🎵 YTSorter - YouTube Music Manager</h1>

<div align="center">
    <img src="https://img.shields.io/badge/Estado-Producción-success?style=for-the-badge&logo=check&logoColor=white" alt="Estado Badge"/>
    <img src="https://img.shields.io/badge/Versión-2.3.0-blue?style=for-the-badge" alt="Version Badge"/>
</div>

<p align="center">
    <a href="https://github.com/martin-ratti" target="_blank" style="text-decoration: none;">
        <img src="https://img.shields.io/badge/👤%20Martín%20Ratti-martin--ratti-000000?style=for-the-badge&logo=github&logoColor=white" alt="Martin"/>
    </a>
</p>

<p align="center">
    <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python Badge"/>
    <img src="https://img.shields.io/badge/GUI-CustomTkinter-2B2B2B?style=for-the-badge&logo=tkinter&logoColor=white" alt="CustomTkinter Badge"/>
    <img src="https://img.shields.io/badge/API-YTMusic-FF0000?style=for-the-badge&logo=youtube&logoColor=white" alt="YTMusic Badge"/>
    <img src="https://img.shields.io/badge/Platform-Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white" alt="Windows Badge"/>
</p>

<hr>

<h2>🎯 Objetivo y Alcance</h2>

<p>
    <strong>YTSorter</strong> es una aplicación de escritorio avanzada diseñada para gestionar y ordenar masivamente playlists de <strong>YouTube Music</strong>. 
    Su prioridad es la seguridad de los datos y la flexibilidad del usuario.
</p>

<p>
    A diferencia de otras herramientas, YTSorter <strong>nunca modifica tus playlists originales</strong>. En su lugar, analiza la lista, 
    permite previsualizar el nuevo orden y genera una <em>nueva</em> playlist ordenada en tu cuenta, garantizando que nunca pierdas tu curaduría original.
</p>

<hr>

<h2>⚙️ Stack Tecnológico & Arquitectura</h2>

<p>El proyecto implementa <strong>Clean Architecture</strong> para asegurar un código mantenible y modular.</p>

<table>
 <thead>
  <tr>
   <th>Capa / Componente</th>
   <th>Tecnología / Ruta</th>
   <th>Descripción</th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td><strong>Interface (GUI)</strong></td>
   <td><code>src/interface/</code> (CustomTkinter)</td>
   <td>Maneja la UI moderna (Dark Mode), hilos de ejecución para no congelar la ventana y feedback visual de progreso.</td>
  </tr>
  <tr>
   <td><strong>Core (Dominio)</strong></td>
   <td><code>src/core/</code> (Python Puro)</td>
   <td>Contiene la lógica pura de ordenamiento (Entidades <code>Track</code> y algoritmos de normalización de texto).</td>
  </tr>
  <tr>
   <td><strong>Infrastructure</strong></td>
   <td><code>src/infrastructure/</code> (ytmusicapi)</td>
   <td>Implementación de la comunicación con YouTube Music, manejo de sesión (<code>auth.json</code>) y subida por lotes.</td>
  </tr>
  <tr>
   <td><strong>Empaquetado</strong></td>
   <td>PyInstaller</td>
   <td>Script de compilación automatizado (<code>build_exe.py</code>) para generar un ejecutable portable.</td>
  </tr>
 </tbody>
</table>

<hr>

<h2>🚀 Características Principales</h2>

<ul>
    <li><strong>🔑 Autenticación Inteligente</strong>: Sistema de login capaz de parsear y limpiar automáticamente los <em>Request Headers</em> crudos del navegador.</li>
    <li><strong>🛡️ Modo Seguro (Non-Destructive)</strong>: Crea copias ordenadas (ej: <em>"Mi Lista [By Artist]"</em>) sin tocar la lista fuente.</li>
    <li><strong>👁️ Previsualización en Vivo</strong>: Tabla interactiva que muestra el "Antes y Después" con indicadores de desplazamiento (▲ ▼) antes de confirmar.</li>
    <li><strong>🎛️ Criterios de Ordenamiento</strong>:
        <ul>
            <li><strong>Artista / Álbum / Título:</strong> Con normalización de caracteres (ignora acentos/mayúsculas).</li>
            <li><strong>Duración:</strong> De corta a larga.</li>
            <li><strong>Shuffle:</strong> Aleatoriedad real.</li>
            <li><strong>Inverso:</strong> Opción Z-A disponible para todos los criterios.</li>
        </ul>
    </li>
    <li><strong>💾 Persistencia de Sesión</strong>: Guarda el token de acceso localmente para evitar re-autenticarse cada vez.</li>
</ul>

<hr>

<h2>🔑 Guía de Conexión (Setup Inicial)</h2>

<p>Para que la aplicación pueda leer y crear playlists en tu cuenta, necesita una "cookie" válida. Solo se hace una vez:</p>

<ol>
    <li>Abre <strong>music.youtube.com</strong> en tu navegador (Chrome/Edge/Firefox).</li>
    <li>Abre las Herramientas de Desarrollador (<code>F12</code>) y ve a la pestaña <strong>Network</strong>.</li>
    <li>Navega por la web (haz clic en "Biblioteca" o "Inicio") hasta que veas una petición llamada <code>browse</code>.</li>
    <li>Haz clic en ella, busca la sección <strong>"Request Headers"</strong>, copia todo el bloque de texto y pégalo en YTSorter.</li>
</ol>

<hr>

<h2>🛠️ Modo de Uso</h2>

<pre>
/YTSorter
├── YTSorter.exe       <-- La aplicación
├── auth.json          <-- Tu sesión (se crea al loguearse)
└── assets/            <-- Fuentes e iconos
</pre>

<ol>
    <li><strong>Conectar:</strong> Pega tus headers y haz clic en "Conectar".</li>
    <li><strong>Seleccionar:</strong> Elige una playlist de tu biblioteca en el menú desplegable.</li>
    <li><strong>Configurar:</strong> Elige el criterio (ej. <em>Artista</em>) y si deseas invertir el orden.</li>
    <li><strong>Analizar:</strong> Presiona "Re-Analizar" para descargar la metadata y ver la previsualización.</li>
    <li><strong>Confirmar:</strong> Si te gusta el resultado, presiona "Confirmar y Crear Playlist".</li>
</ol>

<hr>

<h2>🧑‍💻 Setup para Desarrolladores</h2>

Si deseas modificar el código o compilar tu propia versión:

<h3>1. Configuración del Entorno</h3>
<pre><code># Clonar repositorio
git clone https://github.com/martin-ratti/yt-sorter.git

# Crear entorno virtual
python -m venv venv
.\venv\Scripts\activate  # Windows

# Instalar dependencias
pip install -r requirements.txt
</code></pre>

<h3>2. Ejecución en Desarrollo</h3>
<pre><code>python main.py</code></pre>

<h3>3. Compilación (.exe)</h3>
<p>El proyecto incluye un script de construcción automatizado:</p>
<pre><code>python build_exe.py</code></pre>
<p><em>Esto generará el archivo <code>YTSorter.exe</code> en la carpeta <code>dist/</code> incluyendo todos los assets necesarios.</em></p>

<hr>

<h2>⚖️ Créditos</h2>

<p>
    Desarrollado por <strong>Martín Ratti</strong>. Este proyecto no está afiliado con Google ni YouTube. Úsalo bajo tu propia responsabilidad.
</p>
