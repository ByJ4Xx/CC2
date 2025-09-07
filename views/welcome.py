import customtkinter as ctk
from .base import BaseContent


class WelcomeContent(BaseContent):
    title = "Inicio"

    def __init__(self, master, on_nav=None):
        super().__init__(master)

        self.on_nav = on_nav
        self.body.grid_columnconfigure(0, weight=1)
        for r in range(3):
            self.body.grid_rowconfigure(r, weight=0)
        self.body.grid_rowconfigure(3, weight=1)

        # Título azul
        title = ctk.CTkLabel(
            self.body,
            text="Ciencias de la Computacion 2",
            font=("", 24, "bold"),
            text_color=("#1565c0", "#90caf9"),
        )
        title.grid(row=0, column=0, sticky="w", padx=8, pady=(8, 12))

        subtitle = ctk.CTkLabel(
            self.body,
            text="Accesos rápidos a los apartados:",
        )
        subtitle.grid(row=1, column=0, sticky="w", padx=8, pady=(0, 8))

        # Botones de acceso rápido
        btns = ctk.CTkFrame(self.body)
        btns.grid(row=2, column=0, sticky="w", padx=8, pady=(0, 8))

        def go(key: str):
            if callable(self.on_nav):
                self.on_nav(key)

        b1 = ctk.CTkButton(btns, text="B. Internas · Lineal", command=lambda: go("internas:lineal"))
        b2 = ctk.CTkButton(btns, text="B. Internas · Binaria", command=lambda: go("internas:binaria"))
        b3 = ctk.CTkButton(btns, text="B. Internas · F. Hash", command=lambda: go("internas:hash"))
        b1.grid(row=0, column=0, padx=(0, 8), pady=4)
        b2.grid(row=0, column=1, padx=(0, 8), pady=4)
        b3.grid(row=0, column=2, padx=(0, 8), pady=4)
