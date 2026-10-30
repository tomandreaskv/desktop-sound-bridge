# Desktop Sound Bridge 🎵🖥️

En enkel og brukervennlig desktop-applikasjon skrevet i Python som fanger opp live systemlyd fra en Windows-PC og streamer den i sanntid til Sonos-høyttalere på det lokale nettverket med lav latens.

## Funksjoner
* **Sanntidsopptak:** Fanger opp all systemlyd (f.eks. musikk fra Spotify, YouTube, nettleser) via Windows loopback.
* **Grafisk Brukergrensesnitt (GUI):** Bygget med Tkinter for enkel betjening.
* **Automatisk Enhetssøk:** Oppdager automatisk alle tilgjengelige Sonos-enheter på nettverket ditt via UPnP (`SoCo`).
* **Live Volumkontroll:** Juster volumet direkte fra appens skyvebryter.
* **Dynamisk IP-deteksjon:** Finner maskinens lokale IP-adresse automatisk slik at den fungerer på tvers av nettverk.

---

## 🛠️ Forutsetninger og Biblioteker
For å kjøre dette skriptet fra kildekoden trenger du Python installert sammen med følgende avhengigheter:

```powershell
pip install flask soundcard numpy soco
```

# 🚀 Slik kjører du programmet

1. Last ned eller klon dette repositoryet.
2. Åpne en terminal i prosjektmappen.
3. Start programmet med Python:

```powershell
python sonos_gui.py
```

4. Velg ønsket Sonos-høyttaler i nedtrekksmenyen og trykk Start Strømming.

# 📂 Prosjektstruktur

* sonos_gui.py – Hovedprogrammet som inneholder både Flask-serveren, lydopptaket og det grafiske grensesnittet.
