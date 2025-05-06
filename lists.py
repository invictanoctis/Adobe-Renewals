import pandas as pd
from datetime import datetime
from tkinter import filedialog
import logs

# global dataframes
df1 = None
df2 = None

# ---------------- Functions

def load_excel(interface, button_name) -> None:
    """
    The loading and parsing function that is triggered once an Excel-Select button from ui.UserInterface was pressed

    Args:
        interface (object): object of ui.UserInterface
        button_name (str): the name of the button that was pressed
    """
    global df1, df2

    try:
        file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx;*.xls")])
        if not file_path:
            interface.update_status("Nichts wurde ausgewählt...")
            logs.new_info("Nothing was selected...")
            return

        filename = file_path.split("/")[-1]
        filename_formatted = filename.rsplit(".", 1)[0].lower()

        expected_files = { # best practice use of dict for later list error handling
            "Button 1": "reseller_information",
            "Button 2": "renewal_overview"
        }

        if button_name not in expected_files: # can't be encountered, but prevents possible bugs in the future
            interface.update_status("Unbekannter Button...")
            logs.new_error(f"Unknown button name: {button_name}")
            return

        expected_filename = expected_files[button_name] # looks for correct filename in dict

        if filename_formatted != expected_filename: # if wrong list/filename was selected
            interface.update_status("Falsche Liste ausgewählt...")
            logs.new_info(f"Wrong List selected: {filename}")
            return

        now = datetime.now() #current date and time

        try:
            if button_name == "Button 1":
                df1 = pd.read_excel(file_path, header=None, usecols=[1, 3]) # parses customerid and email
                df1 = df1.drop(index=0)
                df1.sort_values(by=1, inplace=True) # customerid ascending to match df2
                df1.columns = ["Customer ID", "Mail-Address"]
                
                interface.loaded_data1 = True # global ui info check
            
            else:
                df2 = pd.read_excel(file_path, header=None, usecols=[ 3, 5, 6, 18]) # parses contractenddate, enddateinfo, productname columns, customerid
                df2 = df2.drop(index=0)
                df2[3] = pd.to_datetime(df2[3], dayfirst=True) # parses contractenddate column as date

                df2 = df2[ # only leaves the rows that have the current month and current year as a value in column 3 and "Adobe" in 6
                            (df2[3].dt.month == now.month) &
                            (df2[3].dt.year == now.year) &
                            df2[6].str.contains("Adobe", case=False, na=False)
                        ]
                
                df2.sort_values(by=18, inplace=True) # customerid ascending to match df1
                
                df2.columns = ["End-Date", "End-Info", "Product", "Customer ID"]
                
                interface.loaded_data2 = True # global ui info check

            interface.update_status(f"Liste geladen: {filename}")
            logs.new_info(f"List Loaded: {filename} in {button_name}")

        except Exception as e:
            interface.update_status("Error bei File-Lesung...")
            logs.new_error(f"Error reading File: {e}")

    except Exception as f:
        interface.update_status("Error bei File-Auswahl...")
        logs.new_error(f"Error selecting File: {f}")

def read_excel():
    pass
