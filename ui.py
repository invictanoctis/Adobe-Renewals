import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import lists
import authentication
import logs
import os


class UserInterface():
    def __init__(self):
        self.loaded_data1 = False # indicates whether excel 1 was loaded
        self.loaded_data2 = False # indicates whether excel 2 was loaded
        self.loaded_info = False # indicates whether the mail information + excels were loaded

        self.current_version = "v1.0" # current version of application

        # Custom Colors
        self.red = "#ed1c24"
        self.black = "black"
        self.white = "white"
        self.grey = "grey"
        self.offwhite = "#f5f5f5"

        # Root setup
        self.root = tk.Tk()
        self.root.title("Adobe Renewal Mailing")
        self.root.geometry("800x600")
        self.root.configure(bg=self.offwhite)

        # Title Label
        self.title_label = tk.Label(
            self.root,
            text="Adobe Automation: Renewal Mails",
            font=("Arial", 24, "bold"),
            fg=self.black,
            bg=self.red
        ).pack(fill="x", pady=(0, 10))

        # ---------------- Frames

        # Main Frame
        self.main_frame = tk.Frame(self.root, 
                                   bg=self.offwhite).pack(expand=True, 
                                                          fill="both", 
                                                          padx=20, 
                                                          pady=10)

        # Left Frame
        self.left_frame = tk.Frame(self.main_frame, 
                                   bg=self.white).pack(side="left", 
                                                       expand=True, 
                                                       fill="both", 
                                                       padx=(0, 10))

        # Excel Button Frame 1
        self.excel1_btn_frame = tk.Frame(self.left_frame, 
                                    bg=self.white).pack(pady=5, anchor="w")

        # Excel Button Frame 2
        self.excel2_btn_frame = tk.Frame(self.left_frame, 
                                         bg=self.white).pack(pady=5, anchor="w")

        # Right Frame
        self.right_frame = tk.Frame(self.main_frame, 
                                    bg=self.white).pack(side="right", 
                                                        expand=True, 
                                                        fill="both", 
                                                        padx=(10, 0))

        # ---------------- Left Side

        # Excel 1 Label
        tk.Label(self.excel1_btn_frame, 
                 text="Reseller Informationen:", 
                 font=("Arial", 12, "bold"),
                 bg=self.white, 
                 fg=self.black).pack(anchor="w", pady=5)
        
        # Excel 1 Load Button
        tk.Button(self.excel1_btn_frame, 
                  text="Durchsuchen", 
                  bg=self.white, 
                  fg=self.black,
                  command=lambda: lists.load_excel(self, "Button 1")).pack(side="left", 
                                                                           padx=(0, 5))
        
        # Excel 1 View Button
        tk.Button(self.excel1_btn_frame, 
                  text="Aufrufen", 
                  bg=self.white, 
                  fg=self.black,
                  command=lambda: self.display_treeview(lists.df1, 1)).pack(side="left")

        # Excel 2 Label
        tk.Label(self.excel2_btn_frame, 
                 text="Renewal Overview:", 
                 font=("Arial", 12, "bold"),
                 bg=self.white, 
                 fg=self.black).pack(anchor="w", pady=5)
        
        # Excel 2 Load Button
        tk.Button(self.excel2_btn_frame, 
                  text="Durchsuchen", 
                  bg=self.white, 
                  fg=self.black,
                  command=lambda: lists.load_excel(self, "Button 2")).pack(side="left", padx=(0, 5))
        
        # Excel 2 View Button
        tk.Button(self.excel2_btn_frame, 
                  text="Aufrufen", 
                  bg=self.white, 
                  fg=self.black,
                  command=lambda: self.display_treeview(lists.df2, 2)).pack(side="left")

        # Mail Label
        tk.Label(self.left_frame, 
                 text="User-Mail:", 
                 font=("Arial", 12, "bold"),
                 bg=self.white, 
                 fg=self.black).pack(anchor="w", pady=5)
        
        # Mail Entry
        self.user = tk.Entry(self.left_frame, 
                              width=40, 
                              bg=self.offwhite, 
                              relief="groove").pack(pady=2)

        # Subject Label
        tk.Label(self.left_frame,
                 text="Betreff:", 
                 font=("Arial", 12, "bold"),
                 bg=self.white, 
                 fg=self.black).pack(anchor="w", pady=5)
        
        # Subject Entry
        self.subject = tk.Entry(self.left_frame, 
                                width=40, 
                                bg=self.offwhite, 
                                relief="groove").pack(pady=2)

        # Body Label
        tk.Label(self.left_frame, 
                 text="Inhalt:", 
                 font=("Arial", 12, "bold"),
                 bg=self.white, 
                 fg=self.black).pack(anchor="w", pady=5)
        
        # Body Text
        self.body = tk.Text(self.left_frame, 
                            height=8, 
                            width=40, 
                            bg=self.offwhite, 
                            relief="groove").pack(pady=2)

        # ---------------- Right Side

        # Adobe Icon (of course not the most legal thing to do)
        try:
            image_path = "ressources/adobe_icon.png"
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"Error with {image_path}")

            original_image = Image.open(image_path)
            resized_image = original_image.resize((100, 100), Image.Resampling.LANCZOS)
            self.logo = ImageTk.PhotoImage(resized_image)

            self.image_label = tk.Label(self.right_frame, image=self.logo, bg=self.white)
            self.image_label.image = self.logo # garbage collection prevention
            self.image_label.pack(pady=5)

        except Exception as e:
            logs.new_error(f"Failed to load image: {e}")
            self.image_label = tk.Label(self.right_frame, text="Bild konnte nicht geladen werden", fg=self.black, bg=self.white)
            self.image_label.pack(pady=5)

        # Info-Check Button
        self.parse_button = tk.Button(self.right_frame, 
                                      text="Infos Laden",
                                      bg=self.white,
                                      fg=self.black, 
                                      width=20, 
                                      command=self.check_info).pack(pady=20)

        # Send Button
        self.send_button = tk.Button(self.right_frame, 
                                     text="Lossenden", 
                                     bg=self.white,
                                     fg=self.black, 
                                     width=20, 
                                     command=authentication.placeholder).pack(pady=5)

        # Messagebox
        self.status_box = tk.Text(self.right_frame, 
                                  height=10, 
                                  width=50,
                                  state="disabled",
                                  wrap="word", 
                                  bg=self.offwhite).pack(pady=10)

        # ---------------- Other

        # Version Label
        self.version_label = tk.Label(
            self.root,
            text=self.current_version,
            font=("Arial", 8),
            bg=self.offwhite,
            fg=self.grey
        ).place(relx=1.0, 
                rely=1.0, 
                x=-10, 
                y=-5, 
                anchor="se")


    # ---------------- Functions 

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

        logs.new_info("Parse button clicked...")

        user_address = self.get_user()
        subject_info = self.get_subject()
        body_info = self.get_body()

        if all([user_address, subject_info, body_info, self.loaded_data1, self.loaded_data2]):
            self.update_status("Alle Mailinfos wurden geladen...")
            logs.new_info("Mailinfo checked successfully...")
            self.loaded_info = True
        else:
            self.update_status("Nicht alle Informationen wurden angegeben...")
            logs.new_info("Not every mail information was given...")

    def display_treeview(self, df, number) -> None:
        # lag/crash prevention
        if number == 1:
            if not self.loaded_data1:
                self.update_status("Excel noch nicht geladen...")
                return
        else:
            if not self.loaded_data2:
                self.update_status("Excel noch nicht geladen...")
                return
        
        # Toplevel setup
        new_window = tk.Toplevel() 
        new_window.title("Excel Viewing")
        new_window.geometry("800x600")

        # Style setup
        style = ttk.Style()
        style.configure("White.TFrame", background="white")

        # Dataframe Frame
        tree_frame = ttk.Frame(new_window, style="White.TFrame")
        tree_frame.pack(expand=True, 
                        fill="both", 
                        padx=20, 
                        pady=10)

        # Dataframe Treeview
        tree = ttk.Treeview(tree_frame, 
                            columns=list(df.columns), 
                            show="headings", 
                            height=10)

        # Columns
        for col in df.columns:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor=tk.W)

        # Rows
        for _, row in df.iterrows():
            tree.insert("", "end", values=list(row))

        # Dataframe Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.config(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        tree.pack(fill=tk.BOTH, expand=True)