from stores.sqlite import getAllEvaluations, get_stage, getEvaluationById, getStageById
from const_var import (
    StageStatusFailed,
    StageStatusPadding,
    StageStatusDone,
    StandPadding,
    StandDone,
    StandFailed,
)
import json
from const_var import (
    StageInit,
    StageSimilarity,
    StageStyle,
    StageFluency,
    StageUnderstand,
    StageDivergence,
    StageStatusPadding,
    StageStatusDone,
    StageStatusFailed,
)
from dataBus.db import SqlDB
from bson.objectid import ObjectId

def outputWithHtml():
    """
    Read all records from prompt.db evaluation table and output to html format.
    """

    allRecords = SqlDB().getAllEvaluations()
    # Create the HTML table
    htmlTable = """
    <div class="row">
    """
    for record in allRecords:
        # print(record["id"], record["status"])
        if record["status"] == "finish":
            htmlTable += f"""
            <div class="col-1">{record['id']}</div>
            <div class="col-1" >{record['name']}</div>
            <div class="col-5" style="word-break: break-all;">{record['evaluation']}</div>
            <div class="col-1"><button class='btn btn-primary' onclick="window.location.href='/v1/spider/{record['id']}'">GRAPH</button></div>
            <div class="col-3" style="word-break: break-all;">{record['prompt']}</div>
            """
        else:
            htmlTable += f"""
            <div class="col-1">{record['id']}</div>
            <div class="col-2">{record['name']}</div>
            <div class="col-1"><button class='btn btn-primary' onclick="window.location.href='/v1/query_stage/{record['id']}'">{record['status']}</button></div>
            <div class="col-4" style="word-break: break-all;">{record['evaluation']}</div>
            <div class="col-4" style="word-break: break-all;">{record['prompt']}</div>
            """
    htmlTable += """
    </div>
    """

    return htmlTable


def outputStageWithHtml(id: int):
    """
    Read all records from prompt.db stage table and output to html format.
    """
    stage = SqlDB().get_stage(id)
    htmlTable = f"""
    <div class="row">
    <div id="liveAlertPlaceholder"></div>
    """

    # check if the stage is empty
    if stage is None:
        htmlTable += "No stage record found."
        htmlTable += """</div>"""
        return htmlTable
    htmlTable += """
        <div class="col-1" style="word-break: break-all;">ID</div>
        <div class="col-1" style="word-break: break-all;">EID</div>
        <div class="col-1" style="word-break: break-all;">STAGE</div>
        <div class="col-5" style="word-break: break-all;">INPUT</div>
        <div class="col-1" style="word-break: break-all;">OUTPUT</div>
        <div class="col-2" style="word-break: break-all;">STATUS</div>
        <div class="col-1" style="word-break: break-all;">TIMESTAMP</div>
    """

    htmlTable += f"""
        <hr/>
        <div class="col-1" style="word-break: break-all;">{stage[0]}</div>
        <div class="col-1" style="word-break: break-all;">{stage[1]}</div>
        <div class="col-1" style="word-break: break-all;">{stage[2]}</div>
        <div class="col-3" style="word-break: break-all;">{stage[3]
        .encode("utf-8")
        .decode("unicode_escape")
        .encode("utf-8")
        .decode("unicode_escape")}</div>
        <div class="col-3" style="word-break: break-all;">{stage[4]
        .encode("utf-8")
        .decode("unicode_escape")
        .encode("utf-8")
        .decode("unicode_escape")}</div>
        """
    if stage[5] == StageStatusFailed:
        htmlTable += f"""
        <div class="col-2">
            <form method="POST" action="/v1/stage_restart/{id}/{stage[0]}">
                <input type="hidden" name="stage_id" value="{stage[0]}">
                <button type="submit" class='btn btn-primary'>Restart</button>
            </form>
        </div>
        """
    else:
        htmlTable += f"""
        <div class="col-2" style="word-break: break-all;">{status(stage[5])}</div>
        """

    htmlTable += f"""
        <div class="col-1" style="word-break: break-all;">{stage[6]}</div>
        <hr/>
        """
    htmlTable += """</div>"""

    return htmlTable


def status(origin: str) -> str:
    """
    Get the stand name for origin status.
    """

    if origin == StageStatusPadding:
        return StandPadding
    if origin == StageStatusFailed:
        return StandFailed
    if origin == StageStatusDone:
        return StandDone


def spiderWithHtml(id: int) -> str:
    eva = SqlDB().getEvaluationById(id)
    if eva is None:
        return """
        let data = [
            {
                "sm":0.0,
                "st":0.0,
                "fl-c":0.0,
                "fl-g":0.0,
                "fl-e":0.0,
                "fl-l":0.0,
                "di":0.0,
                "un":0.0      
            }
        ];
        """
    result = json.loads(eva["evaluation"])

    fs = json.loads(result["fluency_score"])

    return f"""
        let data = [
            {{
                "sm":{result['similarity_score']},
                "st":{result['style_score']},
                "fl-c":{fs['content']},
                "fl-g":{fs['grammar']},
                "fl-e":{fs['error']},
                "fl-l":{fs['logic']},
                "di":{result['divergence_score']},
                "un":{result['understand_score']}   
            }}
        ];
        """


