from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
    abort,
)

from routes import *

from models.topic import Topic


main = Blueprint('topic', __name__)

import uuid
csrf_tokens = dict()
@main.route("/")
def index():
    ms = Topic.all()
    token = str(uuid.uuid4())
    u = current_user()
    csrf_tokens['token'] = u.id
    return render_template("topic/index.html", ms=ms, token=token)


@main.route('/<int:id>')
def detail(id):
    m = Topic.get(id)
    # 传递 topic 的所有 reply 到 页面中
    return render_template("topic/detail.html", topic=m)


@main.route("/add", methods=["POST"])
def add():
    form = request.form
    u = current_user()
    m = Topic.new(form, user_id=u.id)
    return redirect(url_for('.detail', id=m.id))


@main.route("/delete")
def delete():
    id = int(request.args.get('id'))
    token = request.args.get('token')
    u = current_user()
    if token in csrf_tokens and csrf_tokens['token'] == u.id:
        csrf_tokens.pop(token)
        if u is not None:
            Topic.delete(id)
            return redirect(url_for('.index', token=token))
        else:
            abort(404)
    else:
        abort(403)


@main.route("/new")
def new():
    return render_template("topic/new.html")
