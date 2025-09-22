from __future__ import annotations

from .external_base import ExternalBaseContent
from models.external import ExternalBinaryStructure


class ExternalBinaryContent(ExternalBaseContent):
    title = "B. Externas · Búsqueda Binaria"
    structure_cls = ExternalBinaryStructure
    search_button_text = "Buscar (bin.)"
    search_kind_label = "binaria"
