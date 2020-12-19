import dash
import dash_core_components as dcc
import dash_html_components as html
import mysql.connector
from mysql.connector import Error
import dash_bootstrap_components as dbc
from dash import no_update
from flask import session, copy_current_request_context
from datetime import datetime
import plotly
import plotly.express as px
from plotly import graph_objects
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from dash.dependencies import Input, Output, State, MATCH, ALL
import mysql.connector
import urllib.request
import json 
from dateutil import parser
import dash_table
import yfinance as yf

welcome_msg = ''
custid = ''
account_numbers_list = []
stock_list = []

app = dash.Dash(__name__, suppress_callback_exceptions=True,  external_stylesheets=[dbc.themes.BOOTSTRAP])

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

tabs_styles = {
    'height': '44px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    #'fontWeight': 'bold',
    'align-items': 'center',
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white',
    'padding': '6px'
}


try:
    connection = mysql.connector.connect(host='localhost',
                                         database='BankingDBProject',
                                         user='root',
                                         password='Katniss$11',
                                         auth_plugin = 'mysql_native_password',)
    
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = connection.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)
        cursor.close()

except Error as e:
    print("Error while connecting to MySQL", e)

def login_layout():
    return html.Div([
        dcc.Location(id='login-url',pathname='/login',refresh=False),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
            dbc.Container(
                [
                    dbc.Row(
                        dbc.Col(
                            dbc.Card(
                                [
                                    html.Div([
                                    dcc.Tabs(id="main_tab", value='mtab-1', vertical = False, children=[
                                    dcc.Tab(id = 'admin_tab', value = 'mtab_id_1', style=tab_style, selected_style=tab_selected_style, label='Admin Use Only', children =[
                                    html.Br(),
                                    html.Br(),
                                    #html.H2('Create New Account',className='card-title'),
                                    dbc.Button('Create New Account',id='new_account',color='primary',block=True, n_clicks=0,),
                                    html.Br(),
                                    html.Br(),
                                    #html.H2('Account Admin Works',className='card-title'),
                                    dbc.Button('Existing Account Admin Works',id='existing_account',color='primary',block=True, n_clicks=0,),
                                    html.Br(),
                                    html.Br(),]), # Tab1 close
                                    dcc.Tab(id = 'user_tab', value = 'mtab_id_2', style=tab_style, selected_style=tab_selected_style, label='Account Holders', children =[
                                    html.Br(),
                                    html.Br(),
                                    html.H2('Login',className='card-title'),
                                    dbc.Input(id='login_input-1-state',placeholder='Enter CustomerID'),
                                    html.Br(),
                                    dbc.Input(id='login_input-2-state',placeholder='Enter Password', type='password'),
                                    html.Br(),
                                    html.Br(),
                                    dbc.Button('Submit',id='submit-button-state',color='success',block=True, n_clicks=0,),
                                    html.Br(),
                                    html.Span(id='container-button-timestamp1', style={"vertical-align": "middle", 'width': '49%', 'display': 'inline-block', 'color': 'blue', 'font-style': 'bold', 'font-size': '20', 'font-weight': 'bold'}),
                                    html.Div(id='output-state',),
                                    html.Br(),
                                    html.Br(), ]),]),])
                                ],
                                body=True
                            ),
                            width=6
                        ),
                        justify='center'
                    )
                ]
            )  
    ])
def admin():
    return html.Div([
        dcc.Location(id='admin-url',pathname='/admin'),
        dbc.Container(
            [
                dbc.Row(
                    dbc.Col(
                        [
                            html.Div([
                                html.Br(),
                                html.Br(),
                                dcc.Tabs(id="admin_tab", value='atab-1', vertical = False, children=[
                                dcc.Tab(id = 'Delete Customer', value = 'atab_id_1', style=tab_style, selected_style=tab_selected_style, label='Delete Customer', children =[
                                    html.Br(),
                                    html.Br(),
                                    dbc.Input(id='adminbutton1',placeholder='Enter Customer', type='number'),
                                    html.Br(),
                                    html.Br(),
                                    dbc.Button('Delete Customer',id='delete_customer',color='warning',block=True, n_clicks=0,),
                                    dbc.Modal(
                                    [
                                        dbc.ModalHeader("Alert"),
                                        dbc.ModalBody("Are you sure to remove customer?"),
                                        dbc.ModalFooter(
                                            dbc.Button("Yes", id="yes_customers", className="ml-auto")
                                        ),
                                    ],
                                    id="modal1",
                                    ),
                                    html.Br(),
                                    html.Div(id='admin_message1',),
                                    html.Br(),
                                    html.Br(),
                                    ]), # Tab 1
                                dcc.Tab(id = 'Delete Account', value = 'atab_id_2', style=tab_style, selected_style=tab_selected_style, label='Delete Account', children =[
                                    html.Br(),
                                    html.Br(),
                                    dbc.Input(id='adminbutton2',placeholder='Enter Customer', type='number'),
                                    html.Br(),
                                    dbc.Input(id='adminbutton3',placeholder='Enter Account', type='number'),
                                    html.Br(),
                                    html.Br(),
                                    dbc.Button('Delete Account',id='close_account',color='warning',block=True, n_clicks=0,),
                                    dbc.Modal(
                                    [
                                        dbc.ModalHeader("Alert"),
                                        dbc.ModalBody("Are you sure to remove account?"),
                                        dbc.ModalFooter(
                                            dbc.Button("Yes", id="yes_accounts", className="ml-auto")
                                        ),
                                    ],
                                    id="modal2",
                                    ),
                                    html.Br(),
                                    html.Div(id='admin_message2',),
                                    html.Br(),
                                    html.Br(),
                                    ]), #Tab 2
                                ]),  
                            html.Br(),
                            html.A(dbc.Button('Back to Login Page',id='loginpage-button-state',outline = True, color='info',block=True, n_clicks=0,), href='/login'),
                            html.Br(),
                             ]),
                        ],
                     width=6,),
                    justify='center',
                ),
            ],
        ),
    ])   

