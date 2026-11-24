from typing import Dict, List, Optional

from src.models.pessoa import Pessoa
from src.repositories.pessoa_repository import PessoaRepository


class MemoryPessoaRepository(PessoaRepository):
    def __init__(self):
        self._dados: Dict[int, Pessoa] = {}
        self._proximo_id = 1

    def listar(self, busca: str = "") -> List[Pessoa]:
        b = busca.lower().strip()
        return [p for p in self._dados.values()
                if not b or b in p.nome.lower() or b in p.cpf or b in p.email.lower()]

    def obter(self, pessoa_id: int) -> Optional[Pessoa]:
        return self._dados.get(pessoa_id)

    def obter_por_cpf(self, cpf: str) -> Optional[Pessoa]:
        return next((p for p in self._dados.values() if p.cpf == cpf), None)

    def salvar(self, pessoa: Pessoa) -> Pessoa:
        if pessoa.id is None:
            pessoa.id = self._proximo_id
            self._proximo_id += 1
        self._dados[pessoa.id] = pessoa
        return pessoa

    def excluir(self, pessoa_id: int) -> bool:
        return self._dados.pop(pessoa_id, None) is not None
