import soco

print("Søker etter Sonos-høyttalere på nettverket...")

# Finn alle Sonos-enheter på nettverket automatisk
speakers = list(soco.discover())

if speakers:
    print(f"Fant {len(speakers)} høyttaler(e)!")
    
    # Velg den første høyttaleren som ble funnet
    hoved_hoyttaler = speakers[0]
    print(f"Koblet til: {hoved_hoyttaler.player_name}")
    
    # Eksempel 1: Sjekk hva som spilles nå
    try:
        track_info = hoved_hoyttaler.get_current_track_info()
        print(f"Naa spiller: {track_info.get('title')} av {track_info.get('artist')}")
    except Exception:
        print("Ingen aktiv avspilling akkurat nå.")
        
    # Eksempel 2: Sett volumet (f.eks. til 15%)
    hoved_hoyttaler.volume = 15
    print(f"Volum satt til: {hoved_hoyttaler.volume}%")
    
else:
    print("Fant ingen Sonos-høyttalere. Sjekk at PC-en er på samme Wi-Fi som høyttaleren.")