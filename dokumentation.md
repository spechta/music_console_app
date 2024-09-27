Musik-App Dokumentation
1: Einleitung
Übersicht
Diese Dokumentation beschreibt die Implementierung und Nutzung einer Musik-Anwendung, die es ermöglicht, eine Musikbibliothek zu verwalten, Playlists zu erstellen und Songs basierend auf verschiedenen Attributen und Suchalgorithmen zu durchsuchen. Diese Anwendung bietet zudem Sortiermöglichkeiten und unterstützt die Speicherung und Wiederherstellung der Daten aus einer JSON-Datei.

Funktionen der Anwendung:
Hinzufügen von neuen Songs: Der Benutzer kann neue Songs zur Bibliothek hinzufügen.
Playlist erstellen: Der Benutzer kann Playlists erstellen und verwalten.
Song zu einer Playlist hinzufügen: Vorhandene Songs können Playlists hinzugefügt werden.
Songs durchsuchen: Verschiedene Suchalgorithmen (Lineare Suche, Hash-Suche, LCG-Suche) können verwendet werden, um Songs anhand ihrer Attribute zu finden.
Songs sortieren: Verschiedene Sortieralgorithmen (Python Built-in Sort, Quicksort, Slowsort) stehen zur Verfügung.
Anzeige der Songs und Playlists: Alle Songs und Playlists können angezeigt werden.
Speichern und Laden der Daten: Die Daten können gespeichert und wieder geladen werden.
Aufbau der Dokumentation:
Einleitung

Überblick und Ziel der Anwendung
Hauptfunktionen der Anwendung
Klassenstruktur

Song-Klasse
Playlist-Klasse
MusicApp-Klasse
Suchfunktionen

Lineare Suche
Hash-Suche
LCG-Suche
Sortierfunktionen

Python Built-in Sort
Quicksort
Slowsort
Hauptmenü und Benutzerführung

Funktionsweise des Hauptmenüs
Anwendungsablauf
Seite 2: Klassenstruktur
1. Song-Klasse
Die Song-Klasse ist die grundlegende Einheit der Musikbibliothek und stellt einen Song mit verschiedenen Attributen dar. Diese Attribute umfassen:

id: Einzigartige Identifikationsnummer des Songs.
name: Name des Songs.
artist: Künstler des Songs.
album: Album, in dem der Song enthalten ist.
views: Anzahl der Aufrufe des Songs.
duration: Dauer des Songs in Minuten.
Methoden der Song-Klasse:

__str__: Gibt eine formatierte Zeichenkette des Songs zurück.
to_dict: Konvertiert die Song-Attribute in ein Dictionary-Format.
from_dict: Statische Methode zum Erstellen eines Song-Objekts aus einem Dictionary.
2. Playlist-Klasse
Die Playlist-Klasse repräsentiert eine Sammlung von Songs. Sie enthält:

name: Der Name der Playlist.
songs: Eine Liste von Song-Objekten.
Methoden der Playlist-Klasse:

add_song: Fügt einen Song zur Playlist hinzu.
__str__: Gibt eine formatierte Zeichenkette der Playlist und ihrer Songs zurück.
to_dict: Konvertiert die Playlist-Attribute in ein Dictionary-Format.
from_dict: Statische Methode zum Erstellen eines Playlist-Objekts aus einem Dictionary.
3. MusicApp-Klasse
Die MusicApp-Klasse ist das Herzstück der Anwendung und verwaltet die gesamte Musikbibliothek sowie Playlists. Sie enthält die Methoden zum Hinzufügen, Suchen, Sortieren und Verwalten der Songs und Playlists.

Wichtige Methoden:

