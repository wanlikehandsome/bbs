from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
    abort
)

from routes import *

from models.board import Board


main = Blueprint('board', __name__)


@main.route("/add", methods=["POST"])
def add():
    form = request.form
    u = current_user()
    m = Board.new(form)
    return redirect(url_for('.index'))



@main.route("/admin")
def index():
    u = current_user()
    bs = Board.all()
    return render_template("board/admin_index.html", bs=bs)


@main.route("/delete")
def delete():
    board_id = int(request.args.get('board_id', -1))
    b = Board.find(id=board_id)
    b.delete()
    return redirect(url_for('.index'))

