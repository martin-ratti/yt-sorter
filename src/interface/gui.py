import threading
import os
import sys
import ctypes
import customtkinter as ctk
from tkinter import messagebox
from src.core.entities import PlaylistSorter
from src.infrastructure.yt_service import YTService

# --- UTILS ---
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def load_custom_font(font_path):
    try:
        gdi32 = ctypes.windll.gdi32
        gdi32.AddFontResourceExW(font_path, 0x10, 0)
        return "Roboto Medium"
    except:
        return "Arial"

FONT_FILE = resource_path(os.path.join("assets", "Roboto-Medium.ttf"))
FONT_NAME = load_custom_font(FONT_FILE)

# --- ESTILOS ---
COLOR_BG = "#030303"
COLOR_SURFACE = "#212121"
COLOR_ACCENT = "#FF0000"
COLOR_GREEN = "#2E7D32"
COLOR_TEXT_MAIN = "#FFFFFF"
COLOR_TEXT_SEC = "#AAAAAA"

FONT_TITLE = (FONT_NAME, 22)
FONT_SECTION = (FONT_NAME, 14, "bold")
FONT_NORMAL = (FONT_NAME, 13)
FONT_BUTTON = (FONT_NAME, 13, "bold")
FONT_SMALL = (FONT_NAME, 11)
FONT_LOGS = ("Consolas", 11)

