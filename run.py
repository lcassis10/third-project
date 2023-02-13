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

def update_worksheet(data, worksheet):
    """
    Receives a list of integers to be inserted into a worksheet.
    Update the relevant worksheet with the data provided.
    """
    print(f"Updating {worksheet} worksheet...\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} worksheet updated successfully.\n")

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

def calculate_cost_data(quantity_row):
    """
    Mutiply quantity times cost to get the total cost spend to buy the stock.
    """
    print("Calculating cost of products sold for the day...\n")
    cost = SHEET.worksheet("cost").get_all_values()
    cost_row = cost[-1]

    cost_data = []
    for cost, quantity in zip(cost_row, quantity_row):
        total_cost = int(cost) * quantity
        cost_data.append(total_cost)

    return cost_data


def main():
    """
    Run all program functions.
    """
    data_quantity = get_quantity_data()
    update_worksheet(data_quantity, "quantity")
    new_gross_sale_data = calculate_gross_sale(data_quantity)
    update_worksheet(new_gross_sale_data, "gross sale")
    new_total_cost_data = calculate_cost_data(data_quantity)
    print(new_total_cost_data)

print("Welcome to sales data automation!")
print("---------------------------------")
main()
