function byttModus() {
    const tittel = document.getElementById('tittel');
    const hovedBtn = document.getElementById('hoved-btn');
    const byttBtn = document.getElementById('bytt-btn');
    const skjema = document.getElementById('skjema');
    const valgBoks = document.getElementById('valg-boks');
    const sjekkInput = document.getElementById('sjekk-input');

    if (skjema.action.includes('/register')) {
        tittel.innerText = "Logg inn";
        hovedBtn.innerText = "Logg inn";
        byttBtn.innerText = "Opprett konto";
        skjema.action = "/login";
        valgBoks.style.display = "none";
        sjekkInput.required = false;
    } else {
        tittel.innerText = "Opprett konto";
        hovedBtn.innerText = "Opprett konto";
        byttBtn.innerText = "Logg inn";
        skjema.action = "/register";
        valgBoks.style.display = "block";
        sjekkInput.required = true;
    }
}