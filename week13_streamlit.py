#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 14:48:54 2020

@author: hantswilliams

TO RUN: 
    streamlit run week13_streamlit.py

"""

import streamlit as st

import pandas as pd
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import time



@st.cache
def load_hospitals():
    df_hospital_2 = pd.read_csv('https://raw.githubusercontent.com/hantswilliams/AHI_STATS_507/main/Week13_Summary/output/df_hospital_2.csv')
    return df_hospital_2

@st.cache
def load_inatpatient():
    df_inpatient_2 = pd.read_csv('https://raw.githubusercontent.com/hantswilliams/AHI_STATS_507/main/Week13_Summary/output/df_inpatient_2.csv')
    return df_inpatient_2

@st.cache
def load_outpatient():
    df_outpatient_2 = pd.read_csv('https://raw.githubusercontent.com/hantswilliams/AHI_STATS_507/main/Week13_Summary/output/df_outpatient_2.csv')
    return df_outpatient_2


st.title('Medicare — Expenses - NY')




    
    
# FAKE LOADER BAR TO STIMULATE LOADING    
my_bar = st.progress(0)
for percent_complete in range(100):
     time.sleep(0.1)
     my_bar.progress(percent_complete + 1)
  


  
# Load the data:     
df_hospital_2 = load_hospitals()
df_inpatient_2 = load_inatpatient()
df_outpatient_2 = load_outpatient()







hospitals_ny = df_hospital_2[df_hospital_2['state'] == 'NY']


#Bar Chart
st.subheader('Hospital Type  - NY')
bar1 = hospitals_ny['hospital_type'].value_counts().reset_index()
st.dataframe(bar1)

st.markdown('The majority of hospitals in NY are acute care, while the least are childrens hospitals. ')



st.subheader('Hospital Ownership  - NY')
ownership_ny = df_hospital_2[df_hospital_2['state'] == 'NY']
bar4 = ownership_ny['hospital_ownership'].value_counts().reset_index()
st.dataframe(bar4)

st.markdown('The majority of hospitals in NY are Private non-profit voluntary, while the least are owned by the department of defense.  ')


st.subheader('With a PIE Chart:')
fig = px.pie(bar4, values='hospital_ownership', names='index')
st.plotly_chart(fig)

st.subheader('Map of NY Hospital Locations')

hospitals_ny_gps = hospitals_ny['location'].str.strip('()').str.split(' ', expand=True).rename(columns={0: 'Point', 1:'lon', 2:'lat'}) 	
hospitals_ny_gps['lon'] = hospitals_ny_gps['lon'].str.strip('(')
hospitals_ny_gps = hospitals_ny_gps.dropna()
hospitals_ny_gps['lon'] = pd.to_numeric(hospitals_ny_gps['lon'])
hospitals_ny_gps['lat'] = pd.to_numeric(hospitals_ny_gps['lat'])

st.map(hospitals_ny_gps)




#Timeliness of Care
#st.subheader('NY Hospitals - Timelieness of Care')
#bar2 = hospitals_ny['timeliness_of_care_national_comparison'].value_counts().reset_index()
#fig2 = px.bar(bar2, x='index', y='timeliness_of_care_national_comparison')
#st.plotly_chart(fig2)

#st.markdown('Based on this above bar chart, we can see the majority of hospitals in the NY area fall below the national\
#        average as it relates to timeliness of care')

#Mortality in NY hospitals 
st.subheader('NY Hospitals - Mortality Comparision')
bar5 = hospitals_ny['mortality_national_comparison'].value_counts().reset_index()
fig2 = px.bar(bar5, x='index', y='mortality_national_comparison')
st.plotly_chart(fig2)

st.markdown('Based on the bar chart above, we can see that the majority of hospitals in the NY area are at the national average when it relates to mortality rates')




#Drill down into INPATIENT and OUTPATIENT just for NY 
st.title('A Look into INPATIENT data')


inpatient_ny = df_inpatient_2[df_inpatient_2['provider_state'] == 'NY']
total_inpatient_count = sum(inpatient_ny['total_discharges'])

st.header('Total Count of Discharges from Inpatient Captured: ' )
st.header( str(total_inpatient_count) )


##Common D/C 

common_discharges = inpatient_ny.groupby('drg_definition')['total_discharges'].sum().reset_index()


top10 = common_discharges.head(10)
bottom10 = common_discharges.tail(10)



st.header('DRGs')
st.dataframe(common_discharges)


col1, col2 = st.beta_columns(2)

col1.header('Top 10 DRGs')
col1.dataframe(top10)

col2.header('Bottom 10 DRGs')
col2.dataframe(bottom10)

# Drill down into outpatient data
st.title('A Look into OUTPATIENT data')


outpatient_ny = df_outpatient_2[df_outpatient_2['provider_state'] == 'NY']
total_outpatient_count = sum(outpatient_ny['outpatient_services'])

st.header('Total Count of Services from Outpatient Captured: ' )
st.header( str(total_outpatient_count) )





## Common APC
common_APC = outpatient_ny.groupby('apc')['outpatient_services'].sum().reset_index()


top10 = common_APC.head(10)
bottom10 = common_APC.tail(10)



st.header('APCs')
st.dataframe(common_APC)


col3, col4 = st.beta_columns(2)

col3.header('Top 10 APCs')
col3.dataframe(top10)

col4.header('Bottom 10 APCs')
col4.dataframe(bottom10)



#Bar Charts of the costs 

costs = inpatient_ny.groupby('provider_name')['average_total_payments'].sum().reset_index()
costs['average_total_payments'] = costs['average_total_payments'].astype('int64')


costs_medicare = inpatient_ny.groupby('provider_name')['average_medicare_payments'].sum().reset_index()
costs_medicare['average_medicare_payments'] = costs_medicare['average_medicare_payments'].astype('int64')


costs_sum = costs.merge(costs_medicare, how='left', left_on='provider_name', right_on='provider_name')
costs_sum['delta'] = costs_sum['average_total_payments'] - costs_sum['average_medicare_payments']



st.title('COSTS')
st.markdown('Based on the bar chart below, we can see that New York-Presbyterian hospital has the highest number of total payments, while Medina Memorial hospital has the lowest average total payments. ')

bar3 = px.bar(costs_sum, x='provider_name', y='average_total_payments')


st.plotly_chart(bar3)
st.header("Hospital - ")
st.dataframe(costs_sum)



#Costs by Condition and Hospital / Average Total Payments
costs_condition_hospital = inpatient_ny.groupby(['provider_name', 'drg_definition'])['average_total_payments'].sum().reset_index()
st.header("Costs by Condition and Hospital - Average Total Payments")
st.dataframe(costs_condition_hospital)






#Bar Charts of the costs for APC

costs2 = outpatient_ny.groupby('provider_name')['average_total_payments'].sum().reset_index()
costs2['average_total_payments'] = costs2['average_total_payments'].astype('int64')


costs_estimated = outpatient_ny.groupby('provider_name')['average_estimated_submitted_charges'].sum().reset_index()
costs_estimated['average_estimated_submitted_charges'] = costs_estimated['average_estimated_submitted_charges'].astype('int64')


costs_sum2 = costs2.merge(costs_estimated, how='left', left_on='provider_name', right_on='provider_name')
costs_sum2['delta'] = costs_sum2['average_total_payments'] - costs_sum2['average_estimated_submitted_charges']


st.title('COSTS OF AMBULATORY PAYMENT CLASSIFICATION')

bar6 = px.bar(costs_sum2, x='provider_name', y='average_total_payments')
st.plotly_chart(bar6)
st.markdown('Based on the bar chart above, we can see that Montefiore Medical Center has the highest average total payments while Helen Hayes Hospital has the least. ')



st.header("Hospital - ")
st.dataframe(costs_sum2)


#Costs by APC and Outpatient Hospital / Average Total Payments
costs_condition_APC = outpatient_ny.groupby(['provider_name', 'apc'])['average_total_payments'].sum().reset_index()
st.header("Costs by APC and Outpatient Hospital - Average Total Payments")
st.dataframe(costs_condition_APC)

st.markdown('Based on this chart, we can see that Staten Island Univeristy Hospital has the lowest average total payment for a level1 APC of Electronic analysis of Devices, while Mount Sinai Hospital has the highest average total payment for a level IV Endoscopy upper airway. ')











#hospitals = costs_condition_hospital['provider_name'].drop_duplicates()
#hospital_choice = st.sidebar.selectbox('Select your hospital:', hospitals)
#filtered = costs_sum["provider_name"].loc[costs_sum["provider_name"] == hospital_choice]
#st.dataframe(filtered)







