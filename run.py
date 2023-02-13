import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

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
    Run a while loop to collect a valid data from the user.
    The loop will repeatedly request data, until it is valid.
    """
    while True:
        print("Please enter the quantity of sales for each item")
        print("Data should be only numbers\n")

        data1 = input("Number of Guinness sold: ")
        data2 = input("Number of Fish and Chips sold: ")
        data3 = input("Number of Brownies sold: ")

        if validate_data(data1, data2, data3):
            break

    return ([int(data1), int(data2), int(data3)])

    

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
        return False
    
    return True

def update_quantity_worksheet(data):
    """
    Update quantity worksheet, add new row with the list data provided.
    """
    print("Updating quantity worksheet...\n")
    quantity_worksheet = SHEET.worksheet("quantity")
    quantity_worksheet.append_row(data)
    print("Quantity worksheet updated successfully.\n")

def calculate_gross_sale(quantity_row):
    """
    Mutiply quantity times price to get the total of gross sale.
    """
    print("Calculating gross sale for the day...\n")
    price = SHEET.worksheet("price").get_all_values()
    price_row = price[-1]
    
    gross_sale_data = []
    for price, quantity in zip(price_row, quantity_row):
        gross_sale = int(price) * quantity
        gross_sale_data.append(gross_sale)
    
    return gross_sale_data


def main():
    """
    Run all program functions.
    """
    data_quantity = get_quantity_data()
    update_quantity_worksheet(data_quantity)
    new_gross_sale_data = calculate_gross_sale(data_quantity)
    print(new_gross_sale_data)

print("Welcome to sales data automation!")
print("---------------------------------")
main()
