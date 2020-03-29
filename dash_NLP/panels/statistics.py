# -*- coding: utf-8 -*-
import pandas as pd
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
from plotly import graph_objs as go
from datetime import datetime as dt
from app import app, indicator, df_to_table
import dash_table#看看是什么东西
import numpy as np
import copy
import sqlite3


#########################################################################################3
#曲线选项
curveOption = [{"label": "Dining People", "value": "diningPeople"},
                {"label": "Positive Review Rate", "value": "reviewRate"},
                {"label": "Positive & Negtive Reviews", "value": "review"}]


#divide origin df to show in aspect dropdown
def divideAspect(df):
    """
    input aspectDataFrame

    c.execute('''CREATE TABLE if not EXISTS ASPECT
       (ID INT PRIMARY KEY NOT NULL,
       REVIEW_ID           INT,
       ASPECT        CHAR(50),
       SENTIMENT         INT);''')


    return good &Aspect Dataframe include(aspect name ,number)
    """
    #divide df to good and bad part
    df_b  = df[df["SENTIMENT"]<0]
    df_g  = df[df["SENTIMENT"]>0]
    #find count of each type
    df_good = df_g["ASPECT"].value_counts().to_frame()
    df_bad = df_b["ASPECT"].value_counts().to_frame()
    #structure dataframe
    df_good["Aspect"] = df_good.index
    df_good.columns = ["count","Aspect"]

    df_bad["Aspect"] = df_bad.index
    df_bad.columns = ["count","Aspect"]

    #reset index or it will be error
    df_good = df_good.reset_index(drop=True)
    df_bad = df_bad.reset_index(drop=True)
    return df_good,df_bad



#
#再来一个可以让他自动更新的callback，可以根据时间数据更新内容 首先当然是传入上方函数的数据应该是更新过的
#"aspect_good","date-picker-select"
#这里可以有多个output 因为只有这个更改其他才更改 但是太乱了所以单独再列函数
#为了保证每次都能更新，数据库应该在回调函数里读取
@app.callback(
    [
        Output("aspect_good", "options"),
        Output("aspect_bad", "options"),
        Output("aspect_good", "value"),
        Output("aspect_bad", "value"),
    ],
    [
        Input("date-picker-select", "start_date"),
        Input("date-picker-select", "end_date")
    ],
)
def lead_source_callback(startTime,endTime):
    """
    input date 
    output 1.option of dropdown
    """
    #should begin with SQL Maybe a function
    #cut df

    conn = sqlite3.connect('assets\DashTemp.db')
    c = conn.cursor()

    
    sql = f"select a.* from ASPECT as a, (select ID from REVIEW where TIME >= '{startTime}' and TIME <= '{endTime}') as b where a.REVIEW_ID = b.ID"
    df_Aspect = pd.read_sql(sql,conn)

    conn.commit()
    conn.close()

    # df_Aspect = aspectDataFrame.copy()
    # df_Aspect= df_Aspect[pd.to_datetime(df_Aspect["date"])>=startTime]
    # df_Aspect= df_Aspect[pd.to_datetime(df_Aspect["date"])<=endTime]
    #get aspect dataframe
    df_goodAspect,df_badAspect = divideAspect(df_Aspect)
    # comblne option  + " " +       str(df_goodAspect.iloc[aspectIndex]["count"])
    # + " " +          str(df_badAspect.iloc[aspectIndex]["count"])
    aspectGoodOption = [
            {"label": str(df_goodAspect.iloc[aspectIndex]["Aspect"])  + " " + 
            str(df_goodAspect.iloc[aspectIndex]["count"]), 
            "value": str(
                df_goodAspect.iloc[aspectIndex]["Aspect"])}
            for aspectIndex in df_goodAspect.index
    ]

    aspectBadOption = [
            {"label": str(df_badAspect.iloc[aspectIndex]["Aspect"])  + " " + 
            str(df_badAspect.iloc[aspectIndex]["count"]), 
            "value": str(
                df_badAspect.iloc[aspectIndex]["Aspect"])}
            for aspectIndex in df_badAspect.index
    ]
    
    return aspectGoodOption,aspectBadOption,df_goodAspect["Aspect"],df_badAspect["Aspect"]


#call back for statistic data



@app.callback(
    [
        Output("peopleText_Cal", "children"),
        Output("rateText_Cal", "children"),
    ],
    [
        Input("date-picker-select", "start_date"),
        Input("date-picker-select", "end_date")
    ],
)
def indicator_callback(startTime,endTime):
    # load sql
    # listGraphBar_incb = listGraphBar.copy()
    # #get result
    # listGraphBar_incb = listGraphBar_incb[listGraphBar_incb['Time']>=startTime]
    # listGraphBar_incb = listGraphBar_incb[listGraphBar_incb['Time']<=endTime]

    conn = sqlite3.connect('assets\DashTemp.db')
    c = conn.cursor()
    sql = f"select * from DAY where TIME >= '{startTime}' and TIME <= '{endTime}'"
    listGraphBar_incb = pd.read_sql(sql,conn)
    conn.commit()
    conn.close()


    peopleText= sum(listGraphBar_incb["PEOPLE"])
    rateText= str(listGraphBar_incb["RATE"].mean())[:4] + "%"
    return peopleText,rateText


