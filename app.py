import process
from flask import Flask
from flask import request
import pandas as pd 
import numpy as np

app = Flask(__name__)

data = pd.read_csv('rainfall.csv')

@app.route('/')
def rain():
    re = request.args.get('stationReference')

    data1 = data[~data['value'].isin(['0.0|0.2'])]
    subset1 = data1[data1['stationReference'] == re]
    df = subset1[['dateTime','value']]
    df2 = df.sort_values('dateTime')
    return df2.to_html(index = False)

if __name__ == '__main__':
    app.run(debug = True)