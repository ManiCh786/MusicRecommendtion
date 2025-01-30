import math
from statistical_functions import FeatureStatistics
class SimilarityMeasures:
    @staticmethod
    def euclidean_similarity(features1, features2):
        #formula to calculate euclidean similarity
        distance = math.sqrt(sum((features1[feature] - features2[feature]) ** 2
                                 for feature in features1 if feature in features2)) #sum of all common features
        return 1 / (1 + distance)  # Convert to similarity score , smaller distance means higher similarity

    @staticmethod
    def cosine_similarity(features1, features2):
       
        dot_product = sum(features1[feature] * features2[feature]
                          for feature in features1 if feature in features2)
        magnitude1 = math.sqrt(sum(value ** 2 for value in features1.values()))
        magnitude2 = math.sqrt(sum(value ** 2 for value in features2.values()))
        if magnitude1 == 0 or magnitude2 == 0:
            return 0  # Avoid division by zero
        return dot_product / (magnitude1 * magnitude2)

    @staticmethod
    def pearson_similarity(features1, features2):
        
        common_features = [feature for feature in features1 if feature in features2]
        n = len(common_features)
        if n == 0:
            return 0  # No common features
        # Sum of values for each feature in both sets
        sum1 = sum(features1[f] for f in common_features)
        sum2 = sum(features2[f] for f in common_features)
           # Sum of squared values for each feature in both sets
        sum1_sq = sum(features1[f] ** 2 for f in common_features)
        sum2_sq = sum(features2[f] ** 2 for f in common_features)
           # Sum of douct for feature 
        product_sum = sum(features1[f] * features2[f] for f in common_features)

        numerator = product_sum - (sum1 * sum2 / n)
        denominator = math.sqrt((sum1_sq - (sum1 ** 2 / n)) * (sum2_sq - (sum2 ** 2 / n)))
        if denominator == 0:
            return 0
        return numerator / denominator

    @staticmethod
    def jaccard_similarity(features1, features2):
      
        set1 = set(features1.keys())
        set2 = set(features2.keys())
        intersection = len(set1 & set2)
        union = len(set1 | set2)
        if union == 0:
            return 0
        return intersection / union

    @staticmethod
    def manhattan_similarity(features1, features2):
       
        distance = sum(abs(features1[feature] - features2[feature])
                       for feature in features1 if feature in features2)
        return 1 / (1 + distance)  # Convert to similarity score

# Function to compute similarity using selected metric
    def compute_similarity(data, id1, id2, similarity_function, stats=None):
       
        if id1 not in data :
            raise ValueError(f"Artist Name {id1} not found in the dataset.")
        elif id2 not in data:
            raise ValueError("Artist Name {id2} not found in the dataset.")

        features1 = data[id1][0]["features"]  # Retrieve the features for the first ID
        features2 = data[id2][0]["features"]  # Retrieve the features for the second ID

        # Normalize features if stats are provided
        if stats:
            features1 = FeatureStatistics.normalize_features(features1, stats)
            features2 = FeatureStatistics.normalize_features(features2, stats)

        return similarity_function(features1, features2)
