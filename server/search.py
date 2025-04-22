import matplotlib.pyplot as plt
from dotenv import load_dotenv
from threading import Thread
import pandas as pd
import numpy as np
import threading
import logging
import socket
import json
import os

class Search():
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
    
    def stress_by_sleep_and_overstimulated(self, data: pd.DataFrame, sleep_hours: int, overstimulated: str) -> pd.DataFrame:
        """
        Returns the average stress level of people with the given sleep hours and overstimulated.
        """
        if overstimulated == "Yes":
            overstimulated = 1
        else:
            overstimulated = 0

        # filter dataset for overstimulated
        df = data[data['Overstimulated'] == overstimulated]

        # round sleephours to nearest integer
        df['Sleep_Hours'] = df['Sleep_Hours'].round(0)

        # filter on sleep_hours
        df = df[df['Sleep_Hours'] == sleep_hours]

        # only keep Stress_Level column
        df = df[['Stress_Level']].to_json(orient="records")

        return df

    def depression_by_social_interactions_and_screen_time(self, data: pd.DataFrame, social_interaction: int, screen_time: int) -> pd.DataFrame:
        """
        Returns the average depression score of people with the given social interactions and screen time.
        """
        # filter dataset for social interaction
        df = data[data['Social_Interaction'] == social_interaction]

        # round screen time to nearest integer
        df['Screen_Time'] = df['Screen_Time'].round(0)

        # filter on screen time
        df = df[df['Screen_Time'] == screen_time].to_json(orient="records")

        return df

    def headache_by_exercise_hours_and_overthinking(self, data: pd.DataFrame, exercise_hours: str, overthinking_score: int) -> pd.DataFrame:
        """
        Returns the average headache score of people with the given workout time and overthinking score.
        """
        # filter dataset for overthinking score
        df = data[data['Overthinking_Score'] == overthinking_score]

        # Define your allowed values (buckets)
        rounding_buckets = np.array([0.0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0, 2.25, 2.5, 2.75, 3.0])

        # Custom rounding function
        def round_to_nearest_custom(x):
            return rounding_buckets[np.abs(rounding_buckets - x).argmin()]

        # Round workout time to nearest custom value
        df['Exercise_Hours'] = df['Exercise_Hours'].apply(round_to_nearest_custom)

        # filter on workout time
        df = df[df['Exercise_Hours'] == exercise_hours].to_json(orient="records")

        return df

