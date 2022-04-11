from datetime import datetime as dt
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from qsr import que_sum
from adherence import adherence
from user_prod import acd
import dash_auth

#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__)#, external_stylesheets=external_stylesheets)

# server = app.server

app.config.suppress_callback_exceptions = True
# Keep this out of source code repository - save in a file or a database
# VALID_USERNAME_PASSWORD_PAIRS = [
#   ['[kinray]', '[kinray'],
#  ]

# auth = dash_auth.BasicAuth(
#   app,
#  VALID_USERNAME_PASSWORD_PAIRS
# )


def generate_table(que_sum, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in que_sum.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(que_sum.iloc[i][col]) for col in que_sum.columns
            ]) for i in range(min(len(que_sum), max_rows))
        ])
    ])



results = pd.merge(acd, adherence, how='left', on=['userid'])

#results.set_index('userid', inplace=True)

cols = {'userid': 'Representative', 'totnAnsweredACD': 'Calls Taken', 'acw': 'ACW', 'aht': 'AHT', 'adherence':'ADH', 'goal': 'Goal'}
cols2 = {'DisplaycName': 'Customer Service', 'nEnteredAcd': 'Inbound Calls', 'nAnsweredAcd': 'Calls Answered', 'nAbandonedAcd': 'Abandoned', 'acw': 'ACW', 'aht': 'AHT', 'acw_goal': 'ACW Target', 'aht_goal': 'AHT Target', 'abn_goal': 'ABN Target'}

results.rename(columns=cols, inplace=True)
que_sum.rename(columns=cols2, inplace= True)


fig1 = px.bar(que_sum, x= 'Customer Service', y= ['Inbound Calls', 'Calls Answered', 'Abandoned', 'ABN Target'], barmode = 'group', width= 500, height= 500)
fig2 = px.bar(que_sum, x= 'Customer Service', y= ['ACW', 'ACW Target', 'AHT', 'AHT Target'], barmode = 'group', width= 500, height= 500)

# print(results.columns)

# userid, adherence, goal, totnAnsweredACD, acw, aht

# fig = go.Figure(data=[go.Table(header=dict(values=['Agent', 'Calls Rec', 'ACW', 'AHT', 'ADH']),
#                cells=dict(values=[col1, col2, col3, col4]))
#                   ])

# plotly.offline.plot(fig, filename='Customer Service.html',auto_open=False)

app.layout = html.Div(children=[

    html.H1(children="Customer Service Performance Dashboard", style={'textAlign': 'left',
                                                   'fontSize': '24px', 'display': 'inline-blocks'}),

    dcc.DatePickerRange(
        id="date_range_picker",
        calendar_orientation='horizontal',  # vertical or horizontal
        day_size=39,  # size of calendar image. Default is 39
        end_date_placeholder_text="Select a date",  # text that appears when no end date chosen
        with_portal=False,  # if True calendar will open in a full screen overlay portal
        first_day_of_week=0,  # Display of calendar when open (0 = Sunday)
        reopen_calendar_on_clear=True,
        is_RTL=False,  # True or False for direction of calendar
        clearable=True,  # whether or not the user can clear the dropdown
        number_of_months_shown=1,  # number of months shown when calendar is open
        min_date_allowed=dt(2018, 1, 1),  # minimum date allowed on the DatePickerRange component
        max_date_allowed=dt(2020, 6, 20),  # maximum date allowed on the DatePickerRange component
        initial_visible_month=dt(2020, 5, 1),  # the month initially presented when the user opens the calendar
        start_date=dt(2018, 8, 7).date(),
        end_date=dt(2020, 5, 15).date(),
        display_format='MMM Do, YY',  # how selected dates are displayed in the DatePickerRange component.
        month_format='MMMM, YYYY',  # how calendar headers are displayed when the calendar is opened.
        minimum_nights=2,  # minimum number of days between start and end date
        style={'display': 'inline-blocks', 'textAlign': 'left'},

        persistence=True,
        persisted_props=['start_date'],
        persistence_type='session',  # session, local, or memory. Default is 'local'

        updatemode='singledate'  # singledate or bothdates. Determines when callback is triggered
    ),

    html.H2(children="Grouped Performance", style={'textAlign': 'left',
                                                       'fontSize': '24px', 'display': 'inline-blocks'}),
    generate_table(que_sum),

    html.Div(children=[
    dcc.Graph(id='graph1',figure=fig1,style={'display': 'inline-block'}),
    dcc.Graph(id='graph2',figure=fig2,style={'display': 'inline-block'})
    ]

            ),
    html.H3("Performance by Agent",
            style={'textAlign': 'left', 'fontSize': '24px', 'display': 'inline-blocks'}
    ),

    html.Div([dash_table.DataTable(
        id='datatable-interactivity',
        columns=[
            {"name": i, "id": i, "deletable": False, "selectable": False, "hideable": True}
            if i == "iso_alpha3" or i == "year" or i == "id"
            else {"name": i, "id": i, "deletable": False, "selectable": False}
            for i in results.columns
        ],
        data=results.to_dict('records'),  # the contents of the table
        editable=False,  # allow editing of data inside all cells
        filter_action="none",  # allow filtering of data by user ('native') or not ('none')
        sort_action='native',  # enables data to be sorted per-column by user or not ('none')
        sort_mode="single",  # sort across 'multi' or 'single' columns
        style_table={'height': '200px'},
        column_selectable="multi",  # allow users to select 'multi' or 'single' columns
        row_selectable=False,  # allow users to select 'multi' or 'single' rows
        row_deletable=False,  # choose if user can delete a row (True) or not (False)
        selected_columns=[],  # ids of columns that user selects
        selected_rows=[],  # indices of rows that user selects
        page_action="native",  # all data is passed to the table up-front or not ('none')
        page_current=0,  # page number that user is on
        page_size=24,  # number of rows visible per page

        style_cell={'padding': '5px',},
        style_data={
            'color': 'black',
            'backgroundColor': 'RGB(238,213,210)',
            'whitespace': 'normal',
            'textAlign': 'left',
            'height': 'auto',
        },
        #fill_width=False,

        style_data_conditional=
        [
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'RGB(104,131,139)',
            }
        ] + [
            {
                'if': {'row_index': 'odd'},
                'black': 'white',
            }
        ],
        style_header={
            'backgroundColor': 'RGB(54,100,139)',
            'color': 'white',
            'fontWeight': 'bold',
            'textAlign': 'center',
            'font_size': '13px',
            'height': 'auto',
        },

    )


])
    ])


#@app.callback(
#    dash.dependencies.Output("datatable-interactivity", "data"),
#    [
#        dash.dependencies.Input("my-date-picker-range", "start_date"),
#        dash.dependencies.Input("my-date-picker-range", "end_date"),
#    ],
#)

if __name__ == '__main__':
    app.run_server(debug=True)

# fig.show()
