import datetime
import time
from models.sql import SqlBaseModel
from pymongo import MongoClient
from const_var import padding, finish, failed
from bson.objectid import ObjectId
from log import output_log


class MongoModel(SqlBaseModel):
    evaluation = "evaluation"
    evaluationTable = None

    stage = "stage"
    stageTable = None

    def __init__(self, conf):
        client = MongoClient(conf.mongo.connect)
        if client.server_info():
            print("MongoDB client connected to server")
        else:
            print("MongoDB client failed to connect to server")
            return None
        db = client[conf.mongo.db]
        self.evaluationTable = db[self.evaluation]
        self.stageTable = db[self.stage]

        print("mongo init success")
        return None

    def createEvaluation(self, values):
        # Check whether timestamp is in values
        # If not, add timestamp to values
        if "timestamp" not in values:
            values["timestamp"] = int(time.time())
        if "status" not in values:
            values["status"] = padding
        print(f"values:{values}")

        return str(self.evaluationTable.insert_one(values).inserted_id)

    def createPaddingEvaluation(self, values):
        values["status"] = padding
        if "timestamp" not in values:
            values["timestamp"] = int(time.time())

        self.evaluationTable.insert_one(values)
        return None

    def getEvaluationById(self, id):
        return self.evaluationTable.find_one({"_id": ObjectId(id)})

    def updateEvaluationById(self, id, values):
        return self.evaluationTable.update_one({"_id": ObjectId(id)}, {"$set": values})

    def finishEvaluationById(self, id, values):
        return self.evaluationTable.update_one(
            {"_id": ObjectId(id)},
            {"$set": {"status": finish, "evaluation": values["evaluation"]}},
        )

    def failedEvaluationById(self, id, values):
        return self.evaluationTable.update_one(
            {"_id": ObjectId(id)},
            {"$set": {"status": failed, "evaluation": values["evaluation"]}},
        )

    def deleteEvaluationById(self, id):
        return self.evaluationTable.delete_one({"_id": ObjectId(id)})

    def paddingEvaluationById(self, id):
        return self.evaluationTable.update_one(
            {"_id": ObjectId(id)}, {"$set": {"status": padding}}
        )

    def getAllEvaluations(self):
        return self.evaluationTable.find()

    def create_stage(self, eid: str, stage: str, input: str, output: str, status: str):
        result = self.stageTable.insert_one(
            {
                "eid": eid,
                "stage": stage,
                "input": input,
                "output": output,
                "status": status,
                "timestamp": int(time.time()),
            }
        )

        output_log(f"create_stage result:{result}", level="info")
        return

    def getStageById(self, eid, id):
        return self.stageTable.find_one({"eid": eid, "_id": ObjectId(id)})

    def getStageByEid(self, eid):
        return self.stageTable.find({"eid": eid})

    def get_stage(self, eid):
        return (
            self.stageTable.find_one({"eid": eid}, sort=[("timestamp", -1)])
        )

    def update_stage(self, id, eid, stage, input, output, status):
        return self.stageTable.update_one(
            {"_id": ObjectId(id)},
            {
                "$set": {
                    "eid": eid,
                    "stage": stage,
                    "input": input,
                    "output": output,
                    "status": status,
                }
            },
        )

    def update_stage_status(self, eid, stage, status, output=""):
        return self.stageTable.update_one(
            {"eid": eid, "status": status},
            {"$set": {"status": status, "output": output, "timestamp": datetime.now()}},
        )

    def delete_stage(self, id):
        return self.stageTable.delete_one({"_id": ObjectId(id)})
