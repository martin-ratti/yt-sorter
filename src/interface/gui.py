import threading
import os
import sys
import ctypes
import customtkinter as ctk
from tkinter import messagebox
from src.core.entities import PlaylistSorter
from src.infrastructure.yt_service import YTService

def resource_path(relative_path):
    """Obtiene ruta absoluta para recursos (compatible con PyInstaller)."""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def load_custom_font(font_path):
    """Carga fuente en memoria sin instalación."""
    try:
        gdi32 = ctypes.windll.gdi32
        gdi32.AddFontResourceExW(font_path, 0x10, 0)
        return "Roboto Medium"
    except:
        return "Arial"

# Carga de recursos
FONT_FILE = resource_path(os.path.join("assets", "Roboto-Medium.ttf"))
FONT_NAME = load_custom_font(FONT_FILE)

# Estilos
COLOR_BG = "#030303"
COLOR_SURFACE = "#212121"
COLOR_ACCENT = "#FF0000"
COLOR_TEXT_MAIN = "#FFFFFF"
COLOR_TEXT_SEC = "#AAAAAA"

FONT_TITLE = (FONT_NAME, 28)
FONT_SECTION = (FONT_NAME, 16)
FONT_NORMAL = (FONT_NAME, 14)
FONT_BUTTON = (FONT_NAME, 14)
FONT_LOGS = ("Consolas", 11)

class YTSorterApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("YTM Sorter | Python Scripter")
        self.geometry("600x800")
        self.resizable(False, False)
        
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("dark-blue")
        
        self.service = YTService()
        self.playlists_data = {}
        self._setup_ui()
        self._try_auto_login()

    def _setup_ui(self):
        self.main_frame = ctk.CTkFrame(self, fg_color=COLOR_BG)
        self.main_frame.pack(fill="both", expand=True)

        # Header
        self.header_label = ctk.CTkLabel(self.main_frame, text="YouTube Music Sorter", font=FONT_TITLE, text_color=COLOR_TEXT_MAIN)
        self.header_label.pack(pady=(35, 25))

        # Login Area
        self.login_frame = ctk.CTkFrame(self.main_frame, fg_color=COLOR_SURFACE, corner_radius=12)
        self.login_frame.pack(pady=10, padx=30, fill="x")

        ctk.CTkLabel(self.login_frame, text="1. Autenticación", font=FONT_SECTION, text_color=COLOR_TEXT_MAIN).pack(anchor="w", padx=20, pady=(15, 5))
        
        self.headers_entry = ctk.CTkTextbox(self.login_frame, height=50, fg_color="#000000", text_color="white", font=FONT_NORMAL, border_width=0)
        self.headers_entry.pack(padx=20, pady=5, fill="x")
        
        self.btn_login = ctk.CTkButton(self.login_frame, text="Conectar Cuenta", font=FONT_BUTTON, fg_color=COLOR_SURFACE, border_color="#333333", border_width=2, hover_color="#333333", height=40, command=self.on_login)
        self.btn_login.pack(pady=(10, 15), padx=20, fill="x")

        # Selección Area
        self.ops_frame = ctk.CTkFrame(self.main_frame, fg_color=COLOR_SURFACE, corner_radius=12)
        self.ops_frame.pack(pady=10, padx=30, fill="x")

        ctk.CTkLabel(self.ops_frame, text="2. Playlist a Ordenar", font=FONT_SECTION, text_color=COLOR_TEXT_MAIN).pack(anchor="w", padx=20, pady=(15, 5))
        
        self.playlist_option = ctk.CTkOptionMenu(self.ops_frame, values=["Esperando conexión..."], font=FONT_NORMAL, fg_color="#333333", button_color="#444444", text_color="white", height=35)
        self.playlist_option.pack(padx=20, pady=5, fill="x")
        self.playlist_option.configure(state="disabled")

        # Criterios Area
        ctk.CTkLabel(self.ops_frame, text="3. Criterio", font=FONT_SECTION, text_color=COLOR_TEXT_MAIN).pack(anchor="w", padx=20, pady=(15, 5))
        self.radio_var = ctk.IntVar(value=0)
        criteria = [("Artista", "artist"), ("Título", "title"), ("Álbum", "album"), ("Duración", "duration")]
        self.radio_frame = ctk.CTkFrame(self.ops_frame, fg_color="transparent")
        self.radio_frame.pack(padx=20, pady=(0, 15), fill="x")
        
        self.criterios_map = {}
        for idx, (text, val) in enumerate(criteria):
            r = ctk.CTkRadioButton(self.radio_frame, text=text, variable=self.radio_var, value=idx, font=FONT_NORMAL, fg_color=COLOR_ACCENT, hover_color=COLOR_ACCENT, border_color="#666666")
            r.grid(row=0, column=idx, padx=(0, 15), pady=5)
            self.criterios_map[idx] = val

        # Botón Acción
        self.btn_process = ctk.CTkButton(self.main_frame, text="ORDENAR PLAYLIST", font=("Roboto", 18, "bold"), fg_color=COLOR_ACCENT, hover_color="#CC0000", height=55, corner_radius=27, state="disabled", command=self.start_processing_thread)
        self.btn_process.pack(pady=25, padx=30, fill="x")

        # Logs & Progreso
        self.progress = ctk.CTkProgressBar(self.main_frame, progress_color=COLOR_ACCENT, height=4)
        self.progress.pack(side="bottom", fill="x")
        self.progress.set(0)

        self.log_box = ctk.CTkTextbox(self.main_frame, height=100, fg_color="#000000", text_color="#00FF00", font=FONT_LOGS)
        self.log_box.pack(side="bottom", fill="x", padx=10, pady=5)
        self.log_box.insert("0.0", "> Sistema listo.")
        self.log_box.configure(state="disabled")

    def log(self, message, color=None):
        self.log_box.configure(state="normal")
        self.log_box.insert("end", "\n> " + message)
        self.log_box.see("end")
        self.log_box.configure(state="disabled")

    def _try_auto_login(self):
        saved_auth = self.service.load_session()
        if saved_auth:
            self.headers_entry.delete("0.0", "end")
            self.headers_entry.insert("0.0", "Sesión guardada detectada.")
            self.headers_entry.configure(state="disabled")
            self.log("Autoconectando...", "yellow")
            threading.Thread(target=self._login_and_fetch_bg, args=(saved_auth,)).start()

    def on_login(self):
        headers = self.headers_entry.get("0.0", "end").strip()
        if not headers: return
        self.btn_login.configure(state="disabled", text="Validando...")
        self.log("Procesando...", COLOR_TEXT_MAIN)
        self.progress.start()
        threading.Thread(target=self._login_and_fetch_bg, args=(headers,)).start()

    def _login_and_fetch_bg(self, headers):
        try:
            self.service.login(headers)
            self.log("Obteniendo biblioteca...", "yellow")
            playlists = self.service.fetch_playlists()
            self.playlists_data = {p['title']: p['id'] for p in playlists}
            titles = list(self.playlists_data.keys())
            
            self.playlist_option.configure(values=titles, state="normal")
            if titles: self.playlist_option.set(titles[0])
            
            self.btn_login.configure(text="Conectado", fg_color="#2E7D32", state="disabled")
            self.btn_process.configure(state="normal")
            self.headers_entry.configure(state="normal")
            self.log(f"Listo. {len(titles)} playlists cargadas.", "green")
        except Exception as e:
            self.log(f"Error: {e}", "red")
            self.btn_login.configure(state="normal", text="Conectar")
        finally:
            self.progress.stop()
            self.progress.set(0 if not self.playlists_data else 1)

    def start_processing_thread(self):
        selected_title = self.playlist_option.get()
        criteria_key = self.criterios_map[self.radio_var.get()]
        if not selected_title or selected_title not in self.playlists_data: return
        
        pid = self.playlists_data[selected_title]
        self.btn_process.configure(state="disabled", text="PROCESANDO...")
        self.progress.start()
        threading.Thread(target=self._process_logic, args=(selected_title, pid, criteria_key)).start()

    def _process_logic(self, title, pid, criteria):
        try:
            self.log(f"Analizando '{title}'...", "yellow")
            tracks = self.service.fetch_tracks(pid)
            
            if not tracks: 
                self.log("Error: Playlist vacía.", "red")
                return

            self.log(f"Ordenando {len(tracks)} canciones...", "yellow")
            sorted_tracks = PlaylistSorter.sort_tracks(tracks, criteria)
            
            new_title = f"{title} [Sorted by {criteria.capitalize()}]"
            self.log(f"Creando '{new_title}'...", "yellow")
            self.service.create_playlist(new_title, [t.id for t in sorted_tracks])
            
            self.log("¡ÉXITO! Playlist creada.", "green")
            messagebox.showinfo("YTSorter", "Proceso Finalizado Correctamente")
        except Exception as e:
            self.log(f"Error crítico: {e}", "red")
        finally:
            self.progress.stop()
            self.progress.set(1)
            self.btn_process.configure(state="normal", text="ORDENAR OTRA")