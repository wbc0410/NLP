# -*- coding: utf-8 -*-
import pandas as pd
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
from plotly import graph_objs as go
from datetime import datetime as dt
import datetime
from app import app, indicator
import numpy as np
import sqlite3


colors = {"background": "#F3F6FA", "background_div": "white"}
tableNum = 10


# returns pie chart based on filters values
# column makes the function reusable

"""
1.最上面显示的是最近的三个订单
2.用热度图画表
    1.应该有六行（今天，明天中午，晚上，后天中午，晚上）
    2.设定有10张桌子
    3.有人为1
"""
#应该像table那样写个更新函数
def refresh():
    """
    c.execute('''CREATE TABLE if not EXISTS RESERVATION
       (ID INT PRIMARY KEY NOT NULL,
       NAME           TEXT,
       TABLES            INT,
       TIME        CHAR(50),
       PEOPLE         INT);''')
    """
    #SQL 
    conn = sqlite3.connect('assets\DashTemp.db')
    c = conn.cursor()
    sql = f"select * from RESERVATION where TIME > '{str(dt.today())}'"
    df_order = pd.read_sql(sql,conn)
    conn.commit()
    conn.close()
    # #find order after now
    # df_order = df_order[pd.to_datetime(df_order["TIME"])>dt.today()]
    #sort
    df_order = df_order.sort_values("TIME")
    #find recent order
    df_order = df_order[:3]
    
    html_order = []
    df_order = df_order.reset_index(drop=True)
    for index in df_order.index:
        ask_df = df_order.iloc[index]
        str_order = f'{ask_df["NAME"]}, {ask_df["PEOPLE"]} People, visit at {ask_df["TIME"]}, Table {ask_df["TABLES"]}'
        html_order.append(html.P(str_order))
    if html_order == []:
        html_order = html.P("No Order")
    return html_order

@app.callback(
    Output("heatmap_table", "figure"),
    [
        Input("dropdown_hidden", "value"),
    ],
)
def lead_source_callback(startTime):
    return generate_heatmap()


def index_combine(string_head,duration):
    """
    combine the index to show the heat table 
    """
    return string_head+" "+duration

