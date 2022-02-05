import numpy as np
import pandas as pd
from flask import Flask, request, render_template, abort, jsonify, make_response
from flask_cors import CORS


app = Flask(__name__)

# cors = CORS(app, resources={r"/*": {"origins": "*"}})

import mimetypes
mimetypes.add_type('text/javascript', '.js')

features = ['sewer_and_water','power','roads_and_bridges','medical','buildings','shake_intensity']


df = pd.read_csv("data/mc1-reports-data.csv")
df['time'] = pd.to_datetime(df['time'])

@app.route("/")
def my_index():
    return render_template("index.html")


@app.route("/feature_mean", methods=['POST'])
def getFeatureDmg():
    # req_data = request.json
    print(request.json)
    f1 = df['time'] >= request.json.get('start_time')
    f2 = df['time'] <= request.json.get('end_time')
    feature = request.json.get('feature')
    filtered_df = df[f1 & f2][[feature, "location"]]
    df_g = filtered_df.groupby("location")
    avg = df_g.mean().to_dict()[feature]
    res = make_response(jsonify(avg), 200)
    return res

@app.route("/getMinMaxTime", methods=['GET'])
def getMinMaxTime():
    result = {
        "minTime": str(min(df['time'])),
        "maxTime": str(max(df['time'])),
    }
    res = make_response(jsonify(result), 200)
    return res

@app.route("/correlation", methods=['POST'])
def getCorrelation():
    print(request.json)
    f1 = df['time'] >= request.json.get('start_time')
    f2 = df['time'] <= request.json.get('end_time')
    f3 = df['location'] == request.json.get('location')
    filtered_df = df[f1 & f2 & f3]

    result = {}

    for feat1 in features:
        if not filtered_df[feat1].isnull().values.all():
            filtered_df[feat1].fillna(filtered_df[feat1].mean())

    for feat1 in features:
        if feat1 not in result:
            result[feat1] = {}
        for feat2 in features:
            if filtered_df[feat1].isnull().values.all() or filtered_df[feat2].isnull().values.all():
                result[feat1][feat2] = None
            else:
                result[feat1][feat2] = filtered_df[feat1].corr(filtered_df[feat2])
    res = make_response(jsonify(result), 200)
    return res

@app.route("/summary", methods=['POST'])
def getSummary():
    print(request.json)
    f1 = df['time'] >= request.json.get('start_time')
    f2 = df['time'] <= request.json.get('end_time')
    f3 = df['location'] == request.json.get('location')
    filtered_df = df[f1 & f2 & f3]

    result = {}

    for feat1 in features:
        if not filtered_df[feat1].isnull().values.all():
            filtered_df[feat1].fillna(filtered_df[feat1].mean())

    for feat1 in features:
        if filtered_df[feat1].isnull().values.all():
              result[feat1] = {
                "key": feat1,
                "min": None,
                "max": None,
                "median": None,
                "q1": None,
                "q3": None,
                "color": "#FFFFFF",
            }
        else:
            result[feat1] = {
                "key": feat1,
                "min": float(filtered_df[feat1].min()),
                "max": float(filtered_df[feat1].max()),
                "median": float(filtered_df[feat1].quantile(0.5)),
                "q1": float(filtered_df[feat1].quantile(0.25)),
                "q3": float(filtered_df[feat1].quantile(0.75)),   
                "color": "#000000",         
            }
    res = make_response(jsonify(result), 200)
    return res

@app.route('/timeline_graph', methods=['POST'])
def getTimelineGraphData():
    print(request.json)
    f1 = df['time'] >= request.json.get('start_time')
    f2 = df['time'] <= request.json.get('end_time')
    f3 = df['location'] == request.json.get('location')
    filtered_df = df[f1 & f2 & f3]
    result = {}
    result["medical"] = getDescribeByTimeDF(filtered_df, "medical")
    result["medical_uncertainity"] = getUncertainity(filtered_df, "medical")
    result["power"] = getDescribeByTimeDF(filtered_df, "power")
    result["power_uncertainity"] = getUncertainity(filtered_df, "power")
    result["sewer_and_water"] = getDescribeByTimeDF(filtered_df, "sewer_and_water")
    result["sewer_and_water_uncertainity"] = getUncertainity(filtered_df, "sewer_and_water")
    result["buildings"] = getDescribeByTimeDF(filtered_df, "buildings")
    result["buildings_uncertainity"] = getUncertainity(filtered_df, "buildings")
    result["roads_and_bridges"] = getDescribeByTimeDF(filtered_df, "roads_and_bridges")
    result["roads_and_bridges_uncertainity"] = getUncertainity(filtered_df, "roads_and_bridges")
    result["shake_intensity"] = getDescribeByTimeDF(filtered_df, "shake_intensity")
    result["shake_intensity_uncertainity"] = getUncertainity(filtered_df, "shake_intensity")
    res = make_response(jsonify(result), 200)
    return res


def getDescribeByTimeDF(df, feature):
    df_feat = df[["time", feature]]
    df_g = df_feat.groupby("time")
    df_d = df_g.describe()
    df_d.columns = df_d.columns.get_level_values(1)
    df_d['count'] = df_d['count'].astype(int)
    df_d.reset_index(inplace=True)
    df_d.sort_values(by=['time'], inplace=True)
    df_d.rename(columns={'mean': 'avg'}, inplace=True)
    df_d.rename(columns={"time": "time_ts"}, inplace=True)
    df_d = df_d.fillna(np.nan).replace([np.nan], [None])
    df_d["time"] = df_d["time_ts"].apply(lambda x: x.strftime("%Y-%m-%d %H:%M:%S"))
    df_d.drop('time_ts', 1, inplace=True)
    return df_d.to_dict("records")

def getUncertainity(df, feature):
    feat_std = df[feature].std()
    feat_mean = df[feature].mean()
    row_count = df.shape[0]
    f1 = df[feature] <= (feat_mean + feat_std)
    f2 = df[feature] >= (feat_mean - feat_std)
    filtered = f1 & f2
    within_one = filtered.sum()
    if within_one/row_count >= 0.6826:
        return "certain"
    f1 = df[feature] <= (feat_mean + 2*feat_std)
    f2 = df[feature] >= (feat_mean - 2*feat_std)
    filtered = f1 & f2
    within_two = filtered.sum()
    if within_two/row_count >= 0.9544:
        return "semi-certain"
    return "uncertain"


@app.route('/damage/mean/allcategories/<string:time1>/<string:time2>/<string:location>', methods=['GET'])
def damage_for_all_categories_for_time_period_by_Location(time1, time2, location):

    damage = get_damage_by_location(time1, time2, location)
    return damage.to_json(orient='records')


def get_damage_by_location(t1, t2, location):
    mask = (df['time'] >= t1) & (df['time'] <= t2)
    temp = df.loc[mask]
    #["Shake Intensity","Sewer & Water","Power","Roads and Bridges","Medical","Buildings"];
    categories = ['shake_intensity', 'sewer_and_water', 'power', 'roads_and_bridges', 'medical', 'buildings']
    temp = temp[temp['location']==int(location)]
    location_timelyAverage = []
    for category in categories:
            temp_category=temp.dropna(subset=[category])
            location_timelyAverage.append([category ,temp_category[category].mean()])

    return pd.DataFrame(location_timelyAverage)


app.run()