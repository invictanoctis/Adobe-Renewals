try:
    import threading
    import time
    import ui
    import authentication
    import lists
    import mail
    import logs
except ImportError as e:
    print(f"Error importing modules: {e}")
    logs.new_error(f"Error importing modules: {e}")

def back_loop(interface):
    if not interface.loaded_info:
        interface.update_status("Bitte alle Informationen zuerst angeben...")
        logs.new_info("Not all information was given. Couldn't start sending...")
        return

    token = authentication.get_access_token(interface)
    print(token) #TEMP

    alias = interface.get_user()
    subject = interface.get_subject()
    body = interface.get_body()

    df = lists.df_merged

    for row in df.itertuples(index=True):
        subject_parsed = mail.parse_mail(subject, row)
        body_parsed = mail.parse_mail(body, row)
        recipient_address = row.Mail_Address

        # print(interface, token, alias, subject_parsed, body_parsed, recipient_address) # debug
        authentication.send_mail(interface, token, alias, subject_parsed, body_parsed, recipient_address)
        # authentication.testing(interface, token, alias, subject_parsed, body_parsed, recipient_address) # debug

        time.sleep(3)

    interface.update_status("Alle Mails wurden gesendet!")
    logs.new_info("All mails were sent...")

def start_threaded(interface):
    thread = threading.Thread(target=lambda: back_loop(interface), daemon=True)
    thread.start()

def main():
    interface = ui.UserInterface()
    interface.send_button.config(command=lambda: start_threaded(interface))
    interface.root.mainloop()

if __name__ == "__main__":
    main()