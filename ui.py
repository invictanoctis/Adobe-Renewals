import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk
import lists
import authentication
import logs
import os


class UserInterface():
    def __init__(self):
        self.loaded_data1 = False # indicates whether an excel was loaded
        self.loaded_data2 = False # indicates whether an excel was loaded
        self.loaded_info = False # indicates whether all the mail information + excels were loaded

        self.current_version = "v1.0" # current version of application

        self.red = "#ed1c24"
        self.black = "black"
        self.white = "white"
        self.grey = "grey"
        self.offwhite = "#f5f5f5"

        self.root = tk.Tk()
        self.root.title("Adobe Renewal Mailing")
        self.root.geometry("800x600")
        self.root.configure(bg=self.offwhite)

        self.title_label = tk.Label(
            self.root,
            text="Adobe Automation: Renewal Mails",
            font=("Arial", 24, "bold"),
            fg=self.black,
            bg=self.red
        )

        self.title_label.pack(fill="x", 
                              pady=(0, 10))

        # Frames

        self.main_frame = tk.Frame(self.root, 
                                   bg=self.offwhite)
        self.main_frame.pack(expand=True, 
                             fill="both", 
                             padx=20, 
                             pady=10)

        self.left_frame = tk.Frame(self.main_frame, 
                                   bg=self.white)
        self.left_frame.pack(side="left", 
                             expand=True, 
                             fill="both", 
                             padx=(0, 10))

        self.right_frame = tk.Frame(self.main_frame, 
                                    bg=self.white)
        self.right_frame.pack(side="right", 
                              expand=True, 
                              fill="both", 
                              padx=(10, 0))

        # Left Side

        tk.Label(self.left_frame, 
                 text="Reseller Informationen:", 
                 font=("Arial", 12, "bold"),
                 bg=self.white, 
                 fg=self.black).pack(anchor="w", pady=5)
        
        tk.Button(self.left_frame, 
                  text="Durchsuchen", 
                  bg=self.white, 
                  fg=self.black,
                  command=lambda: lists.load_excel(self, "Button 1")).pack(pady=5)

        tk.Label(self.left_frame, 
                 text="Renewal Overview:", 
                 font=("Arial", 12, "bold"),
                 bg=self.white, 
                 fg=self.black).pack(anchor="w", pady=5)
        
        tk.Button(self.left_frame, 
                  text="Durchsuchen", 
                  bg=self.white, 
                  fg=self.black,
                  command=lambda: lists.load_excel(self, "Button 2")).pack(pady=5)

        tk.Label(self.left_frame, 
                 text="User-Mail:", 
                 font=("Arial", 12, "bold"),
                 bg=self.white, 
                 fg=self.black).pack(anchor="w", pady=5)
        
        self.user = tk.Entry(self.left_frame, 
                              width=40, 
                              bg=self.offwhite, 
                              relief="groove")
        self.user.pack(pady=2)

        tk.Label(self.left_frame,
                 text="Betreff:", 
                 font=("Arial", 12, "bold"),
                 bg=self.white, 
                 fg=self.black).pack(anchor="w", pady=5)
        
        self.subject = tk.Entry(self.left_frame, 
                                width=40, 
                                bg=self.offwhite, 
                                relief="groove")
        self.subject.pack(pady=2)

        tk.Label(self.left_frame, 
                 text="Inhalt:", 
                 font=("Arial", 12, "bold"),
                 bg=self.white, 
                 fg=self.black).pack(anchor="w", pady=5)
        
        self.body = tk.Text(self.left_frame, 
                            height=8, 
                            width=40, 
                            bg=self.offwhite, 
                            relief="groove")
        self.body.pack(pady=2)

        # Right Side

        try:
            image_path = "adobe_icon.png"
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"Image not found at {image_path}")

            original_image = Image.open(image_path)
            resized_image = original_image.resize((100, 100), Image.Resampling.LANCZOS)
            self.logo = ImageTk.PhotoImage(resized_image)

            self.image_label = tk.Label(self.right_frame, image=self.logo, bg=self.white)
            self.image_label.image = self.logo # garbage collection prevention
            self.image_label.pack(pady=5)

        except Exception as e:
            print(f"[ERROR] Failed to load image: {e}")
            self.image_label = tk.Label(self.right_frame, text="Bild konnte nicht geladen werden", fg=self.black, bg=self.white)
            self.image_label.pack(pady=5)

        self.parse_button = tk.Button(self.right_frame, 
                                      text="Infos Laden",
                                      bg=self.white,
                                      fg=self.black, 
                                      width=20, 
                                      command=self.check_info) 
        self.parse_button.pack(pady=20)

        self.send_button = tk.Button(self.right_frame, 
                                     text="Lossenden", 
                                     bg=self.white,
                                     fg=self.black, 
                                     width=20, 
                                     command=authentication.placeholder)
        self.send_button.pack(pady=5)

        self.status_box = tk.Text(self.right_frame, 
                                  height=10, 
                                  width=50,
                                  state="disabled",
                                  wrap="word", 
                                  bg=self.offwhite)
        self.status_box.pack(pady=10)

        # Other

        self.version_label = tk.Label(
            self.root,
            text=self.current_version,
            font=("Arial", 8),
            bg=self.offwhite,
            fg=self.grey
        )
        self.version_label.place(relx=1.0, 
                                 rely=1.0, 
                                 x=-10, 
                                 y=-5, 
                                 anchor="se")


    # Functions 

    def update_status(self, message:str) -> None:
        """
        Adds the specified argument as a message to the ui's status box
        
        Args:
            message (str): message that will be displayed in the status box
        """

        self.status_box.config(state="normal")
        self.status_box.insert("end", message + "\n")
        self.status_box.config(state="disabled")
        self.status_box.yview("end")

    def get_user(self) -> str:
        """
        Get function to retrieve the mails user specified in the ui

        Returns:
            str: the current user
        """

        return self.user.get()
    
    def get_subject(self) -> str:
        """
        Get function to retrieve the mails subject specified in the ui

        Returns:
            str: the mails subject
        """

        return self.subject.get()
    
    def get_body(self) -> str:
        """
        Get function to retrieve the mails body specified in the ui

        Returns:
            str: the mails body
        """

        return self.body.get("1.0", "end").strip()
    
    def get_mail_info(self) -> list:
        """
        Combines all the other get functions into a list of the mail information currently given

        Returns:
            list -> a list of strings containing the mail information given
        """
        return [self.get_user(), self.get_subject(), self.get_body()]
    
    def check_info(self) -> None:
        """
        Checks whether all the mail information was given by the user, sets loaded_info True if that's the case
        """

        logs.new_debug("Parse button clicked...")
        user_address = self.get_user()
        subject_info = self.get_subject()
        body_info = self.get_body()

        if all([user_address, subject_info, body_info, self.loaded_data1, self.loaded_data2]):
            self.update_status("Alle Mailinfos wurden geladen...")
            logs.new_debug("Mailinfo checked successfully...")
            self.loaded_info = True
        else:
            self.update_status("Nicht alle Informationen wurden angegeben...")
            logs.new_debug("Not every mail information was given...")