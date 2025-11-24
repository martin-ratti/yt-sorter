import threading
import customtkinter as ctk
from tkinter import messagebox
from src.core.entities import PlaylistSorter
from src.infrastructure.yt_service import YTService

COLOR_BG = '#000000'
COLOR_SURFACE = '#1F1F1F'
COLOR_ACCENT = '#FF0000'
COLOR_TEXT_MAIN = '#FFFFFF'
COLOR_TEXT_SEC = '#AAAAAA'

class YTSorterApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title('YTM Sorter | Python Scripter')
        self.geometry('600x700')
        self.resizable(False, False)
        
        ctk.set_appearance_mode('Dark')
        ctk.set_default_color_theme('dark-blue')

        self.service = YTService()
        self.playlists_data = {}
        self._setup_ui()

    def _setup_ui(self):
        self.main_frame = ctk.CTkFrame(self, fg_color=COLOR_BG)
        self.main_frame.pack(fill='both', expand=True)

        self.header_label = ctk.CTkLabel(self.main_frame, text='YouTube Music Sorter', font=('Roboto Medium', 24), text_color=COLOR_TEXT_MAIN)
        self.header_label.pack(pady=(30, 20))

        # Login
        self.login_frame = ctk.CTkFrame(self.main_frame, fg_color=COLOR_SURFACE, corner_radius=10)
        self.login_frame.pack(pady=10, padx=30, fill='x')
        ctk.CTkLabel(self.login_frame, text='1. Autenticación (Pegar Headers JSON)', text_color=COLOR_TEXT_SEC).pack(anchor='w', padx=15, pady=(10, 5))
        self.headers_entry = ctk.CTkTextbox(self.login_frame, height=80, fg_color='#121212', text_color='white')
        self.headers_entry.pack(padx=15, pady=5, fill='x')
        self.btn_login = ctk.CTkButton(self.login_frame, text='Conectar Cuenta', fg_color=COLOR_SURFACE, border_color=COLOR_ACCENT, border_width=1, hover_color='#333333', command=self.on_login)
        self.btn_login.pack(pady=10, padx=15, fill='x')

        # Selección
        self.ops_frame = ctk.CTkFrame(self.main_frame, fg_color=COLOR_SURFACE, corner_radius=10)
        self.ops_frame.pack(pady=10, padx=30, fill='x')
        ctk.CTkLabel(self.ops_frame, text='2. Selección de Playlist', text_color=COLOR_TEXT_SEC).pack(anchor='w', padx=15, pady=(10, 5))
        self.playlist_option = ctk.CTkOptionMenu(self.ops_frame, values=['Conecta primero...'], fg_color='#333333', button_color='#444444', text_color='white')
        self.playlist_option.pack(padx=15, pady=5, fill='x')
        self.playlist_option.configure(state='disabled')

        # Criterio
        ctk.CTkLabel(self.ops_frame, text='3. Criterio de Orden', text_color=COLOR_TEXT_SEC).pack(anchor='w', padx=15, pady=(10, 5))
        self.radio_var = ctk.IntVar(value=0)
        criteria = [('Artista', 'artist'), ('Título', 'title'), ('Álbum', 'album'), ('Duración', 'duration')]
        self.radio_frame = ctk.CTkFrame(self.ops_frame, fg_color='transparent')
        self.radio_frame.pack(padx=15, pady=5, fill='x')
        self.criterios_map = {}
        for idx, (text, val) in enumerate(criteria):
            r = ctk.CTkRadioButton(self.radio_frame, text=text, variable=self.radio_var, value=idx, fg_color=COLOR_ACCENT, hover_color=COLOR_ACCENT)
            r.grid(row=0, column=idx, padx=10, pady=10)
            self.criterios_map[idx] = val

        # Acción
        self.btn_process = ctk.CTkButton(self.main_frame, text='ORDENAR PLAYLIST', font=('Roboto Bold', 16), fg_color=COLOR_ACCENT, hover_color='#CC0000', height=50, corner_radius=25, state='disabled', command=self.start_processing_thread)
        self.btn_process.pack(pady=30, padx=30, fill='x')

        # Feedback
        self.status_label = ctk.CTkLabel(self.main_frame, text='Esperando usuario...', text_color=COLOR_TEXT_SEC)
        self.status_label.pack(side='bottom', pady=10)
        self.progress = ctk.CTkProgressBar(self.main_frame, progress_color=COLOR_ACCENT)
        self.progress.pack(side='bottom', fill='x')
        self.progress.set(0)

    def on_login(self):
        headers = self.headers_entry.get('0.0', 'end').strip()
        if not headers: return
        self.status_label.configure(text='Verificando credenciales...', text_color=COLOR_ACCENT)
        if self.service.login(headers):
            self.status_label.configure(text='Conectado. Cargando playlists...', text_color='green')
            self.btn_login.configure(text='Cuenta Conectada ✅', fg_color='green', state='disabled')
            threading.Thread(target=self._load_playlists_bg).start()
        else:
            self.status_label.configure(text='Error: Headers inválidos.', text_color='red')

    def _load_playlists_bg(self):
        try:
            playlists = self.service.fetch_playlists()
            self.playlists_data = {p['title']: p['id'] for p in playlists}
            titles = list(self.playlists_data.keys())
            self.playlist_option.configure(values=titles, state='normal')
            if titles: self.playlist_option.set(titles[0])
            self.btn_process.configure(state='normal')
            self.status_label.configure(text=f'Listo. {len(titles)} playlists encontradas.', text_color=COLOR_TEXT_MAIN)
        except Exception as e:
            self.status_label.configure(text=f'Error cargando listas: {e}', text_color='red')

    def start_processing_thread(self):
        selected_title = self.playlist_option.get()
        criteria_key = self.criterios_map[self.radio_var.get()]
        if not selected_title or selected_title not in self.playlists_data: return
        pid = self.playlists_data[selected_title]
        self.btn_process.configure(state='disabled', text='Procesando...')
        self.progress.start()
        threading.Thread(target=self._process_logic, args=(selected_title, pid, criteria_key)).start()

    def _process_logic(self, title, pid, criteria):
        try:
            self.update_status('Descargando canciones...')
            tracks = self.service.fetch_tracks(pid)
            self.update_status(f'Analizando {len(tracks)} canciones...')
            sorted_tracks = PlaylistSorter.sort_tracks(tracks, criteria)
            sorted_ids = [t.id for t in sorted_tracks]
            new_title = f'{title} [Sorted by {criteria.capitalize()}]'
            self.update_status(f'Creando lista: {new_title}...')
            self.service.create_playlist(new_title, sorted_ids)
            self.update_status('¡Éxito! Playlist creada.')
            messagebox.showinfo('Éxito', f'La playlist {new_title} ha sido creada.')
        except Exception as e:
            self.update_status(f'Error: {str(e)}')
            print(e)
        finally:
            self.progress.stop()
            self.progress.set(1)
            self.btn_process.configure(state='normal', text='ORDENAR OTRA')

    def update_status(self, text):
        self.status_label.configure(text=text)
