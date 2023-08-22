from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/uploadfile", methods=['GET', 'POST'])
def uploadfile():
    file = request.files['file']
    table_name = request.form['table_name']

    if file:
        if file.filename.endswith('.csv'):
            df = pd.read_csv(file)
        elif file.filename.endswith('.xlsx'):
            wb = load_workbook(file)
            sheet = wb.active
            df = pd.DataFrame(sheet.values)
        else:
            return render_template('error.html', message = "Unsupported file format")

        template = [{'name': col, 'datatype': str(df[col].dtype)} for col in df.columns]
        # for c in df.columns:
        #     template[c]=type(df[c].iloc[0])
        print(template)
    return render_template('display_schema.html',columns=template)

@app.route("/idk")
def idk():
    return render_template('index.html')