"""Composition root: único lugar que conhece as implementações concretas."""
import os

from flask import Flask

from src.controllers.pessoa_controller import criar_blueprint
from src.repositories.sqlite_pessoa_repository import SqlitePessoaRepository
from src.services.pessoa_service import PessoaService


def criar_app(repositorio=None) -> Flask:
    app = Flask(__name__, template_folder="src/views")
    app.secret_key = os.environ.get("SECRET_KEY", "dev-n3")
    repositorio = repositorio or SqlitePessoaRepository("pessoas.db")  # injeção de dependência
    service = PessoaService(repositorio)
    app.register_blueprint(criar_blueprint(service))
    return app


if __name__ == "__main__":
    criar_app().run(debug=False)
