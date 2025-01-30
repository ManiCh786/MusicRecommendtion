Music Data Analytics Report 
 
Abstract 
The goal of this project is to design and implement a modular music data analytics system that processes 
datasets, performs statistical analysis, and computes similarity scores between music tracks and artists. 
The system aims to support a music recommendation engine by analyzing features like loudness, energy, 
and valence. Three modules are developed in this project, one for loading and parsing datasets, one for 
statistical analysis, and the third for computing similarity scores using multiple metrics. A graphical user 
interface (GUI) was built using Tkinter to facilitate user interaction. This report provides a detailed 
breakdown of the design, implementation, and the relationships between these modules. 
 
1. Introduction 
With the rapid growth of online music platforms, recommending music tailored to users' preferences is 
essential for user satisfaction. To achieve this, analyzing music datasets for key features and determining 
similarities between songs or artists is crucial. This project focuses on building a music data analytics 
system using python which: 
1. Loads and processes music datasets. 
2. Calculates statistical metrics (mean, standard deviation, etc.) for music features. 
3. Computes similarity between tracks or artists using five different metrics. 
4. Provides a user-friendly graphical interface to interact with the system. 
The system uses a modular design for better maintainability and scalability. Each task performed in this 
project is separately coded to easily make any changes in the future or to easily track errors if the 
program crashes. The report discusses the design decisions, pseudocode, and relationships between 
these modules. 
 
2. Problem Analysis 
Following are the challenges I faced while working on this project: 
• Data Handling: The provided is very complex and ungrouped. It contains different symbols or 
special characters which crashes the program 
• Statistical Analysis: Implementing statistical measures to derive meaningful insights from 
features such as loudness, energy, and tempo. 
• Similarity Computation: Designing robust methods to compute similarity between two items 
(tracks or artists) using multiple metrics given in the project report. 
• User Interaction: Making sure the GUI is efficient and make users comfortable using it. 
To address these challenges, a modular design was implemented, the modules of the project include 
• Load Dataset Module: Loading of the datasets (data and music_genres) and storing the data in 
two dictionaries. 
• Statistics Module: Calculates different statistics on the data including mean, mode,min,max to 
better understand the data. 
• Similarity Module: Implements five similarity metrics which gives results of the similarity based 
on user input. 
• Main Application: Provides GUI-based interaction. 
 
3. Design and Implementation 
3.1 Load Dataset Module 
The MusicDataProcessor class handles loading and processing data from two CSV files: 
• data.csv contains music features. 
• data_genres.csv contains genre information. 
Functionality: 
1. Load data into two dictionaries: 
o artist_music: Maps artists to their tracks and features. 
o music_features: Maps track IDs to genres and features. 
2. Handles special characters such as: 
o Quotes and commas within fields. 
o Missing or invalid values. 
Pseudocode: 
class MusicDataProcessor: 
    def load_genre_data(): 
        For each line in genre file: 
            Extract 'key' and 'genres'. 
            Store genres and features in a dictionary. 
 
    def load_music_data(): 
        For each line in music file: 
            Parse 'artists', 'name', 'features'. 
            Handle quoted text and commas. 
            Populate artist_music and music_features dictionaries. 
 Return artist_music ,music_features 
 
3.2 Statistics Module 
The FeatureStatistics class calculates statistical measures for music features such as loudness, tempo, 
and energy. It supports querying for the highest or lowest values of specific features . 
Implemented Metrics: 
• Mean: Average of all feature values. 
• Standard Deviation: Measure of variance in the feature values. 
• Mode: Most frequent feature value. 
• Min/Max: Extreme values for features. 
Pseudocode: 
class FeatureStatistics: 
    def calculate_statistics(): 
        For each feature: 
            Compute mean, variance, std_dev, min, max. 
            Use Counter(imported from collections library) to determine mode. 
 
    def query_best_feature(feature, criterion): 
        Identify entry with the highest or lowest value of the specified feature. 
 
