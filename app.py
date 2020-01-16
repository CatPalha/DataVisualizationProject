import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import numpy as np
import pandas as pd
import plotly.graph_objs as go

######################################################Data##############################################################

df = pd.read_csv('data.csv', sep = ';')

gas_names = ['CO2_emissions', 'CH4_emissions','N2O_emissions', 'GHG_emissions']


######################################################Interactive Components############################################

country_options = [dict(label=country, value=country) for country in df['Country Name'].unique()]

year = [dict(label = year, value = year) for year in df['year'].unique()]

gas_options = [dict(label=gas.replace('_', ' '), value=gas) for gas in gas_names]

##################################################APP###############################################################
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div([
                html.H1('World Emissions - Data Visualization Project'),
                html.H4('by Catarina, Mafalda and Maren')
            ], className='Title'),
    html.Div([
        html.Label('Choose a year:'),
        dcc.Slider(
            id='year_slider',
            min=df['year'].min(),
            max=df['year'].max(),
            marks={str(i): '{}'.format(str(i)) for i in df['year'].unique()},
            value=df['year'].min(),
            step=None
        ),
        html.Br(),
    ]),
    html.Div([
        html.Div([
            html.Label('Choose one or more countries:'),
            dcc.Dropdown(
                id='country_drop',
                options=country_options,
                value=['Portugal'],
                multi=True
            )
        ], className='column'),
        html.Div([
            html.Label('Choose a projection:'),
            dcc.RadioItems(
                id='projection',
                options=[dict(label='Equirectangular', value=0), dict(label='Orthographic', value=1)],
                value=0,
                labelStyle={'display': 'inline-block'}
            )
        ], className='column'),
        html.Div([
            html.Label('Choose a scale: '),
            dcc.RadioItems(
                id='lin_log',
                options=[dict(label='Linear', value=0), dict(label='Log', value=1)],
                value=0,
                labelStyle={'display': 'inline-block'}
            )
        ], className='column'),
        html.Div([
            html.Label('Choose a gas:'),
            dcc.Dropdown(
                id='gas_option',
                options=gas_options,
                value='CO2_emissions',
            )
        ], className='column')
    ], className='row'),
    html.Div([
        html.Div([
            html.Div([dcc.Tabs([
                            dcc.Tab(label='World Map', children=[
                                html.Div([
                                    html.Div([html.H6('Filter by: year, projection and gas')], className='column'),
                                    html.Div([html.H6('Filter by: year and projection')], className='column')
                                ], className='row'),
                                html.Div([
                                    html.Div([
                                        html.H5('World emissions per capita (kt of CO2)'),
                                        dcc.Graph(id='choropleth')
                                    ], className='columnMap1'),
                                    html.Div([
                                        html.H5('GDP per capita (USD)'),
                                        dcc.Graph(id='choropleth2')
                                    ], className='columnMap2')
                                ], className='row'),
                            ]),
                            dcc.Tab(label='Time Series Data', children=[
                                html.Div([
                                    html.H6('Filter by: countries and scale')
                                    ], className='row'),
                                html.Div([
                                    html.Div([
                                        html.H5('Emissions per capita (kt of CO2) from 1990 until 2012'),
                                        dcc.Graph(id='bar_graph'),
                                    ], className='columnMap1'),
                                    html.Div([
                                        html.H5('GDP per capita (US$) from 1990 until 2012'),
                                        dcc.Graph(id='bar_graph2')
                                    ], className='columnMap2')
                                ], className='row'),
                            ]),
                            dcc.Tab(label='Bar Plot Emissions', children=[
                                html.Div([
                                    html.H6('Filter by: year, countries and scale')
                                    ], className='row'),
                                html.Div([
                                    html.Div([
                                    ], className='columnmi'),
                                    html.Div([
                                        html.H5('Emissions per capita (kt of CO2)'),
                                        dcc.Graph(id='bar_plot'),
                                    ], className='columnBar'),
                                    html.Div([
                                    ], className='columnmi')
                                ], className='row'),
                            ]),
                    ])
                ]),
            ], className='column2 pretty')
    ], className='row')
])


######################################################Callbacks#########################################################
@app.callback(
    [
        Output("bar_graph", "figure"),
        Output("bar_graph2", "figure"),
        Output("choropleth", "figure"),
        Output("choropleth2", "figure"),
        Output("bar_plot", "figure")
    ],
    [
        Input("year_slider", "value"),
        Input("country_drop", "value"),
        Input("gas_option", "value"),
        Input("lin_log", "value"),
        Input("projection", "value"),
    ]
)

