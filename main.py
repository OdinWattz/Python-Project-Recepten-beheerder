import json
import os
import csv

# Laad bestaande recepten als het bestand bestaat
def laad_recepten():
    if os.path.exists("recepten.json"):
        with open("recepten.json", "r") as f:
            return json.load(f)
    return []

# Sla de recepten op in een JSON-bestand
def sla_recepten_op(recepten):
    with open("recepten.json", "w") as f:
        json.dump(recepten, f, indent=4)

# Laad de favoriete recepten
def laad_favoriete_recepten():
    if os.path.exists("favoriete_recepten.json"):
        with open("favoriete_recepten.json", "r") as f:
            return json.load(f)
    return []

# Sla de favoriete recepten op in een JSON-bestand
def sla_favoriete_recepten_op(favoriete_recepten):
    with open("favoriete_recepten.json", "w") as f:
        json.dump(favoriete_recepten, f, indent=4)

# Voeg een nieuw recept toe
def voeg_recept_toe(recepten):
    naam = input("Voer de naam van het recept in: ")
    
    # Ingrediënten per stap invoeren
    print("Voer de ingrediënten stap voor stap in. Typ 'stop' om te stoppen.")
    ingrediënten = []
    while True:
        ingredient = input(f"Ingrediënt {len(ingrediënten) + 1}: ")
        if ingredient.lower() == "stop":
            break
        ingrediënten.append(ingredient)
    
    # Instructies per stap invoeren
    print("Voer de kookinstructies stap voor stap in. Typ 'stop' om te stoppen.")
    instructies = []
    while True:
        stap = input(f"Stap {len(instructies) + 1}: ")
        if stap.lower() == "stop":
            break
        instructies.append(stap)
    
    categorie = input("Voer de categorie van het recept in: ")

    nieuw_recept = {
        "naam": naam,
        "ingrediënten": ingrediënten,
        "instructies": instructies,
        "categorie": categorie
    }

    recepten.append(nieuw_recept)
    sla_recepten_op(recepten)
    print(f"Recept '{naam}' toegevoegd!")


# Verwijder een recept
def verwijder_recept(recepten):
    if not recepten:
        print("Geen recepten beschikbaar om te verwijderen.")
        return

    print("\nBeschikbare recepten om te verwijderen:")
    for i, recept in enumerate(recepten, start=1):
        print(f"{i}. {recept['naam']} - Categorie: {recept.get('categorie', 'Geen categorie')}")
        print(f"   Ingrediënten: {', '.join(recept['ingrediënten'])}")
        
        print("   Instructies:")
        # Toon de eerste paar stappen van de instructies
        for j, stap in enumerate(recept['instructies'][:3], start=1):
            print(f"   Stap {j}: {stap}")
        if len(recept['instructies']) > 3:
            print("   ...")  # Laat zien dat er nog meer stappen zijn

        print(f"   Categorie: {recept.get('categorie', 'Geen categorie')}\n")
    
    keuze = input("Voer het nummer van het recept dat je wilt verwijderen: ")

    if keuze.isdigit() and 1 <= int(keuze) <= len(recepten):
        verwijder_keuze = int(keuze) - 1
        verwijderd_recept = recepten.pop(verwijder_keuze)
        sla_recepten_op(recepten)
        print(f"Recept '{verwijderd_recept['naam']}' is verwijderd!")
    else:
        print("Ongeldige invoer. Probeer opnieuw.")


# Toon alle opgeslagen recepten
def toon_recepten(recepten):
    if recepten:
        print("\nBeschikbare recepten:")
        for i, recept in enumerate(recepten, start=1):
            categorie = recept.get('categorie', 'Geen categorie opgegeven')
            print(f"{i}. {recept['naam']} (Categorie: {categorie})")

        keuze = input("Voer het nummer van het recept in voor meer informatie: ")

        if keuze.isdigit() and 1 <= int(keuze) <= len(recepten):
            toon_recept_details(recepten[int(keuze) - 1])
        elif keuze == "":
            return
        else:
            print("Ongeldige invoer. Probeer opnieuw.")
    else:
        print("\nGeen recepten gevonden.")

# Toon de details van een recept
def toon_recept_details(recept):
    print("\nRecept details:")
    print(f"Naam: {recept['naam']}")
    
    # Ingrediënten per regel tonen
    print("Ingrediënten:")
    for i, ingredient in enumerate(recept['ingrediënten'], start=1):
        print(f"Ingrediënt {i}: {ingredient}")
    print("")
    
    # Instructies per stap tonen
    print("Instructies:")
    for i, stap in enumerate(recept['instructies'], start=1):
        print(f"Stap {i}: {stap}")
    print("")

    print(f"Categorie: {recept.get('categorie', 'Geen categorie opgegeven')}")

