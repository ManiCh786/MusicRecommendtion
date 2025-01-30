import tkinter as tk
from tkinter import messagebox
from load_data_set import MusicDataProcessor
from statistical_functions import FeatureStatistics
from similarity_module import SimilarityMeasures

# Function to determine similarity outcome based on the score
def similarity_outcome(similarity):
    if similarity == 1:
        return "Highly Identical"
    elif 0.8 <= similarity < 1:
        return "Very Similar"
    elif 0.6 <= similarity < 0.8:
        return "Moderately Identical"
    elif 0.4 <= similarity < 0.6:
        return "Slightly Identical"
    elif 0 < similarity < 0.4:
        return "Not Identical"
    else:
        return "Completely Dissimilar"

class MusicAnalyticsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Data Analytics Tool")
        self.root.geometry("1000x700")

        # Load datasets
        self.processor = MusicDataProcessor('dataset/data.csv', 'dataset/data_genres.csv')
        self.processor.load_data()

        self.music_features = self.processor.get_music_features()
        self.artist_music = self.processor.get_artist_music()

        # Create the main menu buttons
        self.create_main_menu()

    def create_main_menu(self):
        # Title label
        self.title_label = tk.Label(self.root, text="Welcome to the Music Data Analytics Tool!", font=("Arial", 16))
        self.title_label.pack(pady=20)

        # Main Menu Buttons
        self.query_button = tk.Button(self.root, text="Query Statistics", width=20, command=self.query_statistics)
        self.query_button.pack(pady=10)

        self.similarity_button = tk.Button(self.root, text="Compute Similarity Between Artists", width=30, command=self.compute_similarity_artists)
        self.similarity_button.pack(pady=10)

        self.track_similarity_button = tk.Button(self.root, text="Compute Similarity Between Tracks", width=30, command=self.compute_similarity_tracks)
        self.track_similarity_button.pack(pady=10)

        self.exit_button = tk.Button(self.root, text="Exit", width=20, command=self.root.quit)
        self.exit_button.pack(pady=20)

    def query_statistics(self):
        stat_window = tk.Toplevel(self.root)
        stat_window.title("Query Statistics")
        stat_window.geometry("600x400")

        tk.Label(stat_window, text="1. Find artist with highest/lowest feature").pack(pady=10)
        tk.Label(stat_window, text="2. Find music track with highest/lowest feature").pack(pady=10)

        stat_choice = tk.StringVar()
        stat_choice.set("1")  # Default choice
        tk.Radiobutton(stat_window, text="Artist Statistics", variable=stat_choice, value="1").pack(pady=5)
        tk.Radiobutton(stat_window, text="Track Statistics", variable=stat_choice, value="2").pack(pady=5)

        tk.Label(stat_window, text="Enter feature (e.g., loudness, energy): ").pack(pady=10)
        feature_entry = tk.Entry(stat_window)
        feature_entry.pack(pady=10)

        tk.Label(stat_window, text="Enter 'highest' or 'lowest': ").pack(pady=10)
        query_type_entry = tk.Entry(stat_window)
        query_type_entry.pack(pady=10)

        def perform_query():
            
            feature = feature_entry.get().strip()
            query_type = query_type_entry.get().strip().lower()
            choice = stat_choice.get()

            if feature and query_type:
                if choice == "1":
                    feature_obj = FeatureStatistics(self.artist_music)
                    result = feature_obj.query_best_feature(feature, query_type)
                    messagebox.showinfo("Query Result", f"Result: {result}")
                elif choice == "2":
                    feature_obj = FeatureStatistics(self.music_features)
                    result = feature_obj.query_best_feature(feature, query_type)
                    messagebox.showinfo("Query Result", f"Result: {result}")
            else:
                messagebox.showerror("Error", "Please fill in all fields.")

        perform_button = tk.Button(stat_window, text="Get Result", command=perform_query)
        perform_button.pack(pady=20)

    def compute_similarity_artists(self):
        similarity_window = tk.Toplevel(self.root)
        similarity_window.title("Compute Similarity Between Artists")
        similarity_window.geometry("600x400")

        tk.Label(similarity_window, text="Enter the first artist Name: ").pack(pady=10)
        self.artist1_entry = tk.Entry(similarity_window)
        self.artist1_entry.pack(pady=10)

        tk.Label(similarity_window, text="Enter the second artist Name: ").pack(pady=10)
        self.artist2_entry = tk.Entry(similarity_window)
        self.artist2_entry.pack(pady=10)

        tk.Label(similarity_window, text="Choose similarity metric: ").pack(pady=10)
        self.metric_choice = tk.StringVar()
        metric_options = ["Euclidean", "Cosine", "Pearson", "Jaccard", "Manhattan"]
        self.metric_menu = tk.OptionMenu(similarity_window, self.metric_choice, *metric_options)
        self.metric_menu.pack(pady=10)

        self.compute_button = tk.Button(similarity_window, text="Compute Similarity", command=self.compute_similarity_result_artists)
        self.compute_button.pack(pady=20)

    def compute_similarity_result_artists(self):
        artist1 = self.artist1_entry.get().strip()
        artist2 = self.artist2_entry.get().strip()
        metric = self.metric_choice.get()

        if artist1 and artist2 and metric:
            similarity_function = {
                "Euclidean": SimilarityMeasures.euclidean_similarity,
                "Cosine": SimilarityMeasures.cosine_similarity,
                "Pearson": SimilarityMeasures.pearson_similarity,
                "Jaccard": SimilarityMeasures.jaccard_similarity,
                "Manhattan": SimilarityMeasures.manhattan_similarity,
            }.get(metric)

            if not similarity_function:
                messagebox.showerror("Error", "Invalid similarity metric.")
                return

            try:
                similarity = SimilarityMeasures.compute_similarity(self.artist_music, artist1, artist2, similarity_function)
                result = similarity_outcome(similarity)
                messagebox.showinfo("Similarity Result", f"Similarity: {similarity:.4f}\nOutcome: {result}")
            except ValueError as e:
                messagebox.showerror("Error", f"Error: {e}")
        else:
            messagebox.showerror("Error", "Please fill in all fields.")

    def compute_similarity_tracks(self):
        similarity_window = tk.Toplevel(self.root)
        similarity_window.title("Compute Similarity Between Music Tracks")
        similarity_window.geometry("600x400")

        tk.Label(similarity_window, text="Enter the first track ID: ").pack(pady=10)
        self.track_id1_entry = tk.Entry(similarity_window)
        self.track_id1_entry.pack(pady=10)

        tk.Label(similarity_window, text="Enter the second track ID: ").pack(pady=10)
        self.track_id2_entry = tk.Entry(similarity_window)
        self.track_id2_entry.pack(pady=10)

        tk.Label(similarity_window, text="Choose similarity metric: ").pack(pady=10)
        self.track_metric_choice = tk.StringVar()
        track_metric_options = ["Euclidean", "Cosine", "Pearson", "Jaccard", "Manhattan"]
        self.track_metric_menu = tk.OptionMenu(similarity_window, self.track_metric_choice, *track_metric_options)
        self.track_metric_menu.pack(pady=10)

        self.track_compute_button = tk.Button(similarity_window, text="Compute Similarity", command=self.compute_similarity_result_tracks)
        self.track_compute_button.pack(pady=20)

    def compute_similarity_result_tracks(self):
        track_id1 = self.track_id1_entry.get().strip()
        track_id2 = self.track_id2_entry.get().strip()
        metric = self.track_metric_choice.get()

        if track_id1 and track_id2 and metric:
            similarity_function = {
                "Euclidean": SimilarityMeasures.euclidean_similarity,
                "Cosine": SimilarityMeasures.cosine_similarity,
                "Pearson": SimilarityMeasures.pearson_similarity,
                "Jaccard": SimilarityMeasures.jaccard_similarity,
                "Manhattan": SimilarityMeasures.manhattan_similarity,
            }.get(metric)

            if not similarity_function:
                messagebox.showerror("Error", "Invalid similarity metric.")
                return

            try:
                similarity = SimilarityMeasures.compute_similarity(self.music_features, track_id1, track_id2, similarity_function)
                result = similarity_outcome(similarity)
                messagebox.showinfo("Similarity Result", f"Similarity: {similarity:.4f}\nOutcome: {result}")
            except ValueError as e:
                messagebox.showerror("Error", f"Error: {e}")
        else:
            messagebox.showerror("Error", "Please fill in all fields.")

if __name__ == "__main__":
    root = tk.Tk()
    app = MusicAnalyticsApp(root)
    root.mainloop()
