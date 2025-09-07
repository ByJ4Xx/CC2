import customtkinter as ctk


class HeaderBar(ctk.CTkFrame):
    def __init__(self, master, on_theme_change):
        super().__init__(master, corner_radius=0)
        self.on_theme_change = on_theme_change
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)

        self.title_label = ctk.CTkLabel(self, text="", font=("", 16, "bold"))
        self.title_label.grid(row=0, column=0, sticky="w", padx=16, pady=12)

        self.theme_selector = ctk.CTkOptionMenu(
            self,
            values=["Sistema", "Claro", "Oscuro"],
            command=self.on_theme_change,
            width=140,
        )
        self.theme_selector.set("Sistema")
        self.theme_selector.grid(row=0, column=1, sticky="e", padx=16, pady=12)

    def set_title(self, title: str):
        self.title_label.configure(text=title or "")

