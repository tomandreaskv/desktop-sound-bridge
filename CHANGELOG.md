# Changelog

Alle større endringer og oppdateringer for dette prosjektet vil bli dokumentert her.

## [0.1.0-beta.1] - 2026-10-30

Første testrelease. Funksjonene er ikke validert på alle Windows- og Sonos-oppsett.

### Forbedringer
* Strømmeserveren lytter bare på den valgte lokale nettverksadressen og krever en tilfeldig sesjonstoken.
* Feil ved oppstart og Sonos-kontroll vises tydeligere i grensesnittet.
* Sonos-søk skjer i bakgrunnen slik at vinduet forblir responsivt.
* La til automatiske tester for WAV-header og tilgangskontroll på lydstrømmen.