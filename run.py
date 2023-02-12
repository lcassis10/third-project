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

    validate_data(data_str1, data_str2, data_str3)

def validate_data(value1, value2, value3):
    """
    Inside the try, converts all strings values into integers.
    Raises ValueError if strings cannot be converted into int,
    or if there is more than one value in each item.
    """
    try:
        if len(value1) != 1:
            raise ValueError("Please enter only one number that correspond the total of sales for each item requested")
        if len(value2) != 1:
            raise ValueError("Please enter only one number that correspond the total of sales for each item requested")
        if len(value3) != 1:
            raise ValueError("Please enter only one number that correspond the total of sales for each item requested")

    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")

    

get_quantity_data()