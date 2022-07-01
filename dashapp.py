#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 13 12:47:50 2022

@author: Kartik
"""

import pickle
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

model = pickle.load(open('predict_interest_rate.pkl','rb'))

app = dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

app.layout = html.Div(
    children = [
        html.H1('Enter the details to predict the type of interest rate that will be applied on you',
                style = {
                    'textAlign':'center',
			  'color': '#7fDBFF'
                    }
                ),
        html.Hr(),
        html.P('Loan_Amount_Requested'),
        dcc.Input(id='Loan_Amount_Requested', type='text', placeholder='Loan_Amount_Requested'),
        html.Hr(),
        html.P('Home_Owner'),
        dcc.Input(id='Home_Owner', type='text', placeholder='Home_Owner'),
        html.Hr(),
        html.P('Income_Verified'),
        dcc.Input(id='Income_Verified', type='text', placeholder='Income_Verified'),
        html.Hr(),
        #html.P('Purpose_Of_Loan'),
        #dcc.Input(id='Purpose_Of_Loan', type='text', placeholder='Purpose_Of_Loan'),
        #html.Hr(),
        html.P('Debt'),
        dcc.Input(id='Debt', type='text', placeholder='Debt'),
        html.Hr(),
        html.P('Inquiries_Last_6Mo'),
        dcc.Input(id='Inquiries_Last_6Mo', type='text', placeholder='Inquiries_Last_6Mo'),
        html.Hr(),
        html.P('Number_Open_Accounts'),
        dcc.Input(id='Number_Open_Accounts', type='text', placeholder='Number_Open_Accounts'),
        html.Hr(),
        html.P('Total_Accounts'),
        dcc.Input(id='Total_Accounts', type='text', placeholder='Total_Accounts'),
        html.Hr(),
        html.P('Annual_Income'),
        dcc.Input(id='Annual_Income', type='text', placeholder='Annual_Income'),
        html.Hr(),
        html.P('Length_Employed'),
        dcc.Input(id='Length_Employed', type='text', placeholder='Length_Employed'),
        html.Hr(),
        html.Button("Get Interest", id = 'get_interest', n_clicks=0),
        html.Hr(),
        html.Br(),
        html.P(id='model_output', style = {
            'textAlign': 'center',
		'color': '#7fDBFF'
            })
        ])

@app.callback(
    Output(component_id='model_output', component_property='children'),
    Input(component_id='Loan_Amount_Requested', component_property='value'),
    Input(component_id='Home_Owner', component_property='value'),
    Input(component_id='Income_Verified', component_property='value'),
    #Input(component_id='Purpose_Of_Loan', component_property='value'),
    Input(component_id='Debt', component_property='value'),
    Input(component_id='Inquiries_Last_6Mo', component_property='value'),
    Input(component_id='Number_Open_Accounts', component_property='value'),
    Input(component_id='Total_Accounts', component_property='value'),
    Input(component_id='Annual_Income', component_property='value'),
    Input(component_id='Length_Employed', component_property='value'),
    Input(component_id='get_interest', component_property='n_clicks')
    )

Purpose_Of_Loan = 2

def get_interest(Loan_Amount_Requested, Home_Owner, Income_Verified, Purpose_Of_Loan, Debt, Inquiries_Last_6Mo, Number_Open_Accounts, Total_Accounts, Annual_Income, Length_Employed, get_interest):
    if get_interest>0:
        if None in [Loan_Amount_Requested, Home_Owner, Income_Verified, Purpose_Of_Loan, Debt, Inquiries_Last_6Mo, Number_Open_Accounts, Total_Accounts, Annual_Income, Length_Employed, get_interest]:
            return 'Please add all the values'
        Loan_Amount_Requested = float(Loan_Amount_Requested)
        Home_Owner = int(Home_Owner)
        Income_Verified = int(Income_Verified)
        Purpose_Of_Loan = int(Purpose_Of_Loan)
        Debt = float(Debt)
        Inquiries_Last_6Mo = int(Inquiries_Last_6Mo)
        Number_Open_Accounts = int(Number_Open_Accounts)
        Total_Accounts = int(Total_Accounts)
        Annual_Income = float(Annual_Income)
        Length_Employed = int(Length_Employed)
        
        #if Loan_Amount_Requested<0:
         #   Loan_Amount_Requested = 0
        Asset_Score = Total_Accounts + Income_Verified*2 + Home_Owner*3
        Savings = 0.2*(Annual_Income*Length_Employed)
        Debt_To_Income = Debt/Annual_Income
        Income_By_Loan = Annual_Income/(Loan_Amount_Requested * 12)
        
        array = [[Loan_Amount_Requested, Home_Owner, Income_Verified, Purpose_Of_Loan, Debt_To_Income, Inquiries_Last_6Mo, Number_Open_Accounts, Total_Accounts, Annual_Income, Length_Employed, Debt, Asset_Score, Savings, Income_By_Loan]]
        rate = model.predict(array)[0]
        
        a = ''
	    if rate == 0:
        	a = 'Low Range'
        if rate == 1:
        	a = 'Mid Range'
        if rate == 2:
        	a = 'High Range'
        
        return (Interest Rate will be of {}).format(a)
    

if __name__=='__main__':
    PORT = 3000
    app.run_server(port = PORT)