load_data: Lädt vorhandene Daten aus einer JSON-Datei.
save_data: Speichert die aktuelle Datenstruktur in eine JSON-Datei.
add_song: Fügt der Bibliothek einen neuen Song hinzu.
create_playlist: Erstellt eine neue Playlist.
add_song_to_playlist: Fügt einen Song zu einer bestehenden Playlist hinzu.
search_songs: Ermöglicht die Auswahl des Suchalgorithmus und die Durchführung der Suche.
sort_songs: Ermöglicht die Auswahl des Sortieralgorithmus und die Durchführung der Sortierung.
display_all_songs: Zeigt alle Songs der Bibliothek an.
display_playlists: Zeigt alle Playlists und deren Inhalt an.
main_menu: Stellt das Hauptmenü der Anwendung dar und ermöglicht die Benutzerführung.
Seite 3: Suchfunktionen
1. Lineare Suche
Die Lineare Suche durchsucht die Song-Liste der Reihe nach, um alle Songs zu finden, die einem bestimmten Suchkriterium entsprechen. Diese Methode ist einfach zu implementieren, kann aber bei großen Listen langsam sein.

Methode:

python
Code kopieren
def linear_search(self, search_term, attribute):
Parameter:

search_term: Der Suchbegriff (String oder numerischer Wert).
attribute: Das Attribut des Songs, nach dem gesucht wird (z.B. name, artist).
2. Hash-Suche
Die Hash-Suche verwendet vorbereitete Hash-Maps, um die Suche effizienter zu gestalten. Diese Methode bietet eine deutlich schnellere Suchgeschwindigkeit, besonders bei großen Datenmengen.

Methode:

python
Code kopieren
def hash_search(self, search_term, attribute):
Parameter:

search_term: Der Suchbegriff (String oder numerischer Wert).
attribute: Das Attribut des Songs, nach dem gesucht wird (z.B. name, artist).
3. LCG-Suche (Linear Congruential Generator)
Die LCG-Suche basiert auf einem Pseudo-Zufallsgenerator, der die Song-Liste auf eine zufällige, aber reproduzierbare Weise durchläuft. Diese Methode kann nützlich sein, um schnell eine Auswahl aus der gesamten Liste zu treffen.

Methode:

python
Code kopieren
def lcg_search(self, search_term, attribute):
Parameter:

search_term: Der Suchbegriff (String oder numerischer Wert).
attribute: Das Attribut des Songs, nach dem gesucht wird (z.B. name, artist).
Seite 4: Sortierfunktionen
1. Built-in Sort
Der eingebaute Sortieralgorithmus von Python wird verwendet, um die Songs basierend auf einem gegebenen Attribut zu sortieren.

Methode:

python
Code kopieren
def built_in_sort(self, key):
Parameter:

key: Eine Funktion, die angibt, wie die Songs verglichen werden sollen (z.B. song.name).
2. Quicksort
Quicksort ist ein effizienter, vergleichsbasierter Sortieralgorithmus, der die Liste rekursiv aufteilt, um die Songs zu sortieren.

Methode:

python
Code kopieren
def quicksort(self, arr, key=lambda x: x):
Parameter:

arr: Die Liste der Songs, die sortiert werden soll.
key: Eine Funktion, die angibt, wie die Songs verglichen werden sollen.
3. Slowsort
Slowsort ist ein ineffizienter Sortieralgorithmus, der für Vergleichszwecke verwendet wird, um die Performanceunterschiede mit effizienteren Algorithmen zu zeigen.

Methode:

python
Code kopieren
def slowsort(self, arr, key=lambda x: x):
Parameter:

arr: Die Liste der Songs, die sortiert werden soll.
key: Eine Funktion, die angibt, wie die Songs verglichen werden sollen.
Seite 5: Hauptmenü und Benutzerführung
Die main_menu-Methode steuert den Ablauf der Anwendung und stellt das Hauptmenü dar, in dem der Benutzer zwischen verschiedenen Aktionen wählen kann.

Hauptmenü-Optionen:
Neuen Song hinzufügen
Playlist erstellen
Song zu einer Playlist hinzufügen
Songs durchsuchen
Songs sortieren
Alle Songs anzeigen
Playlists anzeigen
Speichern und Beenden
Anwendungsablauf
Der Benutzer kann durch die Auswahl im Menü verschiedene Funktionen der Anwendung aufrufen. Die ausgewählten Aktionen werden in der main_menu-Schleife ausgeführt, bis der Benutzer die Option „Speichern und Beenden“ auswählt, um die Daten zu speichern und die Anwendung zu schließen.
