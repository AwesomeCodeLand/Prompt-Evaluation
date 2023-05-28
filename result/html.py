from stores.sqlite import getAllEvaluations

def outputWithHtml():
    """
    Read all records from prompt.db evaluation table and output to html format.
    """

    allRecords = getAllEvaluations()
    # Create the HTML table
    htmlTable = """
    <table class="table table-bordered table-hover align-middle">
        <thead>
            <tr>
                <th  class="w-10">#</th>
                <th  class="w-10">Name</th>
                <th  class="w-30">Response</th>
                <th  class="w-10">Operations</th>
                <th  class="w-40">Prompt</th>
            </tr>
        </thead>
        <tbody>
    """
    for record in allRecords:
        print(record['id'], record['status'])
        if record['status'] == 'finish':
            htmlTable += f"""
            <tr>
                <th class="w-10">{record['id']}</th>
                <td class="w-10">{record['name']}</td>
                <td class="w-30" style="overflow: hidden; text-overflow:ellipsis; white-space: nowrap;">{record['evaluation']}</td>
                <td class="w-10">
                    <button class='btn btn-primary'>get result</button>
                </td>
                <td class="w-40" style="overflow: hidden; text-overflow:ellipsis; white-space: nowrap;">{record['prompt']}</td>
                
            </tr>
            """
        else:
            htmlTable += f"""
            <tr>
                <th class="w-10">{record['id']}</th>
                <td class="w-10">{record['name']}</td>
                <td class="w-30" style="overflow: hidden; text-overflow:ellipsis; white-space: nowrap;">{record['evaluation']}</td>
                <td class="w-10">{record['status']}</td>
                <td class="w-40" style="overflow: hidden; text-overflow:ellipsis; white-space: nowrap;">{record['prompt']}</td>
                
            </tr>
            """
    htmlTable += """
        </tbody>
    </table>
    """
    
    return htmlTable
