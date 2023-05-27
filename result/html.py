from stores.sqlite import getAllEvaluations

def outputWithHtml():
    """
    Read all records from prompt.db evaluation table and output to html format.
    """

    allRecords = getAllEvaluations()
        # Create the HTML table
    htmlTable = "<table>\n<tr><th>ID</th><th>Prompt</th><th>Response</th><th>Score</th><th>Operations</th></tr>\n"
    for record in allRecords:
        if record[4] == 'finish':
            htmlTable += f"<tr><td>{record[0]}</td><td>{record[1]}</td><td>{record[2]}</td><td>{record[3]}</td><td><button>get result</button></td></tr>\n"
        else:
            htmlTable += f"<tr><td>{record[0]}</td><td>{record[1]}</td><td>{record[2]}</td><td>{record[3]}</td><td></td></tr>\n"
    htmlTable += "</table>"
    
    # Print the HTML table
    # print(htmlTable)
    
    # Return the HTML table
    return htmlTable
