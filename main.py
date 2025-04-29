import ui
import threading


def back_loop():
    pass

if __name__ == "__main__":
    interface = ui.UserInterface()
    threading.Thread(target=back_loop, daemon=True).start()
    interface.root.mainloop()