# Zoek een recept op basis van naam, categorie of ingrediënt
def zoek_recept(recepten):
    if recepten:
        print("\nAlle recepten:")
        for i, recept in enumerate(recepten, start=1):
            categorie = recept.get('categorie', 'Geen categorie opgegeven')
            print(f"{i}. {recept['naam']} (Categorie: {categorie})")
    else:
        print("Geen recepten gevonden.")
        return

    zoekoptie = input("\nWil je zoeken op (1) Naam, (2) Categorie, of (3) Ingrediënt? Voer een nummer in: ")

    if zoekoptie == "1":
        zoekterm = input("Voer een naamzoekterm in: ").lower()
        gevonden_recepten = [recept for recept in recepten if zoekterm in recept['naam'].lower()]
    elif zoekoptie == "2":
        zoekterm = input("Voer een categorie in: ").lower()
        gevonden_recepten = [recept for recept in recepten if zoekterm in recept.get('categorie', '').lower()]
    elif zoekoptie == "3":
        zoekterm = input("Voer een ingrediënt in: ").lower()
        gevonden_recepten = [recept for recept in recepten if any(zoekterm in ingredient.lower() for ingredient in recept.get('ingrediënten', []))]
    else:
        print("Ongeldige keuze. Probeer opnieuw.")
        return

    if gevonden_recepten:
        print(f"\nGevonden recepten met '{zoekterm}':")
        for i, recept in enumerate(gevonden_recepten, start=1):
            categorie = recept.get('categorie', 'Geen categorie opgegeven')
            print(f"{i}. {recept['naam']} (Categorie: {categorie})")

        keuze = input("\nKies een nummer om het recept te bekijken (of 0 om terug te gaan): ")
        
        if keuze.isdigit() and 1 <= int(keuze) <= len(gevonden_recepten):
            geselecteerd_recept = gevonden_recepten[int(keuze) - 1]
            toon_recept_details(geselecteerd_recept)
        elif keuze == "0":
            return
        else:
            print("Geen geldige keuze. Terug naar het menu.")
    else:
        print(f"Geen recepten gevonden met '{zoekterm}'.")

# Voeg categorieën toe aan bestaande recepten
def voeg_categorie_toe_aan_bestaan(recepten):
    for recept in recepten:
        if 'categorie' not in recept:
            recept['categorie'] = 'Geen categorie opgegeven'
    sla_recepten_op(recepten)
    print("Categorieën toegevoegd aan bestaande recepten.")

# Wijzig een bestaand recept
def wijzig_recept(recepten):
    if not recepten:
        print("Geen recepten beschikbaar om te wijzigen.")
        return

    print("\nBeschikbare recepten om te wijzigen:")
    for i, recept in enumerate(recepten, start=1):
        print(f"{i}. {recept['naam']} - Categorie: {recept.get('categorie', 'Geen categorie')}")
        
        # Ingrediënten per regel laten zien
        print("   Ingrediënten:")
        for j, ingredient in enumerate(recept['ingrediënten'], start=1):
            print(f"   Ingrediënt {j}: {ingredient}")
        
        # Instructies per regel laten zien
        print("   Instructies:")
        for j, stap in enumerate(recept['instructies'], start=1):
            print(f"   Stap {j}: {stap}")
        
        print(f"   Categorie: {recept.get('categorie', 'Geen categorie')}\n")

    keuze = input("Voer de naam van het recept in dat je wilt wijzigen: ")

    recept = next((r for r in recepten if r['naam'].lower() == keuze.lower()), None)

    if recept:
        print(f"\nJe hebt gekozen om '{recept['naam']}' te wijzigen.")

        while True:
            print("\nWat wil je wijzigen?")
            print("1. Naam")
            print("2. Ingrediënten")
            print("3. Instructies")
            print("4. Categorie")
            print("5. Stoppen met wijzigen")
            keuze_wijzig = input("> ")

            if keuze_wijzig == "1":
                nieuwe_naam = input(f"Voer een nieuwe naam in ({recept['naam']}): ")
                recept['naam'] = nieuwe_naam if nieuwe_naam else recept['naam']
                print(f"Naam gewijzigd naar '{recept['naam']}'.")

            elif keuze_wijzig == "2":
                print("\nHuidige ingrediënten in stappen:")
                for j, ingredient in enumerate(recept['ingrediënten'], start=1):
                    print(f"Ingrediënt {j}: {ingredient}")
                
                print("Voer nieuwe ingrediënten in, één per regel. Typ 'stop' om te stoppen.")
                nieuwe_ingrediënten = []
                while True:
                    nieuwe_ingredient = input(f"Ingrediënt {len(nieuwe_ingrediënten) + 1}: ")
                    if nieuwe_ingredient.lower() == "stop":
                        break
                    nieuwe_ingrediënten.append(nieuwe_ingredient)

                if nieuwe_ingrediënten:
                    recept['ingrediënten'] = nieuwe_ingrediënten
                print(f"Ingrediënten gewijzigd naar: {', '.join(recept['ingrediënten'])}.")

            elif keuze_wijzig == "3":
                print("\nHuidige instructies in stappen:")
                for j, stap in enumerate(recept['instructies'], start=1):
                    print(f"Stap {j}: {stap}")

                print("Voer nieuwe kookinstructies in, één per regel. Typ 'stop' om te stoppen.")
                nieuwe_instructies = []
                while True:
                    nieuwe_stap = input(f"Stap {len(nieuwe_instructies) + 1}: ")
                    if nieuwe_stap.lower() == "stop":
                        break
                    nieuwe_instructies.append(nieuwe_stap)

                if nieuwe_instructies:
                    recept['instructies'] = nieuwe_instructies
                print("Instructies gewijzigd in stappen.")

            elif keuze_wijzig == "4":
                nieuwe_categorie = input(f"Voer een nieuwe categorie in ({recept.get('categorie', 'Geen categorie')}): ")
                recept['categorie'] = nieuwe_categorie if nieuwe_categorie else recept.get('categorie', 'Geen categorie')
                print(f"Categorie gewijzigd naar '{recept['categorie']}'.")

            elif keuze_wijzig == "5":
                print("Wijzigingen opgeslagen.")
                sla_recepten_op(recepten)
                break

            else:
                print("Ongeldige keuze. Probeer opnieuw.")
    else:
        print("Geen recept gevonden met die naam. Probeer opnieuw.")



