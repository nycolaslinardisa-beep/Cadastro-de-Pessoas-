from dataclasses import dataclass
from typing import Optional


@dataclass
class Pessoa:
    nome: str
    cpf: str
    email: str
    telefone: str = ""
    data_nascimento: str = ""  # formato AAAA-MM-DD
    id: Optional[int] = None