def app_layout(user):
    return html.Div([
        dcc.Location(id='home-url',pathname='/home'),
        html.H1(
        children='BANKING WEBSITE',
        style={
            'textAlign': 'center',
        }
    ),
    html.Div(children='Welcome User !', style={
        'textAlign': 'center',
    }),
    html.Div([html.A(dbc.Button('Logout', id='btn-nclicks-13',  className="mr-1", n_clicks=0, color = 'dark',), href='/login'),], style = {'width': '10%', 'float': 'right',}),
    html.Div(children=[
        html.Div([
            dcc.Tabs(id="tabs-styled-with-inline", value='tab-1', vertical = False, children=[
            dcc.Tab(id = 'tab_id_1', value = 'tab_id_1', style=tab_style, selected_style=tab_selected_style, label='Account Details', children =[
                html.Div(children=[
                    html.Div([
                        html.Br(),
                        dbc.Button('Show Account Details', id='show_tab1', size = 'sm', className="mr-1", outline = True, n_clicks=0, color = 'primary'),
                        html.Br(),
                        html.Br(),
                        html.Div(id = 'display_accountid',),
                        html.Br(),
                        html.Div(id = 'display_accountbalance',),
                        html.Br(),
                        dbc.Alert('Transaction Activity Details', color="secondary"),
                        html.Div(id = 'tab1_transaction_history',),
                        html.Br(),
                        dbc.Alert('Stock Activity Details', color="secondary"),
                        html.Div(id = 'tab1_stock_history',),
                        html.Br(),
                        
                ], style = {'width': '50%', 'float': 'center',}),
                ]),
                ]), # Tab 1 tab & children
                dcc.Tab(id = 'tab_id_2',value = 'tab_id_2', style=tab_style, selected_style=tab_selected_style, label='Transfer Money', children =[
                html.Div(children=[
                    html.Div([
                    html.Br(),
                    html.Br(),
                    dbc.Input(id='tinput-1-state',placeholder='Enter Beneficiary Account Number', type="number",),
                    html.Br(),
                    dbc.Input(id='tinput-2-state',placeholder='Enter Transfer Amount',type="float",),
                    html.Br(),
                    dbc.Input(id='tinput-3-state',placeholder='Enter Reason',),
                    html.Br(),
                    dbc.Button('Click to Transfer Money', id='btn-nclicks-10',  className="mr-1", n_clicks=0, color = 'primary'),
                    dbc.Button('Reset', id='reset_transfer_money',  outline=True, className="mr-1", n_clicks=0, color = 'primary'),
                    html.Br(),
                    html.Div(id='output-state5',),
                    html.Br(),
                ], style = {'width': '30%', 'float': 'left',}),
                ]),
                ]), # Tab 2 tab & children
                dcc.Tab(id = 'tab_id_3', value = 'tab_id_3', style=tab_style, selected_style=tab_selected_style, label='Add Beneficiary', children =[
                    html.Div(children=[
                        html.Br(),
                        dbc.Input(id='input-1-states',placeholder='Enter Beneficiary Account Number'),
                        html.Br(),
                        dbc.Input(id='input-2-states',placeholder='Enter Transit Number',type="number",),
                        html.Br(),
                        dbc.Input(id='input-3-states',placeholder='Enter Routing Number',type="number",),
                        html.Br(),
                        html.Br(),
                        dbc.Button('Add Beneficiary', id='btn-nclicks-4', className="mr-1", n_clicks=0, color = 'primary'),
                        dbc.Button('Reset Beneficiary', id='btn-nclicks-17', className="mr-1", outline = True,  n_clicks=0, color = 'info'),
                        html.Br(),
                        html.Div(id='output-state2',),
                        html.Br(),
                        html.Br(),
                ], style = {'width': '30%', 'float': 'left',}),
                ]), # Tab 4 tab & children
                dcc.Tab(id = 'tab_id_5',value = 'tab_id_5', style=tab_style, selected_style=tab_selected_style, label='Trading', children =[
                    html.Div([
                    html.Div([
                        html.Br(),
                        dbc.Button('Show WatchList', id='btn-nclicks-6',  className="mr-1", n_clicks=0, color = 'primary'),
                        html.Br(),
                        html.Div(id='dynamic-dropdown-container', children=[]),
                        html.Br(),
                        html.Br(),
                        html.Div(id='stock_graph', children=[]),
                        html.Br(),
                        ], style = {'width': '40%', 'float': 'right',}),
                    html.Div([
                        html.Br(),
                        dbc.Input(id='input-1-state',placeholder='Enter Stock Code to add/remove to WatchList:'),
                        html.Br(),
                        dbc.Button('Add Stock Code', id='btn-nclicks-5',  className="mr-1", n_clicks=0, color = 'primary'),
                        dbc.Button('Remove Stock Code', id='remove_stockcode',  className="mr-1", n_clicks=0, color = 'info'),
                        html.Br(),
                        html.Div(id='display_stock_addition_status',),
                        html.Br(),
                        dbc.Input(id='input-2-state',placeholder='Enter Stock Code:'),
                        html.Br(),
                        dbc.Input(id='input-3-state',placeholder='Enter Stock Quantity:', type = 'number'),
                        html.Br(),
                        dbc.Input(id='input-4-state',placeholder='Enter Stock Biding Price:', type = 'number'),
                        html.Br(),
                        dbc.Button('Buy Stocks', id='btn-nclicks-7', className="mr-1", n_clicks=0, color = 'success'),
                        dbc.Button('Sell Stocks', id='btn-nclicks-8', className="mr-1", n_clicks=0, color = 'warning'),
                        dbc.Button('Reset', id='btn-nclicks-15', className="mr-1", outline = True,  n_clicks=0, color = 'info'),
                        html.Br(),
                        html.Div(id='display_stocktrade_status',),
                        html.Br(),
                        ], style = {'width': '48%', 'float': 'left',}),
                    ]),
                ]), # Tab 6 tab & children
            ]), # Tabs dcc
        ]), #html Div before Tabs
        ]),

    ])

