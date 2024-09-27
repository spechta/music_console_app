import json
import os
import random
import time
from tqdm import tqdm

class Song:
    def __init__(self, id, name, artist, album, views, duration):
        self.id = id  
        self.name = name
        self.artist = artist
        self.album = album
        self.views = views  
        self.duration = duration  

    def __str__(self):
        return f"Song: {self.name}, Artist: {self.artist}, Album: {self.album}, Views: {self.views}, Duration: {self.duration:.2f} minutes"

    def to_dict(self):
        return {
            "id": self.id, 
            "Track": self.name,  
            "Artist": self.artist,
            "Album": self.album,
            "Views": self.views,  
            "Duration_min": self.duration  
        }

    @staticmethod
    def from_dict(data):
        return Song(
            id=data.get("id", -1), 
            name=data["Track"],
            artist=data["Artist"],
            album=data["Album"],
            views=data["Views"],
            duration=data["Duration_min"]
        )

class Playlist:
    def __init__(self, name):
        self.name = name
        self.songs = []

    def add_song(self, song):
        self.songs.append(song)

    def __str__(self):
        song_list = '\n'.join([str(song) for song in self.songs])
        return f"Playlist: {self.name}\nSongs:\n{song_list}"

    def to_dict(self):
        return {
            "name": self.name,
            "songs": [song.to_dict() for song in self.songs]
        }

    @staticmethod
    def from_dict(data, all_songs):
        playlist = Playlist(data["name"])
        for song_data in data["songs"]:
            track_id = song_data["track_id"]
            song = next((s for s in all_songs if s.id == track_id), None)
            if song:
                playlist.add_song(song)
        return playlist

