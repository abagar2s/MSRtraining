import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import altair as alt
import KlasseMitFunktion 

# Define functions here (load_data, set_page_style, render_sidebar, render_metrics, render_line_chart)

def main():
    #my_object = Projekt1()
    Mydata = KlasseMitFunktion.load_data()
    KlasseMitFunktion.set_page_style()
    Selected_Vehicle, Selected_Land, Selected_Vehicle_Type, plot_Xaxe_Selection, 
    plot_Yaxe_Selection, height, donut_parameter, Stacked_chart_Selection, unique_land= KlasseMitFunktion.render_sidebar(Mydata)
    KlasseMitFunktion.render_metrics(Mydata, Selected_Vehicle, Selected_Land, Selected_Vehicle_Type)
    KlasseMitFunktion.render_line_chart(Mydata, plot_Xaxe_Selection, plot_Yaxe_Selection, height)
    KlasseMitFunktion.render_Donut_chart(Mydata,unique_land,donut_parameter)
    KlasseMitFunktion.render_Stacked_chart(Mydata,Stacked_chart_Selection)

if __name__ == '__main__':
    main()
