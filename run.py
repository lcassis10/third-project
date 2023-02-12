import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('sales_spreadsheet')

def get_quantity_data():
    """
    Get quantity data from the user.
    """
    print("Please enter the quantity of sales for each item")
    print("Data should be only numbers\n")

    data_str1 = input("Number of Guinness sold: ")
    data_str2 = input("Number of Fish and Chips sold: ")
    data_str3 = input("Number of Brownies sold: ")

    print(f"The number of Guinness sold is {data_str1}. The number of Fish and Chips sold is {data_str2}. The number of Brownies sold is {data_str3} ")


get_quantity_data()