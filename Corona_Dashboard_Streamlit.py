import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.title('Toronto COVID-19 Dashboard')
st.sidebar.title('Toronto COVID-19')
st.markdown('*Note*: This is a replicated web-app of the official City of Toronto COVID-19: Status of Cases in Toronto dashboard')
st.markdown('Please visit the following website to view the original dashboard')
st.markdown('https://www.toronto.ca/home/covid-19/covid-19-latest-city-of-toronto-news/covid-19-status-of-cases-in-toronto/')

DATA_URL = pd.ExcelFile('CityofToronto_COVID-19_Data.xlsx')


df_outcomes = pd.read_excel(DATA_URL, 'Cases by Outcome')
df_outbreaks = pd.read_excel(DATA_URL, 'Outbreaks')

df_cum_cases_episode = pd.read_excel(DATA_URL, 'Cumulative Cases by Episode Dat')
df_cum_cases_report = pd.read_excel(DATA_URL, 'Cumulative Cases by Reported Da')

df_cases_episode = pd.read_excel(DATA_URL, 'Cases by Episode Date')
df_cases_report = pd.read_excel(DATA_URL, 'Cases by Reported Date')

df_cases_age = pd.read_excel(DATA_URL, 'Cases by Age')
df_cases_gender = pd.read_excel(DATA_URL, 'Cases by Gender')

df_hosp = pd.read_excel(DATA_URL, 'Currently Hospitalized')
df_cum_hosp = pd.read_excel(DATA_URL, 'Ever Hospitalized')

df_source_inf = pd.read_excel(DATA_URL, 'Source of Infection')

df_severity = pd.read_excel(DATA_URL, 'Severity Indicators by Age Grou')

st.sidebar.subheader('Outcomes')
select = st.sidebar.selectbox('Outcome Types', ['Total Cases', 'Recovered Cases', 'Deaths'], key = 1)
st.markdown('When using the charts below, hover over the bars to view numbers (counts) and other relevant information. Please note that the data shown here may differ from other sources, as data are extracted at different times. The data in the charts are subject to change as the public health investigation into reported cases is currently ongoing. Additionally, data definitions are subject to change as the pandemic evolves.')
st.markdown('This information is updated three times per week on Monday, Wednesday and Friday')

df_outcomes = df_outcomes.set_index('Outcome')
df_outcomes_transposed = df_outcomes.transpose()

tot_cases = df_outcomes_transposed['All Cases']
tot_death = df_outcomes_transposed['Deaths']
tot_recovered = df_outcomes_transposed['Recovered Cases']

if not st.sidebar.checkbox('Hide', True):
    st.subheader('Outcome Types')
    if select == 'Total Cases':
        fig = px.bar(tot_cases)
        fig.data[-1].text = df_outcomes_transposed['All Cases']
        fig.update_traces(textfont_size = 30, textposition='inside', insidetextanchor = 'middle', marker_color='red')
        st.plotly_chart(fig)
    if select == 'Recovered Cases':
        fig = px.bar(tot_recovered)
        fig.data[-1].text = df_outcomes_transposed['Recovered Cases']
        fig.update_traces(textfont_size = 30, textposition='inside', insidetextanchor = 'middle', marker_color='green')
        st.plotly_chart(fig)
    if select == 'Deaths':
        fig = px.bar(tot_death)
        fig.data[-1].text = df_outcomes_transposed['Deaths']
        fig.update_traces(textfont_size = 30, textposition='inside', insidetextanchor = 'middle', marker_color='black')
        st.plotly_chart(fig)

st.sidebar.subheader('Cumulative Institutional Outbreaks')
st.subheader('Cumulative Institutional Outbreaks')
df_outbreaks = df_outbreaks.set_index('Outbreak Type')
df_outbreaks_transposed = df_outbreaks.transpose()

tot_outbreaks = df_outbreaks_transposed['Institutional']
fig2 = px.bar(tot_outbreaks)
fig2.data[-1].text = df_outbreaks_transposed['Institutional']
fig2.update_traces(textfont_size = 30, textposition = 'inside', insidetextanchor = 'middle', marker_color='white')
st.plotly_chart(fig2)

st.sidebar.subheader('Cumulative Cases by Date & Outcome')
st.subheader('Cumulative Cases by Date & Outcome')
select2 = st.sidebar.selectbox('Episode vs. Report', ['Episode Date', 'Reported Date'], key = 1)

df_cum_cases_episode['Episode Date'] = df_cum_cases_episode['Episode Date'].astype('datetime64')
df_cum_cases_report['Reported Date'] = df_cum_cases_report['Reported Date'].astype('datetime64')

