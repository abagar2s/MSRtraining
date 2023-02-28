import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import altair as alt

# load the data

def load_data():
    Mydata = pd.read_csv("MyData2.csv")
    return Mydata

# CSS file for the beauty of website
def set_page_style():
    st.set_page_config(layout='wide', initial_sidebar_state='expanded')
    with open('style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
   

def render_sidebar(Mydata):
    st.sidebar.header('Dashboard')
    
    # all columns of the data
    all_columns = list(Mydata.columns)

    # All the lands in the table
    unique_land = Mydata['Land'].unique()

    st.sidebar.subheader('Metrics parameter')
    
    # Metrics Paramters

    Selected_Vehicle = st.sidebar.selectbox('Metric1', all_columns[4:])
    Selected_Land = st.sidebar.selectbox('Metric2', unique_land) 
    Selected_Vehicle_Type = st.sidebar.selectbox('Metric2', ['Personenkraftwagen','Lastkraftwagen']) 
    
    # Line chart parameters
    # counter for the multiselect key
    counter = 0

    st.sidebar.subheader('Line chart parameters')

    plot_Xaxe_Selection = st.sidebar.multiselect('Select data', all_columns[:2], key=f'select_data_{counter}')
    counter += 1
    plot_Yaxe_Selection = st.sidebar.multiselect('Select data', all_columns[4:], key=f'select_data_{counter}') 
    counter += 1
    height = st.sidebar.slider('Specify plot height', min_value=1, max_value=5, step=1)
    
    #Donut chart parameter
    st.sidebar.subheader('Donut chart parameter')
    donut_parameter = st.sidebar.selectbox('Select data', all_columns[4:])

    #stacked chart parameters
    
    st.sidebar.subheader('stacked chart parameters')
    Stacked_chart_Selection = st.sidebar.multiselect('Select data', all_columns[4:], key=f'select_data_{counter}')
    counter += 1
    
    st.sidebar.markdown('''
    ---
    Created by Aymane Bagari
    ''')

    
    return Selected_Vehicle, Selected_Land, Selected_Vehicle_Type, plot_Xaxe_Selection, plot_Yaxe_Selection, height, donut_parameter, Stacked_chart_Selection, unique_land

def render_metrics(Mydata, Selected_Vehicle, Selected_Land, Selected_Vehicle_Type):
    st.markdown('### Metrics')

    sum_by_Type = Mydata[Selected_Vehicle].sum()
    sum_by_Land = Mydata.loc[Mydata['Land'] == Selected_Land , Selected_Vehicle_Type].sum()
    
    col1, col2 = st.columns(2)
    metric_title1 = 'Anzahl von {}'.format(Selected_Vehicle)
    metric_title2 = 'Anzahl von Außerbetriebsetzungen({}) in {}'.format(Selected_Vehicle_Type,Selected_Land)
    
    col1.metric(metric_title1 , sum_by_Type )
    col2.metric(metric_title2 , sum_by_Land )

def render_line_chart(Mydata, plot_Xaxe_Selection, plot_Yaxe_Selection, height):
    st.markdown('### Line chart')

    fig, ax = plt.subplots()
    sum_by_region = Mydata.groupby(plot_Xaxe_Selection)[plot_Yaxe_Selection].sum()
    for column in plot_Yaxe_Selection:
        ax.bar(sum_by_region.index, sum_by_region[column], label=column)
    ax.set_xlabel('Land')
    ax.set_ylabel('Value')
    plt.xticks(rotation=60)
    plt.xticks(fontsize=4)
    fig.set_size_inches(6,height)
    ax.legend()
    st.pyplot(fig)

# Row 3
def render_Donut_chart(Mydata,unique_land,donut_parameter):
    st.markdown('### Donut chart')
    sum_by_region2 = []

    for column in unique_land:
        sum_by_region2.append(Mydata.loc[Mydata['Land'] == column , donut_parameter].sum())
        fig = go.Figure(data=[go.Pie(labels=unique_land, values=sum_by_region2 , hole=.6)])
        fig.update_layout(title='Außerbetriebsetzungen nach Region', margin=dict(l=0, r=0, b=0))

    st.plotly_chart(fig)

# Row 4
def render_Stacked_chart(Mydata,Stacked_chart_Selection):
    st.markdown('### stacked column chart')
    # pivot data to have selected columns as separate columns
    df_pivot = Mydata.pivot_table(index='Land', values=Stacked_chart_Selection, aggfunc='sum').reset_index()

    # melt data to have a separate row for each stacked bar
    df_melt = df_pivot.melt(id_vars='Land', var_name='Column', value_name='Prozentsatz')

    # create stacked chart with stacked bars colored by their respective columns
    chart = alt.Chart(df_melt).mark_bar().encode(
        x='Land',
        y=alt.Y('Prozentsatz', stack='normalize'),
        color='Column',
        tooltip=['Land', 'Column', 'Prozentsatz']
    ).properties(
        width=500,
        height=400,
        title='Außer Betrieb befindliche Fahrzeuge nach Region'
    )

    st.altair_chart(chart, use_container_width=True)