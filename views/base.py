import customtkinter as ctk


class BaseContent(ctk.CTkFrame):
    title: str = ""

    def __init__(self, master):
        super().__init__(master)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.body = ctk.CTkFrame(self)
        self.body.grid(row=0, column=0, sticky="nsew", padx=16, pady=16)
        self.body.columnconfigure(0, weight=1)