#heat 代码
def generate_heatmap():
    """
    """
    #SQL 
    # df_order = orderDataFrame.copy()
    # #find order after now
    # df_order = df_order[pd.to_datetime(df_order["time"])>dt.today()]
    conn = sqlite3.connect('assets\DashTemp.db')
    c = conn.cursor()
    sql = f"select * from RESERVATION where TIME > '{str(dt.today())}'"
    df_order = pd.read_sql(sql,conn)
    conn.commit()
    conn.close()


    list_index = []
    #build index list
    if (dt.today().hour <=13):
        list_index.append(index_combine(str(dt.today())[5:10],"Lunch"))
        list_index.append(index_combine(str(dt.today())[5:10],"Dinner"))
        list_index.append(index_combine(str(dt.today()+datetime.timedelta(days=1))[5:10],"Lunch"))
        list_index.append(index_combine(str(dt.today()+datetime.timedelta(days=1))[5:10],"Dinner"))
        list_index.append(index_combine(str(dt.today()+datetime.timedelta(days=2))[5:10],"Lunch"))
        list_index.append(index_combine(str(dt.today()+datetime.timedelta(days=2))[5:10],"Dinner"))
    elif dt.today().hour > 13:
        list_index.append(index_combine(str(dt.today())[5:10],"Dinner"))
        list_index.append(index_combine(str(dt.today()+datetime.timedelta(days=1))[5:10],"Lunch"))
        list_index.append(index_combine(str(dt.today()+datetime.timedelta(days=1))[5:10],"Dinner"))
        list_index.append(index_combine(str(dt.today()+datetime.timedelta(days=2))[5:10],"Lunch"))
        list_index.append(index_combine(str(dt.today()+datetime.timedelta(days=2))[5:10],"Dinner"))
        list_index.append(index_combine(str(dt.today()+datetime.timedelta(days=3))[5:10],"Lunch"))
    
    #build data
    #需要新建表，以Columns作为x轴
    new_table = {}
    for table_num in range(1,tableNum+1):
        #从今天的日期向后查询
        new_table[table_num] = list(np.zeros(6))
    
    #建一个时间list 八个最好
    list_time = [dt(dt.today().year,dt.today().month,dt.today().day,0,0,0),
        dt(dt.today().year,dt.today().month,dt.today().day,13,0,0),
    dt((dt.today()+datetime.timedelta(days=1)).year,(dt.today()+datetime.timedelta(days=1)).month,(dt.today()+datetime.timedelta(days=1)).day,0,0,0),
    dt((dt.today()+datetime.timedelta(days=1)).year,(dt.today()+datetime.timedelta(days=1)).month,(dt.today()+datetime.timedelta(days=1)).day,13,0,0),
    dt((dt.today()+datetime.timedelta(days=2)).year,(dt.today()+datetime.timedelta(days=2)).month,(dt.today()+datetime.timedelta(days=2)).day,0,0,0),
    dt((dt.today()+datetime.timedelta(days=2)).year,(dt.today()+datetime.timedelta(days=2)).month,(dt.today()+datetime.timedelta(days=2)).day,13,0,0),
    dt((dt.today()+datetime.timedelta(days=3)).year,(dt.today()+datetime.timedelta(days=3)).month,(dt.today()+datetime.timedelta(days=3)).day,0,0,0),
    dt((dt.today()+datetime.timedelta(days=3)).year,(dt.today()+datetime.timedelta(days=3)).month,(dt.today()+datetime.timedelta(days=3)).day,13,0,0),
    ]

    for index in df_order.index:
        if dt.today().hour <=13:
            #用for循环判断是否在时间区间内
            for i in range(6):
                interval_list = pd.Interval(list_time[i],list_time[i+1], closed='left')
                if pd.to_datetime(df_order.iloc[index]["TIME"]) in interval_list:
                    new_table[df_order.iloc[index]["TABLES"]][i] = df_order.iloc[index]["PEOPLE"]
        elif dt.today().hour >13:
            #用for循环判断是否在时间区间内
            for i in range(6):
                interval_list = pd.Interval(list_time[i+1],list_time[i+2], closed='left')
                if pd.to_datetime(df_order.loc[index]["TIME"]) in interval_list:
                    new_table[df_order.loc[index]["TABLES"]][i] = df_order.iloc[index]["PEOPLE"]
    
    
    df_table = pd.DataFrame(new_table)
    df_table.index = list_index

    df_table
    x_axis = list(range(1,11))  # 24hr time list
    y_axis = list_index

    # Heatmap
    list_z = np.array(df_table)

    hovertemplate = "<b> %{y}  Table%{x} <br><br> %{z} People"
    hover2 = "No Reservation"

    
    fig = go.Figure(data=go.Heatmap(
            z = list_z,
            x = list(range(1,11)),
            y = df_table.index,
            type="heatmap",
            name="",
            xgap = 3,
            ygap = 5,
            hovertemplate=hovertemplate,
            showscale=False,
            colorscale=[ [0, "#FFFFFF"],[1, "#1c62ff"]],
            )
        )

    fig.update_layout(
        margin=dict(l=70, b=50, t=50, r=50),
        modebar={"orientation": "v"},
        font=dict(family="Open Sans"),
        xaxis=dict(
            nticks = 20,
            side="top",
            tickfont=dict(family="sans-serif"),
            tickcolor="#ffffff",
            showgrid = True,
            gridcolor = "black",
            title = "Tables"
        ),
        
        yaxis=dict(
            side="left", tickfont=dict(family="sans-serif"), ticksuffix=" ",showgrid = True
        ),
        hovermode="closest",
        showlegend=False
    )
    
    return fig


def df_to_table():
    """
    #Draw table 
    only update when refresh
    """
    #SQL
    conn = sqlite3.connect('assets\DashTemp.db')
    c = conn.cursor()
    sql = f"select * from RESERVATION where TIME > '{str(dt.today())}'"
    df_order = pd.read_sql(sql,conn)
    conn.commit()
    conn.close()
    df_order = df_order.sort_values("TIME")
    return html.Table(
        [html.Tr([html.Th(col) for col in df_order.columns])]
        + [
            html.Tr([html.Td(df_order.iloc[i][col]) for col in df_order.columns])
            for i in range(len(df_order))
        ],
        style={"height":'98%'}
    )



#可以显示一下接下来的三个订单
layout = [
    html.Div(
        id="cases_grid",
        children=[
            # Zhang 6:00-7:00 Table 31
            html.Div(
                id="order_indicators",
                className="pretty_container",
                children=[
                    html.H3("Cases Type"),
                    html.Div(
                        refresh()
                        ),
                    ]
            ),
            #订座表
            html.Div(
                id="cases_types_container",
                className="pretty_container chart_div",
                children=[
                    html.H3("Fullfilment"),
                    dcc.Graph(id="heatmap_table"),
                ],
            ),
            #订座列表
            html.Div(
                id="cases_reasons_container",
                className="chart_div pretty_container",
                children=[
                    html.H3("Order List"),
                    df_to_table(),
                    dcc.Dropdown( 
                            id="dropdown_hidden",
                            options=[{"label":"hhhhhh","value":"val"}],
                            value="val",
                            className="dcc_control",
                            style={"display":"none"}
                        ),
                ],
                style={'height': 500,'overflow-x': "hidden","overflow-y": 'auto'},
            ),
            
        ],
    ),
]
