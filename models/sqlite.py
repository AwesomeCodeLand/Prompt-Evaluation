import sqlite3
import datetime
from const_var import padding, finish, failed
from models.sql import SqlBaseModel


class SqliteModel(SqlBaseModel):
    def __init__(self, conf):
        conn = sqlite3.connect("db/prompt.db")

        c = conn.cursor()
        c.execute(
            """CREATE TABLE IF NOT EXISTS evaluation
            (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                name TEXT, 
                prompt TEXT,
                evaluation TEXT,
                status TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )"""
        )
        c.execute(
            """
        CREATE TABLE IF NOT EXISTS stage (
            id INTEGER PRIMARY KEY,
            eid INTEGER,
            stage TEXT,
            input TEXT,
            output TEXT,
            status TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """
        )
        conn.commit()
        conn.close()

    # create a new evaluation record
    # values = {'name': 'John Doe', 'prompt': 'Write a program to calculate the sum of two numbers', 'evaluation': 'The program works correctly, but could be more efficient', 'status': 'pending'}
    # createEvaluation(values)
    def createEvaluation(self, values):
        conn = sqlite3.connect("db/prompt.db")
        c = conn.cursor()
        c.execute(
            "INSERT INTO evaluation (name, prompt,evaluation,status) VALUES (?, ?, ?, ?)",
            (values["name"], values["prompt"], values["evaluation"], values["status"]),
        )
        conn.commit()
        id = c.lastrowid
        conn.close()
        return id

    def createPaddingEvaluation(self, values):
        conn = sqlite3.connect("db/prompt.db")
        c = conn.cursor()
        c.execute(
            "INSERT INTO evaluation (name, prompt,  status) VALUES (?, ?, ?)",
            (values["name"], values["prompt"], padding),
        )
        conn.commit()
        id = c.lastrowid
        conn.close()
        return id

    # retrieve an evaluation record by ID
    def getEvaluationById(self, id):
        conn = sqlite3.connect("db/prompt.db")
        c = conn.cursor()
        c.execute("SELECT * FROM evaluation WHERE id = ?", (id,))
        row = c.fetchone()
        conn.close()
        if row:
            return {
                "id": row[0],
                "name": row[1],
                "prompt": row[2],
                "evaluation": row[3],
                "status": row[4],
                "timestamp": row[5],
            }
        else:
            return None

    def updateEvaluationById(self, id, values):
        conn = sqlite3.connect("db/prompt.db")
        c = conn.cursor()
        c.execute(
            "UPDATE evaluation SET name = ?, prompt = ?, evaluation = ?, status = ?, timestamp=? WHERE id = ?",
            (
                values["name"],
                values["prompt"],
                values["evaluation"],
                values["status"],
                self.getNow(),
                id,
            ),
        )
        conn.commit()
        conn.close()

    def finishEvaluationById(self, id, values):
        conn = sqlite3.connect("db/prompt.db")
        c = conn.cursor()
        c.execute(
            "UPDATE evaluation SET evaluation = ?, status = ? WHERE id = ?",
            (values["evaluation"], finish, id),
        )
        conn.commit()
        conn.close()

    def failedEvaluationById(self, id, values):
        conn = sqlite3.connect("db/prompt.db")
        c = conn.cursor()
        c.execute(
            "UPDATE evaluation SET evaluation = ?, status = ? WHERE id = ?",
            (values["evaluation"], failed, id),
        )
        conn.commit()
        conn.close()

    def deleteEvaluationById(self, id):
        conn = sqlite3.connect("db/prompt.db")
        c = conn.cursor()
        c.execute("DELETE FROM evaluation WHERE id = ?", (id,))
        conn.commit()
        conn.close()

    def paddingEvaluationById(self, id):
        conn = sqlite3.connect("db/prompt.db")
        c = conn.cursor()
        c.execute(
            "UPDATE evaluation SET status = ? , evaluation='' WHERE id = ?",
            (padding, id),
        )
        conn.commit()
        conn.close()

    def getAllEvaluations(self):
        conn = sqlite3.connect("db/prompt.db")
        c = conn.cursor()
        c.execute("SELECT * FROM evaluation ORDER BY timestamp DESC")
        rows = c.fetchall()
        conn.close()
        evaluations = []
        for row in rows:
            evaluations.append(
                {
                    "id": row[0],
                    "name": row[1],
                    "prompt": row[2],
                    "evaluation": row[3],
                    "status": row[4],
                    "timestamp": row[5],
                }
            )
        return evaluations

    def create_stage(self, eid: int, stage: str, input: str, output: str, status: str):
        conn = sqlite3.connect("db/prompt.db")
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO stage (eid, stage, input, output, status)
            VALUES (?, ?, ?, ?, ?)
        """,
            (eid, stage, input, output, status),
        )
        conn.commit()
        return cursor.lastrowid

    def getStageById(self, eid, id):
        conn = sqlite3.connect("db/prompt.db")
        c = conn.cursor()
        c.execute("SELECT * FROM stage WHERE eid = ? AND id = ?", (eid, id))
        row = c.fetchone()
        conn.close()
        if row:
            return {
                "id": row[0],
                "eid": row[1],
                "stage": row[2],
                "input": row[3],
                "output": row[4],
                "status": row[5],
                "timestamp": row[6],
            }
        else:
            return None

    def get_stage(self, eid):
        conn = sqlite3.connect("db/prompt.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM stage WHERE eid = ? order by timestamp DESC", (eid,)
        )
        return cursor.fetchone()

    def update_stage(self, id, eid, stage, input, output, status):
        conn = sqlite3.connect("db/prompt.db")
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE stage
            SET eid = ?, stage = ?, input = ?, output = ?, status = ?, timestamp=?
            WHERE id = ?
        """,
            (eid, stage, input, output, status, self.getNow(), id),
        )
        conn.commit()

    def update_stage_status(self, eid, stage, status, output=" "):
        conn = sqlite3.connect("db/prompt.db")
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE stage
            SET status = ?, output=?, timestamp=?
            WHERE eid = ? and stage = ?
        """,
            (status, output, self.getNow(), eid, stage),
        )
        conn.commit()

    def delete_stage(self, id):
        conn = sqlite3.connect("db/prompt.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM stage WHERE id = ?", (id,))
        conn.commit()

    def getNow(self):
        now = datetime.datetime.now()
        return now.strftime("%Y-%m-%d %H:%M:%S")
