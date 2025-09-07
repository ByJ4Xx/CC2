from __future__ import annotations

import customtkinter as ctk
import json
import math
import tkinter.filedialog as fd
import tkinter.messagebox as mb
from typing import Optional

from .base import BaseContent
from models.linear import LinearStructure


class LinealContent(BaseContent):
    title = "B. Internas · Búsqueda Lineal"

    def __init__(self, master):
        super().__init__(master)

        # Estado
        self.structure: Optional[LinearStructure] = None
        self.var_exp = ctk.StringVar(value="3")  # 10^3 por defecto
        self.var_klen = ctk.StringVar(value="4")
        self.var_key = ctk.StringVar()
        self.var_gen_count = ctk.StringVar(value="100")

        # Estado de búsqueda paso a paso
        self.step_active = False
        self.step_index = 0
        self.step_target: Optional[int] = None
        self.after_id: Optional[str] = None
        self.step_delay_ms = 250

        # Layout del body
        self.body.grid_columnconfigure(0, weight=1)
        for r in range(8):
            self.body.grid_rowconfigure(r, weight=0)
        self.body.grid_rowconfigure(7, weight=1)  # visor crece

        # 1) Configuración de tamaño (10^n) y longitud de clave
        cfg_frame = ctk.CTkFrame(self.body)
        cfg_frame.grid(row=0, column=0, sticky="ew", padx=8, pady=(8, 4))
        cfg_frame.grid_columnconfigure(6, weight=1)

        ctk.CTkLabel(cfg_frame, text="Tamaño (10^n):").grid(row=0, column=0, padx=(8, 6), pady=8, sticky="w")
        self.exp_menu = ctk.CTkOptionMenu(cfg_frame, values=["1", "2", "3", "4"], variable=self.var_exp)
        self.exp_menu.grid(row=0, column=1, padx=(0, 8), pady=8)

        ctk.CTkLabel(cfg_frame, text="Longitud de clave:").grid(row=0, column=2, padx=(8, 6), pady=8, sticky="w")
        self.klen_menu = ctk.CTkOptionMenu(
            cfg_frame,
            values=[str(i) for i in range(1, 10)],
            variable=self.var_klen,
        )
        self.klen_menu.grid(row=0, column=3, padx=(0, 8), pady=8)

        self.btn_crear = ctk.CTkButton(cfg_frame, text="Crear", command=self.on_crear)
        self.btn_crear.grid(row=0, column=4, padx=(0, 8), pady=8)

        self.btn_borrar = ctk.CTkButton(cfg_frame, text="Borrar estructura", command=self.on_borrar, state="disabled")
        self.btn_borrar.grid(row=0, column=5, padx=(0, 8), pady=8)

        self.lbl_capacidad = ctk.CTkLabel(cfg_frame, text="Capacidad: — | Ocupados: 0")
        self.lbl_capacidad.grid(row=0, column=6, padx=(8, 8), pady=8, sticky="w")

        # 2) Operaciones: insertar / buscar / eliminar
        ops_frame = ctk.CTkFrame(self.body)
        ops_frame.grid(row=1, column=0, sticky="ew", padx=8, pady=4)
        ops_frame.grid_columnconfigure(6, weight=1)

        ctk.CTkLabel(ops_frame, text="Clave:").grid(row=0, column=0, padx=(8, 6), pady=8, sticky="w")
        self.entry_key = ctk.CTkEntry(ops_frame, textvariable=self.var_key, width=160)
        self.entry_key.grid(row=0, column=1, padx=(0, 8), pady=8)

        self.btn_insert = ctk.CTkButton(ops_frame, text="Insertar", command=self.on_insertar, state="disabled")
        self.btn_insert.grid(row=0, column=2, padx=(0, 6), pady=8)

        self.btn_buscar = ctk.CTkButton(ops_frame, text="Buscar", command=self.on_buscar, state="disabled")
        self.btn_buscar.grid(row=0, column=3, padx=(0, 6), pady=8)

        self.btn_eliminar = ctk.CTkButton(ops_frame, text="Eliminar", command=self.on_eliminar, state="disabled")
        self.btn_eliminar.grid(row=0, column=4, padx=(0, 6), pady=8, sticky="w")

        # 3) Generación aleatoria
        gen_frame = ctk.CTkFrame(self.body)
        gen_frame.grid(row=2, column=0, sticky="ew", padx=8, pady=4)
        gen_frame.grid_columnconfigure(4, weight=1)
        ctk.CTkLabel(gen_frame, text="Generar aleatorios:").grid(row=0, column=0, padx=(8, 6), pady=8, sticky="w")
        self.entry_gen = ctk.CTkEntry(gen_frame, textvariable=self.var_gen_count, width=100)
        self.entry_gen.grid(row=0, column=1, padx=(0, 8), pady=8)
        self.btn_generar = ctk.CTkButton(gen_frame, text="Generar", command=self.on_generar, state="disabled")
        self.btn_generar.grid(row=0, column=2, padx=(0, 8), pady=8)

        # 4) Guardar / Cargar
        io_frame = ctk.CTkFrame(self.body)
        io_frame.grid(row=3, column=0, sticky="ew", padx=8, pady=4)
        io_frame.grid_columnconfigure(2, weight=1)

        self.btn_guardar = ctk.CTkButton(io_frame, text="Guardar estructura", command=self.on_guardar, state="disabled")
        self.btn_guardar.grid(row=0, column=0, padx=8, pady=8)

        self.btn_cargar = ctk.CTkButton(io_frame, text="Cargar estructura", command=self.on_cargar)
        self.btn_cargar.grid(row=0, column=1, padx=8, pady=8)

        # 5) Paso a paso
        step_frame = ctk.CTkFrame(self.body)
        step_frame.grid(row=4, column=0, sticky="ew", padx=8, pady=4)
        step_frame.grid_columnconfigure(6, weight=1)
        ctk.CTkLabel(step_frame, text="Búsqueda paso a paso:").grid(row=0, column=0, padx=(8, 6), pady=8, sticky="w")
        self.btn_step_start = ctk.CTkButton(step_frame, text="Iniciar", command=self.on_step_start, state="disabled")
        self.btn_step_start.grid(row=0, column=1, padx=4, pady=8)
        self.btn_step_next = ctk.CTkButton(step_frame, text="Paso", command=self.on_step_next, state="disabled")
        self.btn_step_next.grid(row=0, column=2, padx=4, pady=8)
        self.btn_step_auto = ctk.CTkButton(step_frame, text="Auto", command=self.on_step_auto, state="disabled")
        self.btn_step_auto.grid(row=0, column=3, padx=4, pady=8)
        self.btn_step_stop = ctk.CTkButton(step_frame, text="Detener", command=self.on_step_stop, state="disabled")
        self.btn_step_stop.grid(row=0, column=4, padx=4, pady=8)

        # 6) Estado y visor
        self.lbl_estado = ctk.CTkLabel(self.body, text="Listo.")
        self.lbl_estado.grid(row=5, column=0, sticky="ew", padx=16, pady=(4, 0))

        viewer_frame = ctk.CTkFrame(self.body)
        viewer_frame.grid(row=7, column=0, sticky="nsew", padx=8, pady=(8, 12))
        viewer_frame.grid_rowconfigure(0, weight=0)
        viewer_frame.grid_rowconfigure(1, weight=1)
        viewer_frame.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(viewer_frame, text="Contenido (máx. 1000 elementos)").grid(
            row=0, column=0, sticky="w", padx=8, pady=(8, 0)
        )
        self.viewer = ctk.CTkTextbox(viewer_frame, wrap="none")
        self.viewer.grid(row=1, column=0, sticky="nsew", padx=8, pady=8)

        # Configure tags for highlighting (robust to CTkTextbox internals)
        try:
            w = getattr(self.viewer, "_textbox", self.viewer)
            w.tag_configure("scan", background="#fde68a", foreground="#000000")
            w.tag_configure("found", background="#86efac", foreground="#000000")
            try:
                w.tag_lower("scan")
                w.tag_raise("found")
            except Exception:
                pass
        except Exception:
            pass

        self._refresh_view()

    # Estado/UI helpers
    def _set_controls_enabled(self, enabled: bool):
        base = "normal" if enabled else "disabled"
        self.btn_insert.configure(state=base)
        self.btn_buscar.configure(state=base)
        self.btn_eliminar.configure(state=base)
        self.btn_guardar.configure(state=base)
        self.btn_generar.configure(state=base)
        self.btn_step_start.configure(state=base)
        self.btn_step_next.configure(state=("normal" if (enabled and self.step_active) else "disabled"))
        self.btn_step_auto.configure(state=base)
        self.btn_step_stop.configure(state=("normal" if (enabled and self.step_active) else "disabled"))

    def _set_config_enabled(self, enabled: bool):
        state = "normal" if enabled else "disabled"
        self.exp_menu.configure(state=state)
        self.klen_menu.configure(state=state)
        self.btn_crear.configure(state=state)
        self.btn_borrar.configure(state="normal" if not enabled else "disabled")

    def _update_counters(self):
        cap = self.structure.capacity if self.structure else 0
        occ = len(self.structure.items) if self.structure else 0
        self.lbl_capacidad.configure(text=f"Capacidad: {cap} | Ocupados: {occ}")

    def _refresh_view(self, highlight_index: int | None = None, found: bool = False):
        self.viewer.configure(state="normal")
        self.viewer.delete("1.0", "end")
        cap = self.structure.capacity if self.structure else 0
        items = self.structure.items if self.structure else []
        mostrar = min(1000, cap)
        if cap == 0:
            self.viewer.insert("end", "Crea o carga la estructura para visualizar contenido.\n")
        else:
            for i in range(mostrar):
                if i < len(items):
                    val = items[i]
                    self.viewer.insert("end", f"[{i:>4}]  {val}\n")
                else:
                    self.viewer.insert("end", f"[{i:>4}]  —\n")
            if cap > mostrar:
                self.viewer.insert("end", f"... ({cap - mostrar} elementos no mostrados)\n")
        # Highlight after text is present
        try:
            w = getattr(self.viewer, "_textbox", self.viewer)
            w.tag_remove("scan", "1.0", "end")
            w.tag_remove("found", "1.0", "end")
            if highlight_index is not None and cap > 0 and highlight_index < mostrar:
                line = highlight_index + 1
                tag = "found" if found else "scan"
                w.tag_add(tag, f"{line}.0", f"{line}.end")
                try:
                    w.see(f"{line}.0")
                except Exception:
                    pass
        except Exception:
            pass
        self.viewer.configure(state="disabled")

    def _set_estado(self, msg: str):
        self.lbl_estado.configure(text=msg)

    def _error(self, msg: str):
        self._set_estado(msg)
        try:
            mb.showerror("Error", msg)
        except Exception:
            pass

    def _parse_key(self) -> tuple[bool, Optional[int], Optional[str]]:
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
            exp = int(self.var_exp.get())
            klen = int(self.var_klen.get())
        except ValueError:
            self._error("Parámetros inválidos")
            return
        try:
            self.structure = LinearStructure(10 ** exp, klen)
        except Exception as e:
            self._error(str(e))
            return
        self._set_estado("Estructura creada.")
        self._set_config_enabled(False)  # Bloquear cambios
        self._set_controls_enabled(True)
        self._update_counters()
        self._refresh_view()

    def on_borrar(self):
        if self.structure is None:
            return
        if not mb.askyesno("Confirmar", "Se borrará la estructura actual. ¿Continuar?"):
            return
        self.on_step_stop()
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
            self._set_estado(f"Insertado {val} en índice {idx}.")
        except Exception as e:
            self._error(str(e))
            return
        self._update_counters()
        self._refresh_view()

    def on_buscar(self):
        ok, val, err = self._parse_key()
        if not ok:
            self._error(err or "")
            return
        idx = self.structure.find(val)  # type: ignore[union-attr]
        if idx == -1:
            self._set_estado(f"{val} no encontrado.")
            self._refresh_view()
        else:
            self._set_estado(f"{val} encontrado en índice {idx}.")
            self._refresh_view(highlight_index=idx, found=True)

    def on_eliminar(self):
        ok, val, err = self._parse_key()
        if not ok:
            self._error(err or "")
            return
        try:
            idx = self.structure.delete(val)  # type: ignore[union-attr]
            self._set_estado(f"Eliminado {val} desde índice {idx}.")
        except Exception as e:
            self._error(str(e))
            return
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
                data = json.load(f)
            struct = LinearStructure.from_dict(data)
        except Exception as e:
            self._error(f"Error al cargar: {e}")
            return
        self.structure = struct
        # Actualizar Selectors y bloquear
        exp = int(round(math.log10(self.structure.capacity)))
        self.var_exp.set(str(exp))
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
        added = self.structure.generate_random(count)
        self._set_estado(f"Generados {added} elementos aleatorios.")
        self._update_counters()
        self._refresh_view()

    # Paso a paso
    def on_step_start(self):
        ok, val, err = self._parse_key()
        if not ok:
            self._error(err or "")
            return
        self.on_step_stop()
        self.step_active = True
        self.step_index = 0
        self.step_target = val
        self._set_controls_enabled(True)
        self._set_estado(f"Paso a paso: buscando {val} desde índice 0…")
        self._refresh_view(highlight_index=self.step_index)

    def on_step_next(self):
        if not self.step_active or not self.structure or self.step_target is None:
            return
        items = self.structure.items
        if self.step_index >= len(items):
            self._set_estado(f"{self.step_target} no encontrado.")
            self.on_step_stop()
            self._refresh_view()
            return
        cur = items[self.step_index]
        if cur == self.step_target:
            self._set_estado(f"Encontrado {cur} en índice {self.step_index}.")
            self._refresh_view(highlight_index=self.step_index, found=True)
            self.on_step_stop()
            return
        # Avanzar
        self._refresh_view(highlight_index=self.step_index)
        self.step_index += 1
        if self.after_id is not None:
            # If auto mode, schedule next
            self.after_id = self.after(self.step_delay_ms, self.on_step_next)

    def on_step_auto(self):
        if not self.step_active:
            # If not started, start from current key
            self.on_step_start()
        if self.after_id is None and self.step_active:
            self.after_id = self.after(self.step_delay_ms, self.on_step_next)
            self.btn_step_stop.configure(state="normal")

    def on_step_stop(self):
        if self.after_id is not None:
            try:
                self.after_cancel(self.after_id)
            except Exception:
                pass
        self.after_id = None
        self.step_active = False
        self.btn_step_stop.configure(state="disabled")
