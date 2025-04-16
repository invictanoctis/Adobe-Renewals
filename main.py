import ui
import threading
import time


def back_loop():
    pass

if __name__ == "__main__":
    interface = ui.UserInterface()
    threading.Thread(target=back_loop, daemon=True).start()
    interface.root.mainloop()