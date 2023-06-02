import sqlite3

padding = "padding"
finish = "finish"
failed = "failed"


# init sqlite db
def sqliteInit():
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
def createEvaluation(values):
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


def createPaddingEvaluation(values):
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
def getEvaluationById(id):
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


# update an evaluation record by ID
# id = 1
# values = {'name': 'Jane Doe', 'prompt': 'Write a program to calculate the product of two numbers', 'evaluation': 'The program works correctly and is very efficient', 'status': 'completed'}
# updateEvaluationById(id, values)
def updateEvaluationById(id, values):
    conn = sqlite3.connect("db/prompt.db")
    c = conn.cursor()
    c.execute(
        "UPDATE evaluation SET name = ?, prompt = ?, evaluation = ?, status = ? WHERE id = ?",
        (values["name"], values["prompt"], values["evaluation"], values["status"], id),
    )
    conn.commit()
    conn.close()


def finishEvaluationById(id, values):
    conn = sqlite3.connect("db/prompt.db")
    c = conn.cursor()
    c.execute(
        "UPDATE evaluation SET evaluation = ?, status = ? WHERE id = ?",
        (values["evaluation"], finish, id),
    )
    conn.commit()
    conn.close()


def failedEvaluationById(id, values):
    conn = sqlite3.connect("db/prompt.db")
    c = conn.cursor()
    c.execute(
        "UPDATE evaluation SET evaluation = ?, status = ? WHERE id = ?",
        (values["evaluation"], failed, id),
    )
    conn.commit()
    conn.close()


# delete an evaluation record by ID
def deleteEvaluationById(id):
    conn = sqlite3.connect("db/prompt.db")
    c = conn.cursor()
    c.execute("DELETE FROM evaluation WHERE id = ?", (id,))
    conn.commit()
    conn.close()


# retrieve all evaluation records and order by timestamp in descending order
def getAllEvaluations():
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


def create_stage(eid: int, stage: str, input: str, output: str, status: str):
    """
    Create a new stage record in the database.
    """
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


# get specify stage by eid and id
def getStageById(eid, id):
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


def get_stage(eid):
    """
    Read a stage record from the database by ID.
    """
    conn = sqlite3.connect("db/prompt.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM stage WHERE eid = ? order by timestamp DESC", (eid,))
    return cursor.fetchone()


def update_stage(id, eid, stage, input, output, status):
    """
    Update a stage record in the database by ID.
    """
    conn = sqlite3.connect("db/prompt.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE stage
        SET eid = ?, stage = ?, input = ?, output = ?, status = ?
        WHERE id = ?
    """,
        (eid, stage, input, output, status, id),
    )
    conn.commit()


def update_stage_status(eid, stage, status,output=""):
    """
    Update a stage record in the database by ID.
    """
    conn = sqlite3.connect("db/prompt.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE stage
        SET status = ?, output=?
        WHERE eid = ? and stage = ?
    """,
        (status,output, eid, stage),
    )
    conn.commit()


def delete_stage(id):
    """
    Delete a stage record from the database by ID.
    """
    conn = sqlite3.connect("db/prompt.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM stage WHERE id = ?", (id,))
    conn.commit()
