# -*- coding: utf-8 -*-
"""
DATA 608 - Assignment 4 - Dash

Created on Mon Mar 22 18:48:46 2021

@author: C.Rosemond
"""
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
from dash.dependencies import Input, Output
#import plotly.express as px
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

available_species = ['black walnut', 'spruce', 'tulip-poplar', 'trident maple',
       'Virginia pine', 'littleleaf linden', 'sugar maple',
       'golden raintree', 'sweetgum', 'sycamore maple', 'ginkgo',
       'Siberian elm', "'Schubert' chokecherry", 'Osage-orange',
       'hawthorn', "Schumard's oak", 'white oak', 'Japanese tree lilac',
       'London planetree', 'two-winged silverbell', 'blackgum',
       'Japanese snowbell', 'white pine', 'mimosa', 'Ohio buckeye',
       'eastern cottonwood', 'silver maple', 'bur oak', 'pine',
       'Chinese elm', 'tree of heaven', 'silver birch', 'Scots pine',
       'common hackberry', 'black maple', 'Douglas-fir',
       'Himalayan cedar', 'horse chestnut', 'Sophora', 'Amur cork tree',
       'river birch', 'cockspur hawthorn', 'ash', 'crab apple',
       'black locust', 'Shantung maple', 'black cherry', 'quaking aspen',
       'red pine', 'serviceberry', 'eastern redcedar', 'pin oak',
       'Japanese zelkova', 'Kentucky yellowwood', 'northern red oak',
       'honeylocust', 'Cornelian cherry', 'Norway maple', 'scarlet oak',
       'pitch pine', 'bigtooth aspen', 'arborvitae', 'paper birch',
       'crepe myrtle', 'Chinese tree lilac', 'cherry', 'bald cypress',
       'English oak', 'black oak', 'flowering dogwood', 'American larch',
       'Atlas cedar', 'maple', 'silver linden', 'Japanese maple',
       'eastern hemlock', 'eastern redbud', 'shingle oak', 'Callery pear',
       'Chinese fringetree', 'Atlantic white cedar', 'red maple',
       'Kentucky coffeetree', 'black pine', 'kousa dogwood', 'white ash',
       'tartar maple', 'magnolia', 'Oklahoma redbud', 'boxelder',
       'American hornbeam', 'katsura tree', 'mulberry', 'sassafras',
       'green ash', 'pagoda dogwood', 'European alder', 'blue spruce',
       'southern red oak', 'holly', 'swamp white oak', 'false cypress',
       'Amur maackia', 'Norway spruce', 'Turkish hazelnut',
       'American elm', 'American linden', 'dawn redwood', 'smoketree',
       'empress tree', 'weeping willow', 'red horse chestnut',
       'pond cypress', 'Amur maple', 'European hornbeam',
       'Japanese hornbeam', 'European beech', 'pignut hickory',
       'American hophornbeam', 'southern magnolia', 'paperbark maple',
       'hardy rubber tree', 'American beech', 'Chinese chestnut',
       'cucumber magnolia', 'catalpa', 'Persian ironwood',
       'crimson king maple', 'purple-leaf plum', 'sawtooth oak',
       'willow oak', 'hedge maple']

app.layout = html.Div([
    html.Div(children=[
        html.H2(children='Tree Health Status, NYC 2015'),

        html.Div(children='''
        Data source: 2015 Street Tree Census - Tree Data, City of New York Department of Parks and Recreation
        ''')
    ]),
    html.Div([
            dcc.Dropdown(
                id='boro',
                options=[{'label': i, 'value': i} for i in ['Bronx','Brooklyn','Manhattan','Staten Island','Queens']],
                value='borough'
            ),            
            dcc.Dropdown(
                id='species',
                options=[{'label': i, 'value': i} for i in available_species],
                value='species')     
    ], style={'width': '50%'}),
    html.Div([
        html.Div(children='''
        Proportion of trees by health status         
                 ''')
    ]),
    dt.DataTable(id='table1',
                columns=[
                    {'name': 'Tree health', 'id': 'health'},
                    {'name': 'Number of trees', 'id': 'count_tree_id'},
                    {'name': 'Proportion', 'id': 'proportion1'}],
                style_as_list_view=True,
                style_cell={'padding': '5px'},
                style_header={
                    'backgroundColor': 'white',
                    'fontWeight': 'bold'}
                ),
    html.Div([
        html.Div(children='''
        Proportion of trees by level of stewardship, by health status       
        ''')    
    ]),
    dt.DataTable(id='table2',
                columns=[
                    {'name': 'Tree health', 'id': 'health'},
                    {'name': 'Level of stewardship', 'id': 'steward'},
                    {'name': 'Number of trees', 'id': 'count_tree_id'},
                    {'name': 'Proportion of health group', 'id': 'proportion2'}],
                style_as_list_view=True,
                style_cell={'padding': '5px'},
                style_header={
                    'backgroundColor': 'white',
                    'fontWeight': 'bold'}
                ),        
    ])

@app.callback(
    Output('table1', 'data'),
    Input('boro', 'value'),
    Input('species', 'value'))
def soql_pull1(boro,species):
    soql_url = ('https://data.cityofnewyork.us/resource/nwxe-4ae8.json?' +\
        '$select=health,count(tree_id)' +\
        '&$where=spc_common=\'' + species + '\'' + '&boroname=\'' + boro + '\'' +\
        '&$group=health' +\
        '&$order=health').replace(' ', '%20')
    pull = pd.read_json(soql_url)
    pull['proportion1'] = round((pull['count_tree_id'] / pull['count_tree_id'].sum())*100,1)
    return pull.to_dict(orient = 'records')


@app.callback(
    Output('table2', 'data'),
    Input('boro', 'value'),
    Input('species', 'value'))
def soql_pull2(boro,species):
    soql_url = ('https://data.cityofnewyork.us/resource/nwxe-4ae8.json?' +\
        '$select=health,steward,count(tree_id)' +\
        '&$where=spc_common=\'' + species + '\'' + '&boroname=\'' + boro + '\'' +\
        '&$group=health,steward' +\
        '&$order=health,steward').replace(' ', '%20')
    pull = pd.read_json(soql_url)
    pull['proportion2'] = round((pull['count_tree_id'] / pull.groupby('health')['count_tree_id'].transform('sum'))*100,1)
    return pull.to_dict(orient = 'records')

if __name__ == '__main__':
    app.run_server(debug=True)