def account_creation():
    return html.Div([
        dcc.Location(id='account_creation-url',pathname='/account_creation'),
        dbc.Container(
            [
                dbc.Row(
                    dbc.Col(
                        [
                            html.H2('Account Creation Form'),
                            dbc.Input(id='ainput-1-state',placeholder='Enter FirstName'),
                            html.Br(),
                            dbc.Input(id='ainput-2-state',placeholder='Enter LastName'),
                            html.Br(),
                            dbc.Input(id='ainput-3-state',placeholder='Enter SIN'),
                            html.Br(),
                            dbc.Input(id='ainput-4-state',placeholder='Enter Email'),
                            html.Br(),
                            dbc.Input(id='ainput-5-state',placeholder='Enter ContactNumber'),
                            html.Br(),
                            dbc.Input(id='ainput-6-state',placeholder='Enter Address'),
                            html.Br(),
                            dbc.Input(id='ainput-7-state',placeholder='Enter Password for Account', type='password'),
                            html.Br(),
                            dcc.Checklist(id='account_type',
                            options=[
                                {'label': ' Savings Account', 'value': 'SAV'},
                                {'label': ' Checkings Account', 'value': 'CHK'},
                            ],labelStyle = dict(display='block'),
                            ),
                            html.Br(),
                            dbc.Button('Submit',id='submit-button-state1',color='success',block=True, n_clicks=0,),
                            dbc.Button('Reset',id='reset-button-state',outline = True, color='success',block=True, n_clicks=0,),
                            html.Br(),
                            html.A(dbc.Button('Login Page',id='loginpage-button-state',outline = True, color='info',block=True, n_clicks=0,), href='/login'),
                            html.Br(),
                            html.Div(id='output-state1',),
                            html.Br(),
                            html.Br(),
                        ],
                     width=6,),
                    justify='center',
                ),
            ],
        ),
    ])

app.layout = html.Div([
    dcc.Location(id='url',refresh=False),
    html.Div(id='intermediate-value', style={'display': 'none'}),
    html.Div(login_layout(),id='page-content'),
    ])

@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname'),dash.dependencies.Input('output-state', 'children'),])

def router(url, user):
    if url =='/home':
        return app_layout(user)
    elif url =='/login':
        return login_layout()
    elif url == '/account_creation':
        return account_creation()
    elif url == '/admin':
        return admin()
    else:
        return login_layout()

@app.callback([ Output('output-state', 'children'), Output('url','pathname'), Output('intermediate-value','children'),],
              [Input('submit-button-state', 'n_clicks'), 
              Input('new_account', 'n_clicks'),
              Input('existing_account', 'n_clicks'),],
              [State('login_input-1-state', 'value'),
               State('login_input-2-state', 'value')])

def update_output(n_clicks, n_clicks1, n_clicks2, input1, input2):    
    if n_clicks == 1:
        cursor = connection.cursor()
        cursor.execute('SELECT CustomerID FROM CustomerDetails WHERE CustomerID = %s AND Password = %s', (input1, input2))
        
        records = cursor.fetchall()

        if cursor.rowcount == 1:
            msg = '{} Login Successful'.format(records)
            listToStr = ' '.join([str(elem) for elem in records])
            user = listToStr.replace('(', '')
            user = user.replace(',)', '')
            #print(user)
            welcome_msg = 'Hello {} !'.format(user)

            #print(welcome_msg)
            return '', '/home', user
        else:
            msg = 'Login Failed'
            return msg, '/login', ''
    elif n_clicks1 == 1:
        return '', '/account_creation',''

    elif n_clicks2 == 1:
        return '', '/admin',''

    else:
        return '', '/login', ''

