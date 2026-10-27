from datetime import date, datetime, timedelta
from pathlib import Path
import sqlite3

from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "pytasks-dev-key-change-me"
DATABASE = Path(__file__).with_name("tasks.db")


def get_connection():
    """Abre uma conexão com o banco de dados SQLite."""
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    """Cria a tabela e adiciona o campo de prazo em bancos antigos."""
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                due_date TEXT,
                completed INTEGER NOT NULL DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        columns = [row["name"] for row in connection.execute("PRAGMA table_info(tasks)")]
        if "due_date" not in columns:
            connection.execute("ALTER TABLE tasks ADD COLUMN due_date TEXT")


def group_tasks_by_day(tasks):
    """Agrupa as tarefas por prazo e destaca hoje, amanhã e atrasadas."""
    today = date.today()
    tomorrow = today + timedelta(days=1)
    groups = {}

    for task in tasks:
        raw_due_date = task["due_date"]
        if not raw_due_date:
            key, label, order = "no-date", "SEM PRAZO", "9999-12-31"
        else:
            due = date.fromisoformat(raw_due_date)
            key = raw_due_date
            order = raw_due_date
            if due < today:
                label = f"ATRASADAS · {due.strftime('%d/%m/%Y')}" if not task["completed"] else due.strftime("%d/%m/%Y")
            elif due == today:
                label = "HOJE · " + due.strftime("%d/%m/%Y")
            elif due == tomorrow:
                label = "AMANHÃ · " + due.strftime("%d/%m/%Y")
            else:
                label = due.strftime("%d/%m/%Y · %A").upper()
        if key not in groups:
            groups[key] = {"key": key, "label": label, "order": order, "tasks": []}
        groups[key]["tasks"].append(task)

    result = list(groups.values())
    result.sort(key=lambda group: (group["key"] == "no-date", group["order"]))
    return result


@app.route("/")
def index():
    """Exibe tarefas organizadas por prazo e os indicadores gerais."""
    with get_connection() as connection:
        tasks = connection.execute("SELECT * FROM tasks ORDER BY completed ASC, due_date IS NULL, due_date ASC, id DESC").fetchall()
        total = connection.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]
        completed = connection.execute("SELECT COUNT(*) FROM tasks WHERE completed = 1").fetchone()[0]
    pending_tasks = [task for task in tasks if not task["completed"]]
    completed_tasks = [task for task in tasks if task["completed"]]
    pending_groups = group_tasks_by_day(pending_tasks)
    completed_groups = group_tasks_by_day(completed_tasks)
    return render_template(
        "index.html", pending_groups=pending_groups,
        completed_groups=completed_groups, total=total,
        completed=completed, pending=total - completed,
        today=date.today().isoformat()
    )


@app.route("/add", methods=["POST"])
def add_task():
    """Valida e cadastra uma tarefa com prazo final opcional."""
    title = request.form.get("title", "").strip()
    due_date = request.form.get("due_date", "").strip() or None
    if not title:
        flash("Digite uma descrição para a tarefa.", "error")
    elif len(title) > 120:
        flash("A tarefa deve ter no máximo 120 caracteres.", "error")
    else:
        try:
            if due_date:
                parsed_date = date.fromisoformat(due_date)
                if parsed_date < date(2000, 1, 1) or parsed_date > date(2100, 12, 31):
                    raise ValueError
        except ValueError:
            flash("Informe uma data válida para o prazo.", "error")
            return redirect(url_for("index"))
        with get_connection() as connection:
            connection.execute("INSERT INTO tasks (title, due_date) VALUES (?, ?)", (title, due_date))
        flash("Tarefa adicionada ao seu mapa!", "success")
    return redirect(url_for("index"))


@app.route("/toggle/<int:task_id>", methods=["POST"])
def toggle_task(task_id):
    """Alterna o status de uma tarefa entre pendente e concluída."""
    with get_connection() as connection:
        task = connection.execute("SELECT completed FROM tasks WHERE id = ?", (task_id,)).fetchone()
        if task is None:
            flash("Tarefa não encontrada.", "error")
        else:
            connection.execute("UPDATE tasks SET completed = ? WHERE id = ?", (0 if task["completed"] else 1, task_id))
    return redirect(url_for("index"))


@app.route("/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    """Exclui uma tarefa pelo identificador."""
    with get_connection() as connection:
        connection.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    flash("Tarefa removida do mapa.", "success")
    return redirect(url_for("index"))


initialize_database()

if __name__ == "__main__":
    app.run(debug=True)
