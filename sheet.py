from module import *

def setup_sheet():
    # Load Google Sheets credentials from environment variable
    google_credentials_path = os.getenv('GOOGLE_SHEETS_CREDENTIALS_PATH')
    if not google_credentials_path:
        raise ValueError("The Google Sheets credentials path is not set in the environment variables")

    # Set the scope and credentials for Google Sheets
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(google_credentials_path, scope)
    client = gspread.authorize(creds)

    # Open the Google Spreadsheet by title
    sheet_url = "https://docs.google.com/spreadsheets/d/1ImUhNYctOUVSLtdktvzsnd8zkpzVDedPYhSix7CRg8c/edit?usp=sharing"
    spreadsheet = client.open_by_url(sheet_url)

    worksheet_name = "Sheet1"
    worksheet = spreadsheet.get_worksheet(0)

    # If the worksheet is not found, create a new one
    if worksheet is None:
        worksheet = spreadsheet.add_worksheet(title=worksheet_name, rows="100", cols="20")

    # Define the header names
    header_names = [
        "Customer Discord ID",
        "Global Order ID",
        "Stripe Payment ID",
        "Customer Payment",
        "Booster Payout",
        "Order Details",
        "Order Status",
        "Booster ID on the Order",
        "Date of Order",
        "Date Order was Completed"
    ]

    # Check if the worksheet is empty (no header row) and add headers if needed
    existing_headers = worksheet.row_values(1)
    if not existing_headers:
        worksheet.insert_row(header_names, index=1)