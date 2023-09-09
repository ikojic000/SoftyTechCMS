# SoFtYTechCMS

SoFtYTechCMS je Content Management System (CMS) za istoimeni portal.

## Značajke aplikacije

### Javni portal

- Čitanje članaka
- Pretraživanje članaka
- Registriranje korisnika
- Prijava korisnika putem korisničkog imena ili e-maila i lozinke i putem Google ili Facebook računa
- Resetiranje zaboravljene lozinke putem e-maila
- Obavijest korisnika o promijenjenoj lozinki nakon resetiranja zaboravljene lozinke
- Ostavljanje komentara i brisanje vlastitih komentara
- Kontaktiranje administratora stranice putem kontakt forme
- Mijenjanje korisničkih postavki (ime, korisničko ime, e-mail, lozinka)

### Admin sučelje

- Prava temeljena na ulogama (Reader, Admin, Superadmin)
- Grafički prikaz broja korisnika, članaka i komentara
- Tablični prikaz svih članaka, korisnika i komentara
- Mogućnost kreiranja novih članaka te ažuriranja ili brisanja postojećih
  - Provjera po imenu i po SSIM sličnosti prilikom upload-a naslovne slike
- Mogućnost kreiranja novih kategorija te ažuriranja ili brisanja postojećih
- Ručno dodavanje korisnika
- Ažuriranje dozvola (uloga) svakog korisnika
- Prikaz detalja korisnika (prikaz podataka, prikaz napisanih članaka ako postoje i prikaz ostavljenih komentara ako postoje)
- Brisanje komentara
- FileManager povezan s datotekama na serveru (slike i ostali sadržaji se ne spremaju u bazu radi uštede na prostoru) - RichFileManager
- Pregled svih Request logova (samo Superadmin korisnici). Svaki request se sprema u bazu podataka
- Pregled svih Error logova (samo Superadmin korisnici). Svaka greška se sprema u bazu podataka

Admin i Superadmin korisnici imaju mogućnost kontrole i pregleda svega što se događa na javnom portalu i u cijeloj web aplikaciji.

## Tehnologije korištene

Aplikacija je izrađena pomoću različitih tehnologija i biblioteka, uključujući:

- **Python** kao programski jezik za razvoj
- **Flask** web framework za izradu aplikacije
- **Flask-SQLAlchemy** za komunikaciju s bazom podataka (koristena MySQL baza podataka)
- **Flask-Login** za upravljanje korisničkim sesijama
- **Flask-Mail** za slanje e-mail obavijesti
- **Flask-WTF** za upravljanje web obrascima
- **Flask-User** za upravljanje korisničkim računima
- **Flask-OAuthlib** za prijavu putem Google/Facebook računa
- **bcrypt** za kriptiranje lozinki

### Ostale tehnologije

Osim toga, upotrebljeni su i drugi alati i tehnologije navedeni u `requirements.txt` datoteci, uključujući:

- aiohttp==3.8.5
- aiosignal==1.3.1
- asn1crypto==0.24.0
- astroid==2.1.0
- async-timeout==4.0.3
- ...
- yarl==1.9.2
- zipp==3.15.0

Za sve dodatne informacije i pitanja, kontaktirajte me na ikojic000@gmail.com.
