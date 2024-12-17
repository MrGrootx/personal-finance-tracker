import pandas as pd
import csv
from datetime import datetime


class CSV:
    CSV_FILE = "finance_data.csv"
    COLUMNS = ["date", "amount", "category", "description"]

    @classmethod
    def initialize_csv(self):
        try:
            pd.read_csv(self.CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns=[self.COLUMNS])
            df.to_csv(self.CSV_FILE, index=False)

    @classmethod
    def add_entry(self, date, amount, category, description):
        new_entry = {
            "date": date,
            "amount": amount,
            "category": category,
            "description": description,
        }
        with open(self.CSV_FILE, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.COLUMNS)
            writer.writerow(new_entry)
        print("Entry added successfully!")


CSV.initialize_csv()

# CSV.add_entry(
#     datetime.now().strftime("%Y-%m-%d"),
#     input("Enter the amount: "),
#     input("Enter the category: "),
#     input("Enter the description: "),
# )

CSV.add_entry("2023-20-07", 100, "Groceries", "Milk")
