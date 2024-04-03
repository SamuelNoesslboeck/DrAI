# [ARS PRIX U19](https://calls.ars.electronica.art/2024/u19/project/edit/9909/)

Status: *Project created*

Deadline: 

## TODO

- [x] Create Project
- [ ] Fill out project information
  - [x] Lebenslauf Samuel
  - [ ] Lebenslauf Rene
- [ ] Upload project images/details etc. (Till March 1)

## Descriptions

### Kurzbeschreibung der Arbeit

Ziel dieses Projekts ist es, die Fähigkeiten von KI bei der Erledigung "kreativer" Aufgaben in Zusammenarbeit mit Menschen zu demonstrieren und menschliche Kreativität nachzuahnen. Der Roboter ist außerdem als Teil von Workshops oder sogar der Ausstellung des ARS Electronica Centers geplant.

Das Endergebnis ist ein interaktiver Roboter sein, der mit einer KI ausgestattet ist, die darauf trainiert ist, vorgezeichnete Skizzen des Benutzers zu interpretieren und sie mit ihrer eigenen "Kreativität" zu vervollständigen. Sobald sich das Blatt im Roboter befindet, ist es sein Ziel, sein Potenzial zu entfalten, indem er zusätzliche Linien auf das Papier des Benutzers zeichnet. Die Möglichkeiten sind hier grenzenlos, die KI kann z. B. einen Wald neben einem Häuschen erschaffen, oder einen Strand neben ein Meer und so weiter.

### Technische Details der Arbeit

Das Projekt beinhaltet ein komplexes Netz aus verschiedensten Algorithmen geschrieben in Python und der eher neuen Systemsprache Rust.

Zuerst wird die exakte Platzierung des Papiers mit der Skizze mithilfe von einer Verschachtelung verschiedener Bildanalysemethoden, wie Canny-Edge-Detection, Harris-Corner-Detection usw., überprüft. So kann der Roboter trotz Ungenauigkeiten des Users beim Einführen des Papiers korrekt zeichnen. 
Die gezeichnete Skizze wird dann durch einen Clip-Interogator in einen Text-Prompt übertragen. Nun wird ein Large Language Model benutzt um der Zeichnung etwas hinzuzufügen. Hierbei ist Prompt Engeneering von nöten um den Output zu verbessern. Würden wir den neu generierten Prompt und das Originalbild durch eine Stable Diffusion Img2Img Pipeline laufen lassen würde zu wenig Kreativität im neuen Bild entstehen, da der Diffusion Algorithmus mit niedriger Strength keine neuen Ansätze generiert und mit zu hoher Strength das Originalbild verschwindet und etwas Unbrauchbares entsteht. Um dieses Problem zu umgehen werden zufällige Linien in das Originalbild gezeichnet. Durch diese simple Methode mit der Kombination der verschiedenen neuronalen Netzwerke und der restlichen komplexen Algorithmen, ist es möglich den Stable Diffusion Algorithmus Kreativität zu verleihen. Da der gesamte Algorithmus sehr leistungsaufwändig ist wurde das ganze Projekt auf die CPU / RAM und GPU / V-RAM diversifiziert und ausgelagert um optimale Leistung auf kostengünstiger Hardware zu ermöglichen.

Eine weiterer Aspekt ist die Steuerung des Roboters, die zu großen Teilen von uns in Rust angefertigt wurde, da es etwas vergleichbares in dieser Sprache noch nicht gibt. Rust hat uns durch ihre Eleganz, Sicherheit und überragende Performance überzeugt. Durch sie ist es möglich, die komplette Steuerung inklusive Bahnberechnungen auf einem simplen Raspberry Pi Einplatinencomputer laufen zu lassen. Da in einem Museum die Aufmerksamkeitsspanne der Besucher eher kurz ist, muss schnell gezeichnet werden. Was durch die robuste Konstruktion, die leistungsstarke Elektronik und die Software, die hochwertige Anlaufkurven für die Motoren berechnet, gewährleistet wird. 

### Projektgeschichte

