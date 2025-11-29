import customtkinter as ctk
from .base import BaseContent


class WelcomeContent(BaseContent):
    title = "Inicio"

    def __init__(self, master, on_nav=None):
        super().__init__(master)

        self.on_nav = on_nav

        # Layout de filas y columnas
        self.body.grid_columnconfigure(0, weight=1)
        self.body.grid_rowconfigure(0, weight=0)
        self.body.grid_rowconfigure(1, weight=0)
        self.body.grid_rowconfigure(2, weight=1)

        # ---------------------------------------------------------
        #  TITULO PRINCIPAL - MÁS GRANDE
        # ---------------------------------------------------------
        title = ctk.CTkLabel(
            self.body,
            text="Ciencias de la Computación 2",
            font=("", 36, "bold"),     # << Título más grande
            text_color=("#0d47a1", "#90caf9"),
        )
        title.grid(row=0, column=0, sticky="nsew", padx=12, pady=(20, 10))

        # ---------------------------------------------------------
        #  SUBTITULO - INSTRUCCIÓN AL USUARIO
        # ---------------------------------------------------------
        subtitle = ctk.CTkLabel(
            self.body,
            text="¡Bienvenido!\nUsa el menú lateral izquierdo para acceder a los apartados de la aplicación.",
            font=("", 18),
            text_color=("#000000", "#ffffff"),
        )
        subtitle.grid(row=1, column=0, sticky="nsew", padx=12, pady=(0, 10))

        # ---------------------------------------------------------
        #  SE ELIMINAN LOS ACCESOS RÁPIDOS COMPLETAMENTE
        # ---------------------------------------------------------
        # No hay botones ni frames adicionales aquí.

