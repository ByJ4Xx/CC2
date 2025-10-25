import customtkinter as ctk


class CollapsibleSidebar(ctk.CTkFrame):
    def __init__(self, master, on_select):
        super().__init__(master)
        self.on_select = on_select

        self.expanded = True
        self.expanded_width = 260
        self.collapsed_width = 56

        self.grid_propagate(False)
        self.configure(width=self.expanded_width)
        self.columnconfigure(0, weight=1)

        # Top bar with hamburger
        self.top_bar = ctk.CTkFrame(self, corner_radius=0)
        self.top_bar.grid(row=0, column=0, sticky="ew", padx=0, pady=(0, 8))
        self.top_bar.columnconfigure(0, weight=1)

        self.toggle_btn = ctk.CTkButton(
            self.top_bar,
            text="☰",
            width=40,
            height=36,
            corner_radius=8,
            command=self.toggle,
        )
        self.toggle_btn.grid(row=0, column=0, sticky="w", padx=8, pady=8)

        # Sections container
        self.sections_container = ctk.CTkFrame(self, fg_color=("#f2f4f8", "#0e1621"))
        self.sections_container.grid(row=1, column=0, sticky="nsew")
        self.rowconfigure(1, weight=1)
        self.sections_container.columnconfigure(0, weight=1)

        # B. Internas
        self.btn_internas = ctk.CTkButton(
            self.sections_container,
            text="B. Internas",
            height=38,
            corner_radius=8,
            command=self._toggle_internas,
        )
        self.btn_internas.grid(row=0, column=0, sticky="ew", padx=8, pady=(0, 4))

        self.panel_internas = ctk.CTkFrame(self.sections_container, fg_color="transparent")
        self.panel_internas.grid(row=1, column=0, sticky="ew", padx=8, pady=(0, 8))
        self.panel_internas.columnconfigure(0, weight=1)

        self.btn_lineal = ctk.CTkButton(
            self.panel_internas,
            text="Lineal",
            height=34,
            fg_color="transparent",
            hover_color=("#e5f0ff", "#16324a"),
            corner_radius=8,
            anchor="w",
            command=lambda: self.on_select("internas", "lineal"),
        )
        self.btn_lineal.grid(row=0, column=0, sticky="ew", padx=8, pady=(8, 4))

        self.btn_binaria = ctk.CTkButton(
            self.panel_internas,
            text="Binaria",
            height=34,
            fg_color="transparent",
            hover_color=("#e5f0ff", "#16324a"),
            corner_radius=8,
            anchor="w",
            command=lambda: self.on_select("internas", "binaria"),
        )
        self.btn_binaria.grid(row=1, column=0, sticky="ew", padx=8, pady=4)

        self.btn_hash = ctk.CTkButton(
            self.panel_internas,
            text="F. Hash",
            height=34,
            fg_color="transparent",
            hover_color=("#e5f0ff", "#16324a"),
            corner_radius=8,
            anchor="w",
            command=lambda: self.on_select("internas", "hash"),
        )
        self.btn_hash.grid(row=2, column=0, sticky="ew", padx=8, pady=(4, 8))

        self.btn_digital = ctk.CTkButton(
            self.panel_internas,
            text="Árbol Digital",
            height=34,
            fg_color="transparent",
            hover_color=("#e5f0ff", "#16324a"),
            corner_radius=8,
            anchor="w",
            command=lambda: self.on_select("internas", "digital"),
        )
        self.btn_digital.grid(row=3, column=0, sticky="ew", padx=8, pady=(4, 8))

        self.btn_residuo = ctk.CTkButton(
            self.panel_internas,
            text="Residuo",
            height=34,
            fg_color="transparent",
            hover_color=("#e5f0ff", "#16324a"),
            corner_radius=8,
            anchor="w",
            command=lambda: self.on_select("internas", "residuo"),
        )
        self.btn_residuo.grid(row=4, column=0, sticky="ew", padx=8, pady=(4, 8))

        # B. Externas
        self.btn_externas = ctk.CTkButton(
            self.sections_container,
            text="B. Externas",
            height=38,
            corner_radius=8,
            command=self._toggle_externas,
        )
        self.btn_externas.grid(row=2, column=0, sticky="ew", padx=8, pady=(0, 4))

        self.panel_externas = ctk.CTkFrame(self.sections_container, fg_color="transparent")
        self.panel_externas.grid(row=3, column=0, sticky="ew", padx=8, pady=(0, 8))
        self.panel_externas.columnconfigure(0, weight=1)

        self.btn_ext_seq = ctk.CTkButton(
            self.panel_externas,
            text="Secuencial",
            height=34,
            fg_color="transparent",
            hover_color=("#e5f0ff", "#16324a"),
            corner_radius=8,
            anchor="w",
            command=lambda: self.on_select("externas", "secuencial"),
        )
        self.btn_ext_seq.grid(row=0, column=0, sticky="ew", padx=8, pady=(8, 4))

        self.btn_ext_bin = ctk.CTkButton(
            self.panel_externas,
            text="Binaria",
            height=34,
            fg_color="transparent",
            hover_color=("#e5f0ff", "#16324a"),
            corner_radius=8,
            anchor="w",
            command=lambda: self.on_select("externas", "binaria"),
        )
        self.btn_ext_bin.grid(row=1, column=0, sticky="ew", padx=8, pady=(4, 8))

        # Grafos
        self.btn_grafos = ctk.CTkButton(
            self.sections_container,
            text="Grafos",
            height=38,
            corner_radius=8,
            command=self._toggle_grafos,
        )
        self.btn_grafos.grid(row=4, column=0, sticky="ew", padx=8, pady=(0, 4))

        self.panel_grafos = ctk.CTkFrame(self.sections_container, fg_color="transparent")
        self.panel_grafos.grid(row=5, column=0, sticky="ew", padx=8, pady=(0, 8))
        self.panel_grafos.columnconfigure(0, weight=1)
        ctk.CTkLabel(self.panel_grafos, text="Próximamente…").grid(
            row=0, column=0, sticky="ew", padx=8, pady=8
        )

        self._collapse_panel(self.panel_externas)
        self._collapse_panel(self.panel_grafos)

        # For selection highlighting
        self.sub_buttons = {
            "internas:lineal": self.btn_lineal,
            "internas:binaria": self.btn_binaria,
            "internas:hash": self.btn_hash,
            "internas:digital": self.btn_digital,
            "internas:residuo": self.btn_residuo,
            "externas:secuencial": self.btn_ext_seq,
            "externas:binaria": self.btn_ext_bin,
        }

    def toggle(self):
        self.expanded = not self.expanded
        if self.expanded:
            self.configure(width=self.expanded_width)
            self.grid_propagate(False)
            self._set_button_texts(True)
            self.sections_container.grid(row=1, column=0, sticky="nsew")
        else:
            self.configure(width=self.collapsed_width)
            self.grid_propagate(False)
            self._set_button_texts(False)
            self.sections_container.grid_remove()
            self._collapse_panel(self.panel_internas)
            self._collapse_panel(self.panel_externas)
            self._collapse_panel(self.panel_grafos)

    def _set_button_texts(self, expanded: bool):
        if expanded:
            self.btn_internas.configure(text="B. Internas")
            self.btn_externas.configure(text="B. Externas")
            self.btn_grafos.configure(text="Grafos")
        else:
            # Hidden container, keep full text for when it reappears
            pass

    def _toggle_internas(self):
        self._toggle_panel(self.panel_internas)

    def _toggle_externas(self):
        self._toggle_panel(self.panel_externas)

    def _toggle_grafos(self):
        self._toggle_panel(self.panel_grafos)

    def _toggle_panel(self, panel: ctk.CTkFrame):
        if panel.winfo_ismapped():
            self._collapse_panel(panel)
        else:
            panel.grid()

    def _collapse_panel(self, panel: ctk.CTkFrame):
        panel.grid_remove()

    def set_selected(self, key: str):
        for _, btn in self.sub_buttons.items():
            btn.configure(fg_color="transparent")
        btn = self.sub_buttons.get(key)
        if btn is not None:
            btn.configure(fg_color=("#cfe6ff", "#133b5c"), text_color=("#0a0a0a", "white"))

