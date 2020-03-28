import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from app import app
from panels import review, statistics, order


server = app.server

app.layout = html.Div(
    [
        html.Div(
            className="row header",
            children=[
                html.Button(id="menu", children=dcc.Markdown("&#8801")),
                html.Span(
                    className="app-title",
                    children=[
                        dcc.Markdown("**Restaurant Name**"),
                        html.Span(
                            id="subtitle",
                            children=dcc.Markdown("&nbsp Restaurant Dashboard"),
                            style={"font-size": "1.8rem", "margin-top": "15px"},
                        ),
                    ],
                ),
            ],
        ),
        html.Div(
            id="tabs",
            className="row tabs",
            children=[
                dcc.Link("Statistics", href="/"),
                dcc.Link("Review", href="/"),
                dcc.Link("Order Management", href="/"),
            ],
        ),
        html.Div(
            id="mobile_tabs",
            className="row tabs",
            style={"display": "none"},
            children=[
                dcc.Link("Statistics", href="/"),
                dcc.Link("Review", href="/"),
                dcc.Link("Order Management", href="/"),
            ],
        ),
        #似乎是存数据的地方 大概率用不到
        # dcc.Store(  # opportunities df
        #     id="opportunities_df",
        #     data="data1",
        # ),
        # dcc.Store(  # leads df
        #     id="leads_df", data="data1"
        # ),
        # dcc.Store(
        #     id="cases_df", data="data1"
        # ),  # cases df
        dcc.Location(id="url", refresh=False),
        html.Div(id="tab_content"),
        html.Link(
            href="https://use.fontawesome.com/releases/v5.2.0/css/all.css",
            rel="stylesheet",
        ),
        html.Link(
            href="https://fonts.googleapis.com/css?family=Dosis", rel="stylesheet"
        ),
        html.Link(
            href="https://fonts.googleapis.com/css?family=Open+Sans", rel="stylesheet"
        ),
        html.Link(
            href="https://fonts.googleapis.com/css?family=Ubuntu", rel="stylesheet"
        ),
    ],
    className="row",
    style={"margin": "0%"},
)

# Update the index


@app.callback(
    [
        Output("tab_content", "children"),
        Output("tabs", "children"),
        Output("mobile_tabs", "children"),
    ],
    [Input("url", "pathname")],
)
def display_page(pathname):
    tabs = [
        dcc.Link("Statistics", href="/dash-salesforce-crm/Statistics"),
        dcc.Link("Review", href="/dash-salesforce-crm/Review"),
        dcc.Link("Order Management", href="/dash-salesforce-crm/Order"),
    ]
    if pathname == "/dash-salesforce-crm/Review":
        tabs[1] = dcc.Link(
            dcc.Markdown("**&#9632 Review**"),
            href="/dash-salesforce-crm/Review",
        )
        return review.layout, tabs, tabs
    elif pathname == "/dash-salesforce-crm/Statistics":
        tabs[0] = dcc.Link(
            dcc.Markdown("**&#9632 Statistics**"), href="/dash-salesforce-crm/Statistics"
        )
        return statistics.layout, tabs, tabs
    tabs[2] = dcc.Link(
        dcc.Markdown("**&#9632 Order Management**"), href="/dash-salesforce-crm/Order"
    )
    return order.layout, tabs, tabs


@app.callback(
    Output("mobile_tabs", "style"),
    [Input("menu", "n_clicks")],
    [State("mobile_tabs", "style")],
)
def show_menu(n_clicks, tabs_style):
    if n_clicks:
        if tabs_style["display"] == "none":
            tabs_style["display"] = "flex"
        else:
            tabs_style["display"] = "none"
    return tabs_style


if __name__ == "__main__":
    app.run_server(debug=True)
