def conditional_text(info):
    renew_string = "Sollte keine manuelle Terminierung erfolgen, verlängert sich das aktuelle Lizenzabonnement per „Auto-Renewal“ automatisch um 12 Monate."
    terminate_string = "Sollte keine Verlängerung erfolgen, endet das Lizenzabonnement am definierten Ablaufdatum."
    
    if info == "Renew":
        return renew_string
    else:
        return terminate_string

def parse_mail(text, row):
    
    text_commands = {
        "[SAP-ID]": str(row.SAP_Number),
        "[Endkunden-Name]": row.Last_Customer_Name,
        "[Endkunden-ID]": str(row.Last_Customer_ID),
        "[Kunden-Name]": row.Customer_Name,
        "[Kunden-ID]": str(row.Customer_ID),
        "[Kunden-Mail]": row.Mail_Address,
        "[Vertrags-Info]": row.End_Info,
        "[Ablaufdatum]": str(row.End_Date), # datetime.strptime(str(row.End_Date), "%d-%m-%Y").date()
        "[Produkt-Name]": row.Product,
        "[Kondition-Text]": conditional_text(row.End_Info)
    }

    for key, value in text_commands.items():
        text = text.replace(key, str(value))
    
    return text