# q: how to return multiple value
# a: return a tuple
def processLineWithHtml():
    """
    Read all records from prompt.db evaluation table and output to html format.
    """
    
    allRecords = SqlDB().getAllEvaluations()
    # Create the HTML table

    svg = ""
    dataSource = ""
    dataList = ""

    for idx, record in enumerate(allRecords):
        # if record.status == 'finish' then add a button(named result) for user to click
        # when user click this button, it will redirect to a new page(/v1/spider/{record['id']})
        # If id in record, then get record['id']
        # If _id in record, then get record['_id']
        id = ""
        if "id" in record:
            id = record["id"]
        else:
            # id is ObjectId type, so need conver it to str
            id = str(record["_id"])

        svg += f"""
        <div style="padding-left: 100px;">
            <div class="row">
                <div class="col-2">
                    <button class='btn btn-outline-primary btn-sm' onclick="window.location.href='/v1/query_stage/{id}'">{record['name']}</button>
                </div>
                <div class="col-2">
                    <p class="fw-lighter">{record['timestamp']}</p> 
                </div>
                
        """

        if record["status"] == "finish":
            svg += f"""
                <div class="col-2">
                    <div style="padding-left: 100px;"><button class='btn btn-outline-success btn-sm' onclick="window.location.href='/v1/spider/{record['id']}'">Result</button></div>
                </div>
            """
        svg += f"""
            </div>
        </div>
        """
        svg += f"""
        <svg width="600" height="120" style="padding-top: 20px;padding-left: 100px;"></svg>
        """

        dataSource += f"""
        var data{idx}=[
            {getStageStatus(record)}
        ]
        """
        dataList += f"""data{idx},"""

    # remove last comma
    dataList = dataList[:-1]
    dataSource += f"""var dataSource = [init, {dataList}]"""

    return svg, dataSource


def getStageStatus(record):
    
    if "id" in record:
        id = record["id"]
    if "_id" in record:
        id = str(record["_id"])    
    stage = SqlDB().get_stage(id)
    print(f"{stage}  {id}")
    return f"""{stageStatus(stage=stage[2], status=stage[5])}"""


def stageStatus(stage: str, status: str) -> str:
    """
    There has six status for stage:
        StageInit: The stage is init.
        StageSimilarity: The stage is similarity.
        StageStyle: The stage is style.
        StageFluency: The stage is fluency.
        StageUnderstand: The stage is understand.
        StageDivergence: The stage is divergence.
    If status is StageInit, then return all six status, and these completed is false.
    If status is StageSimilarity, then return:
        StageInit, and completed: status_done. Residue five status with completed is false.
    If status is StageStyle, then return:
        StageInit, and completed: status_done. StageSimilarity, and completed: status_done. Residue four status with completed is false.
    And so on.
    """

    if stage == StageInit:
        return f"""
        {{ step: "{StageInit}", completed: '{status}' }},
        {{ step: "{StageSimilarity}", completed: 'status_watting' }},
        {{ step: "{StageStyle}", completed: 'status_watting' }},
        {{ step: "{StageFluency}", completed: 'status_watting' }},
        {{ step: "{StageUnderstand}", completed: 'status_watting' }},
        {{ step: "{StageDivergence}", completed: 'status_watting' }},
        """
    if stage == StageSimilarity:
        return f"""
        {{ step: "{StageInit}", completed: 'status_done' }},
        {{ step: "{StageSimilarity}", completed: '{status}' }},
        {{ step: "{StageStyle}", completed: 'status_watting' }},
        {{ step: "{StageFluency}", completed: 'status_watting' }},
        {{ step: "{StageUnderstand}", completed: 'status_watting' }},
        {{ step: "{StageDivergence}", completed: 'status_watting' }},
        """
    if stage == StageStyle:
        return f"""
        {{ step: "{StageInit}", completed: 'status_done' }},
        {{ step: "{StageSimilarity}", completed: 'status_done' }},
        {{ step: "{StageStyle}", completed: '{status}' }},
        {{ step: "{StageFluency}", completed: 'status_watting' }},
        {{ step: "{StageUnderstand}", completed: 'status_watting' }},
        {{ step: "{StageDivergence}", completed: 'status_watting' }},
        """
    if stage == StageFluency:
        return f"""
        {{ step: "{StageInit}", completed: 'status_done' }},
        {{ step: "{StageSimilarity}", completed: 'status_done' }},
        {{ step: "{StageStyle}", completed: 'status_done' }},
        {{ step: "{StageFluency}", completed: '{status}' }},
        {{ step: "{StageUnderstand}", completed: 'status_watting' }},
        {{ step: "{StageDivergence}", completed: 'status_watting' }},
        """
    if stage == StageUnderstand:
        return f"""
        {{ step: "{StageInit}", completed: 'status_done' }},
        {{ step: "{StageSimilarity}", completed: 'status_done' }},
        {{ step: "{StageStyle}", completed: 'status_done' }},
        {{ step: "{StageFluency}", completed: 'status_done' }},
        {{ step: "{StageUnderstand}", completed: '{status}' }},
        {{ step: "{StageDivergence}", completed: 'status_watting' }},
        """
    if stage == StageDivergence:
        return f"""
        {{ step: "{StageInit}", completed: 'status_done' }},
        {{ step: "{StageSimilarity}", completed: 'status_done' }},
        {{  step: "{StageStyle}", completed: 'status_done' }},
        {{ step: "{StageFluency}", completed: 'status_done' }},
        {{ step: "{StageUnderstand}", completed: 'status_done' }},
        {{ step: "{StageDivergence}", completed: '{status}' }},
        """
