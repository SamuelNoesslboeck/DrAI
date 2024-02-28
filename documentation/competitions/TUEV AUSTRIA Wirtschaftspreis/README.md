# [TUEV AUSTRIA Wirtschaftspreis](https://www.tuv.at/wipreis/)

## TODO

- [ ] Einreichen (bis 31/06/2024)

## Daten

### Motivation

Unsere Motivation war es, einen Roboter ausgestattet mit einer moderen KI Technologie zu bauen, der demonstriert, wie KI in "kreativen" Aufgaben 
mit dem Menschen kollaborieren kann.

### Hauptbeschreibung

Das Endergebnis wird ein interaktiver Roboter sein, der mit einer KI ausgestattet ist, die darauf trainiert ist, vorgezeichnete Skizzen des Benutzers zu interpretieren und sie mit ihrer eigenen "Kreativität" zu vervollständigen.  
Um diesen Prozess zu starten, muss der Benutzer eine Skizze auf ein Blatt Papier zeichnen, das dann in den Roboter transportiert wird. Sobald sich das Blatt im Roboter befindet, ist es sein Ziel, sein Potenzial zu entfalten, indem er zusätzliche Linien auf das Papier des Benutzers zeichnet. Die Möglichkeiten sind hier grenzenlos, die KI kann z. B. einen Wald neben einem Häuschen erschaffen, oder einen Strand neben ein Meer und so weiter.

Das Projekt lässt sich in die beiden Hauptteile KI (oder allgemeiner Software) und Roboter (Hardware) aufteilen:

Zunächst muss die Software das Blatt mit einer am Gerät montierten Digitalkamera lokalisieren und ein Foto davon machen. Dann werden alle vom Benutzer gezeichneten Linien erkannt und interpretiert. Je weniger Linien der Benutzer gezeichnet hat, desto "kreativer" kann die KI sein. Alle erzeugten, zusammengefügten Linien werden dann an den Roboter übertragen.

Die Software gibt das aufgenommene Bild zunächst in einen Vision-Transformer, der eine Beschreibung dafür erstellt, die dann von einem "stable diffusion" verwendet wird, um ein farbiges RGB-Bild zu erzeugen. Aus diesem Bild extrahiert ein weiterer Algorithmus die Kanten und fügt sie mit dem Originalbild zusammen.