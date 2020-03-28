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

colors = {"background": "#F3F6FA", "background_div": "white"}
tableNum = 10

# 订餐数据表
orderDataFrame = pd.DataFrame({
                    "Table ID":[1,2,3,4,5],
                    "Name":["A","B","C","D","E"],
                    "Date":[15,15,15,15,15],
                    'time':["2020-03-29 12:30:00","2020-03-29 14:30","2020-03-29 18:30","2020-03-30 22:30","2020-03-30 23:30"],
                    "People":[1,4,2,3,4],
                    "remark":["Null","Null","Null","Null","Null"]
                    })

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
    "Table ID":[1,2,3,4,5],
                    "Name":["A","B","C","D","E"],
                    "Date":[15,15,15,15,15],
                    'time':["2020-03-2 12:30:00","2020-03-2 14:30:00","2020-03-2 18:30:00","2020-03-2 22:30:00","2020-03-2 23:30:00"],
                    "People":[1,4,2,3,4],
                    "remark":["Null","Null","Null","Null","Null"]
                    })
    """
    #SQL 
    df_order = orderDataFrame.copy()
    #find order after now
    df_order = df_order[pd.to_datetime(df_order["time"])>dt.today()]
    #sort
    df_order = df_order.sort_values("time")
    #find recent order
    df_order = df_order[:3]
    
    html_order = []
    df_order = df_order.reset_index(drop=True)
    for index in df_order.index:
        ask_df = df_order.iloc[index]
        str_order = f'{ask_df["Name"]}, {ask_df["People"]} People, visit at {ask_df["time"]}, Table {ask_df["Table ID"]}'
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
    df_order = orderDataFrame.copy()
    #find order after now
    df_order = df_order[pd.to_datetime(df_order["time"])>dt.today()]


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
    
    #建一个时间list 七个最好
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
                if df_order.iloc[index]["time"] in interval_list:
                    new_table[df_order.iloc[index]["Table ID"]][i] = 1
        elif dt.today().hour >13:
            #用for循环判断是否在时间区间内
            for i in range(6):
                interval_list = pd.Interval(list_time[i+1],list_time[i+2], closed='left')
                if pd.to_datetime(df_order.loc[index]["time"]) in interval_list:
                    new_table[df_order.loc[index]["Table ID"]][i] = 1
    
    
    df_table = pd.DataFrame(new_table)
    df_table.index = list_index

    df_table
    x_axis = list(range(1,11))  # 24hr time list
    y_axis = list_index

    # Heatmap
    hovertemplate = "<b> %{y}  %{x} <br><br> %{z} Patient Records"
    list_z = np.array(df_table)
    
    
    fig = go.Figure(data=go.Heatmap(
            z = list_z,
            x = list(range(1,11)),
            y = df_table.index,
            type="heatmap",
            name="",
            xgap = 3,
            ygap = 3,
            # mode = "lines",
            # line= {
            #     'width': 5,
            #     'color': 'black'
            # },
            hovertemplate=False,
            showscale=False,
            colorscale=[[0, "#caf3ff"], [1, "#2c82ff"]],
            )
        )

    fig.update_layout(
        margin=dict(l=70, b=50, t=50, r=50),
        modebar={"orientation": "v"},
        font=dict(family="Open Sans"),
        xaxis=dict(
            nticks = 20,
            side="top",
            ticks="",
            tickfont=dict(family="sans-serif"),
            tickcolor="#ffffff",
            showgrid = True,
            gridcolor = "black"
        ),
        yaxis=dict(
            side="left", ticks="", tickfont=dict(family="sans-serif"), ticksuffix=" ",showgrid = True
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
    df_review = orderDataFrame.copy()
    return html.Table(
        [html.Tr([html.Th(col) for col in df_review.columns])]
        + [
            html.Tr([html.Td(df_review.iloc[i][col]) for col in df_review.columns])
            for i in range(len(df_review))
        ]
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
            ),
            
        ],
    ),
]


# @app.callback(Output("left_cases_indicator", "children"), [Input("cases_df", "data")]), config=dict(displayModeBar=False)
# def left_cases_indicator_callback(df):
#     df = pd.read_json(df, orient="split")
#     low = len(df[(df["Priority"] == "Low") & (df["Status"] == "New")]["Priority"].index)
#     return dcc.Markdown("**{}**".format(low))


# @app.callback(Output("middle_cases_indicator", "children"), [Input("cases_df", "data")])
# def middle_cases_indicator_callback(df):
#     df = pd.read_json(df, orient="split")
#     medium = len(
#         df[(df["Priority"] == "Medium") & (df["Status"] == "New")]["Priority"].index
#     )
#     return dcc.Markdown("**{}**".format(medium))


# @app.callback(Output("right_cases_indicator", "children"), [Input("cases_df", "data")])
# def right_cases_indicator_callback(df):
#     df = pd.read_json(df, orient="split")
#     high = len(
#         df[(df["Priority"] == "High") & (df["Status"] == "New")]["Priority"].index
#     )
#     return dcc.Markdown("**{}**".format(high))


# @app.callback(
#     Output("cases_reasons", "figure"),
#     [
#         Input("priority_dropdown", "value"),
#         Input("origin_dropdown", "value"),
#         Input("cases_df", "data"),
#     ],
# )
# def cases_reasons_callback(priority, origin, df):
#     df = pd.read_json(df, orient="split")
#     chart = pie_chart(df, "Reason", priority, origin)
#     return chart


# @app.callback(
#     Output("cases_types", "figure"),
#     [
#         Input("priority_dropdown", "value"),
#         Input("origin_dropdown", "value"),
#         Input("cases_df", "data"),
#     ],
# )
# def cases_types_callback(priority, origin, df):
#     df = pd.read_json(df, orient="split")
#     chart = pie_chart(df, "Type", priority, origin)
#     chart["layout"]["legend"]["orientation"] = "h"
#     return chart


# @app.callback(
#     Output("cases_by_period", "figure"),
#     [
#         Input("cases_period_dropdown", "value"),
#         Input("origin_dropdown", "value"),
#         Input("priority_dropdown", "value"),
#         Input("cases_df", "data"),
#     ],
# )
# def cases_period_callback(period, origin, priority, df):
#     df = pd.read_json(df, orient="split")
#     return cases_by_period(df, period, priority, origin)


# @app.callback(Output("cases_by_account", "figure"), [Input("cases_df", "data")])
# def cases_account_callback(df):
#     df = pd.read_json(df, orient="split")
#     return cases_by_account(df)


# @app.callback(Output("cases_modal", "style"), [Input("new_case", "n_clicks")])
# def display_cases_modal_callback(n):
#     if n > 0:
#         return {"display": "block"}
#     return {"display": "none"}


# @app.callback(
#     Output("new_case", "n_clicks"),
#     [Input("cases_modal_close", "n_clicks"), Input("submit_new_case", "n_clicks")],
# )
# def close_modal_callback(n, n2):
#     return 0


# @app.callback(
#     Output("cases_df", "data"),
#     [Input("submit_new_case", "n_clicks")],
#     [
#         State("new_case_account", "value"),
#         State("new_case_origin", "value"),
#         State("new_case_reason", "value"),
#         State("new_case_subject", "value"),
#         State("new_case_contact", "value"),
#         State("new_case_type", "value"),
#         State("new_case_status", "value"),
#         State("new_case_description", "value"),
#         State("new_case_priority", "value"),
#         State("cases_df", "data"),
#     ],
# )
# def add_case_callback(
#     n_clicks,
#     account_id,
#     origin,
#     reason,
#     subject,
#     contact_id,
#     case_type,
#     status,
#     description,
#     priority,
#     current_df,
# ):
#     if n_clicks > 0:
#         query = {
#             "AccountId": account_id,
#             "Origin": origin,
#             "Reason": reason,
#             "Subject": subject,
#             "ContactId": contact_id,
#             "Type": case_type,
#             "Status": status,
#             "Description": description,
#             "Priority": priority,
#         }

#         sf_manager.add_case(query)
#         df = sf_manager.get_cases()
#         return df.to_json(orient="split")

    # return current_df
