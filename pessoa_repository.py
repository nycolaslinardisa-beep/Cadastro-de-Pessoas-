from abc import ABC, abstractmethod
from typing import List, Optional

from src.models.pessoa import Pessoa


class PessoaRepository(ABC):
    """Abstração de persistência (Dependency Inversion)."""

    @abstractmethod
    def listar(self, busca: str = "") -> List[Pessoa]: ...

    @abstractmethod
    def obter(self, pessoa_id: int) -> Optional[Pessoa]: ...

    @abstractmethod
    def obter_por_cpf(self, cpf: str) -> Optional[Pessoa]: ...

    @abstractmethod
    def salvar(self, pessoa: Pessoa) -> Pessoa: ...

    @abstractmethod
    def excluir(self, pessoa_id: int) -> bool: ...
