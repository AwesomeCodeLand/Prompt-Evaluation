from stores.sqlite import getAllEvaluations

def outputWithHtml():
    """
    Read all records from prompt.db evaluation table and output to html format.
    """

    allRecords = getAllEvaluations()
    # Create the HTML table
    htmlTable = "<table class='table table-striped'>\n<thead><tr><th>ID</th><th>Name</th><th style='max-width: 50%'>Prompt</th><th style='max-width: 20%'>Response</th><th>Operations</th></tr></thead>\n<tbody>"
    for record in allRecords:
        print(record['id'], record['status'])
        if record['status'] == 'finish':
            htmlTable += f"<tr><td>{record['id']}</td><td>{record['name']}</td><td style='max-width: 50%'>{record['prompt']}</td><td style='max-width: 20%'>{record['evaluation']}</td><td><button class='btn btn-primary'>get result</button></td></tr>\n"
        else:
            htmlTable += f"<tr><td>{record['id']}</td><td>{record['name']}</td><td style='max-width: 50%'>{record['prompt']}</td><td style='max-width: 20%'>{record['evaluation']}</td><td>{record['status']}</td></tr>\n"
    htmlTable += "</tbody></table>"
    
    return htmlTable
