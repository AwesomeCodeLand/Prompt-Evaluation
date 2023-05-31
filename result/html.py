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
        <div class="col-5" style="word-break: break-all;">{stage[3]
        .encode("utf-8")
        .decode("unicode_escape")
        .encode("utf-8")
        .decode("unicode_escape")}</div>
        <div class="col-1" style="word-break: break-all;">{stage[4]
        .encode("utf-8")
        .decode("unicode_escape")
        .encode("utf-8")
        .decode("unicode_escape")}</div>
        <div class="col-2" style="word-break: break-all;">{stage[5]}</div>
        <div class="col-1" style="word-break: break-all;">{stage[6]}</div>
        <hr/>
        """

    htmlTable += """</div>"""

    return htmlTable
