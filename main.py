import os, json
from flask import Flask, render_template, request
from flask_pydantic import validate
from flask_httpauth import HTTPTokenAuth

from config import TOKEN
from model import Chapter

import service

app = Flask(__name__)
auth = HTTPTokenAuth(scheme="Bearer")


@auth.verify_token
def verify_token(token):
    return token == TOKEN


@app.route("/<string:book_id>/<int:number>", methods=["GET"])
def chapter(book_id: str, number: int):
    chapters = service.list_chapters(book_id)
    cur_chapter = service.get_chapter(book_id, number)

    if cur_chapter == None:
        return "not found", 404

    cur_index = next(
        i for i, chapter in enumerate(chapters) if chapter.number == number
    )

    prev_chapter = chapters[cur_index - 1] if cur_index > 0 else None
    next_chapter = chapters[cur_index + 1] if cur_index < len(chapters) - 1 else None

    return render_template(
        "chapter.j2",
        current=cur_chapter,
        previous=prev_chapter,
        next=next_chapter,
        chapters=chapters,
    )


@app.route("/api/upload", methods=["POST"])
@validate()
@auth.login_required
def upload(body: Chapter):
    service.add_chapter(body)
    return "ok", 200
