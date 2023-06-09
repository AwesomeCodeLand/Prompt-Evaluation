import datetime
from pymongo import MongoClient
from const_var import  padding, finish, failed
from bson.objectid import ObjectId
from log import output_log

evaluation="evaluation"
evaluationTable = None

stage = "stage"
stageTable=None

def mongoInit(dsn:str, dbName:str):
    global evaluationTable
    global stageTable

    client = MongoClient(dsn)
    
    # Check if the client is working
    if client.server_info():
        output_log(f"MongoDB client connected to server", level="info")
    else:
        output_log(f"MongoDB client failed to connect to server", level="error")
        return None
    
    db = client[dbName]
    evaluationTable = db[evaluation]
    stageTable = db[stage]
    
    output_log(f"mongo init success", level="info")
    return None

def createEvaluation(values):
    evaluationTable.insert_one(values)
    return None

def createPaddingEvaluation(values):
    values["status"]=padding
    evaluationTable.insert_one(values)
    return None

def getEaluationById(id):
    return evaluationTable.find_one({"_id":ObjectId(id)})

def updateEvaluationById(id, values):
    evaluationTable.update_one({"_id":ObjectId(id)}, {"$set":values})
    return None

def finishEvaluationById(id, values):
    evaluationTable.update_one({"_id":ObjectId(id)}, {"$set":{"status":finish,"evaluation":values['evaluation']}})
    return None

def failedEvaluationById(id, values):
    evaluationTable.update_one({"_id":ObjectId(id)}, {"$set":{"status":failed,"evaluation":values['evaluation']}})
    return None

def deleteEvaluationById(id):
    evaluationTable.delete_one({"_id":ObjectId(id)})
    return None

def paddingEvaluationById(id):
    evaluationTable.update_one({"_id":ObjectId(id)}, {"$set":{"status":padding,"evaluation":''}})
    return None

def getAllEvaluation():
    return evaluationTable.find().sort("timestamp", -1)

def createStage(values):
    if "timestamp" not in values:
        values["timestamp"]=datetime.datetime.now()

    stageTable.insert_one(values)
    return None

def getStageById(id):
    return stageTable.find_one({"_id":ObjectId(id)})

def get_stage(eid):
    return stageTable.find({"eid":eid}).sort("timestamp", -1)

def update_stage(id, eid, stage, input, output, status):
    stageTable.update_one({"id":ObjectId(id)}, {"$set":{ "eid":eid,"stage":stage, "input":input, "output":output, "status":status}})
    return None

def update_stage_status(eid, stage, status, output=""):
    stageTable.update_one({"eid":eid, "status":status}, {"$set":{"status":status, "output":output,"timestamp":datetime.now()}})

def delete_stage(id):
    stageTable.delete_one({"_id":ObjectId(id)})
    return None

