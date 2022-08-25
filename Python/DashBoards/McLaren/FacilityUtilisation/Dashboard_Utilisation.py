from dash import Dash, html, dcc, Input, Output
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.graph_objects import Layout


df = pd.read_csv('C:\\Users\\timo.nielsen\\Documents\\Python Scripts\\Dashboard_Project_Plotly\\Data\\P16R_DashBoardData.csv',header=[0])

po_total = 39991
weekly_cell_cost = 14700
fuel_cost = 1.10 # cost per liter
workingHours_daily = 16
workingDays = 5
workingHours_week = workingHours_daily * workingDays
daily_cell_cost = weekly_cell_cost/workingDays



def CalcFuelUsed(data):
    data.sort_values(by=['Real Time'])
    startFuel = data['Fuel Usage'].iloc[0]
    endFuel = data['Fuel Usage'].iloc[-1]
    
    return endFuel - startFuel

def CalcFuelCost(fuelUsed,cost):
    return fuelUsed*cost

def CalcUtilisation(data):
    return 

def numDataPoints(data):
    logs = data[data['Stage Desc']=='15 Second Avg Log']
    df_avg=logs.groupby(['FileName','Cycle Number']).mean()
    return df_avg

def CalctestDuration(data):
    startEngHrs = data['Total Running Hours'].iloc[0]
    endEngHrs = data['Total Running Hours'].iloc[-1]
    return endEngHrs-startEngHrs

def CalcCellCost(data):
    startDate = pd.to_datetime(data['Date'].iloc[0])
    endDate = pd.to_datetime(data['Date'].iloc[-1])
    delta = endDate-startDate
    return delta.days


app = Dash(__name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}])

# Define the page layout:
# Top row of static data for each point.
# Main X-Y Scatter showing Engine Speed and rl on y-axis
# Two time series plots along side

app.layout = html.Div([
    html.Div([
        html.Div([
            html.Img(src=app.get_asset_url('mcl_logo_master_ful_col_rgb_wht.png'),
                     id='MCL_Logo',
                     style={
                         "height": "60px",
                         "width": "auto",
                         "margin-bottom": "25px",
                     },
                     )
        ],
            className="one-third column",
        ),
        html.Div([
            html.Div([
                html.H3("Weekly Testing Overview", style={"margin-bottom": "0px", 'color': 'white'}),
                html.H5("Intertek Cell 23", style={"margin-top": "0px", 'color': 'white'}),
            ])
        ], className="one-half column", id="title"),

        html.Div([
            html.P('Select Week Number:', className='fix_label',  style={'color': 'white'}),
            dcc.Dropdown(id='week_numbers',
                multi= False, 
                value=22,
                placeholder= 'Select Week Number',
                options =df['WeekNumber'].unique(), className='dcc_compon')

        ], className="one-third column", id='title1'),

    ], id="header", className="row flex-display", style={"margin-bottom": "25px"}),

    html.Div([
        html.Div([
            html.H6(children='# of Data Points',
                    style={
                        'textAlign': 'center',
                        'color': 'white'}
                    ),
            dcc.Graph(id='TestDataPoints',
                    config={'displayModeBar':False}, className='dcc_compon',
                    style={'margin-top': '5px',
                            'fontSize': 40}, ),
                   ], className="card_container two columns",
        ),

        html.Div([
            html.H6(children='Test Duration [Hrs]',
                    style={
                        'textAlign': 'center',
                        'color': 'white'}
                    ),

            dcc.Graph(id='TestingHours',
                    config={'displayModeBar':False}, className='dcc_compon',
                    style={'margin-top': '5px'}, ),
                ], className="card_container two columns",
        ),

        html.Div([
            html.H6(children='Fuel Consumed [L]',
                    style={
                        'textAlign': 'center',
                        'color': 'white'}
                    ),

            dcc.Graph(id='FuelUsed',
                    config={'displayModeBar':False}, className='dcc_compon',
                    style={'margin-top': '5px'}, ),
                   ], className="card_container two columns",
        ),

        html.Div([
            html.H6(children='Fuel Cost [£]',
                    style={
                        'textAlign': 'center',
                        'color': 'white'}
                    ),
            dcc.Graph(id='FuelCost',
                    config={'displayModeBar':False}, className='dcc_compon',
                    style={'margin-top': '5px'}, ),

                ], className="card_container two columns"),

        html.Div([
            html.H6(children='Total Weekly Cost [£]',
                    style={
                        'textAlign': 'center',
                        'color': 'white'}
                    ),

            dcc.Graph(id='TestingCost',
                    config={'displayModeBar':False}, className='dcc_compon',
                    style={'margin-top': '5px'}, ),

                ], className="card_container two columns"),

        html.Div([
            html.H6(children='Utilisation [%]',
                    style={
                        'textAlign': 'center',
                        'color': 'white'}
                    ),
            dcc.Graph(id='Utilisation',
                    config={'displayModeBar':False}, className='dcc_compon',
                    style={'margin-top': '5px'}, ),
            
            html.P()
                ], className="card_container two columns")

    ], className="row flex-display"),       
        
        html.Div([
        html.Div([

                    dcc.Graph(id='xyScatterMain')

        ], className="create_container eight columns", id="cross-filter-options"),
            html.Div([
                      dcc.Graph(id='pie_chart_po',
                              config={'displayModeBar': 'hover'}),

                        dcc.Graph(id='pie_chart_utilisation',
                              config={'displayModeBar': 'hover'})
                              ], className="create_container four columns"),

        ], className="row flex-display")

    ], id="mainContainer",
    style={"display": "flex", "flex-direction": "column"})

