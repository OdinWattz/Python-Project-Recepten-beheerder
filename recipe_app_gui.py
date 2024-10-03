import json
import os
import csv
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

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

        # Initialiseer recepten en favorieten
        self.recepten = laad_recepten()
        self.favoriete_recepten = laad_favoriete_recepten()

        # Maak de GUI-componenten
        self.create_widgets()

    def create_widgets(self):
        # Hoofdframe
        self.frame = ttk.Frame(self.root, padding="10")
        self.frame.grid()

        # Voeg recepten toe
        self.add_button = ttk.Button(self.frame, text="Voeg Recept Toe", command=self.voeg_recept_toe)
        self.add_button.grid(row=0, column=0, padx=5, pady=5)

        # Toon alle recepten
        self.show_button = ttk.Button(self.frame, text="Toon Alle Recepten", command=self.toon_recepten)
        self.show_button.grid(row=0, column=1, padx=5, pady=5)

        # Zoek recepten
        self.search_button = ttk.Button(self.frame, text="Zoek Recept", command=self.zoek_recept)
        self.search_button.grid(row=0, column=2, padx=5, pady=5)

        # Markeer als favoriet
        self.favorieten_button = ttk.Button(self.frame, text="Markeer als Favoriet", command=self.markeer_als_favoriet)
        self.favorieten_button.grid(row=0, column=3, padx=5, pady=5)

        # Toon favoriete recepten
        self.show_favorites_button = ttk.Button(self.frame, text="Toon Favorieten", command=self.toon_favoriete_recepten)
        self.show_favorites_button.grid(row=0, column=4, padx=5, pady=5)

        # Verwijder recept
        self.delete_button = ttk.Button(self.frame, text="Verwijder Recept", command=self.verwijder_recept)
        self.delete_button.grid(row=0, column=5, padx=5, pady=5)

        # Voeg ingrediënten toe aan boodschappenlijst
        self.add_ingredients_button = ttk.Button(self.frame, text="Voeg Ingrediënten Toe aan Boodschappenlijst", command=self.voeg_ingredienten_aan_boodschappenlijst)
        self.add_ingredients_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        # Exporteer boodschappenlijst naar CSV
        self.export_button = ttk.Button(self.frame, text="Exporteer Boodschappenlijst naar CSV", command=self.exporteer_boodschappenlijst)
        self.export_button.grid(row=1, column=2, columnspan=4, padx=5, pady=5)

         # Initialiseer boodschappenlijst
        self.boodschappenlijst = []  # Maak boodschappenlijst een klasse-attribuut


    def voeg_recept_toe(self):
        naam = simpledialog.askstring("Voeg Recept Toe", "Voer de naam van het recept in:")
        if naam:
            ingrediënten = self.vraag_ingredienten()
            instructies = self.vraag_instructies()
            categorie = simpledialog.askstring("Categorie", "Voer de categorie in:")

            nieuw_recept = {
                "naam": naam,
                "ingrediënten": ingrediënten,
                "instructies": instructies,
                "categorie": categorie
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
            details = (
                f"Naam: {recept['naam']}\n\n"
                f"Ingrediënten:\n- " + "\n- ".join(recept['ingrediënten']) + "\n\n"
                f"Instructies:\n" + "\n".join([f"Stap {i + 1}: {stap}" for i, stap in enumerate(recept['instructies'])]) + "\n\n"
                f"Categorie: {recept['categorie']}"
            )
        messagebox.showinfo("Recept Details", details)


    def zoek_recept(self):
        zoekterm = simpledialog.askstring("Zoek Recept", "Voer een zoekterm in:")
        gevonden_recepten = [recept for recept in self.recepten if zoekterm.lower() in recept['naam'].lower()]

        if gevonden_recepten:
            recepten_info = "\n".join([f"{i+1}. {recept['naam']} - Categorie: {recept['categorie']}" for i, recept in enumerate(gevonden_recepten)])
            keuze = simpledialog.askinteger("Gevonden Recepten", f"Gevonden recepten:\n{recepten_info}\nKies een nummer voor details (of laat leeg om te annuleren):")

            if keuze and 1 <= keuze <= len(gevonden_recepten):
                recept = gevonden_recepten[keuze - 1]
                details = f"Naam: {recept['naam']}\nIngrediënten: {', '.join(recept['ingrediënten'])}\nInstructies: {', '.join(recept['instructies'])}\nCategorie: {recept['categorie']}"
                messagebox.showinfo("Recept Details", details)
        else:
            messagebox.showinfo("Info", "Geen recepten gevonden met die zoekterm.")

    def markeer_als_favoriet(self):
        naam = simpledialog.askstring("Markeer als Favoriet", "Voer de naam van het recept in dat je als favoriet wilt markeren:")
        recept = next((r for r in self.recepten if r['naam'].lower() == naam.lower()), None)

        if recept:
            if recept not in self.favoriete_recepten:
                self.favoriete_recepten.append(recept)
                sla_favoriete_recepten_op(self.favoriete_recepten)
                messagebox.showinfo("Succes", f"Recept '{recept['naam']}' is toegevoegd aan je favorieten!")
            else:
                messagebox.showinfo("Info", f"'{recept['naam']}' staat al in je favorieten.")
        else:
            messagebox.showwarning("Niet Gevonden", f"Recept met naam '{naam}' niet gevonden.")

    def toon_favoriete_recepten(self):
        if not self.favoriete_recepten:
            messagebox.showinfo("Info", "Je hebt nog geen favoriete recepten.")
            return

        favorieten_info = "\n".join([f"{i+1}. {recept['naam']}" for i, recept in enumerate(self.favoriete_recepten)])
        messagebox.showinfo("Favoriete Recepten", f"Je favoriete recepten:\n{favorieten_info}")

    def verwijder_recept(self):
        if not self.recepten:
            messagebox.showinfo("Info", "Geen recepten om te verwijderen.")
            return

        recepten_info = "\n".join([f"{i+1}. {recept['naam']}" for i, recept in enumerate(self.recepten)])
        keuze = simpledialog.askinteger("Verwijder Recept", f"Beschikbare recepten:\n{recepten_info}\nKies een nummer om te verwijderen (of laat leeg om te annuleren):")

        if keuze and 1 <= keuze <= len(self.recepten):
            verwijderde_recept = self.recepten.pop(keuze - 1)
            sla_recepten_op(self.recepten)
            messagebox.showinfo("Succes", f"Recept '{verwijderde_recept['naam']}' verwijderd!")

    def voeg_ingredienten_aan_boodschappenlijst(self):
        if not self.recepten:
            messagebox.showinfo("Info", "Geen recepten om ingrediënten van toe te voegen.")
            return

        recepten_info = "\n".join([f"{i+1}. {recept['naam']} - Ingrediënten: {', '.join(recept['ingrediënten'])}" for i, recept in enumerate(self.recepten)])
        keuze = simpledialog.askinteger("Voeg Ingrediënten Toe aan Boodschappenlijst", f"Beschikbare recepten:\n{recepten_info}\nVoer het nummer van het recept in om ingrediënten toe te voegen aan je boodschappenlijst:")

        if keuze and 1 <= keuze <= len(self.recepten):
            gekozen_recept = self.recepten[keuze - 1]
            self.boodschappenlijst.extend(gekozen_recept['ingrediënten'])  # Gebruik de klasse-attribuut
            messagebox.showinfo("Succes", f"Ingrediënten van '{gekozen_recept['naam']}' toegevoegd aan de boodschappenlijst.")

            # Toon de huidige boodschappenlijst
            boodschappen_info = "\n".join([f"- {ingredient}" for ingredient in self.boodschappenlijst])
            messagebox.showinfo("Boodschappenlijst", f"Huidige boodschappenlijst:\n{boodschappen_info}")

    def exporteer_boodschappenlijst(self):
        if not self.boodschappenlijst:
            messagebox.showinfo("Info", "De boodschappenlijst is leeg.")
            return

        exporteer_boodschappenlijst_naar_csv(self.boodschappenlijst)

if __name__ == "__main__":
    root = tk.Tk()
    app = RecipeManagerApp(root)
    root.mainloop()
