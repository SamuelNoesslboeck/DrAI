# Jugend Innovativ

## Infos

[Link](https://www.jugendinnovativ.at/teilnahme/wettbewerb)
Deadline: 30/01/2024

""  
DIE NEUEN TERMINE IM ÜBERBLICK:

- Projektanmeldung von 4. Oktober bis 30. November 2023
- Konzepte für Projekt-Bonus einreichen bis 30. November 2023
- Digitale Info-Hour: 12. Oktober 2023, 14.30-15.30 Uhr -
- Wir empfehlen die Teilnahme!
- Pre-Check aller Anmeldungen & Mitteilung über das Ergebnis: Mitte Dezember 2023
- Projektbericht-Abgabe bis 30. Jänner 2024 (nur für zugesagte Projekte!)
- Bundes-Finale: 27. - 29. Mai 2024

""  
*Jugendinnovativ Website*

## TODO

- [x] Anmeldung                 (bis 30/11/2023)
- [x] Beschreibung einreichen   (bis 30/01/2024)

## Beschreibungen

Komplexere Beschreibungen für den Wettbewerb.

- [**Richtlinien**](https://www.jugendinnovativ.at/fileadmin/user_upload/Callunterlagen/PB_Anleitung_ENGINEERING.pdf)

### Kurzbeschreibung der Zielsetzung

Ziel dieses Projekts ist es, die Fähigkeiten von KI bei der Erledigung "kreativer" Aufgaben in Zusammenarbeit mit Menschen zu demonstrieren und menschliche Kreativität nachzuahnen. Der Roboter ist außerdem als Ausstellungsstück für das Machine Learning Studio des Ars Electronica Center Museums geplant.

Das Endergebnis wird ein interaktiver Roboter sein, der mit einer KI ausgestattet ist, die darauf trainiert ist, vorgezeichnete Skizzen des Benutzers zu interpretieren und sie mit ihrer eigenen "Kreativität" zu vervollständigen. Sobald sich das Blatt im Roboter befindet, ist es sein Ziel, sein Potenzial zu entfalten, indem er zusätzliche Linien auf das Papier des Benutzers zeichnet. Die Möglichkeiten sind hier grenzenlos, die KI kann z. B. einen Wald neben einem Häuschen erschaffen, oder einen Strand neben ein Meer und so weiter.

### Kurzbeschreibung des Vorhabens

Das Projekt beinhaltet ein komplexes Netz aus verschiedensten Algorithmen geschrieben in Python und der eher neuen Systemsprache Rust.

Zuerst wird die exakte Platzierung des Papiers mit der Skizze mithilfe von einer Verschachtelung verschiedener Bildanalysemethoden, wie Canny-Edge-Detection, Harris-Corner-Detection usw., überprüft. So kann der Roboter trotz Ungenauigkeiten des Users beim Einführen des Papiers korrekt zeichnen. 
Die gezeichnete Skizze wird dann durch einen Clip-Interogator in einen Text-Prompt übertragen. Nun wird ein Large Language Model benutzt um der Zeichnung etwas hinzuzufügen. Hierbei ist Prompt Engeneering von nöten um den Output zu verbessern. Würden wir den neu generierten Prompt und das Originalbild durch eine Stable Diffusion Img2Img Pipeline laufen lassen würde zu wenig Kreativität im neuen Bild entstehen, da der Diffusion Algorithmus mit niedriger Strength keine neuen Ansätze generiert und mit zu hoher Strength das Originalbild verschwindet und etwas Unbrauchbares entsteht. Um dieses Problem zu umgehen werden zufällige Linien in das Originalbild gezeichnet. Durch diese simple Methode mit der Kombination der verschiedenen neuronalen Netzwerke und der restlichen komplexen Algorithmen, ist es möglich den Stable Diffusion Algorithmus Kreativität zu verleihen. Da der gesamte Algorithmus sehr leistungsaufwändig ist wurde das ganze Projekt auf die CPU / RAM und GPU / V-RAM diversifiziert und ausgelagert um optimale Leistung auf kostengünstiger Hardware zu ermöglichen.

Eine weiterer Aspekt ist die Steuerung des Roboters, die zu großen Teilen von uns in Rust angefertigt wurde, da es etwas vergleichbares in dieser Sprache noch nicht gibt. Rust hat uns durch ihre Eleganz, Sicherheit und überragende Performance überzeugt. Durch sie ist es möglich, die komplette Steuerung inklusive Bahnberechnungen auf einem simplen Raspberry Pi Einplatinencomputer laufen zu lassen. Da in einem Museum die Aufmerksamkeitsspanne der Besucher eher kurz ist, muss schnell gezeichnet werden. Was durch die robuste Konstruktion, die leistungsstarke Elektronik und die Software, die hochwertige Anlaufkurven für die Motoren berechnet, gewährleistet wird. 

## Finale Abgabe

### Kurzbeschreibung der Zielsetzung

Ziel dieses Projekts ist es, die Fähigkeiten von KI bei der Erledigung kreativer Aufgaben in Zusammenarbeit mit Menschen als Museumsstation zu demonstrieren und menschliche Kreativität nachzuahmen. Es beschäftZiel dieses Projekts ist es, die Fähigkeiten von KI bei der Erledigung kreativer Aufgaben in Zusammenarbeit mit Menschen zu demonstrieren und menschliche Kreativität nachzuahmen. Es beschäftigt sich außerdem mit der Frage, wie weit Kreativität überhaupt menschlich ist. Die Demonstration gelingt durch das Einbauen der KI in einen kleinen Roboter für eine neue Museumsstation des Ars Electronica Center Linz.igt sich außerdem mit der Frage, wie weit Kreativität überhaupt menschlich ist. 

### Kurzbeschreibung des Lösungsweges

Das Projekt beinhaltet ein komplexes Netz aus verschiedensten Algorithmen geschrieben in Python und der eher neuen Systemsprache Rust.

Zuerst wird die exakte Platzierung des Papiers mit der Skizze mithilfe von einer Verschachtelung verschiedener Bildanalysemethoden, wie Canny-Edge-Detection, Harris-Corner-Detection usw., überprüft. So kann der Roboter trotz Ungenauigkeiten des Users beim Einführen des Papiers korrekt zeichnen. 
Die gezeichnete Skizze wird dann durch einen Clip-Interogator in einen Text-Prompt übertragen. Nun wird ein Large Language Model benutzt um der Zeichnung etwas hinzuzufügen. Hierbei ist Prompt Engeneering von nöten um den Output zu verbessern. Würden wir den neu generierten Prompt und das Originalbild durch eine Stable Diffusion Img2Img Pipeline laufen lassen würde zu wenig Kreativität im neuen Bild entstehen, da der Diffusion Algorithmus mit niedriger Strength keine neuen Ansätze generiert und mit zu hoher Strength das Originalbild verschwindet und etwas Unbrauchbares entsteht. Um dieses Problem zu umgehen werden zufällige Linien in das Originalbild gezeichnet. Durch diese simple Methode mit der Kombination der verschiedenen neuronalen Netzwerke und der restlichen komplexen Algorithmen, ist es möglich den Stable Diffusion Algorithmus Kreativität zu verleihen. Da der gesamte Algorithmus sehr leistungsaufwändig ist wurde das ganze Projekt auf die CPU / RAM und GPU / V-RAM diversifiziert und ausgelagert um optimale Leistung auf kostengünstiger Hardware zu ermöglichen.

Eine weiterer Aspekt ist die Steuerung des Roboters, die zu großen Teilen von uns in Rust angefertigt wurde, da es etwas vergleichbares in dieser Sprache noch nicht gibt. Rust hat uns durch ihre Eleganz, Sicherheit und überragende Performance überzeugt. Durch sie ist es möglich, die komplette Steuerung inklusive Bahnberechnungen auf einem simplen Raspberry Pi Einplatinencomputer laufen zu lassen. Da in einem Museum die Aufmerksamkeitsspanne der Besucher eher kurz ist, muss schnell gezeichnet werden. Was durch die robuste Konstruktion, die leistungsstarke Elektronik und die Software, die hochwertige Anlaufkurven für die Motoren berechnet, gewährleistet wird. 

### Projektergebnisse

Zu Beginn unserer Entwicklung standen die Projektteilnehmer zur These, dass kreative Textbeschreibungen benötigt werden, um kreative Bilder durch KI zu generieren. Je weiter die Forschung des Algorithmus fortschritt, desto mehr festigte sich die Erkenntnis, dass diese These inkorrekt ist. Der erstellte Algorithmus hat einerseits die Möglichkeit, aus Bestehendem etwas Neues zu erzeugen und andererseits aus einem weißen Blatt Papier ohne textliche Beschreibungen oder menschliches Einwirken kreative Bilder zu malen. Es ist eine philosophische Frage, ob Maschinen kreativ sein können oder nicht, jedoch sehen die Resultate sehr vielversprechend aus. Die Frage, ob KI kreativ sein kann, wird eher zur Frage, wann KI kreativer wird, als die Menschheit es derzeit ist.

### Beschreibung der Zusammenarbeit

Für diese Beschreibung wechsle ich nun bewusst zur Ich-Form: 

Rene und ich sind schon seit Ewigkeiten Schulfreunde und haben uns gegenseitig immer wieder Inspiration gegeben, mit unseren Interessen weiterzumachen, nicht auf die zu hören, die zweifeln und Dinge sagen wie “Das wird eh nix!”. Gemeinsam haben wir uns die verrücktesten Ideen ausgedacht und nun als Abschluss unserer Ausbildung ein Projekt in diesem Maß auszuführen, hat uns sehr, sehr gefreut. 

Wir haben die Arbeit aufgeteilt in unsere klaren Stärken und Schwächen und haben uns gegenseitig perfekt ausgeglichen. Es war überhaupt keine Schande zu sagen, dass man ansteht, oder mehr Zeit oder Hilfe braucht. Es herrschte immer gegenseitiger Respekt und Wertschätzung, dafür bin ich meinem Projektpartner sehr dankbar. 

Ich schätze seine Fähigkeiten sehr wert und da ich als Koordinator eher der bin, der schreibt und kommuniziert, bin ich geehrt, dass ich seinen Ideen etwas Leben einhauchen darf.