# --- VENTANA AYUDA ---
class HelpWindow(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("450x350")
        self.title("Ayuda")
        self.resizable(False, False)
        self.attributes("-topmost", True)
        self.configure(fg_color=COLOR_BG)
        
        frame = ctk.CTkFrame(self, fg_color=COLOR_SURFACE, corner_radius=10)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(frame, text="¿Cómo obtener los Headers?", font=FONT_SECTION, text_color=COLOR_ACCENT).pack(pady=(20, 10))
        
        steps = [
            "1. Abre music.youtube.com (F12 > Network).",
            "2. Haz clic en cualquier petición (ej. 'browse').",
            "3. Copia todo el bloque 'Request Headers'.",
            "4. Pégalo en la aplicación."
        ]
        
        for step in steps:
            ctk.CTkLabel(frame, text=step, font=FONT_NORMAL, text_color=COLOR_TEXT_MAIN, anchor="w").pack(fill="x", padx=20, pady=5)
            
        ctk.CTkButton(frame, text="Entendido", fg_color=COLOR_ACCENT, hover_color="#CC0000", command=self.destroy).pack(pady=20)

# --- APP PRINCIPAL ---
class YTSorterApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("YTM Sorter v2.3 Final")
        self.geometry("650x750")
        self.resizable(True, True)
        
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("dark-blue")
        
        self.service = YTService()
        self.playlists_data = {}
        self.preview_tracks = [] 
        self.original_title = ""
        self.target_criteria = ""

        self._setup_layout()
        self._try_auto_login()

    def _setup_layout(self):
        # 1. FRAME PRINCIPAL
        self.main_frame = ctk.CTkFrame(self, fg_color=COLOR_BG)
        self.main_frame.pack(fill="both", expand=True)

        # 2. PANEL INFERIOR FIJO (Sticky Footer)
        self.bottom_panel = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.bottom_panel.pack(side="bottom", fill="x", padx=20, pady=10)
        
        # Contenedor del botón de acción
        self.action_container = ctk.CTkFrame(self.bottom_panel, fg_color="transparent", height=50)
        self.action_container.pack(fill="x", pady=(0, 10))
        self.action_container.pack_propagate(False)

        self.btn_process = ctk.CTkButton(
            self.action_container, 
            text="🚀 CONFIRMAR Y CREAR PLAYLIST", 
            font=FONT_BUTTON, 
            fg_color=COLOR_GREEN, 
            hover_color="#1B5E20", 
            height=45, 
            width=400,
            command=self.start_upload
        )

        # Progreso y Logs
        self.progress = ctk.CTkProgressBar(self.bottom_panel, progress_color=COLOR_ACCENT, height=3)
        self.progress.pack(fill="x", pady=(0, 5))
        self.progress.set(0)
        
        self.lbl_status = ctk.CTkLabel(self.bottom_panel, text="Esperando...", font=FONT_SMALL, text_color="#AAA", anchor="w")
        self.lbl_status.pack(fill="x")

        # 3. PANEL SUPERIOR SCROLLABLE
        self.scroll_content = ctk.CTkScrollableFrame(self.main_frame, fg_color="transparent")
        self.scroll_content.pack(side="top", fill="both", expand=True, padx=10)

        # --- CONTENIDO SCROLL ---
        ctk.CTkLabel(self.scroll_content, text="YouTube Music Sorter", font=FONT_TITLE, text_color=COLOR_TEXT_MAIN).pack(pady=(20, 15))

        # Login
        self.login_frame = ctk.CTkFrame(self.scroll_content, fg_color=COLOR_SURFACE, corner_radius=10)
        self.login_frame.pack(fill="x", padx=10, pady=5)
        
        row_login = ctk.CTkFrame(self.login_frame, fg_color="transparent")
        row_login.pack(fill="x", padx=15, pady=10)
        ctk.CTkLabel(row_login, text="1. Autenticación", font=FONT_SECTION).pack(side="left")
        ctk.CTkButton(row_login, text="?", width=25, height=25, fg_color="#444", command=self.open_help_window).pack(side="right")

        self.headers_entry = ctk.CTkTextbox(self.login_frame, height=35, fg_color="#000000", border_width=0, text_color="white")
        self.headers_entry.pack(padx=15, pady=(0, 10), fill="x")
        
        self.btn_login = ctk.CTkButton(self.login_frame, text="Conectar", height=30, fg_color=COLOR_SURFACE, border_color="#444", border_width=1, command=self.on_login)
        self.btn_login.pack(padx=15, pady=(0, 15), fill="x")

        # Config
        self.control_frame = ctk.CTkFrame(self.scroll_content, fg_color=COLOR_SURFACE, corner_radius=10)
        self.control_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(self.control_frame, text="2. Configuración", font=FONT_SECTION).pack(anchor="w", padx=15, pady=10)
        self.playlist_option = ctk.CTkOptionMenu(self.control_frame, values=["..."], fg_color="#333", width=400)
        self.playlist_option.pack(padx=15, fill="x")
        self.playlist_option.configure(state="disabled")

        self.crit_frame = ctk.CTkFrame(self.control_frame, fg_color="transparent")
        self.crit_frame.pack(padx=10, pady=10, fill="x")
        
        self.radio_var = ctk.IntVar(value=0)
        criteria = [("Artista", "artist"), ("Título", "title"), ("Álbum", "album"), ("Duración", "duration")]
        self.criterios_map = {}
        for idx, (text, val) in enumerate(criteria):
            r = ctk.CTkRadioButton(self.crit_frame, text=text, variable=self.radio_var, value=idx, font=FONT_NORMAL, fg_color=COLOR_ACCENT)
            r.grid(row=0, column=idx, padx=5, sticky="w")
            self.criterios_map[idx] = val

        self.chk_reverse = ctk.CTkCheckBox(self.control_frame, text="Invertir (Z-A)", font=FONT_NORMAL, fg_color=COLOR_ACCENT)
        self.chk_reverse.pack(pady=(0, 15))

        # Botón Analizar
        self.btn_analyze = ctk.CTkButton(self.scroll_content, text="🔍 RE-ANALIZAR", font=FONT_BUTTON, fg_color=COLOR_ACCENT, hover_color="#CC0000", height=45, state="disabled", command=self.start_analysis)
        self.btn_analyze.pack(pady=10, padx=20, fill="x")

        # Preview Frame
        self.preview_frame = ctk.CTkFrame(self.scroll_content, fg_color="#111", corner_radius=8)

    # --- LOGICA ---
    def open_help_window(self):
        HelpWindow(self)

    def log(self, text):
        self.lbl_status.configure(text=f"> {text}")

    def _try_auto_login(self):
        saved = self.service.load_session()
        if saved:
            self.headers_entry.insert("0.0", "Sesión guardada.")
            self.headers_entry.configure(state="disabled")
            threading.Thread(target=self._login_bg, args=(saved,)).start()

    def on_login(self):
        h = self.headers_entry.get("0.0", "end").strip()
        if not h: return
        self.btn_login.configure(state="disabled")
        self.progress.start()
        threading.Thread(target=self._login_bg, args=(h,)).start()

    def _login_bg(self, h):
        try:
            self.service.login(h)
            playlists = self.service.fetch_playlists()
            self.playlists_data = {p['title']: p['id'] for p in playlists}
            titles = list(self.playlists_data.keys())
            self.playlist_option.configure(values=titles, state="normal")
            if titles: self.playlist_option.set(titles[0])
            self.btn_login.configure(text="Conectado", fg_color=COLOR_GREEN)
            self.btn_analyze.configure(state="normal")
            self.log(f"Conectado. {len(titles)} playlists.")
        except Exception as e:
            self.log(f"Error: {e}")
            self.btn_login.configure(state="normal")
        finally:
            self.progress.stop()
            self.progress.set(0)

    def start_analysis(self):
        title = self.playlist_option.get()
        pid = self.playlists_data.get(title)
        crit = self.criterios_map[self.radio_var.get()]
        rev = bool(self.chk_reverse.get())
        
        if not pid: return
        
        self.btn_analyze.configure(state="disabled", text="ANALIZANDO...")
        self.progress.start()
        self.btn_process.pack_forget()
        self.preview_frame.pack_forget()
        
        self.original_title = title
        self.target_criteria = crit
        
        threading.Thread(target=self._analysis_bg, args=(pid, crit, rev)).start()

    def _analysis_bg(self, pid, crit, rev):
        try:
            self.log("Descargando canciones...")
            tracks = self.service.fetch_tracks(pid)
            self.log("Ordenando...")
            sorted_tracks = PlaylistSorter.sort_tracks(tracks, crit, rev)
            self.preview_tracks = sorted_tracks
            self.after(0, self._show_preview, sorted_tracks)
        except Exception as e:
            self.log(f"Error: {e}")
        finally:
            self.progress.stop()
            self.progress.set(1)
            self.btn_analyze.configure(state="normal")

    def _show_preview(self, sorted_tracks):
        # Limpieza
        for widget in self.preview_frame.winfo_children():
            widget.destroy()
            
        self.preview_frame.pack(pady=5, padx=10, fill="both")

        # Headers
        ctk.CTkLabel(self.preview_frame, text="#", width=30, font=("Consolas", 12, "bold")).grid(row=0, column=0, pady=5)
        ctk.CTkLabel(self.preview_frame, text="Canción", anchor="w", font=("Consolas", 12, "bold")).grid(row=0, column=1, sticky="w", pady=5)
        ctk.CTkLabel(self.preview_frame, text="Mov.", width=50, font=("Consolas", 12, "bold")).grid(row=0, column=2, pady=5)

        total = len(sorted_tracks)
        self.log(f"Renderizando {total} filas...")
        self.update_idletasks()

        for i, track in enumerate(sorted_tracks):
            old = track.original_index
            diff = old - i
            
            if diff > 0: sym = "▲" ; col = "green"
            elif diff < 0: sym = "▼" ; col = "red"
            else: sym = "=" ; col = "gray"
            
            ctk.CTkLabel(self.preview_frame, text=f"{i+1}", width=30).grid(row=i+1, column=0)
            ctk.CTkLabel(self.preview_frame, text=f"{track.artist} - {track.title}"[:45], anchor="w").grid(row=i+1, column=1, sticky="w")
            ctk.CTkLabel(self.preview_frame, text=f"{sym} {abs(diff)}", text_color=col).grid(row=i+1, column=2)

        # Mostrar botón de acción
        self.btn_process.pack(fill="both", expand=True)
        self.log(f"Vista previa lista.")

    def start_upload(self):
        self.btn_process.configure(state="disabled")
        self.btn_analyze.configure(state="disabled")
        
        # --- SOLUCIÓN AL BLACK SCREEN ---
        # 1. No borramos el frame (pack_forget), solo limpiamos su contenido
        # 2. Mostramos el estado de trabajo AHÍ MISMO
        
        # Limpiar tabla
        for widget in self.preview_frame.winfo_children():
            widget.destroy()
            
        # Mostrar mensaje grande
        self.preview_frame.pack(pady=5, padx=10, fill="both", expand=True)
        ctk.CTkLabel(self.preview_frame, text="⏳", font=(FONT_NAME, 40)).pack(pady=(40, 10))
        ctk.CTkLabel(self.preview_frame, text="TRABAJANDO EN TU PLAYLIST...", font=FONT_TITLE, text_color=COLOR_ACCENT).pack(pady=10)
        ctk.CTkLabel(self.preview_frame, text="Por favor no cierres la ventana.\nEsto puede tardar unos minutos.", font=FONT_NORMAL).pack()
        
        # Ocultar botón de acción (ya se presionó)
        self.btn_process.pack_forget()
        
        # Forzar scroll al tope para que el usuario vea el mensaje
        # (Esto corrige si estaba scrolleado abajo)
        self.scroll_content._parent_canvas.yview_moveto(0)
        
        ids = [t.id for t in self.preview_tracks]
        rev_txt = " [Z-A]" if self.chk_reverse.get() else ""
        new_title = f"{self.original_title} [By {self.target_criteria.capitalize()}{rev_txt}]"
        
        threading.Thread(target=self._upload_bg, args=(new_title, ids)).start()

    def _update_progress(self, msg, percent):
        self.log(msg)
        self.progress.set(percent)

    def _upload_bg(self, title, ids):
        try:
            cb = lambda m, p: self.after(0, self._update_progress, m, p)
            self.service.create_playlist(title, ids, progress_callback=cb)
            self.log("¡ÉXITO TOTAL!")
            self.after(0, lambda: messagebox.showinfo("YTSorter", "Playlist creada correctamente."))
        except Exception as e:
             self.log(f"Error: {e}")
        finally:
             self.btn_analyze.configure(state="normal", text="🔍 ANALIZAR OTRA")
             self.progress.set(1)