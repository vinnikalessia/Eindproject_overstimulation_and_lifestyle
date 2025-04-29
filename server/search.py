import pandas as pd
import numpy as np

class Search():
    def __init__(self):
        """
        Initialize the Search class.
        """
        self.dataset = pd.read_csv("../dataset/dataset.csv")

    # Zoekopdracht 1: How many people are overstimulated with the chosen age?
    def overstimulated_by_age(self, age: int) -> tuple[int, int, pd.DataFrame]:
        """
        Returns the sum of people overstimulated by given age.
        """
        df = self.dataset.copy()
        
        df = df[df["Age"] == age]
        total_by_age = len(df)
        df_overstimulated = df[df["Overstimulated"] == 1]
        total_overstimulated = len(df_overstimulated)

        df["Overstimulated"] = df["Overstimulated"].replace({0: "No", 1: "Yes"})

        # give only columns age and overstimulated
        df = df["Overstimulated"].value_counts().reset_index()
        df.columns = ["Overstimulated", "Count"]

        return total_by_age, total_overstimulated, df
    
    # Zoekopdracht 2: What is the average stress level of people with the chosen sleep hours and overstimulated?
    def stress_by_sleep_and_overstimulated(self, sleep_hours: int, overstimulated: str) -> tuple[str, pd.DataFrame]:
        """
        Returns the average stress level of people with the given sleep hours and overstimulated.
        """
        df = self.dataset.copy()
        if overstimulated == "Yes":
            overstimulated = 1
        else:
            overstimulated = 0

        # filter dataset for overstimulated
        df = df[df['Overstimulated'] == overstimulated]

        # round sleephours to nearest integer
        df['Sleep_Hours'] = df['Sleep_Hours'].round(0)

        # filter on sleep_hours
        df = df[df['Sleep_Hours'] == sleep_hours]

        # only keep Stress_Level column
        df = df[['Stress_Level']]

        modes = df['Stress_Level'].mode()
        mode_values = ' and '.join([str(val) if isinstance(val, int) else str(round(val, 2)) for val in modes])

        df_counts = df["Stress_Level"].value_counts().reset_index()
        df_counts.columns = ["Stress_Level", "Count"]

        return mode_values, df_counts

    # Zoekopdracht 3: What could be my depression score if I have x social interactions and y screen time?
    def depression_by_social_interactions_and_screen_time(self, social_interaction: int, screen_time: int) -> pd.DataFrame:
        """
        Returns the average depression score of people with the given social interactions and screen time.
        """
        df = self.dataset.copy()

        # filter dataset for social interaction
        df = df[df['Social_Interaction'] == social_interaction]

        # round screen time to nearest integer
        df['Screen_Time'] = df['Screen_Time'].round(0)

        # filter on screen_time
        df = df[df['Screen_Time'] == screen_time]

        # only keep Depression_Score column
        df = df[['Depression_Score']]

        modes = df['Depression_Score'].mode()
        mode_values = ' and '.join([str(val) if isinstance(val, int) else str(round(val, 2)) for val in modes])

        df_counts = df["Depression_Score"].value_counts().reset_index()
        df_counts.columns = ["Depression_Score", "Count"]

        return mode_values, df_counts

    # Zoekopdracht 4: How many times could I get a headache in a week if I have x exercise hours and y overthinking?
    def headache_by_exercise_hours_and_overthinking(self, exercise_hours: str, overthinking_score: int) -> pd.DataFrame:
        """
        Returns the average headache score of people with the given exercise time and overthinking score.
        """
        df = self.dataset.copy()
        # filter dataset for overthinking score
        df = df[df['Overthinking_Score'] == overthinking_score]

        # Define your allowed values (buckets) for rounding
        bins = np.arange(0, 3.25, 0.25)

        # Custom rounding function
        def round_to_nearest_custom(x):
            return bins[np.abs(bins - x).argmin()]

        # Round exercise time to nearest custom value
        df['Exercise_Hours'] = df['Exercise_Hours'].apply(round_to_nearest_custom)

        # filter on exercise time
        df = df[df['Exercise_Hours'] == exercise_hours]

        # only keep Headache_Frequency column
        df = df[['Headache_Frequency']]

        modes = df['Headache_Frequency'].mode()
        mode_values = ' and '.join([str(val) if isinstance(val, int) else str(round(val, 2)) for val in modes])

        df_counts = df["Headache_Frequency"].value_counts().reset_index()
        df_counts.columns = ["Headache_Frequency", "Count"]

        return mode_values, df_counts

