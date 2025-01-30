from collections import Counter
class FeatureStatistics:
    def __init__(self, data):
      
        self.data = data
        
    def calculate_statistics(self):
       
        stats = {}
        
        all_features = [] #an empty list ti store features
        for key, items in self.data.items(): #looping the dictionary to get data
            for entry in items: #extracting values
            
                
                all_features.append(entry["features"]) #extracting feature inside the values and storing them into all_features list

        # Extract feature names from the first feature set
        feature_names = all_features[0].keys()

        # Compute statistics for each feature
        for feature in feature_names:
            values = [f[feature] for f in all_features if feature in f] #iterating through each feature i.e loudness,valence etc
            stats[feature] = {
                #formula to calculate mean,min,max,variance,std
                "mean": sum(values) / len(values),
                "min": min(values),
                "max": max(values),
                "variance": sum((x - (sum(values) / len(values))) ** 2 for x in values) / len(values),
                "std_dev": (sum((x - (sum(values) / len(values))) ** 2 for x in values) / len(values)) ** 0.5,
            }
      
            freq = Counter(values)  # Count the frequency of each value
            mode_data = freq.most_common()  # Get a list of value, frequency

            mode = mode_data[0][0]  # The first item in the list will be the most frequent value

            # Store the mode in the stats dictionary
            stats[feature]["mode"] = mode
        return stats
    
    #z-square normalization to ensure each featues equally contributes in similarity calculation 
    @staticmethod
    def normalize_features(features, stats):
     
        normalized = {}
        for feature, value in features.items():
            if feature in stats:
                mean = stats[feature]["mean"]
                std_dev = stats[feature]["std_dev"]
                if std_dev > 0:  # Avoid division by zero
                    normalized[feature] = (value - mean) / std_dev
                else:
                    normalized[feature] = 0  # If std_dev is 0, the feature has no variance
        return normalized

    def query_best_feature(self, feature, criterion):
       
        best_entry = None
        best_value = None

        for key, items in self.data.items(): # iterate through data
            for entry in items: #iterate through values
                features = entry["features"] #extract features
                if feature in features: #if feature(arg) is in features list
                    value = features[feature]
                    # if the current value is better based on the specified criterion (highest or lowest)
                    if best_value is None or (criterion == "highest" and value > best_value) or ( 
                            criterion == "lowest" and value < best_value):
                        best_entry = {"key": key, "entry": entry}
                        best_value = value

        return best_entry