@app.callback(Output('output-state1', 'children'),
              [Input('submit-button-state1', 'n_clicks'),
              Input('ainput-1-state', 'value'),
               Input('ainput-2-state', 'value'),
               Input('ainput-3-state', 'value'),
               Input('ainput-4-state', 'value'),
               Input('ainput-5-state', 'value'),
               Input('ainput-6-state', 'value'),
               Input('ainput-7-state', 'value'),Input('account_type', 'value'),],)

def insert_account(n_clicks, input1, input2, input3, input4, input5, input6, input7, account_type):
    if n_clicks == 1:
        cursor = connection.cursor()
        currdatetime = datetime.now()
        dt_string = currdatetime.strftime("%Y-%m-%d %H:%M:%S")
        
        cursor.execute('INSERT into CustomerDetails (Password, SIN, FirstName, LastName, Address, Email, ContactNumber,  CreatedDate) values (%s, %s, %s, %s, %s, %s, %s, %s);', (input7, input3, input1, input2, input6, input4, input5,  dt_string))
        connection.commit()

        cursor.execute('SELECT CustomerID from CustomerDetails where CreatedDate = %s and SIN = %s', (dt_string, input3))

        newCustomerID = cursor.fetchone()
        newCustomerID = ' '.join([str(elem) for elem in newCustomerID])
        newCustomerID = newCustomerID.replace('(', '')
        newCustomerID = newCustomerID.replace(',)', '')
        account_type = ' '.join([str(elem) for elem in account_type])

        cursor.close()
        cursor1 = connection.cursor()
        cursor1.execute('INSERT into AccountDetails (AccountType, AccountStatus, AccountBalance, TransactionLimit, OpenDate ) values (%s, %s, %s, %s, %s);', (account_type, 'Active', '50000', '2000', dt_string))
        connection.commit()

        print(dt_string, account_type)
        cursor1.execute('SELECT AccountNumber from AccountDetails where OpenDate = %s and AccountType = %s;', (dt_string, account_type))

        newAccountID = cursor1.fetchone()
        cursor1.close()
        
        newAccountID = ' '.join([str(elem) for elem in newAccountID])
        newAccountID = newAccountID.replace('(', '')
        newAccountID = newAccountID.replace(',)', '')
        
        cursor2 = connection.cursor()
        cursor2.execute('INSERT into CustomerAccounts (CustomerID, AccountNumber, AccountStatus) values (%s, %s, %s);', (newCustomerID, newAccountID, 'Active'))
        connection.commit()
        cursor2.close()

        msg = dbc.Alert('Account created successfully! Your CustomerID is {} and your AccountNumber is {}'.format(newCustomerID, newAccountID), color="success" )
        print(msg)
        return msg
    else:
        return ''

@app.callback(Output('output-state2', 'children'),
              [Input('btn-nclicks-4', 'n_clicks'), 
              Input('intermediate-value', 'children'), 
              Input('input-1-states', 'value'),
              Input('input-2-states', 'value'),
               Input('input-3-states', 'value'),],
              )

def add_beneficiary(n_clicks, custid, beneficiary_account, transitnumber, routingnumber):    

    if n_clicks == 1:

        cursor = connection.cursor(buffered=True) 
        cursor.execute('SELECT AccountNumber FROM BankingDBProject.CustomerAccounts WHERE CustomerID = %s;', (custid,))
        accountid = cursor.fetchone()
        i = ' '.join([str(elem) for elem in accountid])
        i = i.replace('(', '')
        i = i.replace(',)', '')
        accountnumber = int(i)
        cursor.close()

        cursor1 = connection.cursor(buffered=True) 
        cursor1.execute('SELECT CustomerID FROM BankingDBProject.CustomerAccounts WHERE AccountNumber = %s;', (beneficiary_account,))

        if cursor1.rowcount != 0:

            cursor = connection.cursor(buffered=True) 
            cursor.execute('SELECT BeneficiaryID from BankingDBProject.BeneficiaryDetails where AccountNumber = %s and BeneficiaryAccount = %s;', (accountnumber, beneficiary_account))
            
            if cursor.rowcount != 0:
                msg = dbc.Alert('Beneficiary already exists!', color = 'warning')
                cursor.close()
            elif cursor.rowcount == 0:
                
                cursor.close()
                cursor1.close()

                cursor1 = connection.cursor(buffered=True) 

                if transitnumber == 1239999 and routingnumber == 9999123:
                    BeneficiaryType = 'INT'

                    cursor1.execute('INSERT into BankingDBProject.BeneficiaryDetails (BeneficiaryType, AccountNumber, RoutingNumber,TransitNumber, BeneficiaryAccount) values (%s, %s, %s, %s, %s);', (BeneficiaryType, accountnumber, routingnumber, transitnumber, beneficiary_account))
                    connection.commit()
                    cursor1.close()
                    msg = dbc.Alert('Beneficiary Added Successfully!', color = 'success')

                elif (transitnumber in range(2300000, 3000000)) and (routingnumber in range(3300000, 4300000)):
                    BeneficiaryType = 'EXT'
                    cursor1.execute('INSERT into BankingDBProject.BeneficiaryDetails (BeneficiaryType, AccountNumber, RoutingNumber,TransitNumber, BeneficiaryAccount) values (%s, %s, %s, %s, %s);', (BeneficiaryType, accountnumber, routingnumber, transitnumber, beneficiary_account))
                    connection.commit()
                    cursor1.close()
                    msg = dbc.Alert('Beneficiary Added Successfully!', color = 'success')

                
                else:
                    msg = dbc.Alert('Invalid External Account Details!', color = 'danger')

        else:
            msg = dbc.Alert('Invalid Account Details!', color = 'danger')

        return msg

    else:
        return ''