if select2 == 'Episode Date':
    fig = px.line(df_cum_cases_episode, x = 'Episode Date', y = ['Recovered Cases', 'Active Cases', 'Deaths'], color_discrete_map = {'Recovered Cases': 'green', 'Active Cases': 'red', 'Deaths':'black'})
    fig.update_layout(autosize = False, width = 1000, height = 600)
    st.plotly_chart(fig)
if select2 == 'Reported Date':
    fig = px.line(df_cum_cases_report, x = 'Reported Date', y = ['Recovered Cases', 'Active Cases', 'Deaths'], color_discrete_map = {'Recovered Cases': 'green', 'Active Cases': 'red', 'Deaths':'black'})
    fig.update_layout(autosize = False, width = 1000, height = 600)
    st.plotly_chart(fig)

st.markdown('Data Notes: Data for the most recent episode dates are least complete, reflecting testing and report processing lags')
st.markdown('Episode date is the earliest of symptom onset, laboratory testing, and reporting dates. In the figures above, cases are shown based on when the persons symptoms started, or if that is not known, the date that they were tested. If the test date is not known, the date that the case was reported to public health is used. AS the case is investigated and new information on these dates is determined, the dates in the graph will be updated')

st.sidebar.subheader('Daily Case Counts')
st.subheader('Daily Case Counts')
select3 = st.sidebar.selectbox('Episode vs Report', ['Episode Date', 'Reported Date'], key = 1)

df_cases_episode['Moving Average'] = df_cases_episode['Case Count'].rolling(5).mean()
df_cases_report['Moving Average'] = df_cases_report['Case Count'].rolling(5).mean()

if select3 == 'Episode Date':
    fig = px.line(df_cases_episode, x = 'Episode Date', y = ['Case Count', 'Moving Average'], color_discrete_map = {'Case Count': 'black', 'Moving Average': 'red'})
    fig.update_layout(autosize = False, width = 1000, height = 600)
    st.plotly_chart(fig)
if select3 == 'Reported Date':
    fig = px.line(df_cases_report, x = 'Reported Date', y = ['Case Count', 'Moving Average'], color_discrete_map = {'Case Count': 'black', 'Moving Average': 'red'})
    fig.update_layout(autosize = False, width = 1000, height = 600)
    st.plotly_chart(fig)

st.sidebar.subheader('Case by Age Group')
st.subheader('Case by Age Group')
fig3 = px.bar(df_cases_age, x = 'Case Count', y = 'Age Group', orientation = 'h', color_discrete_map = {'Age Group':'pink'})
fig3.data[-1].text = df_cases_age['% of Total Case Count'].round(1)
st.plotly_chart(fig3)

st.sidebar.subheader('Cases by Gender')
st.subheader('Cases by Gender')
fig4 = px.bar(df_cases_gender, x = 'Case Count', y = 'Client Gender', orientation = 'h', color_discrete_map = {'Client Gender':'pink'})
fig4.data[-1].text = df_cases_gender['% of Total Case Count'].round(1)
st.plotly_chart(fig4)

st.sidebar.subheader('Currently Hospitalized')
st.subheader('Currently Hospitalized')
fig5 = px.bar(df_hosp, x = 'Case Count', y = 'Intervention', orientation = 'h')
fig5.data[-1].text = df_hosp['% of Total Cases'].round(2)
st.plotly_chart(fig5)

st.sidebar.subheader('Percent Ever Hospitalized')
st.subheader('Percent Ever Hospitalized')
fig6 = px.bar(df_cum_hosp, x = 'Case Count', y = 'Intervention', orientation = 'h')
fig6.data[-1].text = df_cum_hosp['% of Total Cases'].round(1)
st.plotly_chart(fig6)

st.sidebar.subheader('Source of Infection - Sporadic Cases')
st.subheader('Source of Infection - Sporadic Cases')
fig7 = px.bar(df_source_inf, x = '% of Total Case Count', y = 'Most Likely Source', orientation = 'h')
fig7.data[-1].text = df_source_inf['% of Total Case Count'].round(1)
fig7.update_traces(textposition='outside')
st.plotly_chart(fig7)

st.sidebar.subheader('Number of COVID-19 Cases that Ever Resulted in Hospitalization, Intensive Care Unit (ICU) Admission, Intubation, and Deaths, by Age Group')
st.subheader('Number of COVID-19 Cases that Ever Resulted in Hospitalization, Intensive Care Unit (ICU) Admission, Intubation, and Deaths, by Age Group')
fig8 = px.bar(df_severity, x = 'Age Group', y = ['ICU Cases', 'Deaths', 'Hospitalized Cases', 'Intubated Cases'], barmode = 'stack', color_discrete_map = {'Deaths':'black', 'ICU Cases':'orange', 'Intubated Cases':'red', 'Hospitalized Cases':'blue'})
fig8.update_layout(autosize = False, width = 1000, height = 600)
st.plotly_chart(fig8)
