import ui
import threading
import time


def back_loop():
    while True:
        while not interface.loaded_info:
            time.sleep(1)
        
        alias_address, subject_info, body_info = interface.get_mail_info()

if __name__ == "__main__":
    interface = ui.UserInterface()
    threading.Thread(target=back_loop, daemon=True).start()
    interface.root.mainloop()