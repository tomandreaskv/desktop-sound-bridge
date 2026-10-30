# Bidra til Desktop Sound Bridge

Takk for at du har lyst til å bidra til dette prosjektet! Alle bidrag (feilrettinger, nye funksjoner, bedre dokumentasjon) settes stor pris på.

## Slik kan du bidra

1. **Fork prosjektet** (Fork) og klon det til din egen maskin.
2. Opprett en ny grener for endringene dine (`git checkout -b funksjon/min-nye-funksjon`).
3. Gjør endringene dine og test at alt fungerer lokalt.
4. Push endringene til din egen gjenbruk (fork) (`git push origin funksjon/min-nye-funksjon`).
5. Åpne en **Pull Request** mot `main`-grenen i dette hoved-repositoryet.

## Utviklingsmiljø

Installer Python 3.13 og Poetry. Prosjektets lokale Poetry-innstilling oppretter miljøet i `.venv` i prosjektmappen. Installer prosjektets låste avhengigheter derfra:

```powershell
poetry sync
```

Kjør testene med:

```powershell
poetry run python -m unittest discover -s tests
```

## Bygge .exe-fil lokalt

Hvis du vil teste å bygge den kjørbare fila selv, kan du bruke PyInstaller-spec-fila som følger med:

```powershell
poetry run pyinstaller DesktopSoundBridge.spec
```

Takk for at du hjelper til med å gjøre programmet bedre!