#figure
@app.callback(
    [
        Output("lead_source", "figure"),
    ],
    [
        Input("date-picker-select", "start_date"),
        Input("date-picker-select", "end_date"),
        Input("well_statuses","value"),
    ],
)
def figure_callback(startTime,endTime,select):
    # load sql

    conn = sqlite3.connect('assets\DashTemp.db')
    c = conn.cursor()
    sql = f"select * from DAY where TIME >= '{startTime}' and TIME <= '{endTime}'"
    listGraphBar_incb = pd.read_sql(sql,conn)
    conn.commit()
    conn.close()


    # listGraphBar_incb = listGraphBar.copy()
    # listGraphBar_incb = listGraphBar_incb[listGraphBar_incb['Time']>=startTime]
    # listGraphBar_incb = listGraphBar_incb[listGraphBar_incb['Time']<=endTime]
    #get result

    listGraphBar_incb.index = listGraphBar_incb['TIME']
    layout_count = dict(
        autosize=True,
        automargin=True,
        margin=dict(l=30, r=30, b=20, t=60),
        hovermode="closest",
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
        title="Satellite Overview",
    )
    if select == "diningPeople":
        data = [
            dict(
                    type="scatter",
                    mode="lines+markers",
                    x=listGraphBar_incb.index,
                    y=listGraphBar_incb["PEOPLE"],
                    line=dict(shape="spline", smoothing=2, width=1, color="#fac1b7"),
                    marker=dict(symbol="diamond-open"),
                ),
        ]
        layout_count["title"] = "Dining People"
    elif select == "reviewRate":
        data = [
            dict(
                    type="scatter",
                    mode="lines+markers",
                    y=listGraphBar_incb["RATE"],
                    x=listGraphBar_incb.index,
                    line=dict(shape="spline", smoothing=2, width=1, color="#fac1b7"),
                    marker=dict(symbol="diamond-open"),
                ),
            ]
        layout_count["title"] = "Positive Review Rate"
    elif select == "review":
        data = [
            dict(
                    type="scatter",
                    mode="lines+markers",
                    name = "Positive Reviews",
                    y=listGraphBar_incb["POS_REVIEW"],
                    x=listGraphBar_incb.index,
                    line=dict(shape="spline", smoothing=2, width=1, color="#fac1b7"),
                    marker=dict(symbol="diamond-open"),
                ),
            dict(
                    type="scatter",
                    mode="lines+markers",
                    name = "Negative Reviews",
                    y=listGraphBar_incb["NEG_REVIEW"],
                    x=listGraphBar_incb.index,
                    line=dict(shape="spline", smoothing=2, width=1, color="#a9bb95"),
                    marker=dict(symbol="diamond-open"),
                ),
        ]
        layout_count["title"] = "Positive & Negtive Reviews"

    layout_count["dragmode"] = False
    layout_count["showlegend"] = False
    layout_count["autosize"] = False

    figure = dict(data=data, layout=layout_count)
    return [figure]



"""
1.先处理时间选择的显示问题：主要是可不可以得到当天时间
2.建立函数，处理混在一起的aspect，组合重复的aspect并计数
3.统计数据 此数据应该从day表中提取， day表应该写道chatbot文件中
4.画图，四个图，各自建立函数
5.optional 合一起，不能让他每次都读一遍数据库，太花时间
"""

layout = [
    html.Div(
        id="lead_grid",
        children=[
            dcc.DatePickerRange(
                id="date-picker-select",
                start_date=dt(2020, 3, 1),
                end_date=dt.today(),
                min_date_allowed=dt(2019, 1, 1),
                max_date_allowed=dt.today(),
                initial_visible_month=dt.today(),
                style={'padding-left': 9}
            ),
            html.Div(
                className="row indicators",
                children=[
                    indicator("#119DFF", "People", "peopleText_Cal"),
                    indicator("#EF553B", "Mean rate of Positive Reviews", "rateText_Cal"),
                ],
            ),
            #这个位置放aspect统计
            html.Div(
                id="leads_per_state",
                className="chart_div pretty_container",
                children=[
                    html.P("Positive Aspect"),
                    dcc.Dropdown(  # 下拉框可能需要用在显示aspect的部分
                            # well_type_options 在这个选择里填写aspect list全部显示，且不允许删除
                            # 不允许删除似乎不可以用
                            id="aspect_good",
                            multi=True,
                            className="dcc_control",
                        ),
                    html.P("Negative Aspect"),
                    dcc.Dropdown( 
                            id="aspect_bad",
                            multi=True,
                            className="dcc_control",
                        ),
                ],
            ),
            #只需要下拉框 只显示line线（人数曲线， 上座率曲线， 评论好评率曲线， （正向评数，负向评数））
            #这里是全部统计数据图表 包括，好评率，客流量，好评数，差评数，
            #可以改成tab， 不过再说
            html.Div(
                id="leads_source_container",
                className="twelve columns chart_div pretty_container",
                children=[
                    html.P("Choose the curve:"),
                    dcc.Dropdown( 
                            id="well_statuses",
                            options=curveOption,
                            value="reviewRate",
                        ),
                    dcc.Graph(
                        id="lead_source",
                        style={"height": 300, "width": "98%",'padding-top': 10},
                        config=dict(displayModeBar=False),
                    ),
                ],
            ),
        ],
    ),
]

