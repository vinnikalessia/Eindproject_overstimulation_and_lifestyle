import pandas as pd
import numpy as np

class Search():
    # Zoekopdracht 1: How many people are overstimulated with the chosen age?
    def overstimulated_by_age(self, data: pd.DataFrame, age: int) -> pd.DataFrame:
        """
        Returns the sum of people overstimulated by given age.
        """
        rows_by_age = data.loc[data["Age"] == age]
        total_by_age = int(rows_by_age["Age"].count())
        overstimulated = rows_by_age.loc[rows_by_age["Overstimulated"] == 1]
        total_overstimulated = int(overstimulated["Age"].count())

        # give only columns age and overstimulated and convert to json
        res_data = rows_by_age[["Age", "Overstimulated"]].to_json(orient="records")

        return total_by_age, total_overstimulated, res_data
    
    # Zoekopdracht 2: What is the average stress level of people with the chosen sleep hours and overstimulated?
    def stress_by_sleep_and_overstimulated(self, data: pd.DataFrame, sleep_hours: int, overstimulated: str) -> pd.DataFrame:
        """
        Returns the average stress level of people with the given sleep hours and overstimulated.
        """
        if overstimulated == "Yes":
            overstimulated = 1
        else:
            overstimulated = 0

        # filter dataset for overstimulated
        data = data[data['Overstimulated'] == overstimulated]

        # round sleephours to nearest integer
        data['Sleep_Hours'] = data['Sleep_Hours'].round(0)

        # filter on sleep_hours
        data = data[data['Sleep_Hours'] == sleep_hours]

        # only keep Stress_Level column
        res_data = data[['Stress_Level']].to_json(orient="records")

        return res_data

    # Zoekopdracht 3: What could be my depression score if I have x social interactions and y screen time?
    def depression_by_social_interactions_and_screen_time(self, data: pd.DataFrame, social_interaction: int, screen_time: int) -> pd.DataFrame:
        """
        Returns the average depression score of people with the given social interactions and screen time.
        """
        # filter dataset for social interaction
        data = data[data['Social_Interaction'] == social_interaction]

        # round screen time to nearest integer
        data['Screen_Time'] = data['Screen_Time'].round(0)

        # filter on screen_time
        data = data[data['Screen_Time'] == screen_time]

        # only keep Depression_Score column
        res_data = data[['Depression_Score']].to_json(orient="records")

        return res_data

    # Zoekopdracht 4: How many times could I get a headache in a week if I have x exercise hours and y overthinking?
    def headache_by_exercise_hours_and_overthinking(self, data: pd.DataFrame, exercise_hours: str, overthinking_score: int) -> pd.DataFrame:
        """
        Returns the average headache score of people with the given exercise time and overthinking score.
        """
        # filter dataset for overthinking score
        data = data[data['Overthinking_Score'] == overthinking_score]

        # Define your allowed values (buckets) for rounding
        rounding_buckets = np.array([0.0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0, 2.25, 2.5, 2.75, 3.0])

        # Custom rounding function
        def round_to_nearest_custom(x):
            return rounding_buckets[np.abs(rounding_buckets - x).argmin()]

        # Round exercise time to nearest custom value
        data['Exercise_Hours'] = data['Exercise_Hours'].apply(round_to_nearest_custom)

        # filter on exercise time
        data = data[data['Exercise_Hours'] == exercise_hours]

        # only keep Headache_Frequency column
        res_data = data[['Headache_Frequency']].to_json(orient="records")

        return res_data

