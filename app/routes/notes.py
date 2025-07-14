from flask import Blueprint, request, jsonify
from app.models import db, Note, Tag

notes_bp = Blueprint("notes", __name__)

@notes_bp.route('/notes', methods=["GET"])
def get_notes():
    tag_filter = request.args.get('tag')
    search_query = request.args.get('search')

    query = Note.query

    if tag_filter:
        query = query.join(Note.tags).filter(Tag.name == tag_filter)

    if search_query:
        query = query.join(Note.title.contains(search_query) | Note.content.contains(search_query))

    notes = query.order_by(Note.created_at.desc()).all()

    result = [
        {
            "id": note.id,
            "title": note.title,
            "content": note.content,
            "tags": [tag.name for tag in note.tags]
        }
        for note in notes
    ]
    return jsonify(result)

@notes_bp.route('/notes',methods=['POST'])
def create_note():
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')
    tag_names = data.get('tags', [])

    if not title:
        return jsonify({"error": "title is required"}), 400

    note = Note(title=title, content=content)
    for tag_name in tag_names:
        tag = Tag.query.filter_by(name=tag_name).first()
        if not tag:
            tag = Tag(name=tag_name)
        note.tags.append(tag)

    db.session.add(note)
    db.session.commit()

    return jsonify({"message": "Note created"}), 201

@notes_bp.route("/notes/<int:note_id>", methods=["DELETE"])
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)
    try:
        db.session.delete(note)
        db.session.commit()
    except:
        return jsonify({"error": "bad request note is not in the db"}), 404
    return jsonify({"message": "Note deleted"})

@notes_bp.route("/tags", methods=["GET"])
def get_tags():
    tags = Tag.query.all()
    return jsonify([tag.name for tag in tags])
