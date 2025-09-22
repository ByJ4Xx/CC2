from __future__ import annotations

from dataclasses import dataclass
import json
import tkinter as tk
import tkinter.filedialog as fd
import tkinter.messagebox as mb
from typing import Dict, Optional, Tuple, Type, TypeVar

import customtkinter as ctk

from .base import BaseContent
from models.external import ExternalStructureBase


StructureT = TypeVar("StructureT", bound=ExternalStructureBase)


@dataclass
class HighlightState:
    block: int
    offset: Optional[int]
    found: bool = False
    highlight_base: bool = False


class ExternalBaseContent(BaseContent):
    title = ""
    structure_cls: Type[StructureT] = ExternalStructureBase  # type: ignore[assignment]
    search_button_text = "Buscar"
    search_kind_label = "externa"

    def __init__(self, master):
        super().__init__(master)

        self.structure: Optional[StructureT] = None
        self.var_capacity = ctk.StringVar(value="1000")
        self.var_klen = ctk.StringVar(value="4")
        self.var_key = ctk.StringVar()
        self.var_gen_count = ctk.StringVar(value="100")

        self.current_highlight: Optional[HighlightState] = None

        # Layout principal
        self.body.grid_columnconfigure(0, weight=1)
        for r in range(7):
            self.body.grid_rowconfigure(r, weight=0)
        self.body.grid_rowconfigure(6, weight=1)

        # Configuración
        cfg_frame = ctk.CTkFrame(self.body)
        cfg_frame.grid(row=0, column=0, sticky="ew", padx=8, pady=(8, 4))
        cfg_frame.grid_columnconfigure(6, weight=1)

        ctk.CTkLabel(cfg_frame, text="Tamaño (múltiplo de 10):").grid(
            row=0, column=0, padx=(8, 6), pady=8, sticky="w"
        )
        self.capacity_entry = ctk.CTkEntry(cfg_frame, textvariable=self.var_capacity, width=120)
        self.capacity_entry.grid(row=0, column=1, padx=(0, 8), pady=8)

        ctk.CTkLabel(cfg_frame, text="Longitud de clave:").grid(row=0, column=2, padx=(8, 6), pady=8, sticky="w")
        self.klen_menu = ctk.CTkOptionMenu(cfg_frame, values=[str(i) for i in range(1, 10)], variable=self.var_klen)
        self.klen_menu.grid(row=0, column=3, padx=(0, 8), pady=8)

        self.btn_crear = ctk.CTkButton(cfg_frame, text="Crear", command=self.on_crear)
        self.btn_crear.grid(row=0, column=4, padx=(0, 8), pady=8)

        self.btn_borrar = ctk.CTkButton(cfg_frame, text="Borrar estructura", command=self.on_borrar, state="disabled")
        self.btn_borrar.grid(row=0, column=5, padx=(0, 8), pady=8)

        self.lbl_capacidad = ctk.CTkLabel(cfg_frame, text="Capacidad: — | Ocupados: 0 | Bloques: — | Reg/bloque: —")
        self.lbl_capacidad.grid(row=0, column=6, padx=(8, 8), pady=8, sticky="w")

        # Operaciones
        ops_frame = ctk.CTkFrame(self.body)
        ops_frame.grid(row=1, column=0, sticky="ew", padx=8, pady=4)
        ops_frame.grid_columnconfigure(6, weight=1)

        ctk.CTkLabel(ops_frame, text="Clave:").grid(row=0, column=0, padx=(8, 6), pady=8, sticky="w")
        self.entry_key = ctk.CTkEntry(ops_frame, textvariable=self.var_key, width=160)
        self.entry_key.grid(row=0, column=1, padx=(0, 8), pady=8)

        self.btn_insert = ctk.CTkButton(ops_frame, text="Insertar", command=self.on_insertar, state="disabled")
        self.btn_insert.grid(row=0, column=2, padx=(0, 6), pady=8)

        self.btn_buscar = ctk.CTkButton(ops_frame, text=self.search_button_text, command=self.on_buscar, state="disabled")
        self.btn_buscar.grid(row=0, column=3, padx=(0, 6), pady=8)

        self.btn_eliminar = ctk.CTkButton(ops_frame, text="Eliminar", command=self.on_eliminar, state="disabled")
        self.btn_eliminar.grid(row=0, column=4, padx=(0, 6), pady=8, sticky="w")

        # Generación aleatoria
        gen_frame = ctk.CTkFrame(self.body)
        gen_frame.grid(row=2, column=0, sticky="ew", padx=8, pady=4)
        gen_frame.grid_columnconfigure(4, weight=1)

        ctk.CTkLabel(gen_frame, text="Generar aleatorios:").grid(row=0, column=0, padx=(8, 6), pady=8, sticky="w")
        self.entry_gen = ctk.CTkEntry(gen_frame, textvariable=self.var_gen_count, width=100)
        self.entry_gen.grid(row=0, column=1, padx=(0, 8), pady=8)

        self.btn_generar = ctk.CTkButton(gen_frame, text="Generar", command=self.on_generar, state="disabled")
        self.btn_generar.grid(row=0, column=2, padx=(0, 8), pady=8)

        # Guardar / cargar
        io_frame = ctk.CTkFrame(self.body)
        io_frame.grid(row=3, column=0, sticky="ew", padx=8, pady=4)
        io_frame.grid_columnconfigure(2, weight=1)

        self.btn_guardar = ctk.CTkButton(io_frame, text="Guardar estructura", command=self.on_guardar, state="disabled")
        self.btn_guardar.grid(row=0, column=0, padx=8, pady=8)

        self.btn_cargar = ctk.CTkButton(io_frame, text="Cargar estructura", command=self.on_cargar)
        self.btn_cargar.grid(row=0, column=1, padx=8, pady=8)

        # Estado
        self.lbl_estado = ctk.CTkLabel(self.body, text="Listo.")
        self.lbl_estado.grid(row=4, column=0, sticky="ew", padx=16, pady=(4, 0))

        # Visor de bloques
        viewer_frame = ctk.CTkFrame(self.body)
        viewer_frame.grid(row=6, column=0, sticky="nsew", padx=8, pady=(8, 12))
        viewer_frame.grid_rowconfigure(0, weight=0)
        viewer_frame.grid_rowconfigure(1, weight=1)
        viewer_frame.grid_rowconfigure(2, weight=0)
        viewer_frame.grid_columnconfigure(0, weight=1)
        viewer_frame.grid_columnconfigure(1, weight=0)

        ctk.CTkLabel(viewer_frame, text="Bloques (ordenados)").grid(
            row=0, column=0, columnspan=2, sticky="w", padx=8, pady=(8, 0)
        )
        self.blocks_canvas = tk.Canvas(viewer_frame, highlightthickness=0, borderwidth=0)
        self.blocks_canvas.grid(row=1, column=0, sticky="nsew", padx=(8, 0), pady=8)
        self.scrollbar_y = ctk.CTkScrollbar(
            viewer_frame, orientation="vertical", command=self.blocks_canvas.yview
        )
        self.scrollbar_y.grid(row=1, column=1, sticky="ns", pady=8, padx=(0, 8))
        self.scrollbar_x = ctk.CTkScrollbar(
            viewer_frame, orientation="horizontal", command=self.blocks_canvas.xview
        )
        self.scrollbar_x.grid(row=2, column=0, columnspan=2, sticky="ew", padx=8, pady=(0, 8))
        self.blocks_canvas.configure(
            yscrollcommand=self.scrollbar_y.set, xscrollcommand=self.scrollbar_x.set
        )
        self.blocks_container = ctk.CTkFrame(self.blocks_canvas)
        self.blocks_window = self.blocks_canvas.create_window(
            (0, 0), window=self.blocks_container, anchor="nw"
        )
        self.blocks_container.grid_columnconfigure(0, weight=0)
        self.blocks_container.grid_rowconfigure(0, weight=0)
        self.blocks_container.bind("<Configure>", lambda _: self._update_scroll_region())
        self.blocks_canvas.bind("<Configure>", self._on_canvas_configure)
        self._sync_canvas_theme()

        self._refresh_view()

    # Helpers UI
    def _set_controls_enabled(self, enabled: bool):
        base = "normal" if enabled else "disabled"
        self.btn_insert.configure(state=base)
        self.btn_buscar.configure(state=base)
        self.btn_eliminar.configure(state=base)
        self.btn_guardar.configure(state=base)
        self.btn_generar.configure(state=base)

    def _set_config_enabled(self, enabled: bool):
        state = "normal" if enabled else "disabled"
        self.capacity_entry.configure(state=state)
        self.klen_menu.configure(state=state)
        self.btn_crear.configure(state=state)
        self.btn_borrar.configure(state="normal" if not enabled else "disabled")

    def _update_counters(self):
        if not self.structure:
            text = "Capacidad: — | Ocupados: 0 | Bloques: — | Reg/bloque: —"
        else:
            cap = self.structure.capacity
            occ = len(self.structure.items)
            blocks = self.structure.block_count
            size = self.structure.block_size
            text = f"Capacidad: {cap} | Ocupados: {occ} | Bloques: {blocks} | Reg/bloque: {size}"
        self.lbl_capacidad.configure(text=text)

    def _refresh_view(self, highlight: Optional[HighlightState] = None):
        for widget in self.blocks_container.winfo_children():
            widget.destroy()
        self.current_highlight = highlight
        self._sync_canvas_theme()

        if not self.structure:
            ctk.CTkLabel(
                self.blocks_container,
                text="Crea o carga la estructura para visualizar los bloques.",
                anchor="w",
                justify="left",
            ).grid(row=0, column=0, sticky="w", padx=8, pady=8)
            self._update_scroll_region()
            return

        blocks = self.structure.get_blocks(fill=True)
        bases = self.structure.get_block_bases()
        block_count = len(blocks)
        block_size = self.structure.block_size

        # Encabezados de filas
        header_font = ctk.CTkFont(weight="bold")
        self.blocks_container.grid_columnconfigure(0, weight=0)
        ctk.CTkLabel(self.blocks_container, text="", font=header_font, width=60).grid(
            row=0, column=0, padx=4, pady=(0, 4)
        )
        ctk.CTkLabel(self.blocks_container, text="Base", font=header_font).grid(
            row=1, column=0, padx=4, pady=2, sticky="e"
        )
        for r in range(block_size):
            ctk.CTkLabel(self.blocks_container, text=f"R{r + 1}").grid(
                row=r + 2, column=0, padx=4, pady=2, sticky="e"
            )

        # Columnas por bloque
        for col in range(block_count):
            self.blocks_container.grid_columnconfigure(col + 1, weight=1)
            block_highlight = bool(highlight and highlight.block == col)
            base_fg = self._highlight_color(
                block_highlight and highlight.highlight_base if highlight else False,
                highlight,
            )

            header = ctk.CTkLabel(self.blocks_container, text=f"B{col + 1}", font=header_font)
            header.grid(row=0, column=col + 1, padx=4, pady=(0, 4))

            base_val = bases[col]
            base_text = self._format_value(base_val)
            base_label = ctk.CTkLabel(
                self.blocks_container,
                text=base_text,
                fg_color=base_fg,
                corner_radius=6,
                text_color="black" if base_fg else None,
            )
            base_label.grid(row=1, column=col + 1, padx=2, pady=2, sticky="nsew")

            for r, value in enumerate(blocks[col]):
                fg = None
                text_color = None
                if block_highlight and highlight and highlight.offset == r:
                    fg = self._highlight_color(True, highlight)
                    text_color = "black"
                cell = ctk.CTkLabel(
                    self.blocks_container,
                    text=self._format_value(value),
                    fg_color=fg,
                    corner_radius=6,
                    text_color=text_color,
                )
                cell.grid(row=r + 2, column=col + 1, padx=2, pady=2, sticky="nsew")
            self._update_scroll_region()

    def _sync_canvas_theme(self):
        fg_color = self._apply_appearance_mode(self.blocks_container.cget("fg_color"))
        self.blocks_canvas.configure(background=fg_color)

    def _update_scroll_region(self):
        bbox = self.blocks_canvas.bbox("all")
        if bbox is None:
            bbox = (0, 0, 0, 0)
        self.blocks_canvas.configure(scrollregion=bbox)

    def _on_canvas_configure(self, event):
        req_width = self.blocks_container.winfo_reqwidth()
        new_width = max(event.width, req_width)
        self.blocks_canvas.itemconfigure(self.blocks_window, width=new_width)
        self._update_scroll_region()

    def _highlight_color(self, active: bool, highlight: Optional[HighlightState]) -> Optional[str]:
        if not active:
            return None
        if highlight and highlight.found:
            return "#86efac"
        return "#fde68a"

    def _format_value(self, value: Optional[int]) -> str:
        if value is None:
            return "—"
        if self.structure:
            width = int(self.structure.key_length)
            return f"{value:0{width}d}"
        return str(value)

    def _set_estado(self, msg: str):
        self.lbl_estado.configure(text=msg)

    def _error(self, msg: str):
        self._set_estado(msg)
        try:
            mb.showerror("Error", msg)
        except Exception:
            pass

    def _parse_key(self) -> Tuple[bool, Optional[int], Optional[str]]:
        if not self.structure:
            return False, None, "Primero crea o carga la estructura."
        s = (self.var_key.get() or "").strip()
        if not s:
            return False, None, "Ingresa una clave numérica."
        if not s.isdigit():
            return False, None, "La clave debe ser numérica (solo dígitos)."
        try:
            val = int(s)
        except ValueError:
            return False, None, "Clave inválida."
        if len(str(abs(val))) != int(self.structure.key_length):
            return False, None, f"La clave debe tener {self.structure.key_length} dígitos."
        return True, val, None

    # Acciones
    def on_crear(self):
        if self.structure is not None:
            if not mb.askyesno("Confirmar", "Esto borrará la estructura actual. ¿Continuar?"):
                return
        try:
            capacity = int((self.var_capacity.get() or "0").strip())
            klen = int(self.var_klen.get())
        except ValueError:
            self._error("Parámetros inválidos")
            return
        try:
            self.structure = self.structure_cls(capacity, klen)  # type: ignore[call-arg]
        except Exception as e:
            self._error(str(e))
            return
        self._set_estado("Estructura creada.")
        self.var_capacity.set(str(self.structure.capacity))
        self._set_config_enabled(False)
        self._set_controls_enabled(True)
        self._update_counters()
        self._refresh_view()

    def on_borrar(self):
        if self.structure is None:
            return
        if not mb.askyesno("Confirmar", "Se borrará la estructura actual. ¿Continuar?"):
            return
        self.structure = None
        self._set_config_enabled(True)
        self._set_controls_enabled(False)
        self._update_counters()
        self._refresh_view()
        self._set_estado("Estructura borrada. Configura y pulsa Crear.")

    def on_insertar(self):
        ok, val, err = self._parse_key()
        if not ok:
            self._error(err or "")
            return
        try:
            idx = self.structure.insert(val)  # type: ignore[union-attr]
        except Exception as e:
            self._error(str(e))
            return
        block, offset = self.structure.locate_index(idx)  # type: ignore[union-attr]
        self._set_estado(f"Insertado {val} en bloque B{block + 1}, posición {offset + 1}.")
        self._update_counters()
        self._refresh_view(HighlightState(block=block, offset=offset, found=True))

    def on_buscar(self):
        ok, val, err = self._parse_key()
        if not ok:
            self._error(err or "")
            return
        result = self.structure.find(val)  # type: ignore[union-attr]
        if result.found:
            self._set_estado(
                f"Búsqueda {self.search_kind_label}: {val} encontrado en bloque B{result.block + 1}, posición {result.offset + 1}."
            )
            self._refresh_view(
                HighlightState(
                    block=result.block,
                    offset=result.offset,
                    found=True,
                    highlight_base=True,
                )
            )
        else:
            if result.block >= 0:
                self._set_estado(
                    f"Búsqueda {self.search_kind_label}: {val} no encontrado. Revisado hasta bloque B{result.block + 1}."
                )
                self._refresh_view(
                    HighlightState(
                        block=result.block,
                        offset=None,
                        found=False,
                        highlight_base=True,
                    )
                )
            else:
                self._set_estado(
                    f"Búsqueda {self.search_kind_label}: {val} no encontrado."
                )
                self._refresh_view()

    def on_eliminar(self):
        ok, val, err = self._parse_key()
        if not ok:
            self._error(err or "")
            return
        try:
            idx = self.structure.delete(val)  # type: ignore[union-attr]
        except Exception as e:
            self._error(str(e))
            return
        self._set_estado(f"Eliminado {val} desde índice {idx}.")
        self._update_counters()
        self._refresh_view()

    def on_guardar(self):
        if not self.structure:
            self._error("No hay estructura creada para guardar.")
            return
        path = fd.asksaveasfilename(
            title="Guardar estructura",
            defaultextension=".json",
            filetypes=[("JSON", "*.json")],
        )
        if not path:
            return
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(self.structure.to_json())
            self._set_estado(f"Guardado en {path}.")
        except Exception as e:
            self._error(f"Error al guardar: {e}")

    def on_cargar(self):
        path = fd.askopenfilename(
            title="Cargar estructura",
            filetypes=[("JSON", "*.json")],
        )
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                data: Dict[str, object] = json.load(f)
            struct = self.structure_cls.from_dict(data)  # type: ignore[arg-type]
        except Exception as e:
            self._error(f"Error al cargar: {e}")
            return
        self.structure = struct
        self.var_capacity.set(str(self.structure.capacity))
        self.var_klen.set(str(self.structure.key_length))
        self._set_config_enabled(False)
        self._set_controls_enabled(True)
        self._update_counters()
        self._set_estado(f"Estructura cargada desde {path}.")
        self._refresh_view()

    def on_generar(self):
        if not self.structure:
            self._error("Primero crea o carga la estructura.")
            return
        try:
            count = int((self.var_gen_count.get() or "0").strip())
        except ValueError:
            self._error("Cantidad inválida.")
            return
        if count <= 0:
            self._error("La cantidad debe ser mayor que 0.")
            return
        added = self.structure.generate_random(count)  # type: ignore[union-attr]
        self._set_estado(f"Generados {added} elementos aleatorios.")
        self._update_counters()
        self._refresh_view()
