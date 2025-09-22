from __future__ import annotations

from .external_base import ExternalBaseContent
from models.external import ExternalSequentialStructure


class ExternalSequentialContent(ExternalBaseContent):
    title = "B. Externas · Búsqueda Secuencial"
    structure_cls = ExternalSequentialStructure
    search_button_text = "Buscar (sec.)"
    search_kind_label = "secuencial"
