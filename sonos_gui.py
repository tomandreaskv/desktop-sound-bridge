import threading
import socket
import warnings
import os
import sys
import hmac
import secrets
import queue
import soundcard as sc
from soundcard.mediafoundation import SoundcardRuntimeWarning
import numpy as np
import soco
import tkinter as tk
from tkinter import ttk, messagebox
from flask import Flask, Response, request
from werkzeug.serving import make_server

# ==========================================
# 0. INNSTILLINGER, LOGO OG FEILAVHJELPING
# ==========================================

warnings.filterwarnings("ignore", category=SoundcardRuntimeWarning)

def resource_path(relative_path):
    """ Finner riktig filsti for ressurser, uansett om det er kildekode eller .exe. """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

ICON_PATH = resource_path("logo-2.ico")

# ==========================================
# 1. KONFIGURASJON OG SERVEROPPSETT
# ==========================================

app = Flask(__name__)

def get_local_ip():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]

PORT = 5000

SAMPLE_RATE = 44100
CHANNELS = 2
BLOCK_SIZE = 4096  # Litt større buffer for jevnere avspilling

STREAM_TOKEN = secrets.token_urlsafe(32)
audio_errors = queue.SimpleQueue()


# ==========================================
# 2. HJELPEFUNKSJON FOR WAV-STRØM (HEADER)
# ==========================================