@app.callback(Output('display_stock_addition_status', 'children'),
            [Input('btn-nclicks-5', 'n_clicks'), 
            Input('remove_stockcode', 'n_clicks'), 
            Input('input-1-state', 'value'),
              Input('intermediate-value', 'children')],)

def display_stock_addition_status(n_clicks, n_clicks1, input1, custid):

    cursor = connection.cursor(buffered=True) 
    cursor.execute('SELECT AccountNumber FROM BankingDBProject.CustomerAccounts WHERE CustomerID = %s;', (custid,))
    account_id = cursor.fetchone()
    i = ' '.join([str(elem) for elem in account_id])
    i = i.replace('(', '')
    i = i.replace(',)', '')
    accountid = int(i)
    cursor.close()
    

    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]

    if 'btn-nclicks-5' in changed_id:
        
        '''tickerData = yf.Ticker(input1)
        tickerDf = tickerData.history(period='1d', start='2020-1-1', end='2020-12-17')
        
        plot1 = px.line(tickerDf, x=tickerDf.index, y='Close')
        plot1.update_layout(title_text='Stock WatchList', title_font_size=20,autosize=False, width=700, height=400)'''

        cursor = connection.cursor(buffered=True) 
        cursor.execute('INSERT into Stock_WatchList (AccountNumber, StockSymbol) values (%s, %s);', (accountid, input1))
        connection.commit()
        cursor.close()
        display_stock_addition_status = dbc.Alert('Stock Added to your WatchList!', color="info") 
        
        return display_stock_addition_status

    elif 'remove_stockcode'in changed_id:
        
        cursor = connection.cursor(buffered=True) 
        cursor.execute('DELETE FROM Stock_WatchList WHERE AccountNumber = %s and StockSymbol = %s;', (accountid, input1))
        connection.commit()
        cursor.close()
        display_stock_addition_status = dbc.Alert('Stock Removed from your WatchList!', color="info") 
        
        return display_stock_addition_status

    else:
        return ''

@app.callback(Output('display_stocktrade_status', 'children'),
            [Input('btn-nclicks-7', 'n_clicks'), 
            Input('btn-nclicks-8', 'n_clicks'), 
              Input('intermediate-value', 'children'),
              Input('input-2-state', 'value'),
               Input('input-3-state', 'value'),
               Input('input-4-state', 'value'),])
        

