import threading
import time
import soundcard as sc
import numpy as np
import soco
from flask import Flask, Response

# ==========================================
# 1. KONFIGURASJON OG SERVEROPPSETT
# ==========================================

# Initialiserer Flask-webserveren som skal levere lydstrømmen
app = Flask(__name__)

# VIKTIG: Bytt ut denne med din PC sin faktiske IP-adresse på lokalnettet (fra ipconfig)
LOCAL_IP = "Insert din lokale IP her"  # F.eks. "
PORT = 5000

# Lydinnstillinger for strømmen (standard CD-kvalitet)
SAMPLE_RATE = 44100  # 44.1 kHz samplingsfrekvens
CHANNELS = 2         # Stereo (2 kanaler: venstre og høyre)
BLOCK_SIZE = 2048    # Antall samples som leses i hver "bit" (større buffer = mindre risiko for hakk)


# ==========================================
# 2. HJELPEFUNKSJON FOR WAV-STRØM (HEADER)
# ==========================================

def get_wav_header(sample_rate, channels, bits_per_sample):
    """
    Genererer en gyldig WAV-filheader spesielt tilpasset live-streaming.
    Standard WAV-filer krever at filstørrelsen er kjent på forhånd. 
    Her lurer vi avspilleren (Sonos) ved å sette en ekstremt stor data-størrelse, 
    slik at den forstår at dette er en uendelig live-strøm.
    """
    data_size = 0x7FFFFFFF  # Setter en massiv "virtuell" filstørrelse
    byte_rate = sample_rate * channels * (bits_per_sample // 8)
    block_align = channels * (bits_per_sample // 8)
    
    header = bytearray()
    header.extend(b'RIFF') # Identifikator for RIFF-filer
    header.extend((data_size + 36).to_bytes(4, 'little')) # Total størrelse
    header.extend(b'WAVE') # Filformat
    header.extend(b'fmt ') # Format-subchunk
    header.extend((16).to_bytes(4, 'little')) # Subchunk1Size (16 for standard PCM)
    header.extend((1).to_bytes(2, 'little'))  # AudioFormat (1 for ukomprimert PCM)
    header.extend(channels.to_bytes(2, 'little'))     # Antall kanaler (2 = Stereo)
    header.extend(sample_rate.to_bytes(4, 'little'))  # Samplingsfrekvens (44100)
    header.extend(byte_rate.to_bytes(4, 'little'))    # Bytes per sekund
    header.extend(block_align.to_bytes(2, 'little'))  # Block align
    header.extend(bits_per_sample.to_bytes(2, 'little')) # Bits per sample (16-bit)
    header.extend(b'data') # Data-subchunk start
    header.extend(data_size.to_bytes(4, 'little')) # Datastørrelse
    
    return bytes(header)


# ==========================================
# 3. LYDOPPTAK OG GENERATOR-FUNKSJON
# ==========================================

def generate_audio_stream():
    """
    En generator-funksjon i Python. I steden for å returnere alt på en gang,
    'yield'er (sender) den data bit for bit i det uendelige mens musikk spilles av.
    Dette gjør at Flask kan streame sanntidslyd uten at minnet fylles opp.
    """
    try:
        # Fanger opp standard systemlyd (loopback) fra PC-ens aktive høyttaler
        mic = sc.get_microphone(sc.default_speaker().name, include_loopback=True)
    except Exception as e:
        print(f"Kunne ikke finne loopback-enhet: {e}")
        return

    # Steg A: Send WAV-hodet først av alt slik at Sonos forstår lydformatet
    yield get_wav_header(SAMPLE_RATE, CHANNELS, 16)

    # Steg B: Start opptak og strøm rå PCM-lyd i sanntid
    try:
        with mic.recorder(samplerate=SAMPLE_RATE, channels=CHANNELS) as recorder:
            while True:
                # Ta opp en bit med systemlyd (data kommer som desimaltall mellom -1.0 og 1.0)
                data = recorder.record(numframes=BLOCK_SIZE)
                
                # Konverter flyttallene til 16-bits heltall (standard PCM som lydavspillere krever)
                audio_data = (data * 32767).astype(np.int16)
                
                # Send denne binære lydbiten ut på nettverket til Sonos
                yield audio_data.tobytes()
                
    except Exception as e:
        print(f"Feil under opptak: {e}")


# ==========================================
# 4. FLASK WEB-RUTE
# ==========================================

@app.route('/stream.wav')
def live_stream():
    """
    Når Sonos kobler seg til denne adressen, startes 'generate_audio_stream'.
    Mimetype 'audio/x-wav' forteller høyttaleren at den mottar en WAV-strøm.
    """
    return Response(generate_audio_stream(), mimetype="audio/x-wav")


def start_server():
    """Starter Flask-serveren i bakgrunnen."""
    # threaded=True er viktig slik at serveren kan håndtere tilkoblinger samtidig som den genererer lyd
    app.run(host='0.0.0.0', port=PORT, threaded=True)


# ==========================================
# 5. HOVEDPROGRAM (SONOS-KONTROLL)
# ==========================================

if __name__ == '__main__':
    # Start Flask-serveren i en egen tråd (Background Thread)
    # Dette gjør at webserveren kan kjøre samtidig som resten av koden jobber
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    print(f"Lokal live-strømmeserver startet på http://{LOCAL_IP}:{PORT}/stream.wav")

    # Søk etter alle Sonos-enheter på det lokale nettverket via UPnP
    print("Søker etter Sonos-høyttalere...")
    speakers = list(soco.discover())

    if speakers:
        mal_navn = "Kontor"  # Navnet på høyttaleren du vil bruke
        hoved_hoyttaler = None

        # Gå gjennom alle funnede enheter for å finne riktig høyttaler
        for speaker in speakers:
            print(f"Fant enhet: {speaker.player_name}")
            if speaker.player_name.lower() == mal_navn.lower():
                hoved_hoyttaler = speaker
                break
        
        # Hvis vi ikke fant "Kontor", fall tilbake til den første vi fant
        if not hoved_hoyttaler:
            print(f"Fant ikke '{mal_navn}', bruker den første som ble funnet.")
            hoved_hoyttaler = speakers[0]

        print(f"Valgte høyttaler: {hoved_hoyttaler.player_name}")

        # Lag den komplette nettverks-URL-en som Sonos skal koble seg til
        stream_url = f"http://{LOCAL_IP}:{PORT}/stream.wav"

        # Sett ønsket volum (f.eks. 20%) og send kommando om å spille av URL-en
        hoved_hoyttaler.volume = 20
        print("Sender live-lyd til Sonos...")
        
        hoved_hoyttaler.play_uri(stream_url)
        print("Live-strømming i gang! Spill av musikk på PC-en. (Trykk Ctrl+C for å avslutte)")

        # En uendelig løkke for å holde hovedprogrammet i live 
        # slik at tråden og serveren ikke dør med en gang
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nAvslutter programmet...")
    else:
        print("Fant ingen Sonos-høyttalere på nettverket.")