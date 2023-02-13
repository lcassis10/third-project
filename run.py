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
    Run a while loop to collect a valid data from the user.
    The loop will repeatedly request data, until it is valid.
    """
    while True:
        print("Please enter the quantity of sales for each item")
        print("Data should be only numbers\n")

        data1 = input("Number of Guinness sold: \n")
        data2 = input("Number of Fish and Chips sold: \n")
        data3 = input("Number of Brownies sold: \n")

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

def calculate_profit_data(gross_sale_row, cost_row):
    """
    Subtract gross sale minus cost to get the profit of the day.
    """
    print("Calculating profit of the day...\n")

    profit_data = []
    for gross_sale, cost in zip(gross_sale_row, cost_row):
        total_profit = int(gross_sale) - int(cost)
        profit_data.append(total_profit)

    return profit_data 

def main():
    """
    Run all program functions.
    """
    data_quantity = get_quantity_data()
    update_worksheet(data_quantity, "quantity")
    new_gross_sale_data = calculate_gross_sale(data_quantity)
    update_worksheet(new_gross_sale_data, "gross sale")
    new_total_cost_data = calculate_cost_data(data_quantity)
    update_worksheet(new_total_cost_data, "cost of the day")
    new_profit_data = calculate_profit_data(new_gross_sale_data, new_total_cost_data)
    update_worksheet(new_profit_data, "profit")

    print("--------------------------------------------------------------------------------------------------------")
    print("DAILY REPORT\n")
    print(f"You sold {data_quantity[0]} Guinness today")
    print(f"You sold {data_quantity[1]} Fish and Chips today")
    print(f"You sold {data_quantity[2]} Brownies today\n")

    print(f"Your gross sales for Guinness today was €{new_gross_sale_data[0]},00")
    print(f"Your gross sales for Fish and Chips today was €{new_gross_sale_data[1]},00")
    print(f"Your gross sales for Brownies today was €{new_gross_sale_data[2]},00\n")

    print(f"Your PROFIT on Guinness today was €{new_profit_data[0]},00")
    print(f"Your PROFIT on Fish and Chips today was €{new_profit_data[1]},00")
    print(f"Your PROFIT on Brownie today was €{new_profit_data[2]},00\n")

    print(f"TOTAL GROSS SALES OF THE DAY: €{sum(new_gross_sale_data)},00 ")
    print(f"TOTAL PROFIT OF THE DAY: €{sum(new_profit_data)},00 ")

print("Welcome to sales data automation!")
print("---------------------------------")
main()