# Create Dynamic data for the week number.
# This updates the top role of overview values.

# First box, number of data points collected that week
@app.callback(
    Output('TestDataPoints', 'figure'),
    [Input('week_numbers', 'value')])
def update_numDataPts(week_numbers):
    totalDataPts = numDataPoints(df)['Engine Speed'].size/df['WeekNumber'].unique().size
    testDataPoints = df[df['WeekNumber']==week_numbers]
    numDataPts = numDataPoints(testDataPoints)['Engine Speed'].size
    return {
            'data': [go.Indicator(
                    mode='number+delta',
                    value=numDataPts,
                    delta={'reference': totalDataPts,
                              'position': 'bottom',
                              'valueformat': ',',
                              'relative': False,

                              'font': {'size': 16}},
                    number={'valueformat': ',',
                            'font': {'size': 45},

                               },
                    domain={'y': [0, 1], 'x': [0, 1]})],
            'layout': go.Layout(
                title={
                       'y': 1,
                       'x': 0.5,
                       'xanchor': 'center',
                       'yanchor': 'top'},
                font=dict(color='#EC7624',
                size = 30),
                paper_bgcolor='rgb(67, 67, 67)',
                plot_bgcolor='rgb(67, 67, 67)',
                height=61
                ),

            }         

# second box, number of testing hours for that week.
@app.callback(
    Output('TestingHours', 'figure'),
    [Input('week_numbers', 'value')])
def update_numTestingHours(week_numbers):
    AvgEngHours = CalctestDuration(df)/df['WeekNumber'].unique().size
    numHours = CalctestDuration(df[df['WeekNumber']==week_numbers])
    
    return {
            'data': [go.Indicator(
                    mode='number+delta',
                    value=numHours,
                    delta={'reference': AvgEngHours,
                              'position': 'bottom',
                              'valueformat': ',.1f',
                              'relative': False,

                              'font': {'size': 16}},
                    number={'valueformat': ',.1f',
                            'font': {'size': 45},

                               },
                    domain={'y': [0, 1], 'x': [0, 1]})],
            'layout': go.Layout(
                title={
                       'y': 1,
                       'x': 0.5,
                       'xanchor': 'center',
                       'yanchor': 'top'},
                font=dict(color='#EC7624',
                size = 30),
                paper_bgcolor='rgb(67, 67, 67)',
                plot_bgcolor='rgb(67, 67, 67)',
                height=61
                ),

            }  
# Third box, number of testing hours for that week.
@app.callback(
    Output('FuelUsed', 'figure'),
    [Input('week_numbers', 'value')])
