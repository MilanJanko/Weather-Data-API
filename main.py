from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

stations = pd.read_csv('data_small/stations.txt', skiprows=17)
stations = stations[['STAID',
                     'STANAME                                 ']]


@app.route("/")
def home():
    return render_template("home.html", table=stations.to_html())


@app.route("/apis/v1/<station>/<date>")
def about(station, date):
    filename = f"data_small/TG_STAID{str(station).zfill(6)}.txt"
    df = pd.read_csv(filename, parse_dates=['    DATE'], skiprows=20)
    temperature = df.loc[df['    DATE'] == date, '   TG'].squeeze()/10
    return {"station": station,
            "date": date,
            "temperature": temperature}


@app.route("/apis/v1/<station>/")
def all_dates(station):
    filename = f"data_small/TG_STAID{str(station).zfill(6)}.txt"
    df = pd.read_csv(filename, parse_dates=['    DATE'], skiprows=20)
    result = df.to_dict(orient='records')
    return result


@app.route("/apis/v1/annually/<station>/<year>")
def annually(station, year):
    filename = f"data_small/TG_STAID{str(station).zfill(6)}.txt"
    df = pd.read_csv(filename, skiprows=20)
    df['    DATE'] = df['    DATE'].astype(str)
    result = df[df['    DATE'].str.startswith(year)].to_dict(orient='records')
    return result


if __name__ == "__main__":
    app.run(debug=True, port=5000)
