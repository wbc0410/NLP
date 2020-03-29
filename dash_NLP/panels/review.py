# -*- coding: utf-8 -*-
from datetime import date
import pandas as pd
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
from plotly import graph_objs as go
import numpy as np
from app import app, indicator, millify, df_to_table
import sqlite3
df_tm = pd.read_csv("assets\Topic Model Table.csv")
from datetime import datetime as dt
#需要两个词云，一个topic modeling表 一个topic modeling chart 一个review时事table

"""
1.词云
2.做一个假的topic modeling表
3.做一个假的柱状图
4.再下方显示假评论表
"""
# 评论文字表格



###############################################################################################
#假topic modeling表

#评论列表
#单独写一个，因为不需要表头
def df_to_table_for_review():
    """
    #Draw table 
    only update when refresh
    """
    #SQL
    conn = sqlite3.connect('assets\DashTemp.db')
    c = conn.cursor()
    sql = f"select REVIEW from REVIEW where TIME < '{str(dt.today())}' limit 1000"
    df_review = pd.read_sql(sql,conn)
    conn.commit()
    conn.close()
    return html.Table(
        [
            html.Tr([html.Td(df_review.iloc[i][col]) for col in df_review.columns])
            for i in range(len(df_review))
        ]
    )

# update table based on dropdown's value and df updates
def df_to_table():
    """
    #Draw table 
    only update when refresh
    """
    #SQL
    df_review = df_tm.copy()
    return html.Table(
        [html.Tr([html.Th(col) for col in df_review.columns])]
        + [
            html.Tr([html.Td(df_review.iloc[i][col]) for col in df_review.columns])
            for i in range(len(df_review))
        ]
    )


layout = [
    html.Div(
        id="Review_grid",
        children=[
            #tM标题
            html.Div(
                id="Review_indicators",
                className="subtitle",
                children=[
                    indicator(
                        "#00cc96", "Topic Cluster", "left_opportunities_indicator"
                    ),
                ],
            ),
            #词云
            html.Div(
                id="Word_Cloud_container",
                className="chart_div pretty_container",
                children=[
                    html.Div(
                        [
                            html.H4("Positive Word Cloud"),
                            html.Img(src=app.get_asset_url("Positive.png"),style={"width":'100%',"Height":'40%'}),
                        ],
                        style={"display": "inline-block","margin-left":30,"width":'45%'}
                    ),
                    html.Div(
                        [
                            html.H4("Negative Word Cloud"),
                            html.Img(src=app.get_asset_url("Negative.png"),style={"width":'100%',"Height":'40%'}),
                        ],
                        style={"display": "inline-block","margin-left":30,"width":'45%'}
                    )
                ],
            ),
            #TM列表
            html.Div(
                id="TM_Table",
                className="chart_div pretty_container",
                children=df_to_table(),
            ),
            #TM图表
            html.Div(
                id="TM_Chart",
                className="chart_div pretty_container",
                children=[
                    dcc.Graph(
                        id='lead_source',
                        figure={
                            'data': [
                                {'x': ["Topic 1", "Topic 2","Topic 3","Topic 4","Topic 5"], 'y': [16, 10, 20, 34,12], 'type': 'bar'},
                            ],
                            'layout': dict(
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
                                        title = "Topic"
                                    ),
                                    
                                    yaxis=dict(
                                        side="left", tickfont=dict(family="sans-serif"), ticksuffix=" ",showgrid = True,
                                        title = "Number of Reviews"
                                    ),
                                    hovermode="closest",
                                    showlegend=False
                                )
                        }
                    )
                ],
            ),
            #review
            html.Div(
                id="top_lost_container",
                className="pretty_container",
                children=[
                    html.Div([html.P("Reviews")], className="subtitle"),
                    html.Div(id="leads_table", 
                            children=df_to_table_for_review(),
                            style={'height': 400,'overflow-x': "hidden","overflow-y": 'auto'}),
                ],
            ),
            
        ],
    ),
]


