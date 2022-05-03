import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import plotly.express as px
from dash import no_update

app = dash.Dash(__name__)

# REVIEW1: Clear the layout and do not display exception till callback gets executed
app.config.suppress_callback_exceptions = True

# Read the automobiles data into pandas dataframe
auto_data =  pd.read_csv('automobileEDA.csv', 
                            encoding = "ISO-8859-1",
                            )
auto_data.rename(columns={'drive-wheels':'drive_wheels' , 'body-style':'body_style'}, inplace=True)

drives = list(auto_data.drive_wheels.unique())
options_ = []
for m in drives:
    options_.append({'label': m, 'value': m})

# bar
all_fig = px.bar(auto_data, x="body_style", y="price", color='drive_wheels', title='Price of different body styles and drive wheels', barmode="group") 

#Layout Section of Dash

app.layout = html.Div(children=[#TASK 3A
    html.H1(
        children='Automobile Prices',
        style={
            'textAlign': 'center'
        }
    ),

     #outer division starts
     html.Div([
                   # First inner divsion for  adding dropdown helper text for Selected Drive wheels
                    html.Div(
                            #TASK 3B
                            dcc.Dropdown(id='demo-dropdown',
                            options= options_,
                            value='4wd' # Providing a vallue to dropdown
                        ),

                     ),


                    #TASK 3C

                    #Second Inner division for adding 2 inner divisions for 2 output graphs 
                    html.Div([
                        #TASK 3D
                        html.Div([ ], id='bar-plot'),
                        html.Div([ ], id='pie-plot')
                    ], style={'display': 'flex'}),

                    # all drive wheels
                    # Bar graph
                    dcc.Graph(id='all-vehicles',figure=all_fig)

#
    ])
    #outer division ends

])
#layout ends

#Place to add @app.callback Decorator
#TASK 3E
@app.callback([Output(component_id='pie-plot', component_property='children'),
               Output(component_id='bar-plot', component_property='children')],
               Input(component_id='demo-dropdown', component_property='value'))

#Place to define the callback function .
#TASK 3F
#Place to define the callback function .
def display_selected_drive_charts(value):

   filtered_df = auto_data[auto_data['drive_wheels']==value].groupby(['drive_wheels','body_style'],as_index=False). \
            mean()
        
   filtered_df = filtered_df
   
   fig1 = px.pie(filtered_df, values='price', names='body_style', title="Pie Chart")
   fig2 = px.bar(filtered_df, x='body_style', y='price', title='Bar Chart')
    
   return [dcc.Graph(figure=fig1),
            dcc.Graph(figure=fig2) ]



if __name__ == '__main__':
    app.run_server(debug=True)