def stock_trading(n_clicks, n_clicks1, custid, symbol, quantity, price):

    if quantity is 'None':
        raise dash.exceptions.PreventUpdate

    if price is 'None':
        raise dash.exceptions.PreventUpdate

    cursor = connection.cursor(buffered=True) 
    cursor.execute('SELECT AccountNumber FROM BankingDBProject.CustomerAccounts WHERE CustomerID = %s;', (custid,))
    account_id = cursor.fetchone()
    i = ' '.join([str(elem) for elem in account_id])
    i = i.replace('(', '')
    i = i.replace(',)', '')
    accountid = int(i)
    cursor.close()

    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]

    if 'btn-nclicks-7' in changed_id:

        cursor = connection.cursor(buffered=True) 
        cursor.execute('SELECT AccountBalance FROM BankingDBProject.AccountDetails WHERE AccountNumber = %s and AccountStatus = %s;', (accountid, 'Active'))
        current_account_balance = cursor.fetchone()
        cursor.close()
        new_current_account_balance = 0 

        i = ' '.join([str(elem) for elem in current_account_balance])
        i = i.replace('(', '')
        i = i.replace(',)', '')
        account_balance = int(i)

        try:
            amount_to_bid = int(quantity) * int(price)
        except ValueError:
            return 

        print(amount_to_bid, account_balance)
        
        if amount_to_bid < account_balance:

            cursor = connection.cursor(buffered=True) 
            cursor.execute('INSERT INTO BankingDBProject.StockLogs (AccountNumber, StockSymbol, StockLogMessage, StockTransactionType) values (%s, %s, %s, %s);', (accountid, symbol, 'Bid placed', 'Buy_Stock'))
            connection.commit()
            cursor.close()
            tickerData = yf.Ticker(symbol)
            tickerDf = tickerData.history(period='1d', start='2020-12-14', end='2020-12-15')
            print(tickerDf['High'], tickerDf['Low'])

            if (int(price) < tickerDf['High']).bool():
                if (int(price) > tickerDf['Low']).bool():
                    cursor = connection.cursor(buffered=True) 
                    cursor.execute('INSERT INTO BankingDBProject.StockActivity (StockSymbol, AccountNumber, StockQuantity, StockMoney, TradeType) values (%s, %s, %s, %s, %s);', (symbol, accountid, quantity, amount_to_bid, 'Buy'))
                    connection.commit()
                    cursor.close()
                    trade_msg = dbc.Alert('Stock obtained successfully!', color="success") 
                    
                else:
                    cursor = connection.cursor(buffered=True) 
                    cursor.execute('INSERT INTO BankingDBProject.StockLogs (AccountNumber, StockSymbol, StockLogMessage, StockTransactionType) values (%s, %s, %s, %s);', (accountid, symbol, 'Bid declined due to low value', 'Buy_Stock'))
                    connection.commit()
                    cursor.close()
                    trade_msg = dbc.Alert('Stock bid was low!', color="warning")
                    
            else:
                cursor = connection.cursor(buffered=True) 
                cursor.execute('INSERT INTO BankingDBProject.StockLogs (AccountNumber, StockSymbol, StockLogMessage, StockTransactionType) values (%s, %s, %s, %s);', (accountid, symbol, 'Bid declined due to high value', 'Buy_Stock'))
                connection.commit()
                cursor.close()
                trade_msg = dbc.Alert('Stock bid was high!', color="warning")
                
        else:
            trade_msg = dbc.Alert('Low Account Balance!', color="danger")

        return trade_msg


    if 'btn-nclicks-8' in changed_id:

        amount_to_bid = int(quantity) * int(price)
        cursor = connection.cursor(buffered=True) 
        cursor.execute('INSERT INTO BankingDBProject.StockActivity (StockSymbol, AccountNumber, StockQuantity, StockMoney, TradeType) values (%s, %s, %s, %s, %s);', (symbol, accountid, quantity, amount_to_bid, 'Sell'))
        connection.commit()
        cursor.close()
        trade_msg = dbc.Alert('Stock sold successfully!', color="success") 

        return trade_msg

    else:
        return ''

@app.callback(Output('dynamic-dropdown-container', 'children'),
    [Input('btn-nclicks-6', 'n_clicks'),
    Input('intermediate-value', 'children'),],
    [State('dynamic-dropdown-container', 'children'),])

def display_dropdowns(n_clicks, custid, children):

    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]

    if 'btn-nclicks-6' in changed_id:

        cursor = connection.cursor(buffered=True) 
        cursor.execute('SELECT AccountNumber FROM BankingDBProject.CustomerAccounts WHERE CustomerID = %s;', (custid,))
        accountid = cursor.fetchone()
        i = ' '.join([str(elem) for elem in accountid])
        i = i.replace('(', '')
        i = i.replace(',)', '')
        accountid = int(i)
        cursor.close()

        cursor = connection.cursor(buffered=True) 
        query = 'SELECT StockSymbol FROM Stock_WatchList WHERE AccountNumber = %s;'
        cursor.execute(query,(accountid,))
        
        tmp = cursor.fetchall()
        tmplist = []
        cursor.close()
        for i in tmp:
            i = ' '.join([str(elem) for elem in i])
            i = i.replace('(', '')
            i = i.replace(',)', '')
            tmplist.append(i)
            stock_list.append({'label': i, 'value': i},)

        new_element = html.Div([dcc.Dropdown(id={
                    'type': 'dynamic-dropdown',
                    'index': n_clicks
                },
                options=[{'label': i, 'value': i} for i in tmplist]
            ),
        html.Div(
            id={
                'type': 'dynamic-output',
                'index': n_clicks
            }
        )
        ])

        return new_element


@app.callback(
    Output({'type': 'dynamic-output', 'index': MATCH}, 'children'),
    [Input({'type': 'dynamic-dropdown', 'index': MATCH}, 'value'),],
    [State({'type': 'dynamic-dropdown', 'index': MATCH}, 'id'),],
)

def display_output(value, id):

    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]

    if 'value' in changed_id:

        print(value)
        plot1 = go.Figure()

        tickerData = yf.Ticker(value)
        tickerDf = tickerData.history(period='1d', start='2020-1-1', end='2020-12-05')
            
        plot1 = px.line(tickerDf, x=tickerDf.index, y='Close')           
        plot1.update_layout(title_text='Stock WatchList', title_font_size=20,autosize=False, width=700, height=400)

        return html.Div([dcc.Graph(figure= plot1)], style={'width': '45%'})
    
@app.callback(Output('output-state5', 'children'),
            [Input('btn-nclicks-10', 'n_clicks'), 
            Input('tinput-1-state', 'value'), 
            Input('tinput-2-state', 'value'), 
            Input('tinput-3-state', 'value'), 
            Input('intermediate-value', 'children'),],
            )
            

