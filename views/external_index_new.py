import math
import json
import tkinter.filedialog as fd
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
        
        # Variable de Zoom
        self.scale_factor = 1.0

        # Frame de Configuración
        self.config_frame = ctk.CTkFrame(self.body)
        self.config_frame.pack(fill="x", padx=10, pady=10)

        # Inputs
        self._create_input(self.config_frame, "Registros (r):", self.var_r, 0, 0)
        self._create_input(self.config_frame, "Tam. Bloque (B):", self.var_B, 0, 2)
        self._create_input(self.config_frame, "Long. Reg (lr):", self.var_lr, 0, 4)
        self._create_input(self.config_frame, "Long. Indice (lri):", self.var_lri, 0, 6)

        # Fila 2: Tipo, Botones y Zoom
        ctk.CTkLabel(self.config_frame, text="Tipo:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.combo_type = ctk.CTkOptionMenu(
            self.config_frame, 
            variable=self.var_type,
            values=["Primario", "Secundario", "Multinivel Primario", "Multinivel Secundario"]
        )
        self.combo_type.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        # Botones de Acción
        btn_frame = ctk.CTkFrame(self.config_frame, fg_color="transparent")
        btn_frame.grid(row=1, column=2, columnspan=3, padx=5, pady=5)

        self.btn_create = ctk.CTkButton(btn_frame, text="Crear", command=self.create_structure, width=80)
        self.btn_create.pack(side="left", padx=2)
        
        self.btn_save = ctk.CTkButton(btn_frame, text="Guardar JSON", command=self.save_json, width=80, fg_color="green")
        self.btn_save.pack(side="left", padx=2)
        
        self.btn_load = ctk.CTkButton(btn_frame, text="Cargar JSON", command=self.load_json, width=80, fg_color="orange")
        self.btn_load.pack(side="left", padx=2)

        self.btn_clear = ctk.CTkButton(btn_frame, text="Limpiar", command=self.clear_view, width=80, fg_color="red")
        self.btn_clear.pack(side="left", padx=2)

        # Control de Zoom
        zoom_frame = ctk.CTkFrame(self.config_frame, fg_color="transparent")
        zoom_frame.grid(row=1, column=5, columnspan=2, padx=5, pady=5)
        ctk.CTkLabel(zoom_frame, text="Zoom:").pack(side="left", padx=2)
        self.slider_zoom = ctk.CTkSlider(zoom_frame, from_=0.5, to=2.0, number_of_steps=15, command=self.update_zoom)
        self.slider_zoom.set(1.0)
        self.slider_zoom.pack(side="left", padx=5)

        # Area de Visualización (Scrollable)
        self.scroll_frame = ctk.CTkScrollableFrame(self.body, orientation="horizontal")
        self.scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.canvas_frame = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        self.canvas_frame.pack(fill="both", expand=True)
        
        # Guardar datos calculados para redibujar al hacer zoom
        self.last_levels_data = None

    def _create_input(self, parent, text, variable, row, col):
        ctk.CTkLabel(parent, text=text).grid(row=row, column=col, padx=5, pady=5, sticky="e")
        ctk.CTkEntry(parent, textvariable=variable, width=80).grid(row=row, column=col+1, padx=5, pady=5, sticky="w")

    def update_zoom(self, value):
        self.scale_factor = float(value)
        if self.last_levels_data:
            self.render_levels(self.last_levels_data)

    def save_json(self):
        data = {
            "r": self.var_r.get(),
            "B": self.var_B.get(),
            "lr": self.var_lr.get(),
            "lri": self.var_lri.get(),
            "type": self.var_type.get()
        }
        path = fd.asksaveasfilename(defaultextension=".json", filetypes=[("JSON", "*.json")])
        if path:
            try:
                with open(path, "w") as f:
                    json.dump(data, f, indent=4)
            except Exception as e:
                print(f"Error saving: {e}")

    def load_json(self):
        path = fd.askopenfilename(filetypes=[("JSON", "*.json")])
        if path:
            try:
                with open(path, "r") as f:
                    data = json.load(f)
                self.var_r.set(data.get("r", "1000"))
                self.var_B.set(data.get("B", "512"))
                self.var_lr.set(data.get("lr", "50"))
                self.var_lri.set(data.get("lri", "15"))
                self.var_type.set(data.get("type", "Primario"))
                self.create_structure()
            except Exception as e:
                print(f"Error loading: {e}")

    def clear_view(self):
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()
        self.last_levels_data = None

    def create_structure(self):
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
        
        # Items en el ultimo bloque principal
        last_block_items_main = r % bfr
        if last_block_items_main == 0: last_block_items_main = bfr

        # Calculos Indices
        bfri = math.floor(B / lri)
        if bfri < 1: bfri = 1

        levels = [] # Lista de diccionarios con info de cada nivel

        if "Secundario" in idx_type:
            # Indice Secundario (Denso): Apunta a cada registro
            # Numero de entradas = r
            bi = math.ceil(r / bfri)
            last_block_items_idx = r % bfri
            if last_block_items_idx == 0: last_block_items_idx = bfri
            
            levels.append({
                "name": "Índice Secundario", 
                "blocks": bi, 
                "per_block": bfri, 
                "last_block_items": last_block_items_idx,
                "type": "index"
            })
        else:
            # Indice Primario (Disperso): Apunta a cada bloque
            # Numero de entradas = b
            bi = math.ceil(b / bfri)
            last_block_items_idx = b % bfri
            if last_block_items_idx == 0: last_block_items_idx = bfri
            
            levels.append({
                "name": "Índice Primario", 
                "blocks": bi, 
                "per_block": bfri, 
                "last_block_items": last_block_items_idx,
                "type": "index"
            })

        # Multinivel
        if "Multinivel" in idx_type:
            # El nivel mas bajo (ya agregado) apunta a la estructura principal (o registros)
            # Los niveles superiores apuntan a los bloques del nivel inferior
            current_blocks = levels[0]["blocks"]
            level_count = 2
            while current_blocks > 1:
                next_blocks = math.ceil(current_blocks / bfri)
                last_items = current_blocks % bfri
                if last_items == 0: last_items = bfri
                
                levels.insert(0, {
                    "name": f"Nivel {level_count}", 
                    "blocks": next_blocks, 
                    "per_block": bfri, 
                    "last_block_items": last_items,
                    "type": "index"
                })
                current_blocks = next_blocks
                level_count += 1

        # Agregar Estructura Principal al final
        levels.append({
            "name": "Estructura Principal", 
            "blocks": b, 
            "per_block": bfr, 
            "last_block_items": last_block_items_main,
            "type": "main"
        })

        self.last_levels_data = levels
        self.render_levels(levels)

    def render_levels(self, levels):
        # Limpiar visualización anterior
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()

        s = self.scale_factor
        
        # Contenedor horizontal para los niveles
        for i, level in enumerate(levels):
            # Frame para cada nivel
            level_frame = ctk.CTkFrame(self.canvas_frame, border_width=int(2*s), border_color="gray")
            level_frame.pack(side="left", padx=int(20*s), pady=int(20*s), fill="y", anchor="n")

            # Titulo del nivel
            ctk.CTkLabel(level_frame, text=level["name"], font=("Arial", int(14*s), "bold")).pack(pady=int(5*s))
            
            # Info
            info_text = f"Bloques: {level['blocks']}\nReg/Bloque: {level['per_block']}"
            ctk.CTkLabel(level_frame, text=info_text, font=("Arial", int(12*s))).pack(pady=int(2*s))

            # Representacion de Bloques
            blocks_container = ctk.CTkFrame(level_frame, fg_color="transparent")
            blocks_container.pack(pady=int(10*s), padx=int(10*s))

            # Primer Bloque (siempre lleno o con lo que tenga si es el unico)
            first_block_items = level["per_block"] if level["blocks"] > 1 else level["last_block_items"]
            # Start ID para bloque 1 es siempre 1
            self.draw_block(blocks_container, 1, first_block_items, level["type"], start_id=1)

            # Puntos suspensivos si hay mas de 2 bloques
            if level["blocks"] > 2:
                ctk.CTkLabel(blocks_container, text="...", font=("Arial", int(20*s))).pack(pady=int(5*s))
            
            # Ultimo Bloque (si hay mas de 1)
            if level["blocks"] > 1:
                # Start ID para el ultimo bloque
                last_start_id = (level["blocks"] - 1) * level["per_block"] + 1
                self.draw_block(blocks_container, level["blocks"], level["last_block_items"], level["type"], start_id=last_start_id)

            # Flecha hacia el siguiente nivel (si no es el ultimo)
            if i < len(levels) - 1:
                arrow = ctk.CTkLabel(self.canvas_frame, text="➔", font=("Arial", int(30*s)))
                arrow.pack(side="left", pady=int(100*s))

    def draw_block(self, parent, block_num, items_count, type_str, start_id):
        s = self.scale_factor
        # Frame del bloque
        block_frame = ctk.CTkFrame(parent, border_width=max(1, int(1*s)), border_color="white")
        block_frame.pack(pady=int(5*s), fill="x")

        ctk.CTkLabel(block_frame, text=f"Bloque {block_num}", font=("Arial", int(10*s), "bold")).pack(side="left", padx=int(5*s))
        
        # Contenido del bloque (Registros)
        content_frame = ctk.CTkFrame(block_frame, fg_color="transparent")
        content_frame.pack(side="right", padx=int(5*s))

        # Primer registro del bloque
        self.draw_record(content_frame, start_id, type_str)

        # Puntos suspensivos si hay muchos registros
        if items_count > 2:
             ctk.CTkLabel(content_frame, text="...", font=("Arial", int(8*s))).pack()

        # Ultimo registro del bloque (si hay mas de 1)
        if items_count > 1:
            end_id = start_id + items_count - 1
            self.draw_record(content_frame, end_id, type_str)

    def draw_record(self, parent, rec_num, type_str):
        s = self.scale_factor
        f = ctk.CTkFrame(parent, border_width=max(1, int(1*s)), height=int(20*s), width=int(100*s))
        f.pack(pady=1)
        
        if type_str == "index":
            txt = f"Idx {rec_num} | Ptr"
        else:
            txt = f"Reg {rec_num} | Data"
            
        ctk.CTkLabel(f, text=txt, font=("Arial", int(9*s))).place(relx=0.5, rely=0.5, anchor="center")
