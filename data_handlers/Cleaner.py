import pandas as pd

class Cleaner:
    categorii_valide = [
        "Fiction", "Sci-Fi", "Mystery", "Biography",
        "History", "Fantasy", "Business", "Self-Help"
    ]

    def process(self, df: pd.DataFrame) -> pd.DataFrame:
        print("🧼 Cleaner: start")

        if df is None or df.empty:
            return df

        df = df.dropna()

        df = df[df["category"].isin(self.categorii_valide)]

        df = df[df["rating"] <= 5.0]

        print("🧼 Cleaner: done")
        return df