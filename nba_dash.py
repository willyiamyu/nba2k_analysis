import pandas as pd
import plotly.express as px  
import plotly.graph_objects as go

import dash  
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

nba_df = pd.read_csv('nba_rankings_2014-2020')
nba_df.drop(['Unnamed: 0'], axis=1, inplace=True)

average = nba_df[nba_df['rankings'] == 75].loc[:, ['PTS', 'REB', 'AST','STL', 'BLK',  'TOV', '+/-']]

fig = px.bar(x=['PTS', 'REB', 'AST', 'STL', 'BLK', 'TOV',  '+/-'], 
   y=average.mean(), title= 'Average NBA Stats for Given 2K Rating', text=average.mean(), 
             labels=dict(x="Stats", y="Mean"), height=600 )  
fig.update_yaxes(range=[-3.5, 32])
fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
f = go.FigureWidget(fig)

app.layout = html.Div(children=[
	html.Br(),

    html.Div(id='output_container', children=[], style={ 'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}),

    html.Br(),

    dcc.Slider(id='myslider', min=62, value=75, max=98, step=1, updatemode='drag',
    	marks ={62: {'label': '62'},
    	70: {'label': '70'},
    	80: {'label': '80'},
    	90: {'label': '90'},
    	98: {'label': '98'},
    	}),
    
    dcc.Graph(id='nba_map', figure=f)

],style = {'margin':'auto','width': "70%"})

@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='nba_map', component_property='figure')],
    [Input(component_id='myslider', component_property='value')]
)

def update_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))
    
    container = "NBA 2K Ranking: {}".format(option_slctd)
    
    nba_dff = nba_df.copy()
    nba_dff = nba_dff[nba_dff['rankings'] == option_slctd]
    nba_dff = nba_dff.loc[:, ['PTS', 'REB', 'AST','STL', 'BLK',  'TOV', '+/-']]
    
    f.data[0].y = nba_dff.mean()
    f.update_traces(text = nba_dff.mean(), texttemplate='%{text:.3g}', textposition='outside')

    
    return container, f

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)