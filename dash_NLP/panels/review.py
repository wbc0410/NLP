# -*- coding: utf-8 -*-
from datetime import date
import pandas as pd
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
from plotly import graph_objs as go
import numpy as np
from app import app, indicator, millify, df_to_table


#需要两个词云，一个topic modeling表 一个topic modeling chart 一个review时事table

"""
1.词云
2.做一个假的topic modeling表
3.做一个假的柱状图
4.再下方显示假评论表
"""
# 评论文字表格

str1 = """The staff & service are excellent & strike that wonderful balance between professional, knowledgeable & friendly.The ambience & decor are nice."""
str2 = """This was my first time visiting. Firstly, the staff were very attentive and engaged. They explained how the ordering worked and were more than happy to help us take photos of dishes that my father forgot to take (to show to his friends) by waiting for the same dish that would be served to other tables."""
str3 = """The setting is quite casual and comfortable. They serve bread too. if you want your bread to be toasted, you can just let them know."""
str4 = """We celebrated our anniversary at Chef's table and loved it. We went for the 6 course option w/ 4 wine pairing. We called out a number of ingredient we wanted to avoid - which were impeccably followed by the chef into the stunning dishes which continued to surprise us with delight through the evening. We'd look to come back soon!"""
str5 = """Excellent food, great service, nice atmosphere, absolutely go there. Suprise what you get, you only know some ingredients. Loved it."""

wordTable = {
             "Review": [str1, str2, str3, str4, str5]*20,
             }
wordDataFrame = pd.DataFrame(wordTable)
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
    df_review = wordDataFrame.copy()
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
    df_review = wordDataFrame.copy()
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
                id="converted_count_container",
                className="chart_div pretty_container",
                children=[
                    html.P("Positive Word Cloud"),
                    html.Img(src=app.get_asset_url("Positive.png"),style={"width":'100%',"Height":'40%'}),
                    html.P("Negative Word Cloud"),
                    html.Img(src=app.get_asset_url("Negative.png"),style={"width":'100%',"Height":'40%'}),
                ],
            ),
            # #TM列表
            # html.Div(
            #     id="Review_heatmap",
            #     className="chart_div pretty_container",
            #     children=[
            #         html.Div(id="top_open_opportunities", className="table"),
            #     ],
            # ),
            # #TM图表
            # html.Div(
            #     id="top_open_container",
            #     className="chart_div pretty_container",
            #     children=[
            #         dcc.Graph(
            #             id="heatmap",
            #             style={"height": "90%", "width": "98%"},
            #             config=dict(displayModeBar=False),
            #         ),
            #     ],
            # ),
            #TM列表
            html.Div(
                id="Review_heatmap",
                className="chart_div pretty_container",
                children=[
                    html.Table([
                        html.Thead(
                            html.Tr([html.Th(col) for col in ["Topic 1","Topic 2","Topic 3","Topic 4","Topic 5"]])
                        ),
                        html.Tbody([
                            html.Tr([
                                html.Td("NaN") for col in ["Topic 1","Topic 2","Topic 3","Topic 4","Topic 5"]
                            ]) for i in range(5)
                        ])
                    ])
                ],
            ),
            #TM图表
            html.Div(
                id="top_open_container",
                className="chart_div pretty_container",
                children=[
                    dcc.Graph(
                        id='example-graph',
                        figure={
                            'data': [
                                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
                            ],
                            'layout': {
                                'title': 'Dash Data Visualization'
                            }
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