def update_FuelConsumed(week_numbers):
    AvgFuelConsumed = CalcFuelUsed(df)/df['WeekNumber'].unique().size
    fuelConsumed = CalcFuelUsed(df[df['WeekNumber']==week_numbers])
    
    return {
            'data': [go.Indicator(
                    mode='number+delta',
                    value=fuelConsumed ,
                    delta={'reference': AvgFuelConsumed,
                              'position': 'bottom',
                              'valueformat': ',.1f',
                              'relative': False,

                              'font': {'size': 16}},
                    number={'valueformat': ',.1f',
                            'font': {'size': 45},

                               },
                    domain={'y': [0, 1], 'x': [0, 1]})],
            'layout': go.Layout(
                title={
                       'y': 1,
                       'x': 0.5,
                       'xanchor': 'center',
                       'yanchor': 'top'},
                font=dict(color='#EC7624',
                size = 30),
                paper_bgcolor='rgb(67, 67, 67)',
                plot_bgcolor='rgb(67, 67, 67)',
                height=61
                ),

            }  

# Fourth box, fuel cost for that week.
@app.callback(
    Output('FuelCost', 'figure'),
    [Input('week_numbers', 'value')])
def update_FuelCost(week_numbers):
    AvgFuelConsumed = CalcFuelUsed(df)/df['WeekNumber'].unique().size
    AvgFuelCost = AvgFuelConsumed*fuel_cost
    fuelConsumed = CalcFuelUsed(df[df['WeekNumber']==week_numbers])
    FuelCost = fuelConsumed*fuel_cost
    return {
            'data': [go.Indicator(
                    mode='number+delta',
                    value=FuelCost ,
                    delta={'reference': AvgFuelCost,
                              'position': 'bottom',
                              'valueformat': ',.1f',
                              'relative': False,

                              'font': {'size': 16}},
                    number={'valueformat': ',.1f',
                            'font': {'size': 45},

                               },
                    domain={'y': [0, 1], 'x': [0, 1]})],
            'layout': go.Layout(
                title={
                       'y': 1,
                       'x': 0.5,
                       'xanchor': 'center',
                       'yanchor': 'top'},
                font=dict(color='#EC7624',
                size = 30),
                paper_bgcolor='rgb(67, 67, 67)',
                plot_bgcolor='rgb(67, 67, 67)',
                height=61
                ),

            } 

# Fifth box, Test Cell Cost for that week.
@app.callback(
    Output('TestingCost', 'figure'),
    [Input('week_numbers', 'value')])
def update_weeklyCost(week_numbers):
    AvgFuelConsumed = CalcFuelUsed(df)/df['WeekNumber'].unique().size
    AvgFuelCost = AvgFuelConsumed*fuel_cost
    AvgWeeklyCost = AvgFuelCost + weekly_cell_cost
    fuelConsumed = CalcFuelUsed(df[df['WeekNumber']==week_numbers])
    FuelCost = fuelConsumed*fuel_cost
    weeklyCost = FuelCost + weekly_cell_cost
    return {
            'data': [go.Indicator(
                    mode='number+delta',
                    value=weeklyCost,
                    delta={'reference': AvgWeeklyCost,
                              'position': 'bottom',
                              'valueformat': ',.1f',
                              'relative': False,

                              'font': {'size': 16}},
                    number={'valueformat': ',.1f',
                            'font': {'size': 45},

                               },
                    domain={'y': [0, 1], 'x': [0, 1]})],
            'layout': go.Layout(
                title={
                       'y': 1,
                       'x': 0.5,
                       'xanchor': 'center',
                       'yanchor': 'top'},
                font=dict(color='#EC7624',
                size = 30),
                paper_bgcolor='rgb(67, 67, 67)',
                plot_bgcolor='rgb(67, 67, 67)',
                height=61
                ),

            } 

# 6th box, Test Cell Utilisation for that week.
@app.callback(
    Output('Utilisation', 'figure'),
    [Input('week_numbers', 'value')])
