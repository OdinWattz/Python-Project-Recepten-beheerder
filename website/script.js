// Laad bestaande recepten als ze in localStorage staan
function laadRecepten() {
    let recepten = JSON.parse(localStorage.getItem('recepten')) || [];
    recepten.forEach(recept => {
        if (!recept.hasOwnProperty('bereidingstijd')) {
            recept['bereidingstijd'] = "Niet beschikbaar";
        }
    });
    return recepten;
}

// Sla de recepten op in localStorage
function slaReceptenOp(recepten) {
    localStorage.setItem('recepten', JSON.stringify(recepten));
}

// Laad de favoriete recepten
function laadFavorieteRecepten() {
    return JSON.parse(localStorage.getItem('favoriete_recepten')) || [];
}

// Sla de favoriete recepten op in localStorage
function slaFavorieteReceptenOp(favorieteRecepten) {
    localStorage.setItem('favoriete_recepten', JSON.stringify(favorieteRecepten));
}

// Exporteer de boodschappenlijst naar een CSV-bestand
function exporteerBoodschappenlijstNaarCSV(boodschappenlijst, bestandsnaam = "boodschappenlijst.csv") {
    const rows = [["Ingrediënten"], ...boodschappenlijst.map(item => [item])];
    let csvContent = "data:text/csv;charset=utf-8," + rows.map(e => e.join(",")).join("\n");
    let encodedUri = encodeURI(csvContent);
    let link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", bestandsnaam);
    document.body.appendChild(link);
    link.click();
    alert(`Boodschappenlijst succesvol geëxporteerd naar ${bestandsnaam}.`);
}

// Voeg recepten toe
function voegReceptToe() {
    const naam = prompt("Voer de naam van het recept in:");
    if (naam) {
        const ingrediënten = vraagIngredienten();
        const instructies = vraagInstructies();
        const categorie = prompt("Voer de categorie in:");
        const bereidingstijd = prompt("Voer de bereidingstijd in (in minuten):");

        let nieuwRecept = {
            naam: naam,
            ingrediënten: ingrediënten,
            instructies: instructies,
            categorie: categorie,
            bereidingstijd: bereidingstijd
        };

        let recepten = laadRecepten();
        recepten.push(nieuwRecept);
        slaReceptenOp(recepten);
        alert(`Recept '${naam}' toegevoegd!`);
    }
}

// Vraag ingrediënten
function vraagIngredienten() {
    let ingrediënten = [];
    while (true) {
        let ingredient = prompt("Voer een ingrediënt in (of laat leeg om te stoppen):");
        if (ingredient) {
            ingrediënten.push(ingredient);
        } else {
            break;
        }
    }
    return ingrediënten;
}

// Vraag instructies
function vraagInstructies() {
    let instructies = [];
    while (true) {
        let stap = prompt("Voer een kookinstructie in (of laat leeg om te stoppen):");
        if (stap) {
            instructies.push(stap);
        } else {
            break;
        }
    }
    return instructies;
}

// Toon recepten
function toonRecepten() {
    let recepten = laadRecepten();
    if (recepten.length === 0) {
        alert("Geen recepten gevonden.");
        return;
    }

    let receptenInfo = recepten.map((recept, index) => `${index + 1}. ${recept.naam} - Categorie: ${recept.categorie}`).join("\n");
    let keuze = parseInt(prompt(`Beschikbare recepten:\n${receptenInfo}\nKies een nummer voor details:`), 10);

    if (keuze && keuze > 0 && keuze <= recepten.length) {
        let recept = recepten[keuze - 1];
        let details = `
            Naam: ${recept.naam}\n
            Ingrediënten: ${recept.ingrediënten.join(", ")}\n
            Instructies: ${recept.instructies.join(", ")}\n
            Categorie: ${recept.categorie}\n
            Bereidingstijd: ${recept.bereidingstijd || 'Niet beschikbaar'}
        `;
        alert(details);
    }
}

// Zoek recept
function zoekRecept() {
    let zoekterm = prompt("Voer een zoekterm in (naam, categorie, ingrediënt, bereidingstijd):").toLowerCase();
    let recepten = laadRecepten();
    let gevondenRecepten = recepten.filter(recept =>
        recept.naam.toLowerCase().includes(zoekterm) ||
        recept.categorie.toLowerCase().includes(zoekterm) ||
        recept.ingrediënten.some(ing => ing.toLowerCase().includes(zoekterm))
    );

    if (gevondenRecepten.length > 0) {
        let receptenInfo = gevondenRecepten.map((recept, index) => `${index + 1}. ${recept.naam} - Categorie: ${recept.categorie}`).join("\n");
        let keuze = parseInt(prompt(`Gevonden recepten:\n${receptenInfo}\nKies een nummer voor details:`), 10);

        if (keuze && keuze > 0 && keuze <= gevondenRecepten.length) {
            let recept = gevondenRecepten[keuze - 1];
            let details = `
                Naam: ${recept.naam}\n
                Ingrediënten: ${recept.ingrediënten.join(", ")}\n
                Instructies: ${recept.instructies.join(", ")}\n
                Categorie: ${recept.categorie}
            `;
            alert(details);
        }
    } else {
        alert("Geen recepten gevonden met die zoekterm.");
    }
}

// Markeer als favoriet
function markeerAlsFavoriet() {
    let naam = prompt("Voer de naam van het recept in dat je als favoriet wilt markeren:");
    let recepten = laadRecepten();
    let recept = recepten.find(r => r.naam.toLowerCase() === naam.toLowerCase());

    if (recept) {
        let favorieteRecepten = laadFavorieteRecepten();
        if (!favorieteRecepten.some(r => r.naam === recept.naam)) {
            favorieteRecepten.push(recept);
            slaFavorieteReceptenOp(favorieteRecepten);
            alert(`Recept '${recept.naam}' is toegevoegd aan je favorieten!`);
        } else {
            alert(`'${recept.naam}' staat al in je favorieten.`);
        }
    } else {
        alert(`Recept met naam '${naam}' niet gevonden.`);
    }
}

// Toon favorieten
function toonFavorieteRecepten() {
    let favorieteRecepten = laadFavorieteRecepten();
    if (favorieteRecepten.length === 0) {
        alert("Je hebt nog geen favoriete recepten.");
        return;
    }

    let favorietenInfo = favorieteRecepten.map((recept, index) => `${index + 1}. ${recept.naam} - Categorie: ${recept.categorie}`).join("\n");
    let keuze = parseInt(prompt(`Je favoriete recepten:\n${favorietenInfo}\nKies een nummer voor details:`), 10);

    if (keuze && keuze > 0 && keuze <= favorieteRecepten.length) {
        let recept = favorieteRecepten[keuze - 1];
        let details = `
            Naam: ${recept.naam}\n
            Ingrediënten: ${recept.ingrediënten.join(", ")}\n
            Instructies: ${recept.instructies.join(", ")}\n
            Categorie: ${recept.categorie}
        `;
        alert(details);
    }
}
