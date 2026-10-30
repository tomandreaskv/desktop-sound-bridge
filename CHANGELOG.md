# Changelog

Alle større endringer og oppdateringer for dette prosjektet vil bli dokumentert her.

## [1.0.0] - 2026-10-30

### 🚀 Ny funksjonalitet
* **Sanntidsopptak:** Implementert systemlyd-fangst (loopback) via `soundcard`-biblioteket.
* **Sonos-integrasjon:** Støtte for automatisk søk og avspilling på Sonos-enheter ved hjelp av `SoCo` (UPnP).
* **Grafisk Brukergrensesnitt (GUI):** Laget et rent og oversiktlig kontrollpanel med Tkinter for enklere betjening.
* **Live Volumkontroll:** Mulighet til å justere høyttalervolumet i sanntid via appens skyvebryter.
* **Dynamisk IP-deteksjon:** Programmet henter maskinens lokale IP-adresse automatisk slik at det fungerer på tvers av nettverk.

### 🔧 Forbedringer og Fiks
* **Stabil strømming:** Benytter en kontinuerlig live-WAV-strøm med egendefinert header for sømløs avspilling.
* **Feilhåndtering:** Dempet unødvendige `SoundcardRuntimeWarning`-advarsler i terminalen når lydstrømmen pauses midlertidig.