import pandas as pd
import csv
from datetime import datetime
from data_entry import get_date, get_amount, get_category, get_description


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


def add():
    CSV.initialize_csv()
    date = get_date(
        "Enter the date (dd-mm-yyyy) or press Enter for today's date: ",
        allow_default=True,
    )
    amount = get_amount()
    category = get_category()
    description = get_description()
    CSV.add_entry(date, amount, category, description)


add()
CSV.initialize_csv()
