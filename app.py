from flask import Flask, render_template, request
import pandas as pd
import sqlite3

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/uploadfile", methods=['POST'])
def uploadfile():
    file = request.files['file']
    if file:
        if file.filename.endswith('.csv'):
            df = pd.read_csv(file)
        elif file.filename.endswith('.xlsx'):
            wb = load_workbook(file)
            sheet = wb.active
            df = pd.DataFrame(sheet.values)
        else:
            return render_template('error.html', message = "Unsupported file format")

        template = {}
        for c in df.columns:
            template[c]=type(df[c].iloc[0])
    return render_template('display_schema.html',template=template)

@app.route("/create_query", methods=['POST'])
def create_query():
    table_name = request.form['table_name']
    columns = request.form.getlist('column_names[]')
    datatypes = request.form.getlist('column_datatypes[]')

    query = f"CREATE TABLE {table_name} (\n"
    for column, datatype in zip(columns, datatypes):
        query += f"    \"{column}\" \"{datatype}\",\n"
    query = query.rstrip(',\n') + "\n);"

    try:
        connection = sqlite3.connect('temp.db')
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        connection.close()
    except Exception as e:
        return render_template('error.html', message = "Please update the file with correct columns and datatypes."+str(e))
    return render_template('display_query.html',query=query)