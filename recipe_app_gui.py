import json
import os
import csv
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

# Laad bestaande recepten als het bestand bestaat
def laad_recepten():
    if os.path.exists("recepten.json"):
        with open("recepten.json", "r") as f:
            recepten = json.load(f)
            for recept in recepten:
                if 'bereidingstijd' not in recept:
                    recept['bereidingstijd'] = "Niet beschikbaar"
            return recepten
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

# Exporteer de boodschappenlijst naar een CSV-bestand
def exporteer_boodschappenlijst_naar_csv(boodschappenlijst, bestandsnaam="boodschappenlijst.csv"):
    with open(bestandsnaam, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Ingrediënten"])  # Koptekst
        for item in boodschappenlijst:
            writer.writerow([item])
    messagebox.showinfo("Exporteren", f"Boodschappenlijst succesvol geëxporteerd naar {bestandsnaam}.")

class RecipeManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Recepten Beheer Programma")
        self.root.geometry("1450x150")

        self.style = ttk.Style()
        self.style.configure("TButton", font=("Helvetica", 14))
        self.style.configure("TLabel", font=("Helvetica", 14))  
        # Initialiseer recepten en favorieten
        self.recepten = laad_recepten()
        self.favoriete_recepten = laad_favoriete_recepten()

        # Maak de GUI-componenten
        self.create_widgets()

    def create_widgets(self):
        # Hoofdframe
        self.frame = ttk.Frame(self.root, padding="10")
        self.frame.grid()

        # Voeg recepten toe knop
        self.add_button = ttk.Button(self.frame, text="Voeg Recept Toe", command=self.voeg_recept_toe)
        self.add_button.grid(row=0, column=0, padx=10, pady=10)

        # Toon alle recepten knop
        self.show_button = ttk.Button(self.frame, text="Toon Alle Recepten", command=self.toon_recepten)
        self.show_button.grid(row=0, column=1, padx=10, pady=10)

        # Zoek recepten knop
        self.search_button = ttk.Button(self.frame, text="Zoek Recept", command=self.zoek_recept)
        self.search_button.grid(row=0, column=2, padx=10, pady=10)

        # Knop voor favorieten
        self.favorieten_button = ttk.Button(self.frame, text="Markeer als Favoriet", command=self.markeer_als_favoriet)
        self.favorieten_button.grid(row=0, column=3, padx=10, pady=10)

        # Toon favorieten knop
        self.show_favorites_button = ttk.Button(self.frame, text="Toon Favorieten", command=self.toon_favoriete_recepten)
        self.show_favorites_button.grid(row=0, column=4, padx=10, pady=10)

        # Verwijder recept knop
        self.delete_button = ttk.Button(self.frame, text="Verwijder Recept", command=self.verwijder_recept)
        self.delete_button.grid(row=0, column=5, padx=10, pady=10)

        # Wijzig recept knop
        self.edit_button = ttk.Button(self.frame, text="Wijzig Recept", command=self.wijzig_recept)
        self.edit_button.grid(row=0, column=6, padx=10, pady=10)

        # Voeg ingrediënten toe aan boodschappenlijst knop
        self.add_ingredients_button = ttk.Button(self.frame, text="Voeg Ingrediënten Toe aan Boodschappenlijst", command=self.voeg_ingredienten_aan_boodschappenlijst)
        self.add_ingredients_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        # Exporteer boodschappenlijst knop
        self.export_button = ttk.Button(self.frame, text="Exporteer Boodschappenlijst naar CSV", command=self.exporteer_boodschappenlijst)
        self.export_button.grid(row=1, column=2, columnspan=2, padx=10, pady=10)

        # Verwijder alle recepten knop
        self.delete_all_button = ttk.Button(self.frame, text="Verwijder Alle Recepten", command=self.verwijder_alle_recepten)
        self.delete_all_button.grid(row=1, column=4, padx=10, pady=10)

        # Verwijder boodschappenlijst knop
        self.delete_list_button = ttk.Button(self.frame, text="Verwijder Boodschappenlijst", command=self.verwijder_boodschappenlijst)
        self.delete_list_button.grid(row=1, column=5, padx=10, pady=10)

        # Copyright knop
        self.copyright_button = ttk.Button(self.frame, text="Copyright Info", command=self.toon_copyright_info)
        self.copyright_button.grid(row=1, column=6, columnspan=2, padx=10, pady=10)


        # Initialiseer boodschappenlijst
        self.boodschappenlijst = []



    def voeg_recept_toe(self):
        naam = simpledialog.askstring("Voeg Recept Toe", "Voer de naam van het recept in:")
        if naam:
            ingrediënten = self.vraag_ingredienten()
            instructies = self.vraag_instructies()
            categorie = simpledialog.askstring("Categorie", "Voer de categorie in:")
            bereidingstijd = simpledialog.askstring("Bereidingstijd", "Voer de bereidingstijd in (in minuten):")

            nieuw_recept = {
                "naam": naam,
                "ingrediënten": ingrediënten,
                "instructies": instructies,
                "categorie": categorie,
                "bereidingstijd": bereidingstijd
            }

            self.recepten.append(nieuw_recept)
            sla_recepten_op(self.recepten)
            messagebox.showinfo("Succes", f"Recept '{naam}' toegevoegd!")


    def vraag_ingredienten(self):
        ingrediënten = []
        while True:
            ingredient = simpledialog.askstring("Ingrediënten", "Voer een ingrediënt in (of laat leeg om te stoppen):")
            if ingredient:
                ingrediënten.append(ingredient)
            else:
                break
        return ingrediënten

    def vraag_instructies(self):
        instructies = []
        while True:
            stap = simpledialog.askstring("Instructies", "Voer een kookinstructie in (of laat leeg om te stoppen):")
            if stap:
                instructies.append(stap)
            else:
                break
        return instructies

    def toon_recepten(self):
        if not self.recepten:
            messagebox.showinfo("Info", "Geen recepten gevonden.")
            return

        recepten_info = "\n".join([f"{i+1}. {recept['naam']} - Categorie: {recept['categorie']}" for i, recept in enumerate(self.recepten)])
        keuze = simpledialog.askinteger("Toon Recepten", f"Beschikbare recepten:\n{recepten_info}\nKies een nummer voor details (of laat leeg om te annuleren):")

        if keuze and 1 <= keuze <= len(self.recepten):
            recept = self.recepten[keuze - 1]
            bereidingstijd = recept.get('bereidingstijd', 'Niet beschikbaar')  # Controle op ontbrekende bereidingstijd
            details = (
                f"Naam: {recept['naam']}\n\n"
                f"Ingrediënten:\n- " + "\n- ".join(recept['ingrediënten']) + "\n\n"
                f"Instructies:\n" + "\n".join([f"Stap {i + 1}: {stap}" for i, stap in enumerate(recept['instructies'])]) + "\n\n"
                f"Categorie: {recept['categorie']}\n\n"
                f"Bereidingstijd: {bereidingstijd}"
            )
            messagebox.showinfo("Recept Details", details)


    def zoek_recept(self):
        zoekterm = simpledialog.askstring("Zoek Recept", "Voer een zoekterm in (naam, categorie, ingrediënt, bereidingstijd):")
    
        gevonden_recepten = [
            recept for recept in self.recepten
            if zoekterm.lower() in recept['naam'].lower()
            or zoekterm.lower() in recept['categorie'].lower()
            or zoekterm.lower() in " ".join(recept['ingrediënten']).lower()
        ]

        if gevonden_recepten:
            recepten_info = "\n".join([f"{i+1}. {recept['naam']} - Categorie: {recept['categorie']}" for i, recept in enumerate(gevonden_recepten)])
            keuze = simpledialog.askinteger("Gevonden Recepten", f"Gevonden recepten:\n{recepten_info}\nKies een nummer voor details (of laat leeg om te annuleren):")

            if keuze and 1 <= keuze <= len(gevonden_recepten):
                recept = gevonden_recepten[keuze - 1]
                details = f"Naam: {recept['naam']}\nIngrediënten: {', '.join(recept['ingrediënten'])}\nInstructies: {', '.join(recept['instructies'])}\nCategorie: {recept['categorie']}"
                messagebox.showinfo("Recept Details", details)
        else:
            messagebox.showinfo("Info", "Geen recepten gevonden met die zoekterm.")

    def wijzig_recept(self):
        # Toon een lijst met alle beschikbare recepten
        recept_namen = "\n".join([r['naam'] for r in self.recepten])
        messagebox.showinfo("Beschikbare Recepten", f"Beschikbare recepten:\n{recept_namen}")

        # Vraag de gebruiker om de naam van het recept dat ze willen wijzigen
        naam = simpledialog.askstring("Wijzig Recept", "Voer de naam van het recept in dat je wilt wijzigen:")

        # Zoek het recept op basis van de ingevoerde naam
        recept = next((r for r in self.recepten if r['naam'].lower() == naam.lower()), None)

        if recept:
            nieuwe_naam = simpledialog.askstring("Wijzig Naam", f"Huidige naam: {recept['naam']}\nVoer een nieuwe naam in (of laat leeg om niet te wijzigen):") or recept['naam']
            nieuwe_ingredienten = self.vraag_ingredienten() or recept['ingrediënten']
            nieuwe_instructies = self.vraag_instructies() or recept['instructies']
            nieuwe_categorie = simpledialog.askstring("Wijzig Categorie", f"Huidige categorie: {recept['categorie']}\nVoer een nieuwe categorie in (of laat leeg om niet te wijzigen):") or recept['categorie']

            # Wijzig of voeg bereidingstijd toe
            nieuwe_bereidingstijd = simpledialog.askstring(
                "Wijzig Bereidingstijd",
                f"Huidige bereidingstijd: {recept.get('bereidingstijd', 'Niet ingesteld')}\nVoer een nieuwe bereidingstijd in (of laat leeg om niet te wijzigen):"
            ) or recept.get('bereidingstijd', '')

            # Update het recept
            recept.update({
                "naam": nieuwe_naam,
                "ingrediënten": nieuwe_ingredienten,
                "instructies": nieuwe_instructies,
                "categorie": nieuwe_categorie,
                "bereidingstijd": nieuwe_bereidingstijd
            })

            # Sla het recept op
            sla_recepten_op(self.recepten)
            messagebox.showinfo("Succes", f"Recept '{recept['naam']}' is bijgewerkt!")
        else:
            messagebox.showwarning("Niet Gevonden", f"Recept met naam '{naam}' niet gevonden.")


    def markeer_als_favoriet(self):
        naam = simpledialog.askstring("Markeer als Favoriet", "Voer de naam van het recept in dat je als favoriet wilt markeren:")
        recept = next((r for r in self.recepten if r['naam'].lower() == naam.lower()), None)

        if recept:
            if recept not in self.favoriete_recepten:
                self.favoriete_recepten.append(recept)
                sla_favoriete_recepten_op(self.favoriete_recepten)
                samenvatting = f"Naam: {recept['naam']}\nCategorie: {recept['categorie']}"
                messagebox.showinfo("Favoriet Gemarkeerd", f"Recept '{recept['naam']}' is toegevoegd aan je favorieten!\n\nSamenvatting:\n{samenvatting}")
            else:
                messagebox.showinfo("Info", f"'{recept['naam']}' staat al in je favorieten.")
        else:
            messagebox.showwarning("Niet Gevonden", f"Recept met naam '{naam}' niet gevonden.")


    def toon_favoriete_recepten(self):
        if not self.favoriete_recepten:
            messagebox.showinfo("Info", "Je hebt nog geen favoriete recepten.")
            return

        favorieten_info = "\n".join([f"{i+1}. {recept['naam']} - Categorie: {recept['categorie']}" for i, recept in enumerate(self.favoriete_recepten)])
        keuze = simpledialog.askinteger("Favoriete Recepten", f"Je favoriete recepten:\n{favorieten_info}\nKies een nummer voor details (of laat leeg om te annuleren):")

        if keuze and 1 <= keuze <= len(self.favoriete_recepten):
            recept = self.favoriete_recepten[keuze - 1]
            bereidingstijd = recept.get('bereidingstijd', 'Niet beschikbaar')  # Controle op ontbrekende bereidingstijd
            details = (
                f"Naam: {recept['naam']}\n\n"
                f"Ingrediënten:\n- " + "\n- ".join(recept['ingrediënten']) + "\n\n"
                f"Instructies:\n" + "\n".join([f"Stap {i + 1}: {stap}" for i, stap in enumerate(recept['instructies'])]) + "\n\n"
                f"Categorie: {recept['categorie']}\n\n"
                f"Bereidingstijd: {bereidingstijd}"
                )
            messagebox.showinfo("Recept Details", details)


    def verwijder_recept(self):
        if not self.recepten:
            messagebox.showinfo("Info", "Geen recepten om te verwijderen.")
            return

        recepten_info = "\n".join([f"{i+1}. {recept['naam']}" for i, recept in enumerate(self.recepten)])
        keuze = simpledialog.askinteger("Verwijder Recept", f"Beschikbare recepten:\n{recepten_info}\nKies een nummer om te verwijderen (of laat leeg om te annuleren):")

        if keuze and 1 <= keuze <= len(self.recepten):
            verwijderde_recept = self.recepten.pop(keuze - 1)

            # Verwijder het recept ook uit de favoriete recepten als het erin zit
            if verwijderde_recept in self.favoriete_recepten:
                self.favoriete_recepten.remove(verwijderde_recept)

            sla_recepten_op(self.recepten)
            sla_favoriete_recepten_op(self.favoriete_recepten)  # Veronderstelt dat je een functie hebt om favoriete recepten op te slaan
            messagebox.showinfo("Succes", f"Recept '{verwijderde_recept['naam']}' verwijderd!")

    def voeg_ingredienten_aan_boodschappenlijst(self):
        if not self.recepten:
            messagebox.showinfo("Info", "Geen recepten om ingrediënten van toe te voegen.")
            return

        # Toon de lijst met recepten
        recepten_info = "\n".join([f"{i+1}. {recept['naam']} - Ingrediënten: {', '.join(recept['ingrediënten'])}" for i, recept in enumerate(self.recepten)])
    
        # Vraag de gebruiker om meerdere recepten te selecteren (invoer in de vorm van 1,2,3)
        keuzes = simpledialog.askstring("Voeg Ingrediënten Toe aan Boodschappenlijst", 
                                    f"Beschikbare recepten:\n{recepten_info}\n"
                                    "Voer de nummers in van de recepten die je wilt toevoegen (bijv. 1,2,3):")
    
        if keuzes:
            gekozen_nummers = [int(k.strip()) for k in keuzes.split(",") if k.strip().isdigit()]
            for keuze in gekozen_nummers:
                if 1 <= keuze <= len(self.recepten):
                    gekozen_recept = self.recepten[keuze - 1]
                    # Voeg elk ingrediënt toe met het bijbehorende receptnaam
                    self.boodschappenlijst.extend([(gekozen_recept['naam'], ingrediënt) for ingrediënt in gekozen_recept['ingrediënten']])

            # Toon succesbericht en de bijgewerkte boodschappenlijst
            messagebox.showinfo("Succes", f"Ingrediënten van geselecteerde recepten toegevoegd aan de boodschappenlijst.")
    
            # Toon de huidige boodschappenlijst met receptnamen
            boodschappen_info = "\n".join([f"- {ingredient} (van recept: {recept})" for recept, ingredient in self.boodschappenlijst])
            messagebox.showinfo("Boodschappenlijst", f"Huidige boodschappenlijst:\n{boodschappen_info}")

    def verwijder_boodschappenlijst(self):
        # Functie om de huidige boodschappenlijst te verwijderen
        if messagebox.askyesno("Verwijder Boodschappenlijst", "Weet je zeker dat je de huidige boodschappenlijst wilt verwijderen?"):
            self.boodschappenlijst = []  # Reset de boodschappenlijst
            messagebox.showinfo("Succes", "De boodschappenlijst is verwijderd.")

    def exporteer_boodschappenlijst(self):
        if not self.boodschappenlijst:
            messagebox.showinfo("Info", "De boodschappenlijst is leeg.")
            return

        # Exporteer de boodschappenlijst met receptnamen
        exporteer_boodschappenlijst_naar_csv(self.boodschappenlijst)

    def verwijder_alle_recepten(self):
        if messagebox.askyesno("Bevestiging", "Weet je zeker dat je alle recepten wilt verwijderen?"):
            self.recepten.clear()
            self.favoriete_recepten.clear()  # Zorg ervoor dat ook de favoriete recepten worden verwijderd
            sla_recepten_op(self.recepten)
            sla_favoriete_recepten_op(self.favoriete_recepten)  # Veronderstelt dat je een functie hebt om favoriete recepten op te slaan
            messagebox.showinfo("Succes", "Alle recepten zijn verwijderd.")

    def toon_copyright_info(self):
        # Toon een dialoogvenster met copyrightinformatie
        messagebox.showinfo("Copyright", "© Odin Wattez 2024\nAlle rechten voorbehouden.")


if __name__ == "__main__":
    root = tk.Tk()
    app = RecipeManagerApp(root)
    root.mainloop()
