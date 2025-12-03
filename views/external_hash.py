import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import json
import math
from models.external_hash import ExternalHashStructure

class ExternalHashView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.title = "Búsquedas Externas · Hash"
        self.structure = None
        
        # Layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1) # Visualization area expands
        
        # --- Top Control Panel ---
        self.control_panel = ctk.CTkFrame(self)
        self.control_panel.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        self.control_panel.grid_columnconfigure(0, weight=1)
        self.control_panel.grid_columnconfigure(1, weight=1)
        
        # Configuration Section
        self.config_frame = ctk.CTkFrame(self.control_panel, fg_color="transparent")
        self.config_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=5)
        
        ctk.CTkLabel(self.config_frame, text="Configuración Inicial", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=6, sticky="w")
        
        self.entry_n = ctk.CTkEntry(self.config_frame, placeholder_text="Num. Registros (N)")
        self.entry_n.grid(row=1, column=0, padx=4, pady=4, sticky="ew")
        
        self.entry_k = ctk.CTkEntry(self.config_frame, placeholder_text="Longitud Clave (K)")
        self.entry_k.grid(row=1, column=1, padx=4, pady=4, sticky="ew")
        
        self.combo_func = ctk.CTkComboBox(
            self.config_frame, 
            values=["Cuadrado", "Modular", "Plegamiento", "Truncamiento", "Conversion Base"],
            command=self.on_func_change
        )
        self.combo_func.set("Cuadrado")
        self.combo_func.grid(row=1, column=2, padx=4, pady=4, sticky="ew")
        
        # Folding operation selector (visible only for plegamiento)
        self.combo_fold_op = ctk.CTkComboBox(
            self.config_frame,
            values=["Suma", "Multiplicación"],
            state="disabled"
        )
        self.combo_fold_op.set("Suma")
        self.combo_fold_op.grid(row=1, column=3, padx=4, pady=4, sticky="ew")

        self.combo_base = ctk.CTkComboBox(
            self.config_frame,
            values=[str(i) for i in range(2, 10)],
            state="disabled"
        )
        self.combo_base.set("Base (2-9)")
        self.combo_base.grid(row=1, column=4, padx=4, pady=4, sticky="ew")
        
        self.btn_create = ctk.CTkButton(self.config_frame, text="Crear Estructura", command=self.create_structure)
        self.btn_create.grid(row=1, column=5, padx=4, pady=4, sticky="ew")
        
        self.btn_delete_struct = ctk.CTkButton(self.config_frame, text="Borrar Estructura", command=self.delete_structure, fg_color="red", hover_color="darkred")
        
        # Operations Section
        self.ops_frame = ctk.CTkFrame(self.control_panel, fg_color="transparent")
        self.ops_frame.grid(row=0, column=1, sticky="ew", padx=10, pady=5)
        
        ctk.CTkLabel(self.ops_frame, text="Operaciones", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=4, sticky="w")
        
        self.entry_key = ctk.CTkEntry(self.ops_frame, placeholder_text="Clave")
        self.entry_key.grid(row=1, column=0, padx=4, pady=4, sticky="ew")
        
        self.btn_insert = ctk.CTkButton(self.ops_frame, text="Insertar", command=self.insert_key, state="disabled")
        self.btn_insert.grid(row=1, column=1, padx=4, pady=4, sticky="ew")
        
        self.btn_search = ctk.CTkButton(self.ops_frame, text="Buscar", command=self.search_key, state="disabled")
        self.btn_search.grid(row=1, column=2, padx=4, pady=4, sticky="ew")
        
        self.btn_delete_key = ctk.CTkButton(self.ops_frame, text="Eliminar", command=self.delete_key, state="disabled", fg_color="red", hover_color="darkred")
        self.btn_delete_key.grid(row=1, column=3, padx=4, pady=4, sticky="ew")

        # Persistence Section
        # Persistence Section - placed below the control rows
        self.persist_frame = ctk.CTkFrame(self.control_panel, fg_color="transparent")
        self.persist_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=(5,0))
        
        ctk.CTkLabel(self.persist_frame, text="Persistencia", font=("Arial", 14, "bold")).grid(row=0, column=0, sticky="w")
        
        ctk.CTkButton(self.persist_frame, text="Guardar JSON", command=self.save_json).grid(row=0, column=1, padx=6)
        ctk.CTkButton(self.persist_frame, text="Cargar JSON", command=self.load_json).grid(row=0, column=2, padx=6)

        # Highlight tuple for search results (block, 'main'|'collision', idx)
        self.highlight = None

        # --- Visualization Area ---
        self.vis_frame = ctk.CTkScrollableFrame(self)
        self.vis_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        
        self.lbl_info = ctk.CTkLabel(self.vis_frame, text="Cree una estructura para visualizarla.")
        self.lbl_info.pack(pady=20)

    def on_func_change(self, choice):
        if choice == "Conversion Base":
            self.combo_base.configure(state="normal")
            self.combo_base.set("9")
        else:
            self.combo_base.configure(state="disabled")
            self.combo_base.set("Base (2-9)")

        if choice == "Plegamiento":
            self.combo_fold_op.configure(state="normal")
            self.combo_fold_op.set("Suma")
        else:
            self.combo_fold_op.configure(state="disabled")
            self.combo_fold_op.set("Suma")

    def create_structure(self):
        try:
            n = int(self.entry_n.get())
            k = int(self.entry_k.get())
            func_map = {
                "Cuadrado": "cuadrado",
                "Modular": "modular",
                "Plegamiento": "plegamiento",
                "Truncamiento": "truncamiento",
                "Conversion Base": "conversion_base"
            }
            func = func_map[self.combo_func.get()]
            
            base = None
            trunc_positions = None
            folding_op = None

            if func == "conversion_base":
                base_val = self.combo_base.get()
                if not base_val.isdigit():
                    raise ValueError("Seleccione una base válida")
                base = int(base_val)

            # If truncation, open dialog to pick positions
            if func == "truncamiento":
                # Determine number of positions allowed from number of blocks
                blocks = int(math.sqrt(n))
                if blocks == 0:
                    blocks = 1
                allowed = len(str(blocks - 1))
                if allowed == 0:
                    allowed = 1

                sel = []
                dlg = tk.Toplevel(self)
                dlg.title("Seleccionar posiciones de truncamiento")
                tk.Label(dlg, text=f"Seleccione {allowed} posiciones (0..{k-1})").pack(padx=10, pady=6)
                vars = []
                cb_frame = tk.Frame(dlg)
                cb_frame.pack(padx=10, pady=6)
                for i in range(k):
                    v = tk.IntVar(value=0)
                    cb = tk.Checkbutton(cb_frame, text=str(i), variable=v)
                    cb.grid(row=0, column=i, padx=2)
                    vars.append(v)

                def on_ok():
                    chosen = [i for i, vv in enumerate(vars) if vv.get()]
                    if len(chosen) != allowed:
                        messagebox.showerror("Error", f"Debe seleccionar exactamente {allowed} posiciones")
                        return
                    nonlocal sel
                    sel = chosen
                    dlg.destroy()

                def on_cancel():
                    dlg.destroy()

                btn_frame = tk.Frame(dlg)
                btn_frame.pack(pady=6)
                tk.Button(btn_frame, text="OK", command=on_ok).pack(side="left", padx=6)
                tk.Button(btn_frame, text="Cancelar", command=on_cancel).pack(side="left", padx=6)

                # modal
                dlg.transient(self)
                dlg.grab_set()
                self.wait_window(dlg)

                if not sel:
                    raise ValueError("No se seleccionaron posiciones de truncamiento")

                trunc_positions = sel

            if func == "plegamiento":
                op = self.combo_fold_op.get()
                folding_op = "suma" if op == "Suma" else "multiplicacion"

            self.structure = ExternalHashStructure(n, k, func, base, trunc_positions=trunc_positions, folding_op=folding_op)
            
            # UI Updates
            # UI Updates
            self.btn_create.grid_remove()
            self.btn_delete_struct.grid(row=1, column=5, padx=4, pady=4, sticky="ew")
            self.entry_n.configure(state="disabled")
            self.entry_k.configure(state="disabled")
            self.combo_func.configure(state="disabled")
            self.combo_base.configure(state="disabled")
            self.combo_fold_op.configure(state="disabled")

            self.btn_insert.configure(state="normal")
            self.btn_search.configure(state="normal")
            self.btn_delete_key.configure(state="normal")
            
            self.refresh_visualization()
            messagebox.showinfo("Éxito", f"Estructura creada.\nBloques: {self.structure.num_blocks}\nRegistros/Bloque: {self.structure.records_per_block}")
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def delete_structure(self):
        self.structure = None
        self.btn_delete_struct.grid_forget()
        self.btn_create.grid(row=1, column=5, padx=4, pady=4, sticky="ew")
        self.entry_n.configure(state="normal")
        self.entry_k.configure(state="normal")
        self.combo_func.configure(state="normal")
        if self.combo_func.get() == "Conversion Base":
            self.combo_base.configure(state="normal")

        self.btn_insert.configure(state="disabled")
        self.btn_search.configure(state="disabled")
        self.btn_delete_key.configure(state="disabled")
        
        for widget in self.vis_frame.winfo_children():
            widget.destroy()
        self.lbl_info = ctk.CTkLabel(self.vis_frame, text="Cree una estructura para visualizarla.")
        self.lbl_info.pack(pady=20)

    def insert_key(self):
        if not self.structure: return
        try:
            val = int(self.entry_key.get())
            idx, area, slot = self.structure.insert(val)
            self.refresh_visualization()
            messagebox.showinfo("Insertado", f"Clave {val} insertada en Bloque {idx} ({area}), Pos {slot}")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        finally:
            # clear any previous highlight
            self.highlight = None

    def search_key(self):
        if not self.structure: return
        try:
            val = int(self.entry_key.get())
            res = self.structure.search(val)
            if res:
                idx, area, slot = res
                # store highlight and refresh
                self.highlight = (idx, area, slot)
                self.refresh_visualization()
                messagebox.showinfo("Encontrado", f"Clave {val} en Bloque {idx} ({area}), Pos {slot}")
            else:
                messagebox.showwarning("No encontrado", "La clave no existe")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def delete_key(self):
        if not self.structure: return
        try:
            val = int(self.entry_key.get())
            self.structure.delete(val)
            self.refresh_visualization()
            messagebox.showinfo("Eliminado", f"Clave {val} eliminada")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        finally:
            # clear highlight on delete
            self.highlight = None

    def save_json(self):
        if not self.structure: return
        path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON", "*.json")])
        if path:
            try:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(self.structure.to_json())
                messagebox.showinfo("Guardado", "Estructura guardada correctamente")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def load_json(self):
        path = filedialog.askopenfilename(filetypes=[("JSON", "*.json")])
        if path:
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self.structure = ExternalHashStructure.from_dict(data)
                
                # Update UI config to match loaded structure
                self.entry_n.configure(state="normal")
                self.entry_n.delete(0, "end")
                self.entry_n.insert(0, str(self.structure.num_records))
                self.entry_n.configure(state="disabled")
                
                self.entry_k.configure(state="normal")
                self.entry_k.delete(0, "end")
                self.entry_k.insert(0, str(self.structure.key_length))
                self.entry_k.configure(state="disabled")
                
                # Map internal func name back to UI value
                func_map_rev = {
                    "cuadrado": "Cuadrado",
                    "modular": "Modular",
                    "plegamiento": "Plegamiento",
                    "truncamiento": "Truncamiento",
                    "conversion_base": "Conversion Base"
                }
                ui_func = func_map_rev.get(self.structure.hash_func, "Cuadrado")
                self.combo_func.set(ui_func)
                self.combo_func.configure(state="disabled")
                
                if self.structure.hash_func == "conversion_base":
                    self.combo_base.set(str(self.structure.base))
                self.combo_base.configure(state="disabled")
                
                self.btn_create.pack_forget()
                self.btn_delete_struct.pack(pady=5, fill="x")
                self.btn_insert.configure(state="normal")
                self.btn_search.configure(state="normal")
                self.btn_delete_key.configure(state="normal")
                
                self.refresh_visualization()
                messagebox.showinfo("Cargado", "Estructura cargada correctamente")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar: {e}")

    def refresh_visualization(self):
        for widget in self.vis_frame.winfo_children():
            widget.destroy()
            
        if not self.structure:
            return
        # Side-by-side main and collision structures
        container = ctk.CTkFrame(self.vis_frame, fg_color="transparent")
        container.pack(fill="both", expand=True)

        left = ctk.CTkFrame(container, fg_color="transparent")
        left.pack(side="left", fill="both", expand=True, padx=(0,5))
        ctk.CTkLabel(left, text="Estructura Principal", font=("Arial", 16, "bold")).pack(pady=(0, 10))
        self._draw_structure(self.structure.main_structure, parent=left, struct_type="main")

        right = ctk.CTkFrame(container, fg_color="transparent")
        right.pack(side="left", fill="both", expand=True, padx=(5,0))
        ctk.CTkLabel(right, text="Área de Colisiones", font=("Arial", 16, "bold")).pack(pady=(0, 10))
        self._draw_structure(self.structure.collision_structure, parent=right, struct_type="collision")

    def _draw_structure(self, blocks, parent=None, struct_type="main"):
        # Create a grid-like view for blocks
        # Each block is a frame containing records
        if parent is None:
            parent = self.vis_frame

        container = ctk.CTkFrame(parent, fg_color="transparent")
        container.pack(fill="both", expand=True)
        
        # Use grid layout for blocks
        # Maybe 2 blocks per row to save space if they are large, or 1 per row
        
        for i, block in enumerate(blocks):
            block_frame = ctk.CTkFrame(container, border_width=2, border_color="#333")
            block_frame.pack(fill="x", pady=5, padx=5)
            
            # Header: Block ID
            header = ctk.CTkFrame(block_frame, fg_color="#2b2b2b", height=30)
            header.pack(fill="x")
            ctk.CTkLabel(header, text=f"Bloque {i}", font=("Arial", 12, "bold"), text_color="white").pack()
            
            # Records
            records_frame = ctk.CTkFrame(block_frame, fg_color="transparent")
            records_frame.pack(fill="x", padx=5, pady=5)
            
            for j, record in enumerate(block):
                rec_text = str(record) if record is not None else "vacío"
                rec_color = "#1f6aa5" if record is not None else "#555"

                # Highlight if matches search
                if self.highlight and self.highlight[0] == i and self.highlight[1] == struct_type and self.highlight[2] == j:
                    rec_color = "#28a745"

                row = ctk.CTkFrame(records_frame, fg_color="transparent")
                row.pack(fill="x", pady=1)

                ctk.CTkLabel(row, text=f"Reg {j+1}:", width=50, anchor="e").pack(side="left", padx=5)
                lbl_val = ctk.CTkLabel(row, text=rec_text, fg_color=rec_color, corner_radius=4, width=100)
                lbl_val.pack(side="left", fill="x", expand=True)
