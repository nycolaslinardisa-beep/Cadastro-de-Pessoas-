# Cadastro de Pessoas

Trabalho N3. Sistema web de cadastro de pessoas (CRUD) organizado em MVC, com padrão Repository e injeção de dependência.

## Integrantes

- Fabricio Salvino Martins
- Nycolas Souza Linard

## Tema

Cadastro de pessoas.

## Descrição

A aplicação permite cadastrar, listar, buscar, editar e excluir pessoas. Cada pessoa possui nome, CPF, e-mail, telefone e data de nascimento.

Regras de negócio implementadas no serviço:

- nome com no mínimo 3 caracteres;
- CPF validado pelos dígitos verificadores e sem duplicidade;
- e-mail em formato válido;
- telefone opcional com 10 ou 11 dígitos;
- data de nascimento opcional, em formato válido e não futura.

## Arquitetura

| Camada | Local | Responsabilidade |
|---|---|---|
| Model | `src/models` | Entidade `Pessoa` |
| View | `src/views` | Templates HTML |
| Controller | `src/controllers` | Rotas HTTP; delega ao serviço |
| Service | `src/services` | Regras de negócio e validação |
| Repository | `src/repositories` | Interface `PessoaRepository` e duas implementações: SQLite e memória |
| Composition root | `app.py` | Cria as implementações concretas e as injeta no serviço e no controller |

Princípios SOLID aplicados:

- **S**: cada classe tem uma responsabilidade (controller trata HTTP, service trata regras, repository trata persistência).
- **O**: novas formas de persistência são adicionadas criando outra implementação de `PessoaRepository`, sem alterar o serviço.
- **L**: `SqlitePessoaRepository` e `MemoryPessoaRepository` são intercambiáveis.
- **I**: a interface do repositório contém apenas as operações usadas.
- **D**: `PessoaService` depende da abstração `PessoaRepository`, e o controller depende do serviço, ambos recebidos por injeção.

Os diagramas (classes, camadas, sequência e caso de uso) estão em [`docs/diagramas.md`](docs/diagramas.md), em Mermaid, renderizado automaticamente pelo GitHub.

## Ferramentas de IA utilizadas

- Claude (Anthropic): geração inicial da estrutura do projeto, do código e da documentação, revisados pelo grupo.

## Como executar

Requisitos: Python 3.10 ou superior.

```bash
git clone <URL-DO-REPOSITORIO>
cd cadastro-pessoas
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Acesse http://127.0.0.1:5000 no navegador. O banco `pessoas.db` é criado automaticamente na primeira execução.

CPF válido para teste: `529.982.247-25`.

## Testes

```bash
python -m unittest -v
```