def plots(year, countries, gas, scale, projection):
############################# Time Series Plot ##########################################################
    time_scatter = []
    for country in countries:
        df_bar = df.loc[(df['Country Name'] == country)]

        x_bar = df_bar['year']
        y_bar = df_bar[gas]

        time_scatter.append(dict(type='scatter', x=x_bar, y=y_bar, name=country))

    layout_scatter = dict(#title=dict(text='Emissions per capita (kt of CO2) from 1990 until 2015'),
                      xaxis=go.layout.XAxis(
                          rangeselector=dict(
                              buttons=list([
                                  dict(count=1,
                                       label="YTD",
                                       step="year",
                                       stepmode="todate"),
                                  dict(count=5,
                                       label="5y",
                                       step="year",
                                       stepmode="backward"),
                                  dict(count=10,
                                       label="10y",
                                       step="year",
                                       stepmode="backward"),
                                  dict(step="all")
                              ])
                          ),
                          rangeslider=dict(
                              visible=True

                          ),
                          type="date"
                      ),
                      yaxis=dict(title='Emissions', type=['linear', 'log'][scale]),
                      paper_bgcolor='#f9f9f9'
                      )

    time_scatter2 = []
    for country in countries:
        df_bar = df.loc[(df['Country Name'] == country)]

        x_bar = df_bar['year']
        y_bar = df_bar['GDP']

        time_scatter2.append(dict(type='scatter', x=x_bar, y=y_bar, name=country))

    layout_scatter2 = dict(#title=dict(text='GDP per capita (US$) from 1990 until 2015'),
                       xaxis=go.layout.XAxis(
                           rangeselector=dict(
                               buttons=list([
                                   dict(count=1,
                                        label="YTD",
                                        step="year",
                                        stepmode="todate"),
                                   dict(count=5,
                                        label="5y",
                                        step="year",
                                        stepmode="backward"),
                                   dict(count=10,
                                        label="10y",
                                        step="year",
                                        stepmode="backward"),
                                   dict(step="all")
                               ])
                           ),
                           rangeslider=dict(
                               visible=True

                           ),
                           type="date"
                       ),
                       yaxis=dict(title='Emissions', type=['linear', 'log'][scale]),
                       paper_bgcolor='#f9f9f9'
                       )
    ############################################# World Map #####################################################

    df_map = df.loc[df['year'] == year]

    z = np.log(df_map[gas])

    # print(z)
    # print(df_map['Country Name'])

    data_choropleth = dict(type='choropleth',
                           locations=df_map['Country Name'],
                           locationmode='country names',
                           z=z,
                           text=df_map['Country Name'],
                           colorscale='YlOrRd',
                           #colorbar_title='kt of CO2',
                           #reversescale=True,
                           name='')

    #title_choropleth = 'World emissions of ' + gas + ' per capita (kt of CO2) in ' + str(year)

    layout_choropleth = dict(
        #title=title_choropleth,
        geo=dict(scope='world',  # default
                 projection=dict(type=['equirectangular', 'orthographic'][projection]),
                 landcolor='black',
                 lakecolor='white',
                 showocean=True,
                 oceancolor='azure',
                 bgcolor='#f9f9f9'),
        paper_bgcolor='#f9f9f9',
        margin=dict(t=0, b=0, l=0, r=0)
    )

    map = go.Figure(data=data_choropleth, layout=layout_choropleth)

    z2 = np.log(df_map['GDP'])

    data_choropleth2 = dict(type='choropleth',
                            locations=df_map['Country Name'],
                            locationmode='country names',
                            z=z2,
                            text=df_map['Country Name'],
                            colorscale='YlOrRd',
                            #colorbar_title='USD',
                            #reversescale=True,
                            name='')

    #title_choropleth2 = 'GDP per capita (USD) in ' + str(year)

    layout_choropleth2 = dict(
        #title = title_choropleth2,
        geo=dict(scope='world',  # default
                 projection=dict(type=['equirectangular', 'orthographic'][projection]),
                 landcolor='black',
                 lakecolor='white',
                 showocean=True,
                 oceancolor='azure',
                 bgcolor='#f9f9f9'),
        paper_bgcolor='#f9f9f9',
        margin=dict(t=0, b=0, l=0, r=0)
    )

    map2 = go.Figure(data=data_choropleth2, layout=layout_choropleth2)

    #### Bar plot ####

    fig2 = go.Figure()

    for country in countries:
        y = []
        for gas in gas_names:
            #print(df[gas].loc[(df['Country Name'] == country) & (df['year'] == year)])
            y.append(df[gas].loc[(df['Country Name']==country) & (df['year']==year)].values[0])

        fig2.add_trace(go.Bar(
            x=gas_names,
            y=y,
            name=country,
        ))

    # Here we modify the tickangle of the xaxis, resulting in rotated labels.
    fig2.update_layout(
        #title_text='Emissions per capita (kt of CO2) for ' + str(year),
        yaxis=dict(title='Emissions', type=['linear', 'log'][scale]))
    fig2.update_layout(barmode='group', xaxis_tickangle=-45)
    #fig.show()

    return go.Figure(data=time_scatter, layout=layout_scatter),\
           go.Figure(data=time_scatter2, layout=layout_scatter2),\
           map,\
           map2,\
           fig2

server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)