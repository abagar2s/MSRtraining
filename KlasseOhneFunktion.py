
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import altair as alt

#CSV Data

Mydata = pd.read_csv("MyData2.csv")

# Page config with css

st.set_page_config(layout='wide', initial_sidebar_state='expanded')

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Left side
    
st.sidebar.header('Dashboard')

# Get a list of all column names in the DataFrame
all_columns = list(Mydata.columns)

# List of Land
unique_land = list(set(Mydata['Land']))

# Selectbox for the Metrics

st.sidebar.subheader('Metrics parameter')
Parameter1 = st.sidebar.selectbox('Metric1', all_columns[4:])
Parameter2 = st.sidebar.selectbox('Metric2', unique_land) 
Parameter3 = st.sidebar.selectbox('Metric2', ['Personenkraftwagen','Lastkraftwagen']) 

# multiselect for the plot
# Define a counter variable
counter = 0
st.sidebar.subheader('Line chart parameters')
plot_data1 = st.sidebar.multiselect('Select data', all_columns[:2], key=f'select_data_{counter}')
counter += 1
plot_data2 = st.sidebar.multiselect('Select data', all_columns[4:], key=f'select_data_{counter}') 
counter += 1


height = st.sidebar.slider('Specify plot height', min_value=1, max_value=5, step=1)

# Selectbox for the Donut

st.sidebar.subheader('Donut chart parameter')
donut_parameter = st.sidebar.selectbox('Select data', all_columns[4:])

# multiselect for the stacked column chart

st.sidebar.subheader('stacked chart parameters')

# Create the widget with a unique key based on the counter
plot2_data = st.sidebar.multiselect('Select data', all_columns[4:], key=f'select_data_{counter}')
counter += 1



st.sidebar.markdown('''
---
Created by Aymane Bagari
''')

# Right Side

# Row 1

st.markdown('### Metrics')
col1, col2 = st.columns(2)
sumbyType = Mydata[Parameter1].sum()
sumbyLand = Mydata.loc[Mydata['Land'] == Parameter2 , Parameter3].sum()

metric_title1 = 'Anzahl von {}'.format(Parameter1)
metric_title2 = 'Anzahl von Außerbetriebsetzungen({}) in {}'.format(Parameter3,Parameter2)


col1.metric(metric_title1 , sumbyType )
col2.metric(metric_title2 , sumbyLand )

# Row  2

st.markdown('### Line chart')
fig, ax = plt.subplots()
sum_by_region = Mydata.groupby(plot_data1)[plot_data2].sum()
for column in plot_data2:
    ax.bar(sum_by_region.index, sum_by_region[column], label=column)
ax.set_xlabel('Land')
ax.set_ylabel('Value')
plt.xticks(rotation=60)
plt.xticks(fontsize=4)
fig.set_size_inches(6,height)
ax.legend()


# Display the chart in Streamlit
st.pyplot(fig)

# Row 3
sum_by_region2 = []

st.markdown('### Donut chart')
for column in unique_land:
    sum_by_region2.append(Mydata.loc[Mydata['Land'] == column , donut_parameter].sum())
    fig = go.Figure(data=[go.Pie(labels=unique_land, values=sum_by_region2 , hole=.6)])
    fig.update_layout(title='Außerbetriebsetzungen nach Region', margin=dict(l=60, r=0, b=0))

# Render chart using st.plotly_chart
st.plotly_chart(fig)

# Row 4
st.markdown('### stacked column chart')
# pivot data to have selected columns as separate columns
df_pivot = Mydata.pivot_table(index='Land', values=plot2_data, aggfunc='sum').reset_index()

# melt data to have a separate row for each stacked bar
df_melt = df_pivot.melt(id_vars='Land', var_name='Column', value_name='Value')

# create stacked chart with stacked bars colored by their respective columns
chart = alt.Chart(df_melt).mark_bar().encode(
    x='Land',
    y=alt.Y('Value', stack='normalize'),
    color='Column',
    tooltip=['Land', 'Column', 'Value']
).properties(
    width=500,
    height=400,
    title='Cars per Country'
)

    # show the chart
st.altair_chart(chart, use_container_width=True)
