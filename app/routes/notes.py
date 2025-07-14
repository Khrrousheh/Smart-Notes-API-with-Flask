from flask import Blueprint, request, jsonify
from app.models import db, Note, Tag

notes_bp = Blueprint("notes", __name__)


# -------------------------------
# Get all notes (with filtering)
# -------------------------------
@notes_bp.route("/notes", methods=["GET"])
def get_notes():
    """
    Get all notes
    ---
    parameters:
      - name: tag
        in: query
        type: string
        required: false
        description: Filter notes by tag
      - name: search
        in: query
        type: string
        required: false
        description: Search notes by title/content
    responses:
      200:
        description: A list of notes
    """
    tag_filter = request.args.get("tag")
    search_query = request.args.get("search")

    query = Note.query

    if tag_filter:
        query = query.join(Note.tags).filter(Tag.name == tag_filter)

    if search_query:
        query = query.filter(
            Note.title.ilike(f"%{search_query}%") |
            Note.content.ilike(f"%{search_query}%")
        )

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


# -------------------------------
# Create a new note
# -------------------------------
@notes_bp.route("/notes", methods=["POST"])
def create_note():
    """
    Create a new note
    ---
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - title
          properties:
            title:
              type: string
            content:
              type: string
            tags:
              type: array
              items:
                type: string
    responses:
      201:
        description: Note created
      400:
        description: Missing required fields
    """
    data = request.get_json()
    title = data.get("title")
    content = data.get("content", "")
    tag_names = data.get("tags", [])

    if not title:
        return jsonify({"error": "Title is required"}), 400

    note = Note(title=title, content=content)

    for tag_name in tag_names:
        tag = Tag.query.filter_by(name=tag_name).first()
        if not tag:
            tag = Tag(name=tag_name)
        note.tags.append(tag)

    db.session.add(note)
    db.session.commit()

    return jsonify({
        "message": "Note created",
        "id": note.id
    }), 201


# -------------------------------
# Get a specific note
# -------------------------------
@notes_bp.route("/notes/<int:note_id>", methods=["GET"])
def get_note(note_id):
    """
    Get a single note by ID
    ---
    parameters:
      - name: note_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: A single note
      404:
        description: Note not found
    """
    note = Note.query.get_or_404(note_id)
    return jsonify({
        "id": note.id,
        "title": note.title,
        "content": note.content,
        "tags": [tag.name for tag in note.tags]
    })


# -------------------------------
# Update a note
# -------------------------------
@notes_bp.route("/notes/<int:note_id>", methods=["PUT"])
def update_note(note_id):
    """
    Update a note
    ---
    parameters:
      - name: note_id
        in: path
        type: integer
        required: true
      - in: body
        name: body
        schema:
          type: object
          properties:
            title:
              type: string
            content:
              type: string
            tags:
              type: array
              items:
                type: string
    responses:
      200:
        description: Note updated
      404:
        description: Note not found
    """
    note = Note.query.get_or_404(note_id)
    data = request.get_json()

    note.title = data.get("title", note.title)
    note.content = data.get("content", note.content)

    if "tags" in data:
        tag_names = data["tags"]
        note.tags.clear()
        for tag_name in tag_names:
            tag = Tag.query.filter_by(name=tag_name).first()
            if not tag:
                tag = Tag(name=tag_name)
            note.tags.append(tag)

    db.session.commit()
    return jsonify({"message": "Note updated"})


# -------------------------------
# Delete a note
# -------------------------------
@notes_bp.route("/notes/<int:note_id>", methods=["DELETE"])
def delete_note(note_id):
    """
    Delete a note
    ---
    parameters:
      - name: note_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Note deleted
      404:
        description: Note not found
    """
    note = Note.query.get_or_404(note_id)

    try:
        db.session.delete(note)
        db.session.commit()
        return jsonify({"message": "Note deleted"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Internal server error", "details": str(e)}), 500


# -------------------------------
# List all tags
# -------------------------------
@notes_bp.route("/tags", methods=["GET"])
def get_tags():
    """
    Get all tags
    ---
    responses:
      200:
        description: List of all tags
    """
    tags = Tag.query.order_by(Tag.name).all()
    return jsonify([tag.name for tag in tags])
