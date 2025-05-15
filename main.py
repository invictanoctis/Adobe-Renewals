import threading
import ui
import authentication
import lists
import mail


def back_loop():
    global interface
    
    token = authentication.get_token()

    subject = interface.get_subject()
    body = interface.get_body()

    skip_lines = 0

    last_cid = 1 # not False not current_cid
    current_cid = 2 # not False not last_cid

    df = lists.merge_frames()

    for index, row in df.itertuples(index=True):
        if skip_lines:
            skip_lines -= 1
            continue
        elif row.Status == "Inactive":
            continue
        
        current_cid = row[3]
        print(current_cid)

        body = mail.parse_mail()

        recipient_address = row

        
        
        


if __name__ == "__main__":
    interface = ui.UserInterface()
    # threading.Thread(target=back_loop, daemon=True).start()
    interface.root.mainloop()