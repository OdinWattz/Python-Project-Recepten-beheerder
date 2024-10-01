import json
import os

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

# Voeg een nieuw recept toe
def voeg_recept_toe(recepten):
    naam = input("Voer de naam van het recept in: ")
    ingrediënten = input("Voer de ingrediënten in (gescheiden door komma's): ").split(", ")
    instructies = input("Voer de kookinstructies in: ")
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


def verwijder_recept(recepten):
    toon_recepten(recepten)
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
            categorie = recept.get('categorie', 'Geen categorie opgegeven')  # Standaardwaarde als categorie ontbreekt
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


def toon_recept_details(recept):
    print("\nRecept details:")
    print(f"Naam: {recept['naam']}")

    print("Ingrediënten:")
    for ingredient in recept['ingrediënten']:
        print(f"- {ingredient}")
    
    print(f"Instructies: {recept['instructies']}")


# Zoek een recept op basis van een zoekterm
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
            toon_recept_details(geselecteerd_recept)  # Toon details van het geselecteerde recept
        elif keuze == "0":
            return  # Terug naar het menu
        else:
            print("Geen geldige keuze. Terug naar het menu.")
    else:
        print(f"Geen recepten gevonden met '{zoekterm}'.")


def voeg_categorie_toe_aan_bestaan(recepten):
    for recept in recepten:
        if 'categorie' not in recept:
            recept['categorie'] = 'Geen categorie opgegeven'  # Of een andere standaardcategorie

    sla_recepten_op(recepten)  # Sla de bijgewerkte recepten op
    print("Categorieën toegevoegd aan bestaande recepten.")

def wijzig_recept(recepten):
    if not recepten:
        print("Geen recepten beschikbaar om te wijzigen.")
        return

    # Toon een lijst met recepten en hun details
    print("\nBeschikbare recepten om te wijzigen:")
    for i, recept in enumerate(recepten, start=1):
        print(f"{i}. {recept['naam']} - Categorie: {recept.get('categorie', 'Geen categorie')}")
        print(f"   Ingrediënten: {', '.join(recept['ingrediënten'])}")
        print(f"   Instructies: {recept['instructies'][:50]}...")  # Laat de eerste 50 tekens van de instructies zien
        print(f"   Categorie: {recept.get('categorie', 'Geen categorie')}")
        print("")  # Lege regel

    keuze = input("Voer de naam van het recept in dat je wilt wijzigen: ")

    # Zoek het recept op basis van de ingevoerde naam
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
                nieuwe_ingrediënten = input(f"Voer nieuwe ingrediënten in ({', '.join(recept['ingrediënten'])}): ")
                if nieuwe_ingrediënten:
                    recept['ingrediënten'] = nieuwe_ingrediënten.split(", ")
                print(f"Ingrediënten gewijzigd naar {', '.join(recept['ingrediënten'])}.")

            elif keuze_wijzig == "3":
                nieuwe_instructies = input(f"Voer nieuwe kookinstructies in ({recept['instructies']}): ")
                recept['instructies'] = nieuwe_instructies if nieuwe_instructies else recept['instructies']
                print(f"Instructies gewijzigd.")

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

def verwijder_alle_recepten(recepten):
    bevestiging = input("Weet je zeker dat je alle recepten wilt verwijderen? (ja/nee) ")
    if bevestiging == "ja":
        recepten.clear()
        sla_recepten_op(recepten)
        print("Alle recepten zijn verwijderd.")
    else:
        print("De recepten zijn niet verwijderd.")

favoriete_recepten = []

def markeer_als_favoriet(recepten):
    print("\nBeschikbare recepten om te markeren:")
    for i, recept in enumerate(recepten, start=1):
        print(f"{i}. {recept['naam']} - Categorie: {recept.get('categorie', 'Geen categorie')}")

    recept_naam = input("Voer de naam van je gekozen favoriete recept in: ")

    # Zoek het recept op basis van de ingevoerde naam
    recept = next((r for r in recepten if r['naam'].lower() == recept_naam.lower()), None)

    if recept:
        if recept not in favoriete_recepten:
            # Voeg toe aan favorieten
            favoriete_recepten.append(recept)
            print(f"Recept '{recept['naam']}' is toegevoegd aan je favorieten!")
        else:
            # Vraag of het verwijderd moet worden
            keuze = input(f"'{recept['naam']}' staat al in je favorieten. Wil je het verwijderen? (ja/nee): ").lower()
            if keuze == "ja":
                favoriete_recepten.remove(recept)
                print(f"Recept '{recept['naam']}' is verwijderd uit je favorieten.")
            else:
                print(f"'{recept['naam']}' blijft in je favorieten.")
    else:
        print(f"Recept met naam '{recept_naam}' niet gevonden.")


def toon_favoriete_recepten():
    if favoriete_recepten:
        print("\nFavoriete recepten:")
        for recept in favoriete_recepten:
            print(f" - {recept['naam']}")
    else:
        print("\nJe hebt nog geen favoriete recepten.")

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
    print("9. Stoppen")
    keuze = input("> ")
    return keuze

# Start het programma
def start_programma():
    recepten = laad_recepten()
    voeg_categorie_toe_aan_bestaan(recepten)  # Voeg categorieën toe

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
            markeer_als_favoriet(recepten)
        elif keuze == "7":
            toon_favoriete_recepten()
        elif keuze == "8":
            verwijder_alle_recepten(recepten)
        elif keuze == "9":
            print("Programma gestopt.")
            break
        else:
            print("Ongeldige keuze. Probeer opnieuw.")



# Start het programma
if __name__ == "__main__":
    start_programma()
