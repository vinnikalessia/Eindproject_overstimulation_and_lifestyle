import matplotlib.pyplot as plt
from dotenv import load_dotenv
from threading import Thread
import pandas as pd
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
        


