Technologie feature zuordnung und die charakterisierenden Merkmale:

Feature: Absatz
Moegliche Technologien:	Fräsen, Schleifen
Faktoren:
	- Rauheit
	- Ebenheit
	- Parallelität
	- Position
	- Länge (+-)
	- Breite (+-)
	- Höhe (+-)
	- prismatic=true
	- positive=ture
	- Werkstoff

Feature: Bohrung
Moegliche Technologien: Bohren, Fräsen
Faktoren:
	- Bohrungsgrund=kegel
	- Durchmesser (+-)
	- prismatic=false
	- Werkstoff
	- positive=false

Feature: Innengewinde
Moegliche Technologien: Bohren, Fräsen
Faktoren: 
	- Gewindeart
	- Durchmesser (+-)
	- Steigung
	- Länge (+-)
	- prismatic=false
	- positive=false
	- Werkstoff

Feature: T-Nut
Moegliche Technologien: Fräsen, Schleifen
Faktoren:
	- Tiefe (+-)
	- Eckenradius
	- Breite
	- Fuss (+-)
	- Länge (+-)
	- Breite (+-)
	- Tiefe
	- Fuss (+-)
	- prismatic=true
	- positive=false
	- Werkstoff

Feature: Zylindersenkung
Moegliche Technologien: Bohren, Fräsen
Faktoren:
	- Tiefe (+-)
	- Durchmesser (+-)
	- prismatic=false
	- positive=false
	- Halbzeug prismatisch
	- Werkstoff
	- Länge (+-)
	- Breite (+-)
	- Höhe (+-)
	- prismatic=true
	- positive=ture


