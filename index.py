import pandas as pd
import csv
from datetime import datetime
from data_entry import get_date, get_amount, get_category, get_description


class CSV:
    CSV_FILE = "finance_data.csv"
    COLUMNS = ["date", "amount", "category", "description"]
    DATE_FORMAT = "%d-%m-%Y"

    @classmethod
    def initialize_csv(cls):
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns=cls.COLUMNS)
            df.to_csv(cls.CSV_FILE, index=False)

    @classmethod
    def add_entry(cls, date, amount, category, description):
        # Ensure date is in the correct format before adding
        try:
            datetime.strptime(date, cls.DATE_FORMAT)
        except ValueError:
            print(f"Error: Date must be in the format {cls.DATE_FORMAT}.")
            return

        new_entry = {
            "date": date,
            "amount": amount,
            "category": category,
            "description": description,
        }
        with open(cls.CSV_FILE, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMNS)
            if csvfile.tell() == 0:  # If the file is empty, write the header
                writer.writeheader()
            writer.writerow(new_entry)
        print("Entry added successfully!")

    @classmethod
    def get_transactions(cls, start_date, end_date):
        try:
            df = pd.read_csv(cls.CSV_FILE)

            # Attempt to parse dates, allowing for errors
            df["date"] = pd.to_datetime(
                df["date"], format=cls.DATE_FORMAT, errors="coerce"
            )
            df = df.dropna(subset=["date"])  # Remove rows with invalid dates

            # Convert input dates to datetime objects
            start_date = datetime.strptime(start_date, cls.DATE_FORMAT)
            end_date = datetime.strptime(end_date, cls.DATE_FORMAT)

            # Filter rows within the date range
            mask = (df["date"] >= start_date) & (df["date"] <= end_date)
            filtered_df = df.loc[mask]

            if filtered_df.empty:
                print("No transactions found for the given date range.")
            else:
                print(
                    f"Transactions: {start_date.strftime(cls.DATE_FORMAT)} - {end_date.strftime(cls.DATE_FORMAT)}"
                )
                print(
                    filtered_df.to_string(
                        index=False,
                        formatters={"date": lambda x: x.strftime(cls.DATE_FORMAT)},
                    )
                )

                # Calculate totals
                total_income = filtered_df[filtered_df["category"] == "Income"][
                    "amount"
                ].sum()
                total_expense = filtered_df[filtered_df["category"] == "Expense"][
                    "amount"
                ].sum()

                print("\nSummary:")
                print(f"Total Income: {total_income:.2f}")
                print(f"Total Expense: {total_expense:.2f}")
                print(f"Net Balance: {total_income - total_expense:.2f}")
        except FileNotFoundError:
            print("Error: No data found. Please add entries first.")
        except Exception as e:
            print(f"Error: {e}")

    @classmethod
    def preprocess_csv(cls):
        """
        Preprocess the CSV to ensure consistent date formats.
        Run this function once to clean up existing data.
        """
        try:
            df = pd.read_csv(cls.CSV_FILE)
            df["date"] = pd.to_datetime(df["date"], dayfirst=True, errors="coerce")
            df = df.dropna(subset=["date"])
            df["date"] = df["date"].dt.strftime(cls.DATE_FORMAT)
            df.to_csv(cls.CSV_FILE, index=False)
            print("CSV preprocessing completed successfully.")
        except FileNotFoundError:
            print("Error: No CSV file found to preprocess.")


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


CSV.get_transactions("20-07-2023", "18-12-2024")