class MusicApp:
    def __init__(self, data_file):
        self.data_file = data_file
        self.songs = []
        self.playlists = []
        self.song_hash_maps = {}
        self.load_data()

    def load_data(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as file:
                    data = json.load(file)

                    # Load and assign IDs to songs if they don't exist
                    if 'songs' in data:
                        for index, song_data in enumerate(data['songs']):
                            if 'id' == -1:
                                song_data['id'] = index + 1  # Assign a unique ID starting from 1
                            self.songs.append(Song.from_dict(song_data))

                    # Load playlists if present
                    if 'playlists' in data:
                        for pl_data in data['playlists']:
                            playlist = Playlist.from_dict(pl_data, self.songs)
                            self.playlists.append(playlist)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
            except Exception as e:
                print(f"An error occurred: {e}")
        else:
            print(f"No existing data found in {self.data_file}.")

    def save_data(self):
        data = {
            "songs": [song.to_dict() for song in self.songs],
            "playlists": [playlist.to_dict() for playlist in self.playlists]
        }
        with open(self.data_file, 'w') as file:
            json.dump(data, file, indent=4)
        print(f"Data saved to {self.data_file}")

    def add_song(self):
        """
        Adds a new song to the music library.
        """
        name = input("Enter the song name: ")
        artist = input("Enter the artist name: ")
        album = input("Enter the album name: ")
        views = int(input("Enter the number of views: "))  
        duration = float(input("Enter the duration in minutes: "))  

        new_song = Song(len(self.songs) + 1, name, artist, album, views, duration)
        self.songs.append(new_song)
        print(f"Added {new_song}")

    def create_playlist(self):
        """
        Creates a new playlist
        """
        name = input("Enter the playlist name: ")
        playlist = Playlist(name)
        self.playlists.append(playlist)
        print(f"Created playlist: {playlist.name}")

    def add_song_to_playlist(self):
        playlist_name = input("Enter the name of the playlist: ")
        song_name = input("Enter the song name: ")

        # Find the playlist
        playlist = next((p for p in self.playlists if p.name == playlist_name), None)
        if playlist is None:
            print(f"Playlist '{playlist_name}' not found.")
            return  # Return if no playlist found

        # Find the song
        song = next((s for s in self.songs if s.name == song_name), None)
        if song is None:
            print(f"Song '{song_name}' not found.")
            return  # Return if no song found

        # Add song to playlist
        playlist.songs.append(song)
        print(f"Added {song_name} to playlist {playlist_name}.")
        return playlist  # Return the updated playlist


    def linear_search(self, search_term, attribute):
        """
        Searches for songs using linear search based on a specified attribute.
        """
        start_time = time.time()
        results = []
        for song in tqdm(self.songs, desc="Linear Searching", unit="song"):
            value = getattr(song, attribute)
            if isinstance(value, str):
                value = value.lower()  
                if search_term in value:
                    results.append(song)
            else:
                if search_term == str(value):  
                    results.append(song)
        end_time = time.time()
        print("\nSearch Results:")
        for song in results:
            print(song)
        print(f"\nLinear Search completed in {end_time - start_time:.4f} seconds.")
        return results
    
    def build_hash_maps(self):
        """
        Build hash maps for various attributes to speed up hash searches.
        """
        attributes = ['name', 'artist', 'views', 'duration']
        self.song_hash_maps = {attr: {} for attr in attributes}

        for song in self.songs:
            for attr in attributes:
                value = getattr(song, attr)
                if isinstance(value, str):
                    value = value.lower()  # Normalize case for string attributes
                if value not in self.song_hash_maps[attr]:
                    self.song_hash_maps[attr][value] = []
                self.song_hash_maps[attr][value].append(song)

    def hash_search(self, search_term, attribute):
        """
        Efficient search method using a pre-built hash map (dictionary).
        Supports multiple results and different types.
        """
        if attribute not in self.song_hash_maps:
            print(f"No hash map available for attribute '{attribute}'. Building hash maps...")
            self.build_hash_maps()
        
        search_term = search_term.lower() if isinstance(search_term, str) else search_term
        start_time = time.time()

        # Retrieve the results from the pre-built hash map
        results = self.song_hash_maps[attribute].get(search_term, [])
        
        end_time = time.time()
        print("\nSearch Results:")
        for song in results:
            print(song)
        print(f"\nHash Search (with pre-built map) completed in {end_time - start_time:.6f} seconds.")
        return results

    def lcg_search(self, search_term, attribute):
        """
        LCG Search using a pseudo-random walk through the song list to find multiple results
        """
        start_time = time.time()
        a = 1664525
        c = 1013904223
        m = 2**32
        seed = random.randint(0, len(self.songs) - 1)

        search_term = search_term.lower() if isinstance(search_term, str) else search_term
        results = []
        visited_indices = set()
        attempts = 0

        pbar = tqdm(total=len(self.songs), desc="LCG Searching", unit="attempt")
        while attempts < len(self.songs):
            index = seed % len(self.songs)
            if index not in visited_indices:
                song = self.songs[index]
                visited_indices.add(index)
                value = getattr(song, attribute)
                if isinstance(value, str):
                    value = value.lower()
                    if search_term in value:
                        results.append(song)
                elif search_term == str(value):
                    results.append(song)

            seed = (a * seed + c) % m
            attempts += 1
            pbar.update(1)

        pbar.close()
        end_time = time.time()
        print("\nSearch Results:")
        for song in results:
            print(song)
        print(f"\nLCG Search completed in {end_time - start_time:.4f} seconds.")
        return results

    def search_songs(self):
        """
        Allows users to search for songs based on selected algorithm and attribute.
        """
        print("\nChoose search algorithm:")
        print("1. Linear Search")
        print("2. Hash Search")
        print("3. LCG Search")

        algo_choice = input("Enter your choice (1/2/3): ").strip()

        if algo_choice not in ('1', '2', '3'):
            print("Invalid choice. Search cancelled.")
            return

        print("\nChoose search attribute:")
        print("1. Name")
        print("2. Artist")
        print("3. Views")
        print("4. Duration")

        attr_choice = input("Enter your choice (1/2/3/4): ").strip()
        attribute = "name" if attr_choice == '1' else "artist" if attr_choice == '2' else "views" if attr_choice == '3' else "duration" if attr_choice == '4' else None

        if attribute is None:
            print("Invalid choice. Search cancelled.")
            return

        search_term = input(f"Enter your search term for {attribute}: ").lower()

        if algo_choice == '1':
            results = self.linear_search(search_term, attribute)
        elif algo_choice == '2':
            results = self.hash_search(search_term, attribute)
        elif algo_choice == '3':
            results = self.lcg_search(search_term, attribute)
        return results  

    def built_in_sort(self, key):
        """
        Uses Python's built-in sort
        """
        start_time = time.time()
        self.songs.sort(key=lambda song: key(song))
        end_time = time.time()
        print("\nSorted Songs:")
        self.display_all_songs()
        print(f"\nBuilt-in Sort completed in {end_time - start_time:.4f} seconds.")

    def quicksort(self, arr, key=lambda x: x):
        """
        Quicksort algorithm 
        """
        start_time = time.time()
        pbar = tqdm(total=len(arr), desc="Quicksorting", unit="element")

        def quicksort_helper(arr, key):
            if len(arr) <= 1:
                return arr
            pivot = key(arr[len(arr) // 2])
            left = [x for x in arr if key(x) < pivot]
            middle = [x for x in arr if key(x) == pivot]
            right = [x for x in arr if key(x) > pivot]
            pbar.update(1)
            return quicksort_helper(left, key) + middle + quicksort_helper(right, key)

        sorted_songs = quicksort_helper(arr, key)
        pbar.close()
        end_time = time.time()
        print("\nSorted Songs:")
        self.display_all_songs()
        print(f"\nQuicksort completed in {end_time - start_time:.4f} seconds.")
        return sorted_songs

    def slowsort(self, arr, key=lambda x: x):
        """
        Slowsort algorithm 
        """
        start_time = time.time()
        n = len(arr)
        pbar = tqdm(total=n*(n-1)//2, desc="Slowsorting", unit="comparison")

        for i in range(n):
            for j in range(i + 1, n):
                if key(arr[i]) > key(arr[j]):
                    arr[i], arr[j] = arr[j], arr[i]
                pbar.update(1)

        pbar.close()
        end_time = time.time()
        print("\nSorted Songs:")
        self.display_all_songs()
        print(f"\nSlowsort completed in {end_time - start_time:.4f} seconds.")
        return arr

    def sort_songs(self):
        """
        Sorts songs based on selected algorithm and attribute
        """
        print("\nChoose sort algorithm:")
        print("1. Built-in Sort")
        print("2. Quicksort")
        print("3. Slowsort")

        algo_choice = input("Enter your choice (1/2/3): ").strip()

        if algo_choice not in ('1', '2', '3'):
            print("Invalid choice. Sort cancelled.")
            return

        print("\nChoose sort attribute:")
        print("1. Name")
        print("2. Artist")
        print("3. Views")
        print("4. Duration")

        attr_choice = input("Enter your choice (1/2/3/4): ").strip()
        attribute = None

        if attr_choice == '1':
            attribute = 'name'
        elif attr_choice == '2':
            attribute = 'artist'
        elif attr_choice == '3':
            attribute = 'views'
        elif attr_choice == '4':
            attribute = 'duration'

        if attribute is None:
            print("Invalid choice. Sort cancelled.")
            return

        # Sort using a custom key that handles type comparison
        def sort_key(song):
            value = getattr(song, attribute)
            return value if attribute == "views" or attribute == "duration" else str(value)

        if algo_choice == '1':
            self.built_in_sort(key=sort_key)
        elif algo_choice == '2':
            self.songs = self.quicksort(self.songs, key=sort_key)
        elif algo_choice == '3':
            self.songs = self.slowsort(self.songs, key=sort_key)


    def display_all_songs(self):
        """
        Displays all songs in the library
        """
        for song in self.songs:
            print(song)

    def display_playlists(self):
        """
        Displays all playlists and their contents
        """
        if self.playlists:
            for playlist in self.playlists:
                print(playlist)
        else:
            print("No playlists created.")

    def main_menu(self):
        while True:
            print("\n--- Music App ---")
            print("1. Add New Song")
            print("2. Create Playlist")
            print("3. Add Song to Playlist")
            print("4. Search Songs")
            print("5. Sort Songs")
            print("6. Display All Songs")
            print("7. Display Playlists")
            print("8. Save and Exit")

            choice = input("Enter your choice: ").strip()

            if choice == '1':
                self.add_song()
            elif choice == '2':
                self.create_playlist()
            elif choice == '3':
                self.add_song_to_playlist()
            elif choice == '4':
                self.search_songs()
            elif choice == '5':
                self.sort_songs()
            elif choice == '6':
                self.display_all_songs()
            elif choice == '7':
                self.display_playlists()
            elif choice == '8':
                self.save_data()
                print("Exiting the music app.")
                break
            else:
                print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    app = MusicApp(data_file='Web/spotify/spotify_songs.json')
    app.main_menu()
