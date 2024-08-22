import os, json
from flask import Flask, render_template, request

from config import TOKEN

app = Flask(__name__)

@app.route("/<int:chapter_id>")
def index(chapter_id):
    # chapter list
    chapters = []

    with open("./chapters.json", "r", encoding="utf-8") as f:
        # chapters = dict([(int(item[0]), item[1]) for item in json.load(f).items()])
        chapters = [
            {"id": int(item[0]), "title": item[1]} for item in json.load(f).items()
        ]

    # current
    current_index = next(
        i for i, chapter in enumerate(chapters) if chapter["id"] == chapter_id
    )
    current = chapters[current_index]

    with open(f"./chapters/{chapter_id}.txt", "r", encoding="utf-8") as f:
        current["content"] = f.read()

    # previous next
    previous = None
    next_ = None

    if current_index > 0:
        previous = chapters[current_index - 1]

    if current_index < len(chapters) - 1:
        next_ = chapters[current_index + 1]

    return render_template(
        "index.html",
        current=current,
        previous=previous,
        next=next_,
        chapters=chapters,
    )


@app.route("/api/add_chapter", methods=["POST"])
def add_chapter():
    # auth
    if not "Authorization" in request.headers:
        return "Unauthorized", 401

    token = request.headers["Authorization"].split(" ")[1]
    if token != TOKEN:
        return "Unauthorized", 401

    # validate from
    data = request.get_json(force=True)

    if not "id" in data or not "title" in data or not "content" in data:
        return "Wrong entity", 400

    chapter_id = data["id"]
    chapter_title = data["title"]
    chapter_content = data["content"]

    # save file
    with open(f"./chapters/{chapter_id}.txt", "w", encoding="utf-8") as f:
        f.write(chapter_content)

    # add title
    titles = {}

    if os.path.exists("./chapters.json"):
        with open("./chapters.json", "r", encoding="utf-8") as f:
            titles = json.load(f)

    titles[str(chapter_id)] = chapter_title
    titles = dict(sorted(titles.items(), key=lambda item: int(item[0])))

    with open("./chapters.json", "w", encoding="utf-8") as f:
        json.dump(titles, f)

    return "Chapter uploaded", 200
