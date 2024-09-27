import pandas as pd
import csv
from datetime import datetime
from data_entry import get_amount, get_category, get_date, get_description #importing all written functions from other file
import matplotlib.pyplot as plt

class CSV:
    CSV_FILE = "finance_data.csv"
    COLUMNS = ["date", "amount", "category", "description"]
    FORMAT = "%d-%m-%Y"  
      
    @classmethod
    def initialize_csv(cls):
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns = cls.COLUMNS)
            df.to_csv(cls.CSV_FILE, index = False)
    '''
    For example:
    date, amount, category, description
    20-07-2024, 125, Income, Salary
    '''

    #Storing this in Python Dictionary
    @classmethod
    def add_entry(cls, date, amount, category, description):        
        new_entry = {
            "date": date,
            "amount":amount,
            "category": category,
            "description": description
        }
        with open(cls.CSV_FILE, "a", newline = "") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames = cls.COLUMNS)
            '''
            CSV Writer: Takes a dictionary and write it into the csv file
            '''
            writer.writerow(new_entry)
        
        print("Entry added successfully")
    
    #Give us all transactions within a date range
    @classmethod
    def get_transactions(cls, start_date, end_date):
        df = pd.read_csv(cls.CSV_FILE)
        
        #Convert all of the dates inside of the Date Column to a datetime object
        df["date"] = pd.to_datetime(df["date"], format = CSV.FORMAT)
        start_date = datetime.strptime(start_date, CSV.FORMAT)
        end_date = datetime.strptime(end_date, CSV.FORMAT)
        
        '''
        Creating a Mask
        Mask: something that we can apply to the different rows inside of a dataframe
        to see if we should select that row or not
        '''
        mask = (df["date"] >= start_date) & (df["date"] <= end_date) #will be applied to every single row inside of dataframe
        filtered_df = df.loc[mask] #returns a new filtered dataframe
        
        if filtered_df.empty:
            print('No transactions found in the given date range')
        else:
            print(f"Transactions from {start_date.strftime(CSV.FORMAT)} to {end_date.strftime(CSV.FORMAT)}")
            
            print(filtered_df.to_string(index = False, formatters = {"date": lambda x: x.strftime(CSV.FORMAT)}))

            total_income = filtered_df[filtered_df["category"] == "Income"]["amount"].sum()
            total_expense = filtered_df[filtered_df["category"] == "Expense"]["amount"].sum()
            print("\nSummary: ")
            print(f"Total Income: ${total_income:.2f}")
            print(f"Total Expense: ${total_expense:.2f}")
            print(f"Net Savings: ${(total_income - total_expense):.2f}")
            
        return filtered_df
            
            
def add(): 
    '''
    Function that will call functions from data_entry.py
    in the order that we want in order to collect data
    '''
    CSV.initialize_csv()
    date = get_date("Enter the date of the transaction (dd-mm-yyyy) or enter for todays date: ",
                    allow_default = True)
    amount = get_amount()
    category = get_category()
    description = get_description()
    CSV.add_entry(date, amount, category, description)    

#For the plot of data
def plot_transactions(df):
    df.set_index('date', inplace = True)
    
    income_df = df[df["category"] == "Income"].resample("D").sum().reindex(df.index, fill_value = 0) #income dataframe line
    expense_df = df[df["category"] == "Expense"].resample("D").sum().reindex(df.index, fill_value = 0) #expense dataframe line
    
    #Visual Plot:
    plt.figure(figsize = (10, 5))
    plt.plot(income_df.index, income_df["amount"], label = "Income", color = "g")
    plt.plot(expense_df.index, expense_df["amount"], label = "Expense", color = "r")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title('Income and Expenses Over Time')
    plt.legend()
    plt.grid(True)
    plt.show()


#For different features of the tracker
def main():
    while True:
        print("\n1. Add a new transaction")
        print("2. View transactions and summary within date range")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ")
        
        if choice == "1":
            add()
        elif choice == "2":
            start_date = get_date("Enter the start date (dd-mm-yyyy): ")
            end_date = get_date("Enter the end date (dd-mm-yyyy): ")
            df = CSV.get_transactions(start_date, end_date)
            if input("Do you want to see a plot? (y/n) ").lower() == "y":
                plot_transactions(df)
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Enter 1, 2, or 3")


if __name__ == "__main__":
    main()