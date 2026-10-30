# Changelog

Alle større endringer og oppdateringer for dette prosjektet vil bli dokumentert her.

## [Unreleased]

### Forbedringer
* Feil ved oppdagelse av loopback-enhet eller lydopptak vises nå i GUI-et, og kontrollene tilbakestilles slik at brukeren kan prøve igjen.
* GitHub Actions kjører automatiske tester på Windows ved push og pull request.
* Avhengigheter og byggverktøy administreres med Poetry og låses i `poetry.lock`.

## [0.1.0-beta.1] - 2026-10-30

Første testrelease. Funksjonene er ikke validert på alle Windows- og Sonos-oppsett.

### Forbedringer
* Strømmeserveren lytter bare på den valgte lokale nettverksadressen og krever en tilfeldig sesjonstoken.
* Feil ved oppstart og Sonos-kontroll vises i grensesnittet. Feil fra selve lydopptaket ble i denne versjonen bare skrevet til konsollen.
* Sonos-søk skjer i bakgrunnen slik at vinduet forblir responsivt.
* La til automatiske tester for WAV-header og tilgangskontroll på lydstrømmen.