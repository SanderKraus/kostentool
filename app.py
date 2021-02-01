from flask import (Flask, request, render_template)
from werkzeug.utils import secure_filename
import pandas as pd

from data import SanderDataModel

app = Flask(__name__)
app.secret_key = 'secret'

data = None  # not thread-safe


@app.route('/', methods=['GET', 'POST'])
def index():
    global data
    if request.method == 'POST':
        file = request.files["file"]
        if file:
            df_tec = pd.read_excel(file, sheet_name='tec')
            df_1 = pd.read_excel(file, sheet_name='item1')
            df_2 = pd.read_excel(file, sheet_name='item2')
            data = SanderDataModel(df_tec, df_1, df_2)
            data.crunch_all_df()
            return render_template('set_tech.html', data=data)
    return render_template('index.html')
