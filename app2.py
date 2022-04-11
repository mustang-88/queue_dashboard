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

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app2 = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# server = app.server

app2.config.suppress_callback_exceptions = True
# Keep this out of source code repository - save in a file or a database
# VALID_USERNAME_PASSWORD_PAIRS = [
#   ['[kinray]', '[kinray'],
#  ]

# auth = dash_auth.BasicAuth(
#   app,
#  VALID_USERNAME_PASSWORD_PAIRS
# )


results = pd.merge(acd, adherence, how='left', on=['userid'])

#results.set_index('userid', inplace=True)

print(results.columns)

# userid, adherence, goal, totnAnsweredACD, acw, aht

# fig = go.Figure(data=[go.Table(header=dict(values=['Agent', 'Calls Rec', 'ACW', 'AHT', 'ADH']),
#                cells=dict(values=[col1, col2, col3, col4]))
#                   ])

# plotly.offline.plot(fig, filename='Customer Service.html',auto_open=False)

app.layout = dash_table.DataTable(
    data=df.to_dict('records'),
    columns=[{'id': c, 'name': c} for c in df.columns],

    style_data={
        'color': 'black',
        'backgroundColor': 'white'
    },
    style_data_conditional=[
        {
            'if': {'row_index': 'odd'},
            'backgroundColor': 'rgb(220, 220, 220)',
        }
    ],
    style_header={
        'backgroundColor': 'rgb(210, 210, 210)',
        'color': 'black',
        'fontWeight': 'bold'
    },
)



@app2.callback(
    Output('datatable-interactivity', 'style_data_conditional'),
    [Input('datatable-interactivity', 'selected_columns')]
)
def update_styles(selected_columns):
    return [{
        'if': {'column_id': i},
        'background_color': '#D2F3FF'
    } for i in selected_columns]


if __name__ == '__main__':
    app2.run_server(debug=True)

# fig.show()
