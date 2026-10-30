# Veikart for Desktop Sound Bridge 🚀

Dette dokumentet inneholder forslag til fremtidige funksjoner, tekniske forbedringer og utvidelser av **Desktop Sound Bridge**. 

---

## 🎯 Prioriterte forbedringer (Short-term)

### 1. Robust lydutgang og enhetsvalg
* **Spesifikk lydkilde-velger:** Gi brukeren mulighet til å velge hvilken Windows-lydenhet (f.eks. spesifikke virtuelle lydkort, mikrofoner eller applikasjoner) som skal strømmes, i stedet for kun standard loopback.
* **Justerbar bufferstørrelse:** Legge til en innstilling i brukergrensesnittet for å endre `BLOCK_SIZE` / samplingsfrekvens manuelt dersom brukeren har et tregere Wi-Fi-nettverk.

### 2. Nettverk og Sonos-oppdagelse
* **Manuell IP-inntasting for Sonos:** Mulighet til å legge inn IP-adressen til en Sonos-høyttaler manuelt hvis UPnP/discovery blokkeres av lokale brannmurer.
* **Støtte for Sonos-grupper:** Mulighet til å strømme lyd til sammenslåtte høyttalergrupper eller "Stereo Pairs" direkte fra grensesnittet.

---

## 💡 Nye funksjoner (Medium-term)

### 1. System Tray (Minimer til oppgavelinjen)
* **Kjøre i bakgrunnen:** La applikasjonen minimere til oppgavelinjen ved siden av klokken (System Tray) slik at den ikke tar plass på skrivebordet mens du strømmer.
* **Hurtigmeny:** Høyreklikk på tray-ikonet for å raskt starte/stoppe strømming eller endre volum uten å åpne hovedvinduet.

### 2. Auto-start og Profiler
* **Start med Windows:** Valgfri innstilling for å starte appen automatisk når datamaskinen slås på.
* **Husk sist brukte enhet:** Lagre den sist valgte Sonos-høyttaleren og volumnivået i en lokal konfigurasjonsfil (`config.json`), slik at alt er klart ved oppstart.

---

## 🔬 Avanserte utvidelser (Long-term)

### 1. Egendefinert Equalizer (EQ) og Lydbehandling
* **Enkel 3-bånds EQ:** Legge til lavpass-/høypass-filter eller enkel Bass/Treble-justering direkte i appen før lyden sendes ut.
* **Kompressor / Normalisering:** Automatisk utjevning av lydvolum slik at plutselige høye lyder (f.eks. varslinger) dempes.

### 2. Flere strømme-protokoller
* **AirPlay 2 / DLNA-støtte:** Utvide fra rene Sonos/UPnP-kall til å støtte generelle DLNA-mottakere og AirPlay, slik at appen kan brukes mot andre typer smarthøyttalere og TV-er.

---

## 🛠️ Bidrag

Har du ideer til andre funksjoner? Åpne gjerne et *Issue* eller send inn en *Pull Request* på GitHub!