from models.configure import Conf


class SqlBaseModel:
    def __init__(self, conf: Conf) -> None:
        pass

    def createEvaluation(self, values):
        pass

    def createPaddingEvaluation(self, values):
        pass

    def getEvaluationById(self, id):
        pass

    def updateEvaluationById(self, id, values):
        pass

    def finishEvaluationById(self, id, values):
        pass

    def failedEvaluationById(self, id, values):
        pass

    def deleteEvaluationById(self, id):
        pass

    def paddingEvaluationById(self, id):
        pass

    def getAllEvaluations(self):
        pass

    def create_stage(self, eid: int, stage: str, input: str, output: str, status: str):
        pass

    def getStageById(sefl, eid, id):
        pass

    def get_stage(self, eid):
        pass

    def update_stage(self, id, eid, stage, input, output, status):
        pass

    def update_stage_status(self, eid, stage, status, output=" "):
        pass

    def delete_stage(self, id):
        pass
