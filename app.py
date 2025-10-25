import customtkinter as ctk

from ui.sidebar import CollapsibleSidebar
from ui.header import HeaderBar
from views.welcome import WelcomeContent
from views.lineal import LinealContent
from views.binaria import BinariaContent
from views.hash_view import HashContent
from views.digital import DigitalContent
from views.external_sequential import ExternalSequentialContent
from views.external_binary import ExternalBinaryContent
from views.residue import ResidueContent


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Algoritmos · Búsquedas y Grafos")
        self.geometry("1100x700")

        # Apariencia y tema
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("dark-blue")

        # Layout principal
        self.grid_columnconfigure(0, weight=0)  # sidebar
        self.grid_columnconfigure(1, weight=1)  # content
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        # Sidebar
        self.sidebar = CollapsibleSidebar(self, on_select=self.handle_select)
        self.sidebar.grid(row=1, column=0, sticky="nsw")

        # Content wrapper + header
        self.content_wrapper = ctk.CTkFrame(self, corner_radius=0)
        self.content_wrapper.grid(row=1, column=1, sticky="nsew")
        self.content_wrapper.grid_rowconfigure(0, weight=0)
        self.content_wrapper.grid_rowconfigure(1, weight=1)
        self.content_wrapper.grid_columnconfigure(0, weight=1)

        self.header = HeaderBar(self.content_wrapper, on_theme_change=self.change_theme)
        self.header.grid(row=0, column=0, sticky="ew")

        self.content_container = ctk.CTkFrame(self.content_wrapper)
        self.content_container.grid(row=1, column=0, sticky="nsew")
        self.content_container.grid_rowconfigure(0, weight=1)
        self.content_container.grid_columnconfigure(0, weight=1)

        # Contenidos
        self.current_content = None
        self.contents = {
            "welcome": WelcomeContent(self.content_container, on_nav=self.show_content),
            "internas:lineal": LinealContent(self.content_container),
            "internas:binaria": BinariaContent(self.content_container),
            "internas:hash": HashContent(self.content_container),
            "internas:digital": DigitalContent(self.content_container),
            "internas:residuo": ResidueContent(self.content_container),
            "externas:secuencial": ExternalSequentialContent(self.content_container),
            "externas:binaria": ExternalBinaryContent(self.content_container),
        }

        self.show_content("welcome")

    def handle_select(self, section: str, item: str):
        key = f"{section}:{item}"
        self.show_content(key)

    def show_content(self, key: str):
        if self.current_content is not None:
            self.current_content.grid_remove()
        content = self.contents.get(key) or self.contents["welcome"]
        content.grid(row=0, column=0, sticky="nsew")
        self.current_content = content
        # Update header and sidebar selection
        title = getattr(content, "title", "")
        self.header.set_title(title)
        self.sidebar.set_selected(key)

    def change_theme(self, mode_label: str):
        mapping = {"Sistema": "System", "Claro": "Light", "Oscuro": "Dark"}
        ctk.set_appearance_mode(mapping.get(mode_label, "System"))


def main():
    app = App()
    app.mainloop()