def get_wav_header(sample_rate, channels, bits_per_sample):
    data_size = 0x7FFFFFFF
    byte_rate = sample_rate * channels * (bits_per_sample // 8)
    block_align = channels * (bits_per_sample // 8)
    
    header = bytearray()
    header.extend(b'RIFF')
    header.extend((data_size + 36).to_bytes(4, 'little'))
    header.extend(b'WAVE')
    header.extend(b'fmt ')
    header.extend((16).to_bytes(4, 'little'))
    header.extend((1).to_bytes(2, 'little'))
    header.extend(channels.to_bytes(2, 'little'))
    header.extend(sample_rate.to_bytes(4, 'little'))
    header.extend(byte_rate.to_bytes(4, 'little'))
    header.extend(block_align.to_bytes(2, 'little'))
    header.extend(bits_per_sample.to_bytes(2, 'little'))
    header.extend(b'data')
    header.extend(data_size.to_bytes(4, 'little'))
    return bytes(header)


# ==========================================
# 3. LYDOPPTAK OG GENERATOR-FUNKSJON (REN OG STABIL)
# ==========================================

def generate_audio_stream():
    try:
        mic = sc.get_microphone(sc.default_speaker().name, include_loopback=True)
    except Exception as e:
        audio_errors.put(f"Kunne ikke finne loopback-enhet: {e}")
        return

    yield get_wav_header(SAMPLE_RATE, CHANNELS, 16)

    try:
        with mic.recorder(samplerate=SAMPLE_RATE, channels=CHANNELS) as recorder:
            while True:
                data = recorder.record(numframes=BLOCK_SIZE)
                audio_data = (data * 32767).astype(np.int16)
                yield audio_data.tobytes()
    except Exception as e:
        audio_errors.put(f"Feil under opptak: {e}")


# ==========================================
# 4. FLASK WEB-RUTE OG SERVER
# ==========================================

@app.route('/stream.wav')
def live_stream():
    token = request.args.get("token", "")
    if not hmac.compare_digest(token, STREAM_TOKEN):
        return Response(status=401)
    return Response(generate_audio_stream(), mimetype="audio/x-wav")

def start_server(server):
    server.serve_forever()


# ==========================================
# 5. GRAFISK GRENSESNITT (GUI - TKINTER)
# ==========================================

class SonosApp:
    def __init__(self, root, local_ip, server):
        self.root = root
        self.local_ip = local_ip
        self.server = server
        self.server_ready = server is not None
        self.speakers_dict = {}
        self.root.title("Desktop Sound Bridge")
        self.root.geometry("420x390")
        self.root.resizable(False, False)

        try:
            if os.path.exists(ICON_PATH):
                self.root.iconbitmap(ICON_PATH)
        except Exception:
            pass

        # --- Menylinje øverst ---
        menubar = tk.Menu(root)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Avslutt", command=self.close_app)
        menubar.add_cascade(label="Fil", menu=file_menu)
        
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="Om programmet", command=self.show_about)
        menubar.add_cascade(label="Hjelp", menu=help_menu)
        
        root.config(menu=menubar)

        # --- Overskrift ---
        title_label = ttk.Label(root, text="Desktop Sound Bridge", font=("Arial", 14, "bold"))
        title_label.pack(pady=15)

        # --- Høyttaler-seksjon ---
        frame_speakers = ttk.LabelFrame(root, text=" Velg høyttaler ", padding=10)
        frame_speakers.pack(fill="x", padx=20, pady=5)

        self.combo_speakers = ttk.Combobox(frame_speakers, state="readonly", width=28)
        self.combo_speakers.pack(side="left", padx=5)

        btn_scan = ttk.Button(frame_speakers, text="Søk", command=self.scan_speakers)
        btn_scan.pack(side="right", padx=5)

        # --- Volum-seksjon ---
        frame_vol = ttk.LabelFrame(root, text=" Volum ", padding=10)
        frame_vol.pack(fill="x", padx=20, pady=10)

        self.vol_slider = ttk.Scale(frame_vol, from_=0, to=100, orient="horizontal", command=self.change_volume)
        self.vol_slider.set(20)
        self.vol_slider.pack(fill="x", padx=5)

        # --- Kontrollknapper ---
        frame_btn = ttk.Frame(root, padding=10)
        frame_btn.pack(fill="x", padx=20, pady=10)

        self.btn_start = ttk.Button(frame_btn, text="Start Strømming", command=self.start_streaming)
        self.btn_start.pack(side="left", expand=True, fill="x", padx=5)

        self.btn_stop = ttk.Button(frame_btn, text="Stopp", command=self.stop_streaming, state="disabled")
        self.btn_stop.pack(side="right", expand=True, fill="x", padx=5)

        # --- Statusfelt ---
        status = f"IP: {local_ip} | Klar" if self.server_ready else "Strømming utilgjengelig"
        self.status_label = ttk.Label(root, text=status, font=("Arial", 9, "italic"))
        self.status_label.pack(pady=10)

        self.btn_scan = btn_scan
        if not self.server_ready:
            self.btn_start.config(state="disabled")

        self.audio_error_poll_id = self.root.after(250, self._poll_audio_errors)
        self.scan_speakers()

    def _poll_audio_errors(self):
        try:
            error = audio_errors.get_nowait()
        except queue.Empty:
            error = None

        if error is not None:
            self.status_label.config(text="Lydstrømmen stoppet på grunn av en feil.")
            self.btn_start.config(state="normal" if self.server_ready else "disabled")
            self.btn_stop.config(state="disabled")
            self.combo_speakers.config(state="readonly")
            messagebox.showerror("Lydopptak feilet", error)

        self.audio_error_poll_id = self.root.after(250, self._poll_audio_errors)

    def close_app(self):
        self.root.after_cancel(self.audio_error_poll_id)
        if self.server is not None:
            self.server.shutdown()
            self.server.server_close()
        self.root.destroy()

    def show_about(self):
        messagebox.showinfo(
            "Om programmet",
            "Desktop Sound Bridge v0.1.0-beta.1\n\n"
            "Lar deg streame live systemlyd fra din Windows-PC "
            "direkte til Sonos-høyttalere på det lokale nettverket."
        )

    def scan_speakers(self):
        self.status_label.config(text="Søker etter Sonos-enheter...")
        self.btn_scan.config(state="disabled")

        def discover_speakers():
            try:
                found = list(soco.discover())
            except Exception as e:
                self.root.after(0, self._finish_scan, None, e)
                return
            self.root.after(0, self._finish_scan, found, None)

        threading.Thread(target=discover_speakers, daemon=True).start()

    def _finish_scan(self, found, error):
        self.btn_scan.config(state="normal")
        if error is not None:
            self.status_label.config(text="Feil under søk.")
            messagebox.showerror("Feil", f"Kunne ikke søke etter enheter:\n{error}")
            return

        self.speakers_dict = {sp.player_name: sp for sp in found}
        names = list(self.speakers_dict.keys())
        self.combo_speakers["values"] = names
        if names:
            self.combo_speakers.current(0)
            self.status_label.config(text=f"Fant {len(names)} enhet(er).")
        else:
            self.combo_speakers.set("")
            self.status_label.config(text="Fant ingen Sonos-enheter.")

    def start_streaming(self):
        selected_name = self.combo_speakers.get()
        if not selected_name:
            messagebox.showwarning("Advarsel", "Vennligst velg en høyttaler først!")
            return

        target_speaker = self.speakers_dict.get(selected_name)
        if target_speaker is None:
            messagebox.showerror("Feil", "Den valgte høyttaleren er ikke lenger tilgjengelig. Søk på nytt.")
            return
        if not self.server_ready:
            messagebox.showerror("Feil", "Strømmeserveren er ikke tilgjengelig.")
            return

        try:
            target_speaker.volume = int(self.vol_slider.get())
            stream_url = f"http://{self.local_ip}:{PORT}/stream.wav?token={STREAM_TOKEN}"
            target_speaker.play_uri(stream_url)

            self.status_label.config(text=f"Spiller av på: {selected_name}")
            self.btn_start.config(state="disabled")
            self.btn_stop.config(state="normal")
            self.combo_speakers.config(state="disabled")
        except Exception as e:
            messagebox.showerror("Feil", f"Kunne ikke starte avspilling:\n{e}")

    def stop_streaming(self, *args):
        selected_name = self.combo_speakers.get()
        target_speaker = self.speakers_dict.get(selected_name)
        if target_speaker is None:
            messagebox.showerror("Feil", "Fant ikke den valgte høyttaleren. Søk på nytt.")
            return
        try:
            target_speaker.stop()
        except Exception as e:
            messagebox.showerror("Feil", f"Kunne ikke stoppe avspillingen:\n{e}")
            return

        self.status_label.config(text="Avspilling stoppet.")
        self.btn_start.config(state="normal")
        self.btn_stop.config(state="disabled")
        self.combo_speakers.config(state="readonly")

    def change_volume(self, val):
        selected_name = self.combo_speakers.get()
        target_speaker = self.speakers_dict.get(selected_name)
        if target_speaker:
            try:
                target_speaker.volume = int(float(val))
            except Exception as e:
                self.status_label.config(text=f"Kunne ikke endre volum: {e}")


# ==========================================
# 6. HOVEDPROGRAM
# ==========================================

if __name__ == '__main__':
    root = tk.Tk()
    local_ip = None
    server = None
    startup_error = None
    try:
        local_ip = get_local_ip()
    except OSError as e:
        startup_error = e

    if local_ip is not None:
        try:
            server = make_server(local_ip, PORT, app, threaded=True)
        except OSError as e:
            startup_error = e

    sonos_app = SonosApp(root, local_ip, server)
    if startup_error is not None:
        message = (
            f"Kunne ikke finne en lokal nettverksadresse:\n{startup_error}"
            if local_ip is None
            else f"Kunne ikke starte strømmeserveren på port {PORT}:\n{startup_error}"
        )
        messagebox.showerror(
            "Strømmeserver utilgjengelig",
            message,
        )

    if server is not None:
        server_thread = threading.Thread(target=start_server, args=(server,), daemon=True)
        server_thread.start()

    root.protocol("WM_DELETE_WINDOW", sonos_app.close_app)
    root.mainloop()