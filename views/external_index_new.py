import math
import customtkinter as ctk
from .base import BaseContent

class ExternalIndexNewView(BaseContent):
    title = "B. Externas · Índices"
    
    def __init__(self, master):
        super().__init__(master)
        
        # Variables de entrada
        self.var_r = ctk.StringVar(value="1000")   # Numero de registros
        self.var_B = ctk.StringVar(value="512")    # Tamaño del bloque
        self.var_lr = ctk.StringVar(value="50")    # Longitud del registro
        self.var_lri = ctk.StringVar(value="15")   # Longitud del registro indice
        self.var_type = ctk.StringVar(value="Primario") # Tipo de indice

        # Frame de Configuración
        self.config_frame = ctk.CTkFrame(self.body)
        self.config_frame.pack(fill="x", padx=10, pady=10)

        # Inputs
        self._create_input(self.config_frame, "Registros (r):", self.var_r, 0, 0)
        self._create_input(self.config_frame, "Tam. Bloque (B):", self.var_B, 0, 2)
        self._create_input(self.config_frame, "Long. Reg (lr):", self.var_lr, 0, 4)
        self._create_input(self.config_frame, "Long. Indice (lri):", self.var_lri, 0, 6)

        # Combo Tipo
        ctk.CTkLabel(self.config_frame, text="Tipo:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.combo_type = ctk.CTkOptionMenu(
            self.config_frame, 
            variable=self.var_type,
            values=["Primario", "Secundario", "Multinivel Primario", "Multinivel Secundario"]
        )
        self.combo_type.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        # Boton Crear
        self.btn_create = ctk.CTkButton(self.config_frame, text="Crear Estructura", command=self.create_structure)
        self.btn_create.grid(row=1, column=2, columnspan=2, padx=10, pady=10)

        # Area de Visualización (Scrollable)
        self.scroll_frame = ctk.CTkScrollableFrame(self.body, orientation="horizontal")
        self.scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.canvas_frame = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        self.canvas_frame.pack(fill="both", expand=True)

    def _create_input(self, parent, text, variable, row, col):
        ctk.CTkLabel(parent, text=text).grid(row=row, column=col, padx=5, pady=5, sticky="e")
        ctk.CTkEntry(parent, textvariable=variable, width=80).grid(row=row, column=col+1, padx=5, pady=5, sticky="w")

    def create_structure(self):
        # Limpiar visualización anterior
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()

        try:
            r = int(self.var_r.get())
            B = int(self.var_B.get())
            lr = int(self.var_lr.get())
            lri = int(self.var_lri.get())
            idx_type = self.var_type.get()
        except ValueError:
            return

        # Calculos Estructura Principal
        bfr = math.floor(B / lr)
        if bfr < 1: bfr = 1
        b = math.ceil(r / bfr)

        # Calculos Indices
        bfri = math.floor(B / lri)
        if bfri < 1: bfri = 1

        levels = [] # Lista de diccionarios con info de cada nivel

        if "Secundario" in idx_type:
            # Indice Secundario (Denso): Apunta a cada registro
            # Numero de entradas = r
            bi = math.ceil(r / bfri)
            levels.append({"name": "Índice Secundario", "blocks": bi, "per_block": bfri, "type": "index"})
        else:
            # Indice Primario (Disperso): Apunta a cada bloque
            # Numero de entradas = b
            bi = math.ceil(b / bfri)
            levels.append({"name": "Índice Primario", "blocks": bi, "per_block": bfri, "type": "index"})

        # Multinivel
        if "Multinivel" in idx_type:
            current_blocks = levels[0]["blocks"]
            level_count = 2
            while current_blocks > 1:
                next_blocks = math.ceil(current_blocks / bfri)
                levels.insert(0, {"name": f"Nivel {level_count}", "blocks": next_blocks, "per_block": bfri, "type": "index"})
                current_blocks = next_blocks
                level_count += 1

        # Agregar Estructura Principal al final
        levels.append({"name": "Estructura Principal", "blocks": b, "per_block": bfr, "type": "main"})

        # Renderizar
        self.render_levels(levels)

    def render_levels(self, levels):
        # Contenedor horizontal para los niveles
        for i, level in enumerate(levels):
            # Frame para cada nivel
            level_frame = ctk.CTkFrame(self.canvas_frame, border_width=2, border_color="gray")
            level_frame.pack(side="left", padx=20, pady=20, fill="y", anchor="n")

            # Titulo del nivel
            ctk.CTkLabel(level_frame, text=level["name"], font=("Arial", 14, "bold")).pack(pady=5)
            
            # Info
            info_text = f"Bloques: {level['blocks']}\nReg/Bloque: {level['per_block']}"
            ctk.CTkLabel(level_frame, text=info_text).pack(pady=2)

            # Representacion de Bloques
            blocks_container = ctk.CTkFrame(level_frame, fg_color="transparent")
            blocks_container.pack(pady=10, padx=10)

            # Primer Bloque
            self.draw_block(blocks_container, 1, level["per_block"], level["type"])

            # Puntos suspensivos si hay mas de 2 bloques
            if level["blocks"] > 2:
                ctk.CTkLabel(blocks_container, text="...", font=("Arial", 20)).pack(pady=5)
            
            # Ultimo Bloque (si hay mas de 1)
            if level["blocks"] > 1:
                self.draw_block(blocks_container, level["blocks"], level["per_block"], level["type"])

            # Flecha hacia el siguiente nivel (si no es el ultimo)
            if i < len(levels) - 1:
                arrow = ctk.CTkLabel(self.canvas_frame, text="➔", font=("Arial", 30))
                arrow.pack(side="left", pady=100)

    def draw_block(self, parent, block_num, items_per_block, type_str):
        # Frame del bloque
        block_frame = ctk.CTkFrame(parent, border_width=1, border_color="white")
        block_frame.pack(pady=5, fill="x")

        ctk.CTkLabel(block_frame, text=f"Bloque {block_num}", font=("Arial", 10, "bold")).pack(side="left", padx=5)
        
        # Contenido del bloque (Registros)
        content_frame = ctk.CTkFrame(block_frame, fg_color="transparent")
        content_frame.pack(side="right", padx=5)

        # Primer registro
        self.draw_record(content_frame, 1, type_str)

        # Puntos suspensivos si hay muchos registros
        if items_per_block > 2:
             ctk.CTkLabel(content_frame, text="...", font=("Arial", 8)).pack()

        # Ultimo registro (si hay mas de 1)
        if items_per_block > 1:
            self.draw_record(content_frame, items_per_block, type_str)

    def draw_record(self, parent, rec_num, type_str):
        f = ctk.CTkFrame(parent, border_width=1, height=20, width=100)
        f.pack(pady=1)
        
        if type_str == "index":
            txt = f"Idx {rec_num} | Ptr"
        else:
            txt = f"Reg {rec_num} | Data"
            
        ctk.CTkLabel(f, text=txt, font=("Arial", 9)).place(relx=0.5, rely=0.5, anchor="center")

