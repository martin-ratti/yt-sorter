import threading
import customtkinter as ctk
from tkinter import messagebox
from src.core.entities import PlaylistSorter
from src.infrastructure.yt_service import YTService

COLOR_BG = "#000000"
COLOR_SURFACE = "#1F1F1F"
COLOR_ACCENT = "#FF0000"
COLOR_TEXT_MAIN = "#FFFFFF"
COLOR_TEXT_SEC = "#AAAAAA"

class YTSorterApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("YTM Sorter | Python Scripter")
        self.geometry("600x750")
        self.resizable(False, False)
        
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("dark-blue")

        self.service = YTService()
        self.playlists_data = {}
        self._setup_ui()
        
        # INTENTO DE AUTO-LOGIN
        self._try_auto_login()

    def _setup_ui(self):
        self.main_frame = ctk.CTkFrame(self, fg_color=COLOR_BG)
        self.main_frame.pack(fill="both", expand=True)

        self.header_label = ctk.CTkLabel(self.main_frame, text="YouTube Music Sorter", font=("Roboto Medium", 24), text_color=COLOR_TEXT_MAIN)
        self.header_label.pack(pady=(20, 10))

        # Login
        self.login_frame = ctk.CTkFrame(self.main_frame, fg_color=COLOR_SURFACE, corner_radius=10)
        self.login_frame.pack(pady=10, padx=30, fill="x")
        self.lbl_auth = ctk.CTkLabel(self.login_frame, text="1. Autenticación", text_color=COLOR_TEXT_SEC)
        self.lbl_auth.pack(anchor="w", padx=15, pady=(10, 5))
        
        self.headers_entry = ctk.CTkTextbox(self.login_frame, height=60, fg_color="#121212", text_color="white")
        self.headers_entry.pack(padx=15, pady=5, fill="x")
        
        self.btn_login = ctk.CTkButton(self.login_frame, text="Conectar Cuenta", fg_color=COLOR_SURFACE, border_color=COLOR_ACCENT, border_width=1, hover_color="#333333", command=self.on_login)
        self.btn_login.pack(pady=10, padx=15, fill="x")

        # Selección
        self.ops_frame = ctk.CTkFrame(self.main_frame, fg_color=COLOR_SURFACE, corner_radius=10)
        self.ops_frame.pack(pady=10, padx=30, fill="x")
        ctk.CTkLabel(self.ops_frame, text="2. Selección de Playlist", text_color=COLOR_TEXT_SEC).pack(anchor="w", padx=15, pady=(10, 5))
        
        self.playlist_option = ctk.CTkOptionMenu(self.ops_frame, values=["Conecta primero..."], fg_color="#333333", button_color="#444444", text_color="white")
        self.playlist_option.pack(padx=15, pady=5, fill="x")
        self.playlist_option.configure(state="disabled")

        # Criterio
        ctk.CTkLabel(self.ops_frame, text="3. Criterio de Orden", text_color=COLOR_TEXT_SEC).pack(anchor="w", padx=15, pady=(10, 5))
        self.radio_var = ctk.IntVar(value=0)
        criteria = [("Artista", "artist"), ("Título", "title"), ("Álbum", "album"), ("Duración", "duration")]
        self.radio_frame = ctk.CTkFrame(self.ops_frame, fg_color="transparent")
        self.radio_frame.pack(padx=15, pady=5, fill="x")
        self.criterios_map = {}
        for idx, (text, val) in enumerate(criteria):
            r = ctk.CTkRadioButton(self.radio_frame, text=text, variable=self.radio_var, value=idx, fg_color=COLOR_ACCENT, hover_color=COLOR_ACCENT)
            r.grid(row=0, column=idx, padx=10, pady=10)
            self.criterios_map[idx] = val

        # Acción
        self.btn_process = ctk.CTkButton(self.main_frame, text="ORDENAR PLAYLIST", font=("Roboto Bold", 16), fg_color=COLOR_ACCENT, hover_color="#CC0000", height=50, corner_radius=25, state="disabled", command=self.start_processing_thread)
        self.btn_process.pack(pady=20, padx=30, fill="x")

        # Feedback Area
        self.progress = ctk.CTkProgressBar(self.main_frame, progress_color=COLOR_ACCENT)
        self.progress.pack(side="bottom", fill="x")
        self.progress.set(0)

        self.log_box = ctk.CTkTextbox(self.main_frame, height=60, fg_color="transparent", text_color="red", font=("Consolas", 12))
        self.log_box.pack(side="bottom", fill="x", padx=10, pady=5)
        self.log_box.insert("0.0", "Esperando conexión...")
        self.log_box.configure(state="disabled")

    def log(self, message, color=None):
        self.log_box.configure(state="normal")
        self.log_box.delete("0.0", "end")
        self.log_box.insert("0.0", message)
        if color:
            self.log_box.configure(text_color=color)
        self.log_box.configure(state="disabled")

    def _try_auto_login(self):
        """Intenta cargar la sesión guardada al iniciar."""
        saved_auth = self.service.load_session()
        if saved_auth:
            self.headers_entry.insert("0.0", "Sesión guardada detectada. Conectando...")
            self.headers_entry.configure(state="disabled") # Bloqueamos para que se note
            self.log("Sesión previa encontrada. Autoconectando...", "yellow")
            
            # Lanzamos el login automático en hilo
            threading.Thread(target=self._login_and_fetch_bg, args=(saved_auth,)).start()

    def on_login(self):
        headers = self.headers_entry.get("0.0", "end").strip()
        if not headers: return
        
        self.btn_login.configure(state="disabled", text="Validando...")
        self.log("Procesando headers...", COLOR_TEXT_MAIN)
        self.progress.start()

        threading.Thread(target=self._login_and_fetch_bg, args=(headers,)).start()

    def _login_and_fetch_bg(self, headers):
        try:
            self.service.login(headers)
            self.log("Autenticado. Descargando lista de playlists...", "yellow")
            
            playlists = self.service.fetch_playlists()
            self.playlists_data = {p['title']: p['id'] for p in playlists}
            titles = list(self.playlists_data.keys())

            self.playlist_option.configure(values=titles, state="normal")
            if titles: self.playlist_option.set(titles[0])
            
            self.btn_login.configure(text="Cuenta Conectada ✅", fg_color="green", state="disabled")
            self.btn_process.configure(state="normal")
            self.headers_entry.configure(state="normal") # Desbloqueamos por si quiere cambiar
            self.log(f"Conectado. {len(titles)} playlists encontradas.", "green")
            
        except Exception as e:
            self.log(f"Error: {str(e)}", "red")
            self.btn_login.configure(state="normal", text="Conectar Cuenta")
            self.headers_entry.configure(state="normal")
            self.headers_entry.delete("0.0", "end") # Limpiar si falló el auto-login
        finally:
            self.progress.stop()
            self.progress.set(0 if not self.playlists_data else 1)

    def start_processing_thread(self):
        selected_title = self.playlist_option.get()
        criteria_key = self.criterios_map[self.radio_var.get()]
        if not selected_title or selected_title not in self.playlists_data: return
        
        pid = self.playlists_data[selected_title]
        self.btn_process.configure(state="disabled", text="Procesando...")
        self.progress.start()
        
        threading.Thread(target=self._process_logic, args=(selected_title, pid, criteria_key)).start()

    def _process_logic(self, title, pid, criteria):
        try:
            self.log("1/3 Descargando canciones (puede tardar)...", "yellow")
            tracks = self.service.fetch_tracks(pid)
            
            self.log(f"2/3 Ordenando {len(tracks)} canciones...", "yellow")
            sorted_tracks = PlaylistSorter.sort_tracks(tracks, criteria)
            sorted_ids = [t.id for t in sorted_tracks]
            
            new_title = f"{title} [Sorted by {criteria.capitalize()}]"
            self.log(f"3/3 Creando '{new_title}' (Modo Lento Seguro)...", "yellow")
            self.service.create_playlist(new_title, sorted_ids)
            
            self.log(f"¡ÉXITO! Playlist '{new_title}' completa.", "green")
            messagebox.showinfo("Éxito", f"La playlist '{new_title}' ha sido creada correctamente con {len(sorted_ids)} canciones.")
        except Exception as e:
            self.log(f"Error: {str(e)}", "red")
        finally:
            self.progress.stop()
            self.progress.set(1)
            self.btn_process.configure(state="normal", text="ORDENAR OTRA")