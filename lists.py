import pandas as pd
from tkinter import filedialog
import logs


dataframe1 = None
dataframe2 = None

def load_excel(interface, button_name) -> None:
    global dataframe1, dataframe2

    try:
        file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx;*.xls")])
        
        if file_path:
            try:
                filename = file_path.split("/")[-1]
                filename_formatted = filename.split(".")[0]
                
                if button_name == "Button 1" and filename_formatted.lower() == "reseller_information":     
                    dataframe1 = pd.read_excel(file_path)
                    interface.update_status(f"Liste geladen: {filename}") 
                    logs.new_debug(f"List Loaded: {filename} in {button_name}")
                    interface.loaded_data1 = True

                elif button_name == "Button 2" and filename_formatted.lower() == "renewal_overview":
                    dataframe2 = pd.read_excel(file_path)
                    interface.update_status(f"Liste geladen: {filename}")
                    logs.new_debug(f"List Loaded: {filename} in {button_name}")
                    interface.loaded_data2 = True

                else:
                    interface.update_status("Falsche Liste ausgewählt...")
                    logs.new_debug(f"Wrong List selected: {filename}")

            except Exception as e:
                interface.update_status("Error bei File-Lesung...")
                logs.new_error(f"Error reading File: {e}")
        
        else:
            interface.update_status("Nichts wurde ausgewählt...")
            logs.new_debug(f"Nothing was selected...")

    except Exception as f:
        interface.update_status("Error bei File-Auswahl...")
        logs.new_error(f"Error selecting File: {f}")


def read_excel():
    pass