def update_Utilisation(week_numbers):
    AvgTestingTime = CalctestDuration(df)/df['WeekNumber'].unique().size
    AvgNumDays = workingDays
    AvgUtilisation = (AvgTestingTime / (AvgNumDays*workingHours_daily))*100
    TestingTime = CalctestDuration(df[df['WeekNumber']==week_numbers])
    numDays = workingDays
    testingUtilisation = (TestingTime / (numDays*workingHours_daily))*100
  
    return {
            'data': [go.Indicator(
                    mode='number+delta',
                    value=testingUtilisation,
                    delta={'reference': AvgUtilisation,
                              'position': 'bottom',
                              'valueformat': ',.1f',
                              'relative': False,
                              'font': {'size': 16}},
                    number={'valueformat': ',.1f',
                            'font': {'size': 45},

                               },
                    domain={'y': [0, 1], 'x': [0, 1]})],
            'layout': go.Layout(
                title={
                       'y': 1,
                       'x': 0.5,
                       'xanchor': 'center',
                       'yanchor': 'top'},
                font=dict(color='#EC7624',
                size = 30),
                paper_bgcolor='rgb(67, 67, 67)',
                plot_bgcolor='rgb(67, 67, 67)',
                height=61
                ),

            } 

@app.callback(
    Output('xyScatterMain', 'figure'),
    [Input('week_numbers', 'value')])