# Verwijder alle recepten
def verwijder_alle_recepten(recepten):
    bevestiging = input("Weet je zeker dat je alle recepten wilt verwijderen? (ja/nee) ")
    if bevestiging == "ja":
        recepten.clear()
        sla_recepten_op(recepten)
        print("Alle recepten zijn verwijderd.")
    else:
        print("Verwijdering geannuleerd.")

# Markeer een recept als favoriet of verwijder een favoriet
def markeer_als_favoriet(recepten, favoriete_recepten):
    print("\nBeschikbare recepten om te markeren of te verwijderen:")
    for i, recept in enumerate(recepten, start=1):
        print(f"{i}. {recept['naam']} - Categorie: {recept.get('categorie', 'Geen categorie')}")

    recept_naam = input("Voer de naam van je gekozen favoriete recept in: ")

    # Zoek het recept op basis van de ingevoerde naam
    recept = next((r for r in recepten if r['naam'].lower() == recept_naam.lower()), None)

    if recept:
        if recept not in favoriete_recepten:
            # Voeg toe aan favorieten
            favoriete_recepten.append(recept)
            sla_favoriete_recepten_op(favoriete_recepten)  # Sla de favorieten op
            print(f"Recept '{recept['naam']}' is toegevoegd aan je favorieten!")
        else:
            # Vraag of het verwijderd moet worden
            keuze = input(f"'{recept['naam']}' staat al in je favorieten. Wil je het verwijderen? (ja/nee): ").lower()
            if keuze == "ja":
                favoriete_recepten.remove(recept)
                sla_favoriete_recepten_op(favoriete_recepten)  # Sla de favorieten op
                print(f"Recept '{recept['naam']}' is verwijderd uit je favorieten.")
            else:
                print(f"'{recept['naam']}' blijft in je favorieten.")
    else:
        print(f"Recept met naam '{recept_naam}' niet gevonden.")

