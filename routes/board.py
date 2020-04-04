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
    if u.role == 1:
        m = Board.new(form)
        return redirect(url_for('.index'))
    else:
        abort(403)


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
    print(b)
    return redirect(url_for('.index'))

