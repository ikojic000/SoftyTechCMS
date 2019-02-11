# SoFtYTech
Flask CMS for a blogsite

*** HRV ***
- Flask-WhooshAlchemy -
Nakon instalacije svega potrebnoga, potrebno je file flask_whooshalchemy.py ili preraditi ili zamijeniti sa onim uploadanim na github.
Ako se to ne napravi, APP nece raditi jer je Flask-WhooshAlchemy napravljen za Python2, a APP je u Python3.

- Flask-Mail - 
Da bi Flask-Mail radio i stvarno slao mail-ove potrebno je u config.py promijeniti postavke te staviti prave podatke koje ce Flask-Mail korisiti.

- DataBase - 
Baza podataka je napravljena sa SqLite3 te je uploadana na github sa "dummy data". 
Nju mozete izbrisati, a da bi je APP automatski napravila pri prvom pokretanju potrebno je maknuti komentar iz "models.py".
Komentirani dio se nalazi na dnu file-a te je zaduzen za izradu baze podataka sa jednim Admin user-om i jednim Reader user-om.
Nakon prvog pokretanja APP-a potrebno je opet zakomentirati taj dio.

- Admin/Media - 
Subpage zaduzen za upload slika te za prikaz istih. Te slike sprema na server u static/media/images .

- Admin/AddPosts - 
Subpage zaduzen za dodavanje i uploadanje postova na blogu. Moze se dodati "headImage", ali ako se ne doda ona je automatski odredena.
U odjeljku gdje se pise tekst clanka je ugraden WYSIWYG editor kojim se moze oblikovati text te takoder uploadati slike te ih i oblikovati.

- User - 
Korisnici imaju mogucnost registracije, prijave, promjene sifre, promjene maila, promjene username-a, komentiranja clanaka (ugradeni smajlici), 
resetiranja sifre nakon zaborava, brisanja racuna...

- Admin -
Admin ima mogucnost odredivanja uloga svakom User-u, uploadanja postova, uploadanja slika...



*** VAZNO ***

Ova Web stranica / Web aplikacija jos nije gotova konacno. S obzirom da namjeravam korisiti ovu web stranicu i CMS za pisanje i vodenje bloga, stranica jos nije sasvim gotova te se jos uvijek doraduje.
Planiram dodati jos par funkcionalnosti te popraviti design gdje je to potrebno. 
Sav design je napravljen rucno i nije koristen nikakav template.

Za sve informacije mozete me kontaktirati na ikojic000@gmail.com


