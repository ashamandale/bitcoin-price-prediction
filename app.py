import numpy as np
import pandas as pd
from pandas._libs.missing import NA
import streamlit as st
import time
import plotly.graph_objects as go
import pickle as pkl
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import plotly.express as px


st.title('BITCOIN PRICE PREDICTION APPS')

############################ Processing Phase ################################################
# @st.cache(persist=True)
def data_prep(df,price):    
    df=pd.DataFrame(df[df['Price']==price])
    df.dropna(inplace=True)    
    df.reset_index(drop=True,inplace=True)
       
    return df


# @st.cache(persist=True)
def test_stock(stocks_test,q_table,invest):

    num_stocks=0
    epsilon=0
    net_worth=[invest]
    np.random.seed()

    for dt in range(len(stocks_test)):
        long_ma=stocks_test.iloc[dt]['5day_MA']
        short_ma=stocks_test.iloc[dt]['1day_MA']
        close_price=stocks_test.iloc[dt]['close']
        t=trade_t(num_stocks,net_worth[-1],close_price)
        state=get_state(long_ma,short_ma,t)
        action=next_act(state,q_table,epsilon)

        if action==0:#Buy
            num_stocks+=1
            to_append=net_worth[-1]-close_price
            net_worth.append(np.round(to_append,1))
            
        
        elif action==1:#Sell
            num_stocks-=1
            to_append=net_worth[-1]+close_price
            net_worth.append(np.round(to_append,1))
        
        elif action==2:#hold
            to_append=net_worth[-1]+close_price
            net_worth.append(np.round(to_append,1))
      
        try:
            next_state=get_state(stocks_test.iloc[dt+1]['5day_MA'],stocks_test.iloc[dt+1]['1day_MA'],t)
            
        except:
            break

    return net_worth










def Progress_bar():
    'Starting a long computation...'
    # Add a placeholder
    latest_iteration = st.empty()
    bar = st.progress(0)
    
    for i in range(1,101):
  # Update the progress bar with each iteration.
        latest_iteration.text(f'Progress {i}%')
        bar.progress(i)
        time.sleep(0.05)

    latest_iteration=st.empty()
    '...and now we\'re done!'
    bar.empty()



def fun():

    #Reading the Dataset
    df=pd.read_csv("Bitcoin Historical Data - Investing.com India.csv")
    names=list(df['Price'].unique())
    global numeric_columns
    df1=df.head(20)
    st.write(df1.head(10))
    numeric_columns=list(df1.columns)
  
        
    #Sidebar Investment value # Price Open HIgh Low  
    st.sidebar.title("Bitcoin Price Predicition App")
 
    price = st.sidebar.number_input("Enter the Price")
    
    openp = st.sidebar.number_input("Enter the Open Price of Bitcoin")
    
    highp = st.sidebar.number_input("Enter the Highest Price of Bitcoin")
    
    lowp = st.sidebar.number_input("Enter the Lowest Price of Bitcoin")
    
    vol = st.sidebar.number_input("Enter the Vol of Bitcoin")
    
    if st.sidebar.button("Prediction"): 
    	Progress_bar()
    	bitcoin = pkl.load(open('bitcoin.pkl','rb'))
   	

     
    
    #select chart type
    chart_select=st.sidebar.selectbox(label="Select the chart type",options=['Scatterplots','Lineplots','Histogram','Boxplot'])
    if chart_select=='Scatterplots':
        st.sidebar.subheader("Scatterplot Settings")
        x_values=st.sidebar.selectbox('X axis',options=numeric_columns)
        y_values=st.sidebar.selectbox('Y axis',options=numeric_columns)
        plot=px.scatter(data_frame=df1,x=x_values,y=y_values)
        st.plotly_chart(plot)
        
    elif chart_select=='Lineplots':
        st.sidebar.subheader("Lineplot Settings")
        x_values=st.sidebar.selectbox('X axis',options=numeric_columns)
        y_values=st.sidebar.selectbox('Y axis',options=numeric_columns)
        plot=px.line(data_frame=df1,x=x_values,y=y_values)
        st.plotly_chart(plot)
        
    elif chart_select=='Histogram':
        st.sidebar.subheader("Histogram Settings")
        x_values=st.sidebar.selectbox('X axis',options=numeric_columns)
        y_values=st.sidebar.selectbox('Y axis',options=numeric_columns)
        plot=px.histogram(data_frame=df1,x=x_values,y=y_values)
        st.plotly_chart(plot)
        
    elif chart_select=='Boxplot':
        st.sidebar.subheader("Boxplot Settings")
        x_values=st.sidebar.selectbox('X axis',options=numeric_columns)
        y_values=st.sidebar.selectbox('Y axis',options=numeric_columns)
        plot=px.box(data_frame=df1,x=x_values,y=y_values)
        st.plotly_chart(plot)




if __name__=='__main__':
    fun()
        
   


