from stores.sqlite import getAllEvaluations

def outputWithHtml():
    """
    Read all records from prompt.db evaluation table and output to html format.
    """

    allRecords = getAllEvaluations()
        # Create the HTML table
    htmlTable = "<table>\n<tr><th>ID</th><th>Name</th><th>Prompt</th><th>Response</th><th>Operations</th></tr>\n"
    for record in allRecords:
        # print(record)
        if record['status'] == 'finish':
            htmlTable += f"<tr><td>{record['id']}</td><td>{record['name']}</td><td>{record['prompt']}</td><td>{record['evaluation']}</td><td><button>get result</button></td></tr>\n"
        else:
            htmlTable += f"<tr><td>{record['id']}</td><td>{record['name']}</td><td>{record['prompt']}</td><td>{record['evaluation']}</td><td>{record['status']}</td></tr>\n"
    htmlTable += "</table>"
    
    # Print the HTML table
    # print(htmlTable)
    
    # Return the HTML table
    return htmlTable
