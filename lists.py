import pandas as pd
from tkinter import filedialog
import logs


df1 = None
df2 = None

def load_excel(interface, button_name) -> None:
    global df1, df2

    try:
        file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx;*.xls")])
        if not file_path:
            interface.update_status("Nichts wurde ausgewählt...")
            logs.new_info("Nothing was selected...")
            return

        filename = file_path.split("/")[-1]
        filename_formatted = filename.rsplit(".", 1)[0].lower()

        expected_files = {
            "Button 1": "reseller_information",
            "Button 2": "renewal_overview"
        }

        if button_name not in expected_files:
            interface.update_status("Unbekannter Button...")
            logs.new_error(f"Unknown button name: {button_name}")
            return

        expected_filename = expected_files[button_name]

        if filename_formatted != expected_filename:
            interface.update_status("Falsche Liste ausgewählt...")
            logs.new_info(f"Wrong List selected: {filename}")
            return

        # Reading Excel
        try:
            df = pd.read_excel(file_path)
            if button_name == "Button 1":
                df1 = df
                interface.loaded_data1 = True
            else:
                df2 = df
                interface.loaded_data2 = True

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
