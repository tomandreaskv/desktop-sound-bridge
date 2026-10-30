# Desktop Sound Bridge 🎵🖥️

En enkel og brukervennlig desktop-applikasjon skrevet i Python som fanger opp live systemlyd fra en Windows-PC og streamer den i sanntid til Sonos-høyttalere på det lokale nettverket med lav latens.

## Funksjoner
* **Sanntidsopptak:** Fanger opp all systemlyd (f.eks. musikk fra Spotify, YouTube, nettleser) via Windows loopback.
* **Grafisk Brukergrensesnitt (GUI):** Bygget med Tkinter for enkel betjening.
* **Automatisk Enhetssøk:** Oppdager automatisk alle tilgjengelige Sonos-enheter på nettverket ditt via UPnP (`SoCo`).
* **Live Volumkontroll:** Juster volumet direkte fra appens skyvebryter.
* **Dynamisk IP-deteksjon:** Finner maskinens lokale IP-adresse automatisk slik at den fungerer på tvers av nettverk.

## Testrelease

Dette er en første testrelease (`0.1.0-beta.1`), ikke en stabil 1.0.0. Den er foreløpig bare kontrollert med automatiske tester; avspilling bør testes på din Windows-PC og Sonos-modell før daglig bruk.

Strømmeserveren lytter på PC-ens valgte lokale nettverksadresse og krever en tilfeldig nøkkel som genereres ved oppstart. Sonos og PC-en må være på et nettverk der de kan nå hverandre. Brannmurregler kan måtte tillate innkommende trafikk på port 5000.

---

## Forutsetninger og installasjon

Installer Python 3.13 og [Poetry](https://python-poetry.org/). Kjør så følgende fra prosjektmappen for å opprette et virtuelt miljø og installere de låste avhengighetene:

```powershell
poetry sync
```

## Slik kjører du programmet

1. Last ned eller klon dette repositoryet.
2. Åpne en terminal i prosjektmappen.
3. Start programmet med Python:

```powershell
poetry run python sonos_gui.py
```

4. Velg ønsket Sonos-høyttaler i nedtrekksmenyen og trykk Start Strømming.

## Tester

Kjør testene fra prosjektmappen:

```powershell
poetry run python -m unittest discover -s tests
```

GitHub Actions kjører de samme testene på Windows ved push til `main`, pull requests mot `main` og ved manuell kjøring.

## Bygg Windows-programmet

PyInstaller er inkludert som en utviklingsavhengighet. Bygg med den medfølgende spec-filen:

```powershell
poetry run pyinstaller DesktopSoundBridge.spec
```

Den kjørbare filen blir lagt i `dist`. Test den bygde filen på en Windows-maskin med Sonos før du distribuerer den.

## Prosjektstruktur

* sonos_gui.py – Hovedprogrammet som inneholder både Flask-serveren, lydopptaket og det grafiske grensesnittet.
