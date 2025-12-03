import customtkinter as ctk
from .base import BaseContent
from models.dynamic_total import DynamicTotalArray
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox as mb
import json


class ExternalDynamicContent(BaseContent):
    title = "Estructura Dinámica (Expansión Total)"

    def __init__(self, master):
        super().__init__(master)

        self.arr = None  # DynamicTotalArray instance

        # Layout: top menu (controls) and viewer area below
        self.body.grid_columnconfigure(0, weight=1)
        self.body.grid_rowconfigure(0, weight=0)  # top menu
        self.body.grid_rowconfigure(1, weight=1)  # viewer

        # Top menu frame with configuration and operation controls
        top_frame = ctk.CTkFrame(self.body)
        top_frame.grid(row=0, column=0, sticky='ew', padx=8, pady=(8, 4))
        top_frame.grid_columnconfigure(0, weight=1)
        
        # Crear dos filas dentro de top_frame: una para configuración y otra para operaciones
        config_frame = ctk.CTkFrame(top_frame)
        config_frame.grid(row=0, column=0, sticky='ew', padx=0, pady=0)
        
        ops_frame = ctk.CTkFrame(top_frame)
        ops_frame.grid(row=1, column=0, sticky='ew', padx=0, pady=(8, 0))
        
        # Configuración de las columnas en config_frame
        for i in range(12):
            config_frame.grid_columnconfigure(i, weight=1 if i == 11 else 0)
        
        # Configuración de las columnas en ops_frame
        for i in range(8):
            ops_frame.grid_columnconfigure(i, weight=1 if i == 7 else 0)

        # Configuration row en config_frame
        cfg_row = 0
        ctk.CTkLabel(config_frame, text="Cubetas:").grid(row=cfg_row, column=0, padx=(8,4), pady=6, sticky='w')
        self.entry_cols = ctk.CTkEntry(config_frame, width=80)
        self.entry_cols.grid(row=cfg_row, column=1, padx=4, pady=6)

        ctk.CTkLabel(config_frame, text="Registros:").grid(row=cfg_row, column=2, padx=(12,4), pady=6, sticky='w')
        self.entry_records = ctk.CTkEntry(config_frame, width=80)
        self.entry_records.grid(row=cfg_row, column=3, padx=4, pady=6)

        ctk.CTkLabel(config_frame, text="DO expansión:").grid(row=cfg_row, column=4, padx=(12,4), pady=6, sticky='w')
        self.entry_do = ctk.CTkEntry(config_frame, width=80)
        self.entry_do.grid(row=cfg_row, column=5, padx=4, pady=6)
        self.entry_do.insert(0, '75')

        ctk.CTkLabel(config_frame, text="DO reducción:").grid(row=cfg_row, column=6, padx=(12,4), pady=6, sticky='w')
        self.entry_dore = ctk.CTkEntry(config_frame, width=80)
        self.entry_dore.grid(row=cfg_row, column=7, padx=4, pady=6)
        self.entry_dore.insert(0, '85')

        ctk.CTkLabel(config_frame, text="Tipo expansión:").grid(row=cfg_row, column=8, padx=(12,4), pady=6, sticky='w')
        self.expansion_type_var = tk.StringVar(value='Total')
        self.expansion_type_menu = ctk.CTkOptionMenu(config_frame, values=['Total', 'Parcial'], 
                                                    variable=self.expansion_type_var, width=100)
        self.expansion_type_menu.grid(row=cfg_row, column=9, padx=4, pady=6)

        self.init_btn = ctk.CTkButton(config_frame, text="Inicializar", command=self.on_init, width=100)
        self.init_btn.grid(row=cfg_row, column=10, padx=(12,8), pady=6)

        # Operations row en ops_frame
        ops_row = 0
        ctk.CTkLabel(ops_frame, text="Clave:").grid(row=ops_row, column=0, padx=(8,4), pady=(0,8), sticky='w')
        self.key_entry = ctk.CTkEntry(ops_frame, width=120)
        self.key_entry.grid(row=ops_row, column=1, padx=4, pady=(0,8))

        self.insert_btn = ctk.CTkButton(ops_frame, text="Insertar", command=self.on_insert)
        self.insert_btn.grid(row=ops_row, column=2, padx=(8,4), pady=(0,8))

        self.delete_btn = ctk.CTkButton(ops_frame, text="Eliminar", command=self.on_delete)
        self.delete_btn.grid(row=ops_row, column=3, padx=(4,4), pady=(0,8))

        self.search_btn = ctk.CTkButton(ops_frame, text="Buscar", command=self.on_search)
        self.search_btn.grid(row=ops_row, column=4, padx=(8,4), pady=(0,8))

        self.save_btn = ctk.CTkButton(ops_frame, text="Guardar", command=self.on_save)
        self.save_btn.grid(row=ops_row, column=5, padx=(8,4), pady=(0,8))

        self.load_btn = ctk.CTkButton(ops_frame, text="Cargar", command=self.on_load)
        self.load_btn.grid(row=ops_row, column=6, padx=(4,4), pady=(0,8))

        self.clear_btn = ctk.CTkButton(ops_frame, text="Limpiar", fg_color="#b00020", 
                                      hover_color="#c62828", command=self.on_clear)
        self.clear_btn.grid(row=ops_row, column=7, padx=(8,8), pady=(0,8))

        # Status line below the top frame
        self.status = ctk.CTkLabel(self.body, text="", anchor='w', justify='left')
        self.status.grid(row=2, column=0, sticky='ew', padx=12, pady=(0,6))
        
        # DO current label
        self.do_label = ctk.CTkLabel(self.body, text="DO expansión: - | DO reducción: -", anchor='e')
        self.do_label.grid(row=2, column=0, sticky='e', padx=12, pady=(0,6))

        # Viewer area using a scrollable canvas (similar to other external views)
        viewer_frame = ctk.CTkFrame(self.body)
        viewer_frame.grid(row=1, column=0, sticky="nsew", padx=(8, 12), pady=(4, 12))
        viewer_frame.grid_rowconfigure(0, weight=1)
        viewer_frame.grid_columnconfigure(0, weight=1)

        self.blocks_canvas = tk.Canvas(viewer_frame, highlightthickness=0, borderwidth=0)
        self.blocks_canvas.grid(row=0, column=0, sticky="nsew", padx=(8, 0), pady=8)
        self.scrollbar_y = ctk.CTkScrollbar(viewer_frame, orientation="vertical", command=self.blocks_canvas.yview)
        self.scrollbar_y.grid(row=0, column=1, sticky="ns", pady=8, padx=(0, 8))
        self.blocks_canvas.configure(yscrollcommand=self.scrollbar_y.set)

        self.blocks_container = ctk.CTkFrame(self.blocks_canvas)
        self.blocks_window = self.blocks_canvas.create_window((0, 0), window=self.blocks_container, anchor="nw")
        self.blocks_container.bind("<Configure>", lambda _: self._update_scroll_region())
        self.blocks_canvas.bind("<Configure>", self._on_canvas_configure)
        self.blocks_container.grid_columnconfigure(0, weight=0)

        self.current_highlight = None
        self._init_done = True
        self._draw()

    def _on_canvas_configure(self, event):
        # keep the inner frame width matched to the canvas width
        try:
            self.blocks_canvas.itemconfig(self.blocks_window, width=event.width)
        except Exception:
            pass

    def _update_scroll_region(self):
        self.blocks_canvas.update_idletasks()
        self.blocks_canvas.configure(scrollregion=self.blocks_canvas.bbox('all'))

    def _draw(self, **kwargs):
        # draw using CTk widgets, not matplotlib. Accept kwargs for CTk init calls.
        if not getattr(self, '_init_done', False):
            return
        for w in self.blocks_container.winfo_children():
            w.destroy()
        if not self.arr:
            ctk.CTkLabel(self.blocks_container, text="Estructura no inicializada", anchor='w').grid(row=0, column=0, padx=8, pady=8)
            self._update_scroll_region()
            return

        snapshot = self.arr.snapshot()
        cols = snapshot['cols']
        collisions = snapshot.get('collisions', [[] for _ in range(snapshot['columns'])])
        C = snapshot['columns']
        R = snapshot['records']

        header_font = ctk.CTkFont(weight='bold')
        # Header row: Base + bucket names
        ctk.CTkLabel(self.blocks_container, text="Base", font=header_font, width=60).grid(row=0, column=0, padx=4, pady=(0,4))
        for ci in range(C):
            self.blocks_container.grid_columnconfigure(ci+1, weight=1)
            ctk.CTkLabel(self.blocks_container, text=f"C{ci+1}", font=header_font).grid(row=0, column=ci+1, padx=4, pady=(0,4))

        # Records rows (fixed to R). Start immediately below header (row 1)
        for r in range(R):
            ctk.CTkLabel(self.blocks_container, text=f"R{r+1}").grid(row=r+1, column=0, padx=4, pady=2, sticky='e')
            for ci in range(C):
                val = ''
                fg = None
                text_color = None
                if ci < len(cols) and r < len(cols[ci]):
                    val = str(cols[ci][r])
                    # highlight only active records
                    if self.current_highlight and self.current_highlight.get('column') == ci:
                        positions = self.current_highlight.get('positions', [])
                        if r in positions:
                            fg = '#fde68a' if not self.current_highlight.get('found') else '#86efac'
                            text_color = 'black'
                cell = ctk.CTkLabel(self.blocks_container, text=val or '—', fg_color=fg, corner_radius=6, text_color=text_color)
                cell.grid(row=r+1, column=ci+1, padx=2, pady=2, sticky='nsew')

        # Collision rows: show collisions per column below the fixed records
        max_collision_rows = max((len(c) for c in collisions), default=0)
        for cr in range(max_collision_rows):
            ctk.CTkLabel(self.blocks_container, text=f"Col{cr+1}").grid(row=R+1+cr, column=0, padx=4, pady=2, sticky='e')
            for ci in range(C):
                val = ''
                fg = '#fca5a5' if (ci < len(collisions) and cr < len(collisions[ci])) else None
                text_color = 'black' if fg else None
                if ci < len(collisions) and cr < len(collisions[ci]):
                    val = str(collisions[ci][cr])
                cell = ctk.CTkLabel(self.blocks_container, text=val or '—', fg_color=fg, corner_radius=6, text_color=text_color)
                cell.grid(row=R+1+cr, column=ci+1, padx=2, pady=2, sticky='nsew')

        self._update_scroll_region()

    def on_init(self):
        try:
            cols = int(self.entry_cols.get())
            rec = int(self.entry_records.get())
            do = int(self.entry_do.get())
            dore = int(self.entry_dore.get())
        except Exception:
            mb.showerror("Error", "Ingrese valores numéricos válidos")
            self.status.configure(text='Ingrese valores numéricos válidos')
            return
        # Validate DO ranges per spec
        if not (65 <= do <= 85):
            mb.showerror("Error", 'DO de expansión debe estar entre 65 y 85')
            self.status.configure(text='DO de expansión debe estar entre 65 y 85')
            return
        if not (85 <= dore <= 110):
            mb.showerror("Error", 'DO de reducción debe estar entre 85 y 110')
            self.status.configure(text='DO de reducción debe estar entre 85 y 110')
            return
        if dore <= do:
            mb.showerror("Error", 'DO de reducción debe ser mayor que DO de expansión')
            self.status.configure(text='DO de reducción debe ser mayor que DO de expansión')
            return

        # If partial expansion selected, require initial columns to be even
        if self.expansion_type_var.get() == 'Parcial' and (cols % 2 != 0):
            mb.showerror("Error", 'Para expansión parcial, el número inicial de cubetas debe ser par')
            self.status.configure(text='Para expansión parcial, el número inicial de cubetas debe ser par')
            return

        try:
            self.arr = DynamicTotalArray(columns=cols, records=rec, do_threshold=do, do_reduction_threshold=dore)
            self.status.configure(text=f'Estructura inicializada: {cols}x{rec}, DO_exp={do}%, DO_red={dore}%')
            self._draw()
            self._update_do_display()
        except Exception as e:
            mb.showerror("Error", str(e))
            self.status.configure(text=str(e))

    def _prompt_expansion(self, new_columns: int):
        """Show a modal dialog asking the user to accept the expansion."""
        top = ctk.CTkToplevel(self)
        top.title("Expansión de estructura")
        top.geometry("420x120")
        msg = ctk.CTkLabel(top, text=f"La estructura se va a expandir a {new_columns} cubetas.\n¿Desea aceptar la expansión?", wraplength=380)
        msg.pack(padx=12, pady=(12, 8))

        def _on_accept():
            try:
                # choose expansion type
                if self.expansion_type_var.get() == 'Parcial':
                    res = self.arr.expand_partial()
                else:
                    res = self.arr.expand()
                self.status.configure(text=f"Estructura expandida: {res['columns']} columnas")
                top.destroy()
                self._draw()
                self._update_do_display()
                
                # 🔴 SI DESPUÉS DE EXPANDIR EL DO SIGUE ALTO, EXPANDIR DE NUEVO
                if res['do_expansion'] >= self.arr.do_threshold:
                    # Calcular nueva expansión potencial
                    if self.expansion_type_var.get() == 'Parcial':
                        next_columns = self.arr.columns + max(1, self.arr.columns // 2)
                    else:
                        next_columns = self.arr.columns * 2
                    
                    # 🔴 EXPANDIR NUEVAMENTE (RECURSIVO)
                    self._prompt_expansion(next_columns)
                    
            except Exception as e:
                self.status.configure(text=f"Error al expandir: {e}")
                top.destroy()

        btn = ctk.CTkButton(top, text="Aceptar", command=_on_accept)
        btn.pack(side='right', padx=12, pady=12)
        # make modal
        try:
            top.transient(self)
            top.grab_set()
            self.wait_window(top)
        except Exception:
            pass

    def on_insert(self):
        if not self.arr:
            self.status.configure(text='Inicialice la estructura primero')
            return
        try:
            key = int(self.key_entry.get())
        except Exception:
            self.status.configure(text='Ingrese una clave entera válida')
            return
        try:
            res = self.arr.insert(key)
            # update DO display
            try:
                self._update_do_display()
            except Exception:
                pass
            if res.get('collision'):
                # collision: not part of structure until expansion
                col = key % (self.arr.columns if self.arr and self.arr.columns > 0 else 1)
                msg = f"Colisión: {key} registrada en C{col+1} (no forma parte de la estructura)"
                self.status.configure(text=msg)
                try:
                    self.key_entry.delete(0, 'end')
                except Exception:
                    pass
                self._draw()
                return

            # normal insertion: show inserted element in the view
            msg = f"Insertado {key}. DO_expansión={res['do_expansion']:.2f}%, DO_reducción={res['do_reduction']:.2f}%"
            self.status.configure(text=msg)
            try:
                self.key_entry.delete(0, 'end')
            except Exception:
                pass
            self._draw()

            # if expansion is needed, prompt user to confirm (after drawing)
            if res.get('expansion_needed'):
                try:
                    # compute preview columns depending on expansion type
                    if self.expansion_type_var.get() == 'Parcial':
                        preview = self.arr.columns + max(1, self.arr.columns // 2)
                    else:
                        preview = self.arr.columns * 2
                    self._prompt_expansion(preview)
                except Exception:
                    # fallback: immediately expand
                    if self.expansion_type_var.get() == 'Parcial':
                        e_res = self.arr.expand_partial()
                    else:
                        e_res = self.arr.expand()
                    self.status.configure(text=f"EXPANDIDO a {e_res['columns']} columnas")
                    self._draw()
                    self._update_do_display()
                    
                    # 🔴 SI DESPUÉS DE EXPANDIR EL DO SIGUE ALTO, EXPANDIR DE NUEVO
                    if e_res['do_expansion'] >= self.arr.do_threshold:
                        # Calcular nueva expansión potencial
                        if self.expansion_type_var.get() == 'Parcial':
                            next_columns = self.arr.columns + max(1, self.arr.columns // 2)
                        else:
                            next_columns = self.arr.columns * 2
                        
                        # 🔴 EXPANDIR NUEVAMENTE (no solo mostrar mensaje)
                        self._prompt_expansion(next_columns)
        except Exception as e:
            self.status.configure(text=str(e))

    def on_delete(self):
        if not self.arr:
            self.status.configure(text='Inicialice la estructura primero')
            return
        try:
            key = int(self.key_entry.get())
        except Exception:
            self.status.configure(text='Ingrese una clave entera válida')
            return
        try:
            res = self.arr.delete(key)
            try:
                self.key_entry.delete(0, 'end')
            except Exception:
                pass
            
            # 🔴 ACTUALIZAR VISTA DESPUÉS DE ELIMINAR
            self._draw()
            
            # Usar DO de reducción calculado para decidir si reducir
            if res.get('should_reduce'):
                top = ctk.CTkToplevel(self)
                top.title("Reducción de estructura")
                top.geometry("420x120")
                
                msg = ctk.CTkLabel(
                    top, 
                    text=f"DO reducción actual: {res.get('do_reduction', 0):.2f}% < Umbral: {self.arr.do_reduction_threshold}%\n"
                        f"¿Desea reducir a la mitad las columnas?",
                    wraplength=380
                )
                msg.pack(padx=12, pady=(12, 8))

                def _on_accept_reduce():
                    try:
                        rres = self.arr.reduce()
                        self.status.configure(text=f"Estructura reducida: {rres['columns']} columnas")
                        top.destroy()
                        self._draw()
                        self._update_do_display()
                        
                        # 🔴 SI DESPUÉS DE REDUCIR EL DO_EXPANSION >= UMBRAL, EXPANDIR
                        if rres['do_expansion'] >= self.arr.do_threshold:
                            # Calcular nueva expansión potencial
                            if self.expansion_type_var.get() == 'Parcial':
                                next_columns = self.arr.columns + max(1, self.arr.columns // 2)
                            else:
                                next_columns = self.arr.columns * 2
                            
                            # 🔴 LLAMAR A LA EXPANSIÓN AUTOMÁTICAMENTE
                            self._prompt_expansion(next_columns)
                    except Exception as e:
                        self.status.configure(text=f"Error al reducir: {e}")
                        top.destroy()

                # 🟢 SOLO UN BOTÓN: Aceptar (sin cancelar)
                btn_accept = ctk.CTkButton(top, text="Aceptar", command=_on_accept_reduce)
                btn_accept.pack(side='right', padx=12, pady=12)
                
                # Hacer que la ventana sea modal
                try:
                    top.transient(self)
                    top.grab_set()
                    self.wait_window(top)
                except Exception:
                    pass
            else:
                self.status.configure(text=f"Eliminado {key}. DO_exp={res.get('do_expansion', 0):.2f}%, DO_red={res.get('do_reduction', 0):.2f}%")
                self._update_do_display()
        except Exception as e:
            self.status.configure(text=str(e))

    def on_search(self):
        if not self.arr:
            self.status.configure(text='Inicialice la estructura primero')
            return
        try:
            key = int(self.key_entry.get())
        except Exception:
            self.status.configure(text='Ingrese una clave entera válida')
            return
        try:
            res = self.arr.find(key)
            if res.get('found'):
                col = res['column']
                positions = res.get('positions', [])
                self.current_highlight = {'column': col, 'positions': positions, 'found': True}
                self.status.configure(text=f'Clave {key} encontrada en columna {col+1}, posiciones {positions}')
            else:
                # highlight base where it would map
                col = key % (self.arr.columns if self.arr.columns > 0 else 1)
                self.current_highlight = {'column': col, 'positions': [], 'found': False}
                self.status.configure(text=f'Clave {key} no encontrada. Base candidata: C{col+1}')
            self._draw()
        except Exception as e:
            self.status.configure(text=str(e))

    def _update_do_display(self):
        try:
            if not self.arr:
                self.do_label.configure(text="DO expansión: - | DO reducción: -")
                return
            
            do_expansion = self.arr.current_do_expansion()
            do_reduction = self.arr.current_do_reduction()
            threshold_expansion = self.arr.do_threshold
            threshold_reduction = self.arr.do_reduction_threshold
            
            self.do_label.configure(
                text=f"DO expansión: {do_expansion:.2f}% (umbral: {threshold_expansion}%) | "
                     f"DO reducción: {do_reduction:.2f}% (umbral: {threshold_reduction}%)"
            )
        except Exception:
            pass

    def on_save(self):
        if not self.arr:
            self.status.configure(text='Nada para guardar')
            return
        path = fd.asksaveasfilename(defaultextension='.json', filetypes=[('JSON files', '*.json')])
        if not path:
            return
        try:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(self.arr.to_dict(), f, ensure_ascii=False, indent=2)
            self.status.configure(text=f'Guardado en {path}')
        except Exception as e:
            self.status.configure(text=f'Error guardando: {e}')

    def on_load(self):
        path = fd.askopenfilename(filetypes=[('JSON files', '*.json')])
        if not path:
            return
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            arr = DynamicTotalArray.from_dict(data)
            self.arr = arr
            self.status.configure(text=f'Cargado desde {path}')
            self._draw()
            self._update_do_display()
        except Exception as e:
            self.status.configure(text=f'Error cargando: {e}')

    def on_clear(self):
        # Remove the structure entirely so the user can initialize a new one
        if not self.arr:
            self.status.configure(text='No hay estructura para eliminar')
            return
        self.arr = None
        self.current_highlight = None
        self.status.configure(text='Estructura eliminada. Puede crear una nueva.')
        self._draw()
