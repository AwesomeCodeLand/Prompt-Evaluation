from stores.sqlite import getAllEvaluations, get_stage


def outputWithHtml():
    """
    Read all records from prompt.db evaluation table and output to html format.
    """

    allRecords = getAllEvaluations()
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
            <div class="col-1"><button class='btn btn-primary' onclick="window.location.href='/v1/query_stage/{record['id']}'">{record['status']}</button></div>
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
    stage = get_stage(id)
    htmlTable = """
    <div class="row">
    """

    # check if the stage is empty
    if stage is None or len(stage) == 0:
        htmlTable += "No stage record found."
        htmlTable += """</div>"""
        return htmlTable

    for s in stage:
        htmlTable += f"""
        <div class="col-1">{s['eid']}</div>
        <div class="col-1">{s['stage']}</div>
        <div class="col-4">{s['input']}</div>
        <div class="col-1">{s['output']}</div>
        <div class="col-2">{s['status']}</div>
        <div class="col-2">{s['timestamp']}</div>
        """
    htmlTable += """</div>"""
