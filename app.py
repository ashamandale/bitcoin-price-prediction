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
    
    xx= np.array([price, openp, highp, lowp, vol])
    xx=xx.reshape(1,5)
    
    if st.sidebar.button("Prediction"): 
    	Progress_bar()
    	bitcoin = pkl.load(open('bitcoin.pkl','rb'))
    	yy = bitcoin.predict(xx)
    	st.write("With PCA")
    	if yy==0:
    		st.write("Change is Positive")
    	else:
        	st.write("Change is Negative")

   	

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
        
   