def update_graph(week_numbers):
    xyDF = numDataPoints(df[df['WeekNumber']==week_numbers])

    return {
        'data': [go.Scatter(x=xyDF['Engine Speed'],
                    y=xyDF['MEngine'],
                    mode='markers',
                    marker = dict(
                        color='#EC7624',
                        size = 8 ),
                    hovertext=round(xyDF['Engine Speed'],0)
                    )],
        'layout': go.Layout(
             plot_bgcolor='rgb(67, 67, 67)',
             paper_bgcolor='rgb(67, 67, 67)',
            # autosize=True,
             height = 900,
             title={
                'text': 'Averaged Data Points for Week: ' + str(week_numbers),
                'y': 0.93,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
             titlefont={
                        'color': 'white',
                        'size': 20},

                     hovermode='x',
             margin = dict(r = 0),

             xaxis=dict(title='<b>nEngine [RPM]</b>',
                        color='white',
                        showline=True,
                        showgrid=True,
                        range= [500, 9000],
                        showticklabels=True,
                        linecolor='white',
                        linewidth=2,
                        ticks='outside',
                        tickfont=dict(
                            family='McLaren Bespoke',
                            size=12,
                            color='white'
                        )

                ),

             yaxis=dict(title='<b>MEngine [Nm]</b>',
                        color='white',
                        showline=True,
                        showgrid=True,
                        range=[0, 1000],
                        showticklabels=True,
                        linecolor='white',
                        linewidth=2,
                        ticks='outside',
                        tickfont=dict(
                           family='McLaren Bespoke',
                           size=12,
                           color='white'
                        )

                ),
        )
    }

# Create pie chart (total casualties)
@app.callback(Output('pie_chart_po', 'figure'),
              [Input('week_numbers', 'value')])

def update_graph(week_numbers):
    fuelConsumed = CalcFuelUsed(df[df['WeekNumber']==week_numbers])
    FuelCost = fuelConsumed*fuel_cost
    weeklyCost = FuelCost + weekly_cell_cost
    current_spent = weeklyCost

    # if df['WeekNumber'].unique()>1:
    #     # Need to calculate the spent based on previous weeks.
    #     pass
    # else:
    #     current_spent = weeklyCost
    colours = ['rgba(175,177,177,0.5)','#EC7624']
    return {
        'data': [go.Pie(labels=['Total Order Cover', 'Spent'],
                        values=[po_total, current_spent],
                        marker=dict(colors=colours),
                        hoverinfo='label+value+percent',
                        textinfo='label+value',
                        textposition='outside',
                        textfont=dict(size=13),
                        hole=.65,
                        rotation=0
                        # insidetextorientation='radial',


                        )],

        'layout': go.Layout(
            # width=800,
            # height=520,
            plot_bgcolor='#434343',
            paper_bgcolor='#434343',
            hovermode='closest',
            title={
                'text': 'Remaining Coverage for Week: ' + str(week_numbers),
                'y': 0.93,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
            titlefont={
                       'color': 'white',
                       'size': 20},
            legend={
                'orientation': 'h',
                'bgcolor': '#434343',
                'xanchor': 'center', 'x': 0.5, 'y': -0.07},
            font=dict(
                family="McLaren Bespoke",
                size=12,
                color='white')
            ),


        }

# Create pie chart (Cell Running Breakdown)
@app.callback(Output('pie_chart_utilisation', 'figure'),
              [Input('week_numbers', 'value')])

def update_graph(week_numbers):
    breakdownDF = df[df['WeekNumber']==week_numbers]
    weeklyTotal = CalctestDuration(breakdownDF)
    cellLive = ((breakdownDF[breakdownDF['Stage Desc']=='Cell Live'])['Engine Speed'].size*1)/3600
    ASAPConnect = ((breakdownDF[breakdownDF['Stage Desc']=='ASAP Connect'])['Engine Speed'].size*1)/3600
    CANConnect = ((breakdownDF[breakdownDF['Stage Desc']=='CAN Connect'])['Engine Speed'].size*1)/3600
    cellChecks = ((breakdownDF[breakdownDF['Stage Desc']=='Cell Checks'])['Engine Speed'].size*1)/3600

    startingCell = cellLive+ASAPConnect+cellChecks+CANConnect

    IgnitionOn = ((breakdownDF[breakdownDF['Stage Desc']=='Ignition On'])['Engine Speed'].size*1)/3600

    EngineStart1 = ((breakdownDF[breakdownDF['Stage Desc']=='Engine Start 1'])['Engine Speed'].size*1)/3600
    EngineStart2 = ((breakdownDF[breakdownDF['Stage Desc']=='Engine Start 2'])['Engine Speed'].size*1)/3600
    EngineWarm1 = ((breakdownDF[breakdownDF['Stage Desc']=='Engine Warm 1'])['Engine Speed'].size*1)/3600
    EngineWarm2 = ((breakdownDF[breakdownDF['Stage Desc']=='Engine Warm 2'])['Engine Speed'].size*1)/3600

    EngineWarmUp = EngineStart1+EngineStart2+EngineWarm1+EngineWarm2
    engineRunning = ((breakdownDF[breakdownDF['Stage Desc']=='Manual Running'])['Engine Speed'].size*1)/3600
    engineLogging = ((breakdownDF[breakdownDF['Stage Desc']=='15 Second Avg Log'])['Engine Speed'].size*1)/3600

    NoRunning = workingHours_week - weeklyTotal

    colours = ['rgba(255,212,0,0.65)', 'rgba(000,000,000,0.65)', 'rgba(6,167,224,0.65)',  '#EC7624',  'rgba(0,86,126,0.65)', 'rgba(175,177,177,0.5)' ]
    return {
        'data': [go.Pie(labels=['Starting Cell', 'Ign On (No Running)', 'Engine WarmUp', 'Engine Running', '15[s] Log', 'No Running'],
                        values=[ startingCell, IgnitionOn, EngineWarmUp,  engineRunning, engineLogging, NoRunning],
                        marker=dict(colors=colours),
                        hoverinfo='label+value+percent',
                        textinfo='label+percent',
                        textposition = 'outside',
                        textfont=dict(size=13),
                        hole=.65,
                        rotation=145
                        # insidetextorientation='radial',


                        )],

        'layout': go.Layout(
            # width=800,
            # height=520,
            plot_bgcolor='#434343',
            paper_bgcolor='#434343',
            hovermode='closest',
            title={
                'text': 'Dyno Breakdown for Week: ' + str(week_numbers),
                'y': 0.93,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
            titlefont={
                       'color': 'white',
                       'size': 20},
            legend={
                'orientation': 'h',
                'bgcolor': '#434343',
                'xanchor': 'center', 'x': 0.5, 'y': -0.07},
            font=dict(
                family="McLaren Bespoke",
                size=12,
                color='white')
            ),


        }

if __name__ == '__main__':
    app.run_server(debug=True)