import re
from datetime import date, datetime
from typing import Dict, List, Optional

from src.models.pessoa import Pessoa
from src.repositories.pessoa_repository import PessoaRepository


class ValidacaoError(Exception):
    def __init__(self, erros: Dict[str, str]):
        super().__init__("Dados inválidos")
        self.erros = erros


def somente_digitos(texto: str) -> str:
    return re.sub(r"\D", "", texto or "")


def cpf_valido(cpf: str) -> bool:
    cpf = somente_digitos(cpf)
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False
    for tam in (9, 10):
        soma = sum(int(cpf[i]) * (tam + 1 - i) for i in range(tam))
        dv = (soma * 10) % 11 % 10
        if dv != int(cpf[tam]):
            return False
    return True


class PessoaService:
    """Regras de negócio do cadastro. Depende apenas da abstração do repositório."""

    def __init__(self, repositorio: PessoaRepository):
        self._repo = repositorio

    def listar(self, busca: str = "") -> List[Pessoa]:
        return self._repo.listar(busca)

    def obter(self, pessoa_id: int) -> Optional[Pessoa]:
        return self._repo.obter(pessoa_id)

    def cadastrar(self, dados: dict) -> Pessoa:
        pessoa = self._montar(dados)
        self._validar(pessoa)
        return self._repo.salvar(pessoa)

    def atualizar(self, pessoa_id: int, dados: dict) -> Pessoa:
        if self._repo.obter(pessoa_id) is None:
            raise LookupError("Pessoa não encontrada")
        pessoa = self._montar(dados)
        pessoa.id = pessoa_id
        self._validar(pessoa)
        return self._repo.salvar(pessoa)

    def excluir(self, pessoa_id: int) -> bool:
        return self._repo.excluir(pessoa_id)

    @staticmethod
    def _montar(d: dict) -> Pessoa:
        return Pessoa(nome=(d.get("nome") or "").strip(),
                      cpf=somente_digitos(d.get("cpf", "")),
                      email=(d.get("email") or "").strip().lower(),
                      telefone=somente_digitos(d.get("telefone", "")),
                      data_nascimento=(d.get("data_nascimento") or "").strip())

    def _validar(self, p: Pessoa) -> None:
        erros: Dict[str, str] = {}
        if len(p.nome) < 3:
            erros["nome"] = "Informe o nome completo (mínimo 3 caracteres)."
        if not cpf_valido(p.cpf):
            erros["cpf"] = "CPF inválido."
        else:
            existente = self._repo.obter_por_cpf(p.cpf)
            if existente and existente.id != p.id:
                erros["cpf"] = "CPF já cadastrado."
        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", p.email):
            erros["email"] = "E-mail inválido."
        if p.telefone and len(p.telefone) not in (10, 11):
            erros["telefone"] = "Telefone deve ter 10 ou 11 dígitos."
        if p.data_nascimento:
            try:
                if datetime.strptime(p.data_nascimento, "%Y-%m-%d").date() > date.today():
                    erros["data_nascimento"] = "Data de nascimento no futuro."
            except ValueError:
                erros["data_nascimento"] = "Data inválida."
        if erros:
            raise ValidacaoError(erros)