Eine Internetrecherche in Zusammenarbeit mit dem Projektleiter ergab, dass es zwar schon Zeichenroboter gab, die auf gewisse Datensätze trainiert wurden, jedoch funktionierten diese nur auf kleine Datensätze oder Zeichnungen und wiesen nicht die benötigte gewünschte Vielfältigkeit und Kreativität auf. Auch waren viele der existierenden Konzepte nicht für den Museumsbetrieb geeignet.
Die anfängliche Idee des Projektes war, zu einer bestehenden Zeichnung etwas Kreatives hinzuzufügen und die Besucher*innen mit der KI kollaborieren zu lassen. Das Projekt sollte zur Demonstration von kreativer Zusammenarbeit von Künstlicher Intelligenz und Mensch dienen. 
Zu Beginn des Projektes existierte die Meinung, künstliche Intelligenz werde in den nächsten Jahren zu einem neuen Werkzeug für die Menschheit, wie die Erfindung des Taschenrechners. Bereits zu dieser Zeit existierten diverse Algorithmen, mit denen sich durch menschliches Einwirken Herausragendes entwickeln lässt. Durch Programme wie Github Copilot lassen sich komplexe Programme in beliebigen Programmiersprachen durch eine Textbeschreibung entwickeln. Oft genügt eine einfache Beschreibung des Lösungsansatzes und schon liefert ein Large Language Model (LLM) wie GPT-4 den Programmcode. Was jedoch hierbei wichtig ist, ist die Beschreibung des Lösungsansatzes. Neuronale Netzwerke sind nur so gut wie ihre Trainingsdaten. Befindet sich das Problem nicht in den Datensätzen, so fällt es dem Programm meist schwer, eine komplexe Lösung zu finden, die auch wirklich funktioniert. Hierbei wird die menschliche Kreativität benötigt, um einen Lösungsansatz zu finden, der dann beschrieben und in Code umgesetzt wird. 
Mit Bildern ist es das gleiche, es wird menschliche Kreativität benötigt, um kreative Textbeschreibungen für Bilder zu finden, die im Anschluss gezeichnet werden. Je weiter die Forschung des Algorithmus fortschritt, desto mehr festigte sich die Erkenntnis, dass diese These inkorrekt ist. Der Programmcode hat einerseits die Möglichkeit, aus Bestehendem etwas Neues zu erzeugen und andererseits aus einem weißen Blatt Papier ohne textliche Beschreibungen oder menschliches Einwirken kreative Bilder zu malen. Es ist eine philosophische Frage, ob Maschinen kreativ sein können oder nicht, jedoch sehen die Resultate sehr vielversprechend aus. Die Frage, ob KI kreativ sein kann, wird eher zur Frage, wann KI kreativer wird, als die Menschheit es derzeit ist.
Der zunächst beschriebene Algorithmus versucht die menschliche Kreativität nachzuahmen, indem er generative Künstliche Intelligenz mit zufällig in das Eingangsbild generierten Inhalten kombiniert. Die Innovation liegt in dieser Interpretation menschlicher Kreativität als genau dieser Kombination von zufälligen Impulsen in der menschlichen Wahrnehmung, abgebildet durch die Zufallsgeneratoren, und der Erkennung von Mustern, abgebildet durch KI.

### Kurzbiographie Samuel

Schon lange bastelt Samuel Nösslböck an den verschiedensten Projekten im Bereich der Robotik. Dabei glaubt er an die Relevanz der Kunst und Kreativität in der sonst sehr regulierten und genormten Technik. 

So entstand 2022 SyLa, eine für Netzwerkanwendungen optimierte Skriptsprache, 
Im Jahre 2023 SyArm, ein Roboterarm gebaut aus simplen Teilen und im Jahr darauf in Kooperation mit Rene Schwarz DrAI, ein intelligenter Zeichenroboter mit neuen Ansätzen zur Interpretation und Nachahmung von Kreativität.

### Kurzbiographie Rene

Rene Schwarz war von klein auf sehr technikbegeistert. Schon lange kannte er Samuel Nösslböck, welcher ihn überredete, die Programmiersprache Python zu lernen. Die Faszination für den Marvel-Charakter Ironman und dessen interaktives Sprachprogramm Jarvis, setzen den ersten Grundstein für die Begeisterung für KI.

Mit 15 Jahren entdeckte er Deep Learning. 3 Jahre später folgte die erste Gesichteserkennungs- und Identifikationssoftware Facevec. Im Jahre 2023 entwickelte er eine Rechenleistungsoptimierte Speech to Text Software und im Jahr darauf in Kooperation mit Samuel Nösslböck DrAI, ein intelligenter Zeichenroboter mit neuen Ansätzen zur Interpretation und Nachahmung von Kreativität.
