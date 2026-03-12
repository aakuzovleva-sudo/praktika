from fastapi import FastAPI, HTTPException, Query, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from schemas import Note, NoteCreate, NoteUpdate
from database import SessionLocal, engine, Base
from models import NoteDB

app = FastAPI(title="NoteAPI")

templates = Jinja2Templates(directory="templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# создаём таблицы
Base.metadata.create_all(bind=engine)


# -----------------------
# Подключение к БД
# -----------------------

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -----------------------
# Главная страница
# -----------------------

@app.get("/", response_class=HTMLResponse)
def home():

    return """
    <html>
    <head>
        <title>Note Manager</title>

        <style>

        body{
            font-family: Arial;
            background:#ffe6f0;
            text-align:center;
            padding-top:80px;
        }

        h1{
            color:#d63384;
            margin-bottom:40px;
        }

        .menu{
            display:flex;
            flex-direction:column;
            gap:15px;
            width:220px;
            margin:auto;
        }

        button{
            background:#ffb6d9;
            border:none;
            padding:15px;
            border-radius:12px;
            font-size:16px;
            cursor:pointer;
            transition:0.3s;
            box-shadow:0 4px 8px rgba(0,0,0,0.1);
        }

        button:hover{
            background:#ff8fc5;
            transform:scale(1.05);
        }

        </style>
    </head>

    <body>

        <h1>🌸 Note Manager 🌸</h1>

        <div class="menu">

        <button onclick="location.href='/get'">Посмотреть заметки</button>

        <button onclick="location.href='/post'">Создать заметку</button>

        <button onclick="location.href='/put'">Полностью изменить</button>

        <button onclick="location.href='/patch'">Частично изменить</button>

        <button onclick="location.href='/delete'">Удалить заметку</button>

        </div>

    </body>
    </html>
    """

# -----------------------
# HTML страницы
# -----------------------

@app.get("/get", response_class=HTMLResponse)
def get_page():

    return """
    <html>
    <head>
    <title>GET</title>

    <style>

    body{
        font-family:Arial;
        background:#ffe6f0;
        text-align:center;
        padding-top:60px;
    }

    h1{color:#d63384;}

    button{
        background:#ffb6d9;
        border:none;
        padding:12px 20px;
        margin:10px;
        border-radius:12px;
        font-size:16px;
        cursor:pointer;
    }

    button:hover{
        background:#ff8fc5;
    }

    .note{
        background:white;
        padding:15px;
        border-radius:10px;
        width:300px;
        margin:10px auto;
    }

    </style>
    </head>

    <body>

    <h1>📄 Все заметки</h1>

    <button onclick="getNotes()">Показать заметки</button>

    <div id="notes"></div>

    <br>
    <button onclick="location.href='/'">⬅ Назад</button>

    <script>

    function getNotes(){

        fetch('/notes')
        .then(res => res.json())
        .then(data => {

            let html="";

            data.forEach(note => {
                html += `
                <div class="note">
                <b>ID:</b> ${note.id}<br>
                <b>Title:</b> ${note.title}<br>
                <b>Content:</b> ${note.content}
                </div>
                `;
            });

            document.getElementById("notes").innerHTML = html;

        });

    }

    </script>

    </body>
    </html>
    """


@app.get("/post", response_class=HTMLResponse)
def post_page():

    return """
    <html>
    <head>

    <style>
    body{font-family:Arial;background:#ffe6f0;text-align:center;padding-top:60px;}
    h1{color:#d63384;}

    input{
        padding:10px;
        margin:5px;
        border-radius:10px;
        border:1px solid pink;
    }

    button{
        background:#ffb6d9;
        border:none;
        padding:10px 20px;
        border-radius:10px;
        margin:5px;
        cursor:pointer;
    }

    button:hover{background:#ff8fc5;}
    </style>

    </head>

    <body>

    <h1>➕ Создать заметку</h1>

    <input id="title" placeholder="Title"><br>
    <input id="content" placeholder="Content"><br>

    <button onclick="createNote()">Создать</button>

    <br><br>

    <button onclick="location.href='/'">⬅ Назад</button>

    <script>

    function createNote(){

        fetch('/notes',{

            method:'POST',

            headers:{
                'Content-Type':'application/json'
            },

            body:JSON.stringify({
                title:document.getElementById("title").value,
                content:document.getElementById("content").value,
                is_public:true
            })

        })
        .then(res=>res.json())
        .then(data=>alert("Заметка создана"));

    }

    </script>

    </body>
    </html>
    """


@app.get("/put", response_class=HTMLResponse)
def put_page():

    return """
    <html>
    <head>

    <style>
    body{font-family:Arial;background:#ffe6f0;text-align:center;padding-top:60px;}
    h1{color:#d63384;}

    input{
        padding:10px;
        margin:5px;
        border-radius:10px;
        border:1px solid pink;
    }

    button{
        background:#ffb6d9;
        border:none;
        padding:10px 20px;
        border-radius:10px;
    }

    button:hover{background:#ff8fc5;}
    </style>

    </head>

    <body>

    <h1>✏ Изменить заметку</h1>

    <input id="id" placeholder="ID"><br>
    <input id="title" placeholder="Title"><br>
    <input id="content" placeholder="Content"><br>

    <button onclick="updateNote()">Изменить</button>

    <br><br>

    <button onclick="location.href='/'">⬅ Назад</button>

    <script>

    function updateNote(){

        let id=document.getElementById("id").value;

        fetch('/notes/'+id,{
            method:'PUT',
            headers:{'Content-Type':'application/json'},

            body:JSON.stringify({
                title:document.getElementById("title").value,
                content:document.getElementById("content").value,
                is_public:true
            })

        })
        .then(res=>res.json())
        .then(data=>alert("Обновлено"));

    }

    </script>

    </body>
    </html>
    """


@app.get("/patch", response_class=HTMLResponse)
def patch_page():

    return """
    <html>
    <head>

    <style>
    body{font-family:Arial;background:#ffe6f0;text-align:center;padding-top:60px;}
    h1{color:#d63384;}

    input{
        padding:10px;
        margin:5px;
        border-radius:10px;
        border:1px solid pink;
    }

    button{
        background:#ffb6d9;
        border:none;
        padding:10px 20px;
        border-radius:10px;
    }

    button:hover{background:#ff8fc5;}
    </style>

    </head>

    <body>

    <h1>🩹 Частично изменить</h1>

    <input id="id" placeholder="ID"><br>
    <input id="title" placeholder="Новый title"><br>

    <button onclick="patchNote()">Изменить</button>

    <br><br>

    <button onclick="location.href='/'">⬅ Назад</button>

    <script>

    function patchNote(){

        let id=document.getElementById("id").value;

        fetch('/notes/'+id,{
            method:'PATCH',
            headers:{'Content-Type':'application/json'},

            body:JSON.stringify({
                title:document.getElementById("title").value
            })

        })
        .then(res=>res.json())
        .then(data=>alert("Изменено"));

    }

    </script>

    </body>
    </html>
    """


@app.get("/delete", response_class=HTMLResponse)
def delete_page():

    return """
    <html>
    <head>

    <style>
    body{font-family:Arial;background:#ffe6f0;text-align:center;padding-top:60px;}
    h1{color:#d63384;}

    input{
        padding:10px;
        border-radius:10px;
        border:1px solid pink;
    }

    button{
        background:#ffb6d9;
        border:none;
        padding:10px 20px;
        border-radius:10px;
        margin:5px;
    }

    button:hover{background:#ff8fc5;}
    </style>

    </head>

    <body>

    <h1>🗑 Удалить заметку</h1>

    <input id="id" placeholder="ID заметки">

    <button onclick="deleteNote()">Удалить</button>

    <br><br>

    <button onclick="location.href='/'">⬅ Назад</button>

    <script>

    function deleteNote(){

        let id=document.getElementById("id").value;

        fetch('/notes/'+id,{
            method:'DELETE'
        })
        .then(res=>res.json())
        .then(data=>alert("Удалено"));

    }

    </script>

    </body>
    </html>
    """


# -----------------------
# CREATE
# -----------------------

@app.post("/notes", response_model=Note)
def create_note(note: NoteCreate, db: Session = Depends(get_db)):
    new_note = NoteDB(
        title=note.title,
        content=note.content,
        is_public=note.is_public
    )

    db.add(new_note)
    db.commit()
    db.refresh(new_note)

    return new_note


# -----------------------
# READ ALL
# -----------------------

@app.get("/notes", response_model=List[Note])
def get_notes(public_only: bool = Query(False), db: Session = Depends(get_db)):

    notes = db.query(NoteDB).all()

    if public_only:
        notes = [note for note in notes if note.is_public]

    return notes


# -----------------------
# READ ONE
# -----------------------

@app.get("/notes/{note_id}", response_model=Note)
def get_note(note_id: int, db: Session = Depends(get_db)):

    note = db.query(NoteDB).filter(NoteDB.id == note_id).first()

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    return note


# -----------------------
# UPDATE
# -----------------------

@app.put("/notes/{note_id}", response_model=Note)
def update_note(note_id: int, updated_note: NoteCreate, db: Session = Depends(get_db)):

    note = db.query(NoteDB).filter(NoteDB.id == note_id).first()

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    note.title = updated_note.title
    note.content = updated_note.content
    note.is_public = updated_note.is_public

    db.commit()
    db.refresh(note)

    return note


# -----------------------
# PATCH
# -----------------------

@app.patch("/notes/{note_id}")
def patch_note(note_id: int, updated_data: NoteUpdate, db: Session = Depends(get_db)):

    note = db.query(NoteDB).filter(NoteDB.id == note_id).first()

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    data = updated_data.dict(exclude_unset=True)

    for key, value in data.items():
        setattr(note, key, value)

    db.commit()
    db.refresh(note)

    return note


# -----------------------
# DELETE
# -----------------------

@app.delete("/notes/{note_id}")
def delete_note(note_id: int, db: Session = Depends(get_db)):

    note = db.query(NoteDB).filter(NoteDB.id == note_id).first()

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    db.delete(note)
    db.commit()

    return {"message": "Note deleted successfully"}