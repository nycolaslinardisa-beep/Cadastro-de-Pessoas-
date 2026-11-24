import unittest

from app import criar_app
from src.repositories.memory_pessoa_repository import MemoryPessoaRepository
from src.services.pessoa_service import PessoaService, ValidacaoError, cpf_valido

VALIDO = {"nome": "Maria Silva", "cpf": "529.982.247-25", "email": "maria@exemplo.com",
          "telefone": "(64) 99999-1234", "data_nascimento": "1990-05-10"}


class ServiceTest(unittest.TestCase):
    def setUp(self):
        self.s = PessoaService(MemoryPessoaRepository())

    def test_cpf(self):
        self.assertTrue(cpf_valido("529.982.247-25"))
        self.assertFalse(cpf_valido("111.111.111-11"))
        self.assertFalse(cpf_valido("123"))

    def test_cadastrar_e_listar(self):
        p = self.s.cadastrar(VALIDO)
        self.assertEqual(p.id, 1)
        self.assertEqual(len(self.s.listar()), 1)
        self.assertEqual(len(self.s.listar("maria")), 1)
        self.assertEqual(len(self.s.listar("zzz")), 0)

    def test_cpf_duplicado(self):
        self.s.cadastrar(VALIDO)
        with self.assertRaises(ValidacaoError) as ctx:
            self.s.cadastrar(VALIDO)
        self.assertIn("cpf", ctx.exception.erros)

    def test_dados_invalidos(self):
        with self.assertRaises(ValidacaoError) as ctx:
            self.s.cadastrar({"nome": "A", "cpf": "1", "email": "x"})
        self.assertEqual({"nome", "cpf", "email"}, set(ctx.exception.erros))

    def test_atualizar_e_excluir(self):
        p = self.s.cadastrar(VALIDO)
        self.s.atualizar(p.id, {**VALIDO, "nome": "Maria Souza"})
        self.assertEqual(self.s.obter(p.id).nome, "Maria Souza")
        self.assertTrue(self.s.excluir(p.id))
        self.assertFalse(self.s.excluir(p.id))


class HttpTest(unittest.TestCase):
    def test_fluxo(self):
        c = criar_app(MemoryPessoaRepository()).test_client()
        self.assertEqual(c.get("/").status_code, 200)
        r = c.post("/pessoas/nova", data=VALIDO, follow_redirects=True)
        self.assertIn("Maria Silva", r.get_data(as_text=True))
        r = c.post("/pessoas/nova", data={**VALIDO, "cpf": "000"})
        self.assertIn("CPF inválido", r.get_data(as_text=True))
        self.assertEqual(c.post("/pessoas/1/excluir").status_code, 302)


if __name__ == "__main__":
    unittest.main()
