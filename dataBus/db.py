from models.sql import SqlBaseModel

sqlDB:SqlBaseModel = None

def setSqlDB(db:SqlBaseModel):
    global sqlDB
    sqlDB = db
    return

def SqlDB()->SqlBaseModel:
    global sqlDB
    return sqlDB