def transfer_money(n_clicks, beneficiaryaccountid, amount, reason, custid):

    if n_clicks == 1:
        
        cursor = connection.cursor(buffered=True) 
        cursor.execute('SELECT AccountNumber FROM BankingDBProject.CustomerAccounts WHERE CustomerID = %s;', (custid,))
        accountid = cursor.fetchone()
        i = ' '.join([str(elem) for elem in accountid])
        i = i.replace('(', '')
        i = i.replace(',)', '')
        accountid = int(i)
        cursor.close()
        
        cursor = connection.cursor(buffered=True) 
        cursor.execute('SELECT AccountBalance FROM BankingDBProject.AccountDetails WHERE AccountNumber = %s and AccountStatus = %s;', (accountid, 'Active'))
        
        if cursor.rowcount != 0:
            current_account_balance = cursor.fetchone()
            new_current_account_balance = 0 
            i = ' '.join([str(elem) for elem in current_account_balance])
            i = i.replace('(', '')
            i = i.replace(',)', '')
            account_balance = int(i)
            cursor.close()

            cursor = connection.cursor(buffered=True) 
            cursor.execute('SELECT BeneficiaryAccount FROM BankingDBProject.BeneficiaryDetails where AccountNumber = %s;', (accountid,))
            beneficiaryaccount = cursor.fetchone()
            cursor.close()

            i = ' '.join([str(elem) for elem in beneficiaryaccount])
            i = i.replace('(', '')
            i = i.replace(',)', '')

            if int(i) == int(beneficiaryaccountid):

                TransactionType = 'DBT'

                if account_balance > int(amount):
                    cursor = connection.cursor(buffered=True) 
                    cursor.execute('INSERT INTO BankingDBProject.Transactions (AccountNumber, TransactionAmount, TransactionStatus, TransactionMessage, TransactionType, CustomerID, BeneficiaryAccount) values (%s, %s, %s, %s, %s, %s, %s);', ( accountid, amount, 'Debited', reason, TransactionType ,custid, beneficiaryaccountid))
                    connection.commit()
                    cursor.close()

                    msg = dbc.Alert('Transfer Initiated!', color="success") 

                    cursor1 = connection.cursor(buffered=True) 
                    cursor1.execute('INSERT INTO BankingDBProject.Transactions (AccountNumber, TransactionAmount, TransactionStatus, TransactionMessage, TransactionType, CustomerID, BeneficiaryAccount) values (%s, %s, %s, %s, %s, %s, %s);', ( beneficiaryaccountid, amount, 'Credited', reason, 'CRD' ,custid, accountid))
                    connection.commit()
                    cursor1.close()

                elif account_balance <= int(amount):
                    msg = dbc.Alert('Sufficient amount not in the account to transfer money!', color="danger") 

            else:

                msg = dbc.Alert('Please Add Beneficiary Account Details from Beneficiary page!', color="warning") 

            cursor.close()
            return msg
        else:
            return ''

@app.callback([
            Output('btn-nclicks-10', 'n_clicks'), 
            Output('tinput-1-state', 'value'), 
            Output('tinput-2-state', 'value'), 
            Output('tinput-3-state', 'value'), ],
            [Input('reset_transfer_money', 'n_clicks'),],
            )
            
def reset_transfer_money(n_clicks):

    if n_clicks == 1:
        return 0, '', '', ''
    else:
        return 0, '', '', ''


@app.callback([
            Output('btn-nclicks-7', 'n_clicks'),
            Output('btn-nclicks-8', 'n_clicks'), 
            Output('input-2-state', 'value'), 
            Output('input-3-state', 'value'), 
            Output('input-4-state', 'value'), 
            ],
            [Input('btn-nclicks-15', 'n_clicks'),],
            )
            
def reset_stocktrade(n_clicks):

    if n_clicks == 1:
        return 0, 0, '', '', ''
    else:
        return 0, 0, '', '', ''

@app.callback([
            Output('btn-nclicks-4', 'n_clicks'),
            Output('input-1-states', 'value'), 
            Output('input-2-states', 'value'), 
            Output('input-3-states', 'value'), 
            ],
            [Input('btn-nclicks-17', 'n_clicks'),],
            )

def reset_beneficiary(n_clicks):

    if n_clicks == 1:
        return 0, '', '', ''
    else:
        return 0, '', '', ''

@app.callback([Output('submit-button-state1', 'n_clicks'),
            Output('ainput-1-state', 'value'),
               Output('ainput-2-state', 'value'),
               Output('ainput-3-state', 'value'),
               Output('ainput-4-state', 'value'),
               Output('ainput-5-state', 'value'),
               Output('ainput-6-state', 'value'),
               Output('ainput-7-state', 'value')],
               [Input('reset-button-state', 'n_clicks'),],)

def reset_account_details(n_clicks):
    if n_clicks == 1:
        return 0, '', '', '', '', '', '', ''
    else:
        return 0, '', '', '', '', '', '', ''


@app.callback(
            Output('admin_message1', 'children'),
            [Input('delete_customer', 'n_clicks'),
            Input('adminbutton1', 'value'),
             Input("yes_customers", "n_clicks")],
            [State("modal1", "is_open")],
            )

def delete_customer(n_clicks, customerid, n_clicks1, is_open):

    if n_clicks or n_clicks1:

        cursor1 = connection.cursor(buffered=True) 

        cursor1.execute('SELECT * FROM BankingDBProject.CustomerDetails WHERE CustomerID = %s;', (customerid, ))

        if cursor1.rowcount != 0:
            
            cursor1.close()

            cursor = connection.cursor(buffered=True) 
            cursor.execute('DELETE FROM BankingDBProject.CustomerDetails WHERE CustomerID = %s;', (customerid, ))
            connection.commit()
            cursor.close()

            msg = dbc.Alert('Customer removed from the Bank!', color="info") 
            return msg 
        else:
            msg = dbc.Alert('Customer not found!', color="danger") 
            return msg

    else:
        return ''

@app.callback(
            Output('admin_message2', 'children'),
            [Input('close_account', 'n_clicks'),
            Input('adminbutton2', 'value'),
            Input('adminbutton3', 'value'),
             Input("yes_accounts", "n_clicks")],
            [State("modal2", "is_open")],
            )

def close_account(n_clicks, customerid, accountid, n_clicks1, is_open):

    if n_clicks or n_clicks1:

        cursor = connection.cursor(buffered=True) 
        cursor.execute('SELECT CustomerID FROM BankingDBProject.CustomerAccounts WHERE AccountNumber = %s;', (accountid,))

        if cursor.rowcount != 0:

            cursor = connection.cursor(buffered=True) 
            
            cursor.execute('UPDATE BankingDBProject.AccountDetails SET AccountStatus = %s WHERE AccountNumber = %s ;', ('Inactive', accountid,))

            connection.commit()
            cursor.close()

            cursor = connection.cursor(buffered=True) 
            cursor.execute('INSERT INTO BankingDBProject.UserActivityLog (CustomerID, msgUserActiveLog) values (%s, %s);', (customerid, 'Customer-AccountInactive'))
            cursor.close()

            msg = dbc.Alert('Account removed from the Bank!', color="info") 
            return msg 
        else:
            return dbc.Alert('Account not found!', color="danger") 

    else:
        return ''

@app.callback(
            [Output('display_accountid', 'children'),
            Output('display_accountbalance', 'children'),
            Output('tab1_transaction_history', 'children'),
            Output('tab1_stock_history', 'children'),],
            [Input('show_tab1', 'n_clicks'),
            Input('intermediate-value', 'children'),],
            )

def main_tab_1(n_clicks, custid):

    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]

    if 'show_tab1' in changed_id:
    
        cursor = connection.cursor(buffered=True) 
        cursor.execute('SELECT AccountNumber FROM BankingDBProject.CustomerAccounts WHERE CustomerID = %s;', (custid,))
        accountid = cursor.fetchone()
        i = ' '.join([str(elem) for elem in accountid])
        i = i.replace('(', '')
        i = i.replace(',)', '')
        accountid = int(i)

        cursor.close()
        cursor = connection.cursor(buffered=True) 
        cursor.execute('SELECT AccountBalance FROM BankingDBProject.AccountDetails WHERE AccountNumber = %s and AccountStatus = %s;', (accountid, 'Active'))
        
        if cursor.rowcount != 0:
            current_account_balance = cursor.fetchone()
            new_current_account_balance = 0 
            i = ' '.join([str(elem) for elem in current_account_balance])
            i = i.replace('(', '')
            i = i.replace(',)', '')
            new_current_account_balance = int(i)
            
            text1 = 'Account Number is {}'.format(accountid)
            text2 = 'Account Balance is CAD {}.00'.format(new_current_account_balance)
            display_accountid = dbc.Alert(text1, color="primary") 
            display_accountbalance = dbc.Alert(text2, color="info") 

            transaction_df = pd.read_sql('SELECT * FROM BankingDBProject.Transactions WHERE AccountNumber = %s' %accountid, connection) 
            table = dash_table.DataTable(id='table', columns=[{"name": i, "id": i} for i in transaction_df.columns], data=transaction_df.to_dict("rows"),style_header={'backgroundColor': 'rgb(57,156,189)'}, style_cell={'backgroundColor': 'rgb(233,245,248)','color': 'black',}, )

            stocktransaction_df = pd.read_sql('SELECT * FROM BankingDBProject.StockActivity WHERE AccountNumber = %s' %accountid, connection) 
            stock_table = dash_table.DataTable(id='table', columns=[{"name": i, "id": i} for i in stocktransaction_df.columns], data=stocktransaction_df.to_dict("rows"),style_header={'backgroundColor': 'rgb(57,156,189)'}, style_cell={'backgroundColor': 'rgb(233,245,248)','color': 'black'}, )
            
        cursor.close()


        return display_accountid, display_accountbalance, table, stock_table

    else:
        return '', '', '', ''

if __name__ == '__main__':
    app.run_server(debug=True)
