try:
    import threading
    import tkinter as tk
    from tkinter import ttk
    import tkcalendar as tkc
    from PIL import Image, ImageTk
    import lists
    import authentication
    import logs
    import os
except ImportError as e:
    print(f"Error importing modules: {e}")
    logs.new_error(f"Error importing modules: {e}")

class UserInterface():
    def __init__(self):
        self.loaded_data1 = False # indicates whether excel 1 was loaded
        self.loaded_data2 = False # indicates whether excel 2 was loaded
        self.loaded_info = False # indicates whether the mail information + excels were loaded

        self.current_version = "v1.0" # current version of application

        # custom colors
        self.red = "#ed1c24"
        self.black = "black"
        self.white = "white"
        self.grey = "grey"
        self.offwhite = "#f5f5f5"

        # root setup
        self.root = tk.Tk()
        self.root.title("Adobe Renewal Mailing")
        self.root.geometry("1200x800")
        self.root.configure(bg=self.offwhite)

        # title label
        self.title_label = tk.Label(
            self.root,
            text="Adobe Automation: Renewal Mails",
            font=("Arial", 24, "bold"),
            fg=self.black,
            bg=self.red
        )
        self.title_label.pack(fill="x", pady=(0, 10))

        # ---------------- Frames

        # main frame
        self.main_frame = tk.Frame(self.root, bg=self.offwhite)
        self.main_frame.pack(expand=True, fill="both", padx=20, pady=10)

        # left frame
        self.left_frame = tk.Frame(self.main_frame, bg=self.white)
        self.left_frame.pack(side="left", expand=True, fill="both", padx=(0, 10))

        # right frame
        self.right_frame = tk.Frame(self.main_frame, bg=self.white)
        self.right_frame.pack(side="right", expand=True,  fill="both", padx=(10, 0))

        # ---------------- Left Side
        
        # date frame
        self.date_frame = tk.Frame(self.left_frame, bg=self.white)
        self.date_frame.pack(anchor="w", pady=2)

        # date label
        tk.Label(self.date_frame,
                 text="Zeitraum definieren:", 
                 font=("Arial", 12, "bold"),
                 bg=self.white,
                 fg=self.black).pack(anchor="w", pady=2, padx=10)

        # date input frame
        self.date_input_frame = tk.Frame(self.date_frame, bg=self.white)
        self.date_input_frame.pack(anchor="w", pady=2, padx=10)

        # date entry
        self.enddate = tkc.DateEntry(
                    self.date_input_frame,
                    width=12,
                    background=self.grey,
                    foreground=self.white,
                    borderwidth=1,
                    date_pattern='dd-mm-y'
        )
        self.enddate.pack(pady=2, side="left", fill="x", expand=True)

        # date checkbutton + variable
        self.duedate_value = tk.BooleanVar(value=False)

        self.duedate_checkbox = tk.Checkbutton(
                    self.date_input_frame,
                    text="Stichtag verwenden",
                    variable=self.duedate_value,
                    bg=self.white,
                    fg=self.black,
                    font=("Arial", 10)
        )
        self.duedate_checkbox.pack(side="left", padx=10)

        # Excel button frame 1
        self.excel1_btn_frame = tk.Frame(self.left_frame, bg=self.white)
        self.excel1_btn_frame.pack(pady=5, anchor="w")

        # Excel 1 label
        tk.Label(self.excel1_btn_frame, 
                 text="Reseller Informationen:", 
                 font=("Arial", 12, "bold"),
                 bg=self.white, 
                 fg=self.black).pack(anchor="w", pady=5, padx=10)
        
        # Excel 1 load button
        tk.Button(self.excel1_btn_frame, 
                  text="Durchsuchen", 
                  bg=self.white, 
                  fg=self.black,
                  command=lambda: lists.load_excel(self, "Button 1")).pack(side="left", padx=10)

        # Excel button frame 2
        self.excel2_btn_frame = tk.Frame(self.left_frame, bg=self.white)
        self.excel2_btn_frame.pack(pady=5, anchor="w")

        # Excel 2 label
        tk.Label(self.excel2_btn_frame, 
                 text="Renewal Overview:", 
                 font=("Arial", 12, "bold"),
                 bg=self.white, 
                 fg=self.black).pack(anchor="w", pady=5, padx=10)
        
        # Excel 2 load button
        tk.Button(self.excel2_btn_frame, 
                  text="Durchsuchen", 
                  bg=self.white, 
                  fg=self.black,
                  command=lambda: lists.load_excel(self, "Button 2")).pack(side="left", padx=10)

        # Excel view button
        tk.Button(self.left_frame, 
                  text="Listen Aufrufen", 
                  bg=self.white, 
                  fg=self.black,
                  command=lambda: self.display_treeview(lists.df_merged)).pack(anchor="w", pady=15, padx=10)

        # mail label
        tk.Label(self.left_frame, 
                 text="User-Mail:", 
                 font=("Arial", 12, "bold"),
                 bg=self.white, 
                 fg=self.black).pack(anchor="w", pady=5, padx=10)

        # mail entry
        self.user = tk.Entry(self.left_frame, 
                             width=40, 
                             bg=self.offwhite, 
                             relief="groove")
        self.user.pack(fill="x", padx=10)

        # subject label
        tk.Label(self.left_frame,
                 text="Betreff:", 
                 font=("Arial", 12, "bold"),
                 bg=self.white, 
                 fg=self.black).pack(anchor="w", pady=5, padx=10)

        # subject entry
        self.subject = tk.Entry(self.left_frame, 
                                width=40, 
                                bg=self.offwhite, 
                                relief="groove")
        self.subject.pack(fill="x", padx=10)

        # body label
        tk.Label(self.left_frame, 
                 text="Inhalt:", 
                 font=("Arial", 12, "bold"),
                 bg=self.white, 
                 fg=self.black).pack(anchor="w", pady=5, padx=10)

        # body text
        self.body = tk.Text(self.left_frame, 
                            height=8, 
                            width=40, 
                            bg=self.offwhite, 
                            relief="groove")
        self.body.pack(fill="both", expand=True, padx=10, pady=5)
        
        # ---------------- Right Side

        # Icon
        try:
            image_path = "ressources/adobe_logo.png"

            if not os.path.exists(image_path):
                raise FileNotFoundError(f"Error with {image_path}")

            original_image = Image.open(image_path)
            resized_image = original_image.resize((100, 100), Image.LANCZOS)
            self.logo = ImageTk.PhotoImage(resized_image)

            self.image_label = tk.Label(self.right_frame, image=self.logo, bg=self.white)
            self.image_label.image = self.logo # garbage collection prevention
            self.image_label.pack(pady=5)

        except Exception as e:
            logs.new_error(f"Failed to load image: {e}")
            self.image_label = tk.Label(self.right_frame, text="Bild konnte nicht geladen werden", fg=self.black, bg=self.white)
            self.image_label.pack(pady=5)

        # info-check button
        self.parse_button = tk.Button(self.right_frame, 
                                      text="Infos Laden",
                                      bg=self.white,
                                      fg=self.black, 
                                      width=20, 
                                      command=self.check_info)
        self.parse_button.pack(pady=20)

        # send button
        self.send_button = tk.Button(self.right_frame, 
                                     text="Lossenden", 
                                     bg=self.white,
                                     fg=self.black, 
                                     width=20, 
                                     )
        self.send_button.pack(pady=5)
        
        # messagebox
        self.status_box = tk.Text(self.right_frame, 
                                  height=10, 
                                  width=50,
                                  state="disabled",
                                  wrap="word", 
                                  bg=self.offwhite)
        self.status_box.pack(pady=10, padx=30, fill="both", expand=True)

        # ---------------- Other

        # version label
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

    def get_enddate(self) -> str:
        """
        Get function to retrieve the enddate -specified in the ui- that is needed for filtering the dataframes

        Returns:
            str: the current enddate
        """

        return self.enddate.get()
        
    def get_mail_info(self) -> list:
        """
        Combines all the other get functions into a list of the mail information currently given

        Returns:
            list[str]: a list of strings containing the mail information given
        """
        return [self.get_user(), self.get_subject(), self.get_body()]
    
    def get_duedate_info(self) -> bool:
        """
        Get function to retrieve the duedate checkbox value

        Returns:
            bool: the current value of the duedate checkbox
        """
        return self.duedate_value.get()

    def check_info(self) -> None:
        """
        Checks whether all the mail information was given by the user, sets loaded_info True if that's the case
        """

        logs.new_info("Parse button clicked...")

        user_address = self.get_user()
        subject_info = self.get_subject()
        body_info = self.get_body()

        if all([user_address, subject_info, body_info, self.loaded_data1, self.loaded_data2]): # if all information is not empty
            self.update_status("Alle Mailinfos wurden geladen...")
            logs.new_info("Mailinfo checked successfully...")
            self.loaded_info = True # sets loaded_info to True, so the send button can be used
        else:
            self.update_status("Nicht alle Informationen wurden angegeben...")
            logs.new_info("Not every mail information was given...")

    def display_treeview(self, df:object) -> None:
        """
        Function to display the loaded and merged dataframes/excel files in a comprehensive treeview

        Args:
            df (object): panda dataframe object
        """

        # lag/crash prevention to check whether both lists was loaded
        if not all([self.loaded_data1, self.loaded_data2]):
            threading.Thread(target=lambda: self.update_status("Excel noch nicht geladen..."), daemon=True).start()
            return
        
        # toplevel setup
        new_window = tk.Toplevel() 
        new_window.title("Excel Viewing")
        new_window.geometry("1000x800")

        # style setup
        style = ttk.Style()
        style.configure("White.TFrame", background="white")

        # dataframe frame
        tree_frame = ttk.Frame(new_window, style="White.TFrame")
        tree_frame.pack(expand=True, 
                        fill="both", 
                        padx=20, 
                        pady=10)

        # dataframe treeview
        tree = ttk.Treeview(tree_frame, 
                            columns=list(df.columns), 
                            show="headings", 
                            height=10)

        # columns
        for col in df.columns:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor=tk.W)

        # rows
        for row in df.to_dict('records'):
            tree.insert("", "end", values=list(row.values()))

        # vertical scrollbar
        v_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.config(yscrollcommand=v_scrollbar.set)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # horizontal scrollbar
        h_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal", command=tree.xview)
        tree.config(xscrollcommand=h_scrollbar.set)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        tree.pack(fill=tk.BOTH, expand=True)