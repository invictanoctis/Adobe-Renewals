import pandas as pd
from datetime import datetime
from tkinter import filedialog
import logs

# global dataframes
df1 = None
df2 = None
df_merged = None

# ---------------- Functions

def normalize_dates(series:object) -> object:
    """
    Function to normalize date formats in a pandas series

    Args:
        series (object): pd.Series object containing date values
    
    Returns:
        object: pd.Series object containing nomalized date values
    """

    def parse_date(x):
        if isinstance(x, (pd.Timestamp, datetime)):
            return x
        if pd.isna(x):
            return pd.NaT
        return pd.to_datetime(x, dayfirst=True, errors='coerce')

    return series.apply(parse_date)

def merge_frames(interface:object) -> object | None:
    """
    The merging function that is triggered once list 2 was loaded

    Args:
        interface (object): object of ui.UserInterface

    Returns:
        object | None: Merged DataFrame if both lists were loaded, None if dataframes are not loaded or empty
    """
    global df1, df2

    if interface.loaded_data1 and interface.loaded_data2:
        merged_df = df1.merge(df2, on='Customer_ID', how='inner', suffixes=('_df1', '_df2'))
        merged_df.sort_values(by='End_Date', inplace=True)
        return merged_df
    else:
        logs.new_info("Dataframes not yet loaded or empty.")
        return None

def load_excel(interface:object, button_name:str) -> None:
    """
    The loading and parsing function that is triggered once an Excel-Select button from ui.UserInterface was pressed

    Args:
        interface (object): object of ui.UserInterface
        button_name (str): the name of the button that was pressed
    """
    global df1, df2, df_merged

    try:
        file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx;*.xls")])
        if not file_path:
            interface.update_status("Nichts wurde ausgewählt...")
            logs.new_info("Nothing was selected...")
            return

        filename = file_path.split("/")[-1]
        filename_formatted = filename.rsplit(".", 1)[0].lower()

        expected_files = {
            "Button 1": [
                "reseller_information",
                "reseller_information (1)",
                "reseller_information (2)",
                "reseller_information (3)",
                "reseller_information (4)",
                "reseller_information (5)",
                "reseller_information (6)",
                "reseller_information (7)",
                "reseller_information (8)",
                "reseller_information (9)"
                ],

            "Button 2": [
                "renewal_overview",
                "renewal_overview (1)",
                "renewal_overview (2)",
                "renewal_overview (3)",
                "renewal_overview (4)",
                "renewal_overview (5)",
                "renewal_overview (6)",
                "renewal_overview (7)",
                "renewal_overview (8)",
                "renewal_overview (9)"
                ]
            }


        if button_name not in expected_files: # can't be encountered rn, future error prevention
            interface.update_status("Unbekannter Button...")
            logs.new_error(f"Unknown button name: {button_name}")
            return

        if filename_formatted not in expected_files[button_name]:
            interface.update_status("Falsche Liste ausgewählt...")
            logs.new_info(f"Wrong List selected: {filename}")
            return
        
        # now = datetime.now() #current date and time

        try:
            if button_name == "Button 1":
                df1 = pd.read_excel(file_path, header=None, usecols=[1, 2, 3, 9]) # parses customerid, email, sap number
                df1 = df1.drop(index=0)
                df1.sort_values(by=1, inplace=True) # customerid ascending to match df2
                df1.columns = ["Customer_ID", "Customer_Name", "Mail_Address", "SAP_Number"]
                df1["Customer_ID"] = df1["Customer_ID"].astype(str).str.strip()

                
                interface.loaded_data1 = True # global ui info check
            
            else:
                try:
                    selected_enddate = datetime.strptime(interface.get_enddate(), "%d-%m-%Y").date() # tk date formatting error prevention
                    selected_startdate = datetime.strptime(interface.get_startdate(), "%d-%m-%Y").date() # tk date formatting error prevention
                except ValueError:
                    interface.update_status("Ungültiges Datum-Format.")
                    logs.new_info("Invalid date format.")
                    return
                
                if selected_enddate != datetime.today().date() and selected_enddate > datetime.today().date(): # if enddate not today and before today
                    if selected_startdate < selected_enddate: # if startdate is before enddate
                        end_date = pd.to_datetime(interface.get_enddate(), dayfirst=True) # parse enddate as panda datetime object
                        start_date = pd.to_datetime(interface.get_startdate(), dayfirst=True) # parse startdate as panda datetime object
                    else:
                        interface.update_status("Startdatum muss vor Enddatum liegen...")
                        logs.new_info("Date logic error: startdate must be before enddate.")
                        return
                else:
                    interface.update_status("Enddatum darf nicht heute sein...")
                    logs.new_info("Date logic error: enddate set as 'today'.")
                    return
                
                df2 = pd.read_excel(file_path, header=None, usecols=[3, 5, 6, 16, 17, 18]) # parses contractenddate, enddateinfo, productname, customerid
                df2 = df2.drop(index=0)
                print(df2[3].apply(type).value_counts()) # debug
                
                df2[3] = normalize_dates(df2[3])
                # df2[3] = pd.to_datetime(df2[3], dayfirst=True, errors='coerce') # other solution for debug use
                # df2[3] = pd.to_datetime(df2[3], dayfirst=True) # other solution for debug use

                if interface.get_duedate_info() == False:
                    df2 = df2[ # only leaves the rows that have the current month and current year as a value in column 3 and "Adobe" in 6
                                (start_date <= df2[3]) & (df2[3] <= end_date) &
                                df2[6].str.contains("Adobe", case=False, na=False)
                            ]
                else:
                    df2 = df2[ # only leaves the rows that have the due date as a value in column 3 and "Adobe" in 6
                                (df2[3] == end_date) &
                                df2[6].str.contains("Adobe", case=False, na=False)
                            ]
                
                df2.sort_values(by=18, inplace=True) # customerid ascending to match df1
                
                df2.columns = ["End_Date", "End_Info", "Product", "Last_Customer_ID", "Last_Customer_Name", "Customer_ID"]
                df2["Customer_ID"] = df2["Customer_ID"].astype(str).str.strip()

                
                interface.loaded_data2 = True # global ui info check

            interface.update_status(f"Liste geladen: {filename}")
            logs.new_info(f"List Loaded: {filename} in {button_name}")

        except Exception as e:
            interface.update_status("Error bei File-Lesung...")
            logs.new_error(f"Error reading File: {e}")

    except Exception as f:
        interface.update_status("Error bei File-Auswahl...")
        logs.new_error(f"Error selecting File: {f}")
    
    df_merged = merge_frames(interface)