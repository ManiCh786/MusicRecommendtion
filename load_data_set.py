from tabulate import tabulate


class MusicDataProcessor: # music data processor class to load data from data set and save data in dictionaries
    def __init__(self, file_path, genre_file_path): #initializer 
        self.file_path = file_path #artist music data set path
        self.genre_file_path = genre_file_path #genre data set path
        self.artist_music = {} #empty dictionaries to store data
        self.music_features = {}

    def load_genre_data(self): #load genre data function to retrieve genre data from genres dataset
        genre_data = {} #empty dictionary

        with open(self.genre_file_path, 'r', encoding='utf-8') as genre_file: #opening the file in read mode
            header = genre_file.readline().strip().split(',') #reading  the file data by spliting using , and strip function to cut unsual spaces from the data
            columns = {col: idx for idx, col in enumerate(header)} #enumerate builtin function to map each column name to its index

            # Process each row in the genre file
            for line in genre_file:
                values = line.strip().split(',')
                track_key = values[columns["key"]].strip()  # remove spaces from key using strip function 

                #handling exception if  no genres column found return Unknown else assign the genre name 
                genre_name = values[columns["genres"]].strip() if "genres" in columns else "Unknown"
                
                # Function to safely convert value to float, with a default value 0.0 if conversion fails in case if we get a string in the data this will tackle
                def safe_float(value, default=0.0):
                    try:
                        return float(value)
                    except ValueError:
                        return default
                    #storing features in a dictionary
                features = {
                    "acousticness": safe_float(values[columns["acousticness"]]),
                    "danceability": safe_float(values[columns["danceability"]]),
                    "duration_ms": safe_float(values[columns["duration_ms"]]),
                    "energy": safe_float(values[columns["energy"]]),
                    "instrumentalness": safe_float(values[columns["instrumentalness"]]),
                    "liveness": safe_float(values[columns["liveness"]]),
                    "loudness": safe_float(values[columns["loudness"]]),
                    "speechiness": safe_float(values[columns["speechiness"]]),
                    "tempo": safe_float(values[columns["tempo"]]),
                    "valence": safe_float(values[columns["valence"]]),
                    "popularity": safe_float(values[columns["popularity"]]),
                }

                # If the track key is already in genre_data, append the genre and its features
                #this is for storing multiple genres against single Id because one song can have multiple genres
                if track_key in genre_data:
                    genre_data[track_key].append({"genre_name": genre_name, "features": features})
                #else store genre name and features in genre daa
                else:
                    genre_data[track_key] = [{"genre_name": genre_name, "features": features}]
        
        return genre_data
    #load aritst music data
    def load_music_data(self, genre_data):
        with open(self.file_path, 'r', encoding='utf-8') as file:
            # Read the header line and strip(removes spaces or tabs) and split with ,
            header = file.readline().strip().split(',')

            columns = {
                "artists": header.index("artists"),
                "name": header.index("name"),
                "id": header.index("id"),
                "key": header.index("key"),
                "valence": header.index("valence"),
                "acousticness": header.index("acousticness"),
                "danceability": header.index("danceability"),
                "energy": header.index("energy"),
                "liveness": header.index("liveness"),
                "loudness": header.index("loudness"),
                "popularity": header.index("popularity"),
                "speechiness": header.index("speechiness"),
                "tempo": header.index("tempo"),
            }

            # Process each line in the music data file
            for line in file:
                # Split line into values, accounting for potential commas inside quotes
                #this code is to split text with commas without giving any harm to data 
                #for example if a , is inside "" it means it is the part of the data and if outside "" it means another values is started
                values = []
                current = ""
                in_quotes = False
                for char in line:
                    if char == '"' and not in_quotes: #in_quotes tracks whether we are in quotes string
                        in_quotes = True #we are in ""
                    elif char == '"' and in_quotes:
                        in_quotes = False #again " means we exited the quotes
                    elif char == ',' and not in_quotes: # if it comma and outside the ""
                        values.append(current.strip()) #append the value in th the values list 
                        current = ""
                    else:
                        current += char #iterates the characters
                values.append(current.strip())  # Add the last value
              
                # Parse the artists column
                raw_artists = values[columns["artists"]]
                artists = raw_artists.strip('[]"').split("', '")#split artist column
                # Parse other fields
                track_name = values[columns["name"]]
                track_id = values[columns["id"]]
                track_key = values[columns["key"]].strip() 

                try:
                    # Parse features
                    features = {
                        "valence": float(values[columns["valence"]].strip()),
                        "acousticness": float(values[columns["acousticness"]].strip()),
                        "danceability": float(values[columns["danceability"]].strip()),
                        "energy": float(values[columns["energy"]].strip()),
                        "liveness": float(values[columns["liveness"]].strip()),
                        "loudness": float(values[columns["loudness"]].strip()),
                        "popularity": int(values[columns["popularity"]].strip()),
                        "speechiness": float(values[columns["speechiness"]].strip()),
                        "tempo": float(values[columns["tempo"]].strip()),
                    }
                except ValueError as e:
                    # Skip rows with invalid numeric data
                    print(f"Error parsing features for track ID {track_id}: {e}")
                    continue

                # Populate artist_music dictionary
                for artist in artists:
                    normalized_artist = artist.strip("'\" ").strip()  # Ensure all unnecessary characters are removed because it causes the error
                    if normalized_artist not in self.artist_music:
                        self.artist_music[normalized_artist] = []
                    self.artist_music[normalized_artist].append({
                        "name": track_name,
                        "id": track_id,
                        "features": features,
                    })

                # Store each genre with its own features in music_features
                if track_key and track_key in genre_data:
                    genre_entries = genre_data[track_key]
                    self.music_features[track_id] = []  # Initialize an empty list for this track_id

                    # Append each genre with its respective features
                    for genre_entry in genre_entries:
                        self.music_features[track_id].append({
                            "genre_name": genre_entry["genre_name"],
                            
                            "features": genre_entry["features"]
                        })

    def load_data(self):
        # Load the genre data and music data
        genre_data = self.load_genre_data()
        self.load_music_data(genre_data)

    def get_music_features(self):
        return self.music_features

    def get_artist_music(self):
        return self.artist_music