# Toon de favoriete recepten en bekijk details of verwijder een favoriet
def toon_favoriete_recepten(favoriete_recepten):
    if favoriete_recepten:
        print("\nFavoriete recepten:")
        for i, recept in enumerate(favoriete_recepten, start=1):
            print(f"{i}. {recept['naam']}")

        keuze = input("Voer het nummer van een favoriet recept in voor meer details of om te verwijderen ('q' om terug te gaan): ")

        if keuze.isdigit() and 1 <= int(keuze) <= len(favoriete_recepten):
            geselecteerd_recept = favoriete_recepten[int(keuze) - 1]
            print(f"\nGeselecteerd favoriet: {geselecteerd_recept['naam']}")
            
            # Toon de details van het recept
            toon_recept_details(geselecteerd_recept)

            # Vraag of je het recept wilt verwijderen uit favorieten
            verwijder_keuze = input("Wil je dit recept uit je favorieten verwijderen? (ja/nee): ").lower()
            if verwijder_keuze == 'ja':
                favoriete_recepten.remove(geselecteerd_recept)
                sla_favoriete_recepten_op(favoriete_recepten)  # Sla de favorieten op
                print(f"Recept '{geselecteerd_recept['naam']}' is verwijderd uit je favorieten.")
            else:
                print(f"'{geselecteerd_recept['naam']}' blijft in je favorieten.")
        elif keuze.lower() == 'q':
            return
        else:
            print("Ongeldige invoer. Probeer opnieuw.")
    else:
        print("\nJe hebt nog geen favoriete recepten.")

# Functie om receptdetails te tonen
def toon_recept_details(recept):
    print("\nRecept details:")
    print(f"Naam: {recept['naam']}")
    print("Ingrediënten:")
    for ingredient in recept['ingrediënten']:
        print(f"- {ingredient}")
    print("Instructies:")
    for i, stap in enumerate(recept['instructies'], start=1):
        print(f"Stap {i}: {stap}")
    print(f"Categorie: {recept.get('categorie', 'Geen categorie opgegeven')}")


# Voeg ingrediënten toe aan een boodschappenlijst
def voeg_ingredienten_aan_boodschappenlijst(recepten):
    boodschappenlijst = []

    print("\nBeschikbare recepten:")
    for i, recept in enumerate(recepten, start=1):
        print(f"{i}. {recept['naam']} - Ingrediënten: {', '.join(recept['ingrediënten'])}")

    keuze = input("Voer het nummer van het recept in om ingrediënten toe te voegen aan je boodschappenlijst: ")

    if keuze.isdigit() and 1 <= int(keuze) <= len(recepten):
        gekozen_recept = recepten[int(keuze) - 1]
        boodschappenlijst.extend(gekozen_recept['ingrediënten'])
        print(f"Ingrediënten van '{gekozen_recept['naam']}' toegevoegd aan de boodschappenlijst.")
    else:
        print("Ongeldige invoer.")

    # Toon de huidige boodschappenlijst
    print("\nBoodschappenlijst:")
    for ingredient in boodschappenlijst:
        print(f"- {ingredient}")

    return boodschappenlijst

# Exporteer de boodschappenlijst naar een CSV-bestand
def exporteer_boodschappenlijst_naar_csv(boodschappenlijst, bestandsnaam="boodschappenlijst.csv"):
    with open(bestandsnaam, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Ingrediënten"])  # Koptekst
        for item in boodschappenlijst:
            writer.writerow([item])

    print(f"Boodschappenlijst succesvol geëxporteerd naar {bestandsnaam}.")

# Hoofdmenu
def toon_menu():
    print("\nMaak een keuze:")
    print("1. Voeg een recept toe")
    print("2. Verwijder een recept")
    print("3. Toon alle recepten")
    print("4. Zoek een recept")
    print("5. Wijzig een recept")
    print("6. Markeer Favoriet")
    print("7. Toon Favorieten")
    print("8. Verwijder alle recepten")
    print("9. Exporteer boodschappenlijst naar CSV")
    print("10. Stoppen")
    keuze = input("> ")
    return keuze

# Start het programma
def start_programma():
    recepten = laad_recepten()
    favoriete_recepten = laad_favoriete_recepten()  # Laad favoriete recepten
    voeg_categorie_toe_aan_bestaan(recepten)  # Voeg categorieën toe aan bestaande recepten

    while True:
        keuze = toon_menu()
        if keuze == "1":
            voeg_recept_toe(recepten)
        elif keuze == "2":
            verwijder_recept(recepten)
        elif keuze == "3":
            toon_recepten(recepten)
        elif keuze == "4":
            zoek_recept(recepten)
        elif keuze == "5":
            wijzig_recept(recepten)
        elif keuze == "6":
            markeer_als_favoriet(recepten, favoriete_recepten)
        elif keuze == "7":
            toon_favoriete_recepten(favoriete_recepten)
        elif keuze == "8":
            verwijder_alle_recepten(recepten)
        elif keuze == "9":
            boodschappenlijst = voeg_ingredienten_aan_boodschappenlijst(recepten)
            exporteer_boodschappenlijst_naar_csv(boodschappenlijst)
        elif keuze == "10":
            print("Programma gestopt.")
            break
        else:
            print("Ongeldige keuze. Probeer opnieuw.")

# Start het programma
if __name__ == "__main__":
    start_programma()
