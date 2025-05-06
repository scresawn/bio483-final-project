from flask import Flask
import duckdb
DB_PATH="Actino_Draft.duckdb"

app = Flask(__name__)

@app.route('/')
def hello_world():
    x = 'Hello'
    y = 'World'
    return f'<h1>Hello, World!</h1><table><tr><td>{x}</td><td>{y}</td></tr></table>'

@app.route('/phages')
def phages():
    # this is where we need to query DuckDB for the phages data...
    con = duckdb.connect(DB_PATH)
    rows = con.sql("SELECT ANY_VALUE(Cluster), phage.Name, ANY_VALUE(Status), COUNT(*) AS geneCount FROM phage JOIN gene ON phage.PhageID = gene.PhageID GROUP BY phage.Name ORDER BY ANY_VALUE(Cluster) ASC").fetchall()

    html_table = f'<table>'
    html_table += f'<tr><td>Cluster</td><td>Phage Name</td><td>Annotation Status</td><td>Number of Genes</td></tr>'
    
    for row in rows:
        html_table += f'<tr>'
        html_table += f'<td>{row[0]}</td>'
        html_table += f'<td>{row[1]}</td>'
        html_table += f'<td>{row[2]}</td>'
        html_table += f'<td>{row[3]}</td>'
        html_table += f'</tr>'
    
    html_table += f'</table>'

    return html_table

if __name__ == '__main__':

    app.run(debug=True)