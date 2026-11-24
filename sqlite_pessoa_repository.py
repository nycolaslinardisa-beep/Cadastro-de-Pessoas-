import sqlite3
from typing import List, Optional

from src.models.pessoa import Pessoa
from src.repositories.pessoa_repository import PessoaRepository


class SqlitePessoaRepository(PessoaRepository):
    def __init__(self, caminho: str = "pessoas.db"):
        self._caminho = caminho
        with self._conn() as c:
            c.execute("""CREATE TABLE IF NOT EXISTS pessoas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                cpf TEXT NOT NULL UNIQUE,
                email TEXT NOT NULL,
                telefone TEXT,
                data_nascimento TEXT)""")

    def _conn(self):
        return sqlite3.connect(self._caminho)

    @staticmethod
    def _para_pessoa(l) -> Pessoa:
        return Pessoa(id=l[0], nome=l[1], cpf=l[2], email=l[3],
                      telefone=l[4] or "", data_nascimento=l[5] or "")

    def listar(self, busca: str = "") -> List[Pessoa]:
        like = f"%{busca.strip()}%"
        with self._conn() as c:
            linhas = c.execute(
                "SELECT id,nome,cpf,email,telefone,data_nascimento FROM pessoas "
                "WHERE nome LIKE ? OR cpf LIKE ? OR email LIKE ? ORDER BY nome",
                (like, like, like)).fetchall()
        return [self._para_pessoa(l) for l in linhas]

    def obter(self, pessoa_id: int) -> Optional[Pessoa]:
        with self._conn() as c:
            l = c.execute("SELECT id,nome,cpf,email,telefone,data_nascimento "
                          "FROM pessoas WHERE id=?", (pessoa_id,)).fetchone()
        return self._para_pessoa(l) if l else None

    def obter_por_cpf(self, cpf: str) -> Optional[Pessoa]:
        with self._conn() as c:
            l = c.execute("SELECT id,nome,cpf,email,telefone,data_nascimento "
                          "FROM pessoas WHERE cpf=?", (cpf,)).fetchone()
        return self._para_pessoa(l) if l else None

    def salvar(self, pessoa: Pessoa) -> Pessoa:
        with self._conn() as c:
            if pessoa.id is None:
                cur = c.execute(
                    "INSERT INTO pessoas(nome,cpf,email,telefone,data_nascimento) "
                    "VALUES(?,?,?,?,?)",
                    (pessoa.nome, pessoa.cpf, pessoa.email, pessoa.telefone, pessoa.data_nascimento))
                pessoa.id = cur.lastrowid
            else:
                c.execute(
                    "UPDATE pessoas SET nome=?,cpf=?,email=?,telefone=?,data_nascimento=? WHERE id=?",
                    (pessoa.nome, pessoa.cpf, pessoa.email, pessoa.telefone,
                     pessoa.data_nascimento, pessoa.id))
        return pessoa

    def excluir(self, pessoa_id: int) -> bool:
        with self._conn() as c:
            return c.execute("DELETE FROM pessoas WHERE id=?", (pessoa_id,)).rowcount > 0