3.3 Similarity Module 
The SimilarityMeasures class computes similarity scores using five different metrics: 
1. Euclidean Similarity:  
o Measures the distance between two feature vectors. 
o This measure calculates the linear distance between two points in the n-dimensional 
space. 
o  It is often used for continuous numerical data and is easy to understand and implement. 
2. Cosine Similarity:  
o Measures the cosine of the angle between two feature vectors. 
o This metric calculates the similarity between two vectors by considering their angle. 
o  It is often used for text data and is resistant to changes in the magnitude of the vectors. 
o It does not consider the relative importance of different features. 
3. Pearson Similarity:  
o This metric calculates the linear correlation between two variables. 
o  It is often used for continuous numerical data and considers the relative importance of 
different features.  
o It may not accurately reflect non-linear relationships. 
4. Jaccard Similarity:  
o This metric calculates the similarity between two sets by considering the size of their 
intersection and union.  
o It is often used for categorical data and is resistant to changes in the size of the sets. 
5. Manhattan Similarity:  
o Measures the sum of absolute differences. 
o This metric calculates the distance between two points by summing the absolute 
difference of the coordinates 
Before Implementing these metrics: 
1. Features are normalized using z-scores for fair comparison. 
2. Implemented in SimilarityMeasures with methods like euclidean_similarity and 
cosine_similarity. 
Best Metric for this project: 
According to this project, I think the Cosine Similarity is best similarity metric for this project because, 
Cosine Similarity looks at the direction of feature values, not their size. This is important because 
features in music datasets often differ greatly in their scale (e.g., loudness can range from -60 to 0, while 
energy is between 0 and 1). Features like energy or valence, although numerically distinct, may point in 
the same "direction" across tracks, making Cosine similarity ideal for determining their similarity without 
being affected by magnitude differences. 
 
 
Pseudocode: 
class SimilarityMeasures: 
    def euclidean_similarity(f1, f2): 
        Compute sqrt of sum of squared differences. 
        Return 1 / (1 + distance). 
 
    def cosine_similarity(f1, f2): 
        Compute dot product and magnitudes. 
        Return dot_product / (magnitude1 * magnitude2). 
 
    def pearson_similarity(f1, f2): 
        Compute numerator and denominator using sums and means. 
        Return normalized correlation. 
 
    def jaccard_similarity(f1, f2): 
        Compute intersection and union of keys. 
        Return ratio of intersection to union. 
 
    def manhattan_similarity(f1, f2): 
        Compute sum of absolute differences. 
        Return 1 / (1 + distance). 
3.4 Main Application 
The main application integrates all modules and provides a Tkinter-based GUI for user interaction. Users 
can: 
• Query statistical metrics (e.g., "Find artist with highest/lowest loudness"). 
• Compute similarity between artists or tracks using any selectable metrics. 
• Receive similarity outcomes with similarity value and corresponding prediction (e.g., "Highly 
Identical" or "Not Identical"). 
Key Features: 
User Inputs: Artist names, track IDs, similarity metrics. 
• Outputs: Computed statistics and similarity scores. 
• Error Handling: Handles invalid inputs gracefully. 
 
4. Relationships Between Modules 
The project follows a modular structure to promote maintainability, reliability and reusability: 
1. Load Dataset Module: Supplies cleaned data to other modules. 
2. Statistics Module: Analyzes the data to provide feature insights. 
3. Similarity Module: Uses processed data and computed statistics to calculate similarity scores. 
4. Main Application: Integrates all modules and serves as the user interface. 
This clear separation ensures each module has a single responsibility, making the system scalable and 
easier to debug. 
 
5. Reflection 
What Worked Well: 
• Successfully implemented robust data parsing and cleaning. 
• Successfully code multiple statistical functions 
• Provided multiple similarity measures to offer flexibility. 
• Developed an intuitive GUI to enhance usability. 
Challenges: 
• Handling edge cases (special characters) in CSV parsing. 
• Normalizing features to ensure fair comparison. 
Future Improvements: 
• Integrate persistence (e.g., a database) for storing data. 
• Use machine learning for more advanced recommendations. 
 
5. How to execute this application: 
To run this project simply extract this zip file. 
• Open any code editor e.g vscode 
• Navigate to main.py 
• Run it  
• The application GUI window will open and you can perform you desired task. 
 
6. Conclusion 
This project successfully delivers a modular music data analytics tool that processes datasets, analyzes 
music features, and computes similarity scores using various metrics. The system demonstrates how 
effective data handling, statistical analysis, and user interaction can address real-world challenges in 
music recommendation systems. Future enhancements can further improve its scalability and 
functionality. 
 
