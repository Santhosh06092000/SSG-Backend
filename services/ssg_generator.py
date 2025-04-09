from typing import Set, Tuple
import pandas as pd


class SecretSantaGenerator:
    def __init__(self, df: pd.DataFrame, previous_pairs: Set[Tuple[str, str]] = set()):
        self.df = df
        self.previous_pairs = previous_pairs

    def validate_columns(self):
        if not {"Employee_Name", "Employee_EmailID"}.issubset(self.df.columns):
            raise ValueError(
                f"DataFrame must contain 'Employee_Name' and 'Employee_EmailID' columns.")

    def generate_secret_santa(self, max_attempts: int = 100) -> pd.DataFrame:
        # validate the columns
        self.validate_columns()

        # copy the dataframe
        secret_df = self.df.copy()
        attempt = 0

        while attempt < max_attempts:
            shuffled_df = self.df.sample(frac=1).reset_index(drop=True)
            invalid = False

            for i in range(len(self.df)):
                giver = self.df.iloc[i]["Employee_EmailID"]
                receiver = shuffled_df.iloc[i]["Employee_EmailID"]

                if giver == receiver or (giver, receiver) in self.previous_pairs:
                    invalid = True
                    break
            if not invalid:
                break

            attempt += 1

        secret_df["Secret_Child_Name"] = shuffled_df["Employee_Name"]
        secret_df["Secret_Child_EmailID"] = shuffled_df["Employee_EmailID"]

        return secret_df
