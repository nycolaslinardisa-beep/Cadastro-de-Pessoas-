from flask import Blueprint, abort, redirect, render_template, request, url_for, flash

from src.services.pessoa_service import PessoaService, ValidacaoError


def criar_blueprint(service: PessoaService) -> Blueprint:
    """O serviço é injetado pelo composition root (app.py)."""
    bp = Blueprint("pessoas", __name__)

    @bp.get("/")
    def listar():
        busca = request.args.get("q", "")
        return render_template("lista.html", pessoas=service.listar(busca), busca=busca)

    @bp.route("/pessoas/nova", methods=["GET", "POST"])
    def nova():
        if request.method == "POST":
            try:
                service.cadastrar(request.form)
                flash("Pessoa cadastrada com sucesso.")
                return redirect(url_for("pessoas.listar"))
            except ValidacaoError as e:
                return render_template("form.html", dados=request.form, erros=e.erros, titulo="Nova pessoa")
        return render_template("form.html", dados={}, erros={}, titulo="Nova pessoa")

    @bp.route("/pessoas/<int:pessoa_id>/editar", methods=["GET", "POST"])
    def editar(pessoa_id):
        pessoa = service.obter(pessoa_id)
        if pessoa is None:
            abort(404)
        if request.method == "POST":
            try:
                service.atualizar(pessoa_id, request.form)
                flash("Cadastro atualizado.")
                return redirect(url_for("pessoas.listar"))
            except ValidacaoError as e:
                return render_template("form.html", dados=request.form, erros=e.erros, titulo="Editar pessoa")
        return render_template("form.html", dados=pessoa.__dict__, erros={}, titulo="Editar pessoa")

    @bp.post("/pessoas/<int:pessoa_id>/excluir")
    def excluir(pessoa_id):
        if not service.excluir(pessoa_id):
            abort(404)
        flash("Pessoa excluída.")
        return redirect(url_for("pessoas.listar"))

    return bp
