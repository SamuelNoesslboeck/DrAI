# Jugend Innovativ

## Infos

[Link](https://www.jugendinnovativ.at/teilnahme/wettbewerb)
Deadline: 30/11/2023

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
- [ ] Beschreibung einreichen   (bis 30/01/2024)

## Beschreibungen

Komplexere Beschreibungen für den Wettbewerb.

### Kurzbeschreibung der Zielsetzung

Ziel dieses Projekts ist es, die Fähigkeiten von KI bei der Erledigung "kreativer" Aufgaben in Zusammenarbeit mit Menschen zu demonstrieren. Der Roboter ist außerdem als Ausstellungsstück für das Machine Learning Studio des Ars Electronica Center Museums geplant.

Das Endergebnis wird ein interaktiver Roboter sein, der mit einer KI ausgestattet ist, die darauf trainiert ist, vorgezeichnete Skizzen des Benutzers zu interpretieren und sie mit ihrer eigenen "Kreativität" zu vervollständigen. Sobald sich das Blatt im Roboter befindet, ist es sein Ziel, sein Potenzial zu entfalten, indem er zusätzliche Linien auf das Papier des Benutzers zeichnet. Die Möglichkeiten sind hier grenzenlos, die KI kann z. B. einen Wald neben einem Häuschen erschaffen, oder einen Strand neben ein Meer und so weiter.

### Kurzbeschreibung des Vorhabens

Das Projekt beinhaltet ein komplexes Netz aus verschiedensten Algorithmen geschrieben in Python und der eher neuen Systemsprache Rust.

Zuerst wird die exakte Platzierung des Papiers mit der Skizze mithilfe von einer Verschachtelung verschiedener Bildanalysemethoden, wie Canny-Edge-Detection, Harris-Corner-Detection usw., überprüft. So kann der Roboter trotz Ungenauigkeiten des Users beim Einführen des Papiers korrekt zeichnen. 
Die gezeichnete Skizze wird dann durch einen Clip-Interogator in einen Text-Prompt übertragen. Nun wird ein Large Language Model benutzt um der Zeichnung etwas hinzuzufügen. Hierbei ist Prompt Engeneering von nöten um den Output zu verbessern. Würden wir den neu generierten Prompt und das Originalbild durch eine Stable Diffusion Img2Img Pipeline laufen lassen würde zu wenig Kreativität im neuen Bild entstehen, da der Diffusion Algorithmus mit niedriger Strength keine neuen Ansätze generiert und mit zu hoher Strength das Originalbild verschwindet und etwas Unbrauchbares entsteht. Um dieses Problem zu umgehen werden zufällige Linien in das Originalbild gezeichnet. Durch diese simple Methode mit der Kombination der verschiedenen neuronalen Netzwerke und der restlichen komplexen Algorithmen, ist es möglich den Stable Diffusion Algorithmus Kreativität zu verleihen. Da der gesamte Algorithmus sehr leistungsaufwändig ist wurde das ganze Projekt auf die CPU / RAM und GPU / V-RAM diversifiziert und ausgelagert um optimale Leistung auf kostengünstiger Hardware zu ermöglichen.

Eine weiterer Aspekt ist die Steuerung des Roboters, die zu großen Teilen von uns in Rust angefertigt wurde, da es etwas vergleichbares in dieser Sprache noch nicht gibt. Rust hat uns durch ihre Eleganz, Sicherheit und überragende Performance überzeugt. Durch sie ist es möglich, die komplette Steuerung inklusive Bahnberechnungen auf einem simplen Raspberry Pi Einplatinencomputer laufen zu lassen. Da in einem Museum die Aufmerksamkeitsspanne der Besucher eher kurz ist, muss schnell gezeichnet werden. Was durch die robuste Konstruktion, die leistungsstarke Elektronik und die Software, die hochwertige Anlaufkurven für die Motoren berechnet, gewährleistet wird. 
