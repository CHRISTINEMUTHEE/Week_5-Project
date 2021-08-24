import streamlit as st
import pandas as pd
import numpy as np
from streamlit.elements.arrow import Data
from streamlit.elements.legacy_data_frame import marshall_data_frame
import plotly.graph_objects as go
from streamlit.proto.Markdown_pb2 import Markdown
import plotly.express as px

header=st.container()
datasets=st.container()
plots=st.container()

with header:
    st.title('The burden of air pollution on the health sector with emphasis on respiratory diseases.')
    st.markdown('We seek to carry out this project to find out the burden that air pollution places on the health sector in the Afrian continent.')
    st.markdown('Air pollution continues to be a significant concern to public health worldwide and a tough problem confronted by both developed and developing countries. Compared to most developed countries that have rapidly progressed in industrialization for years, developing countries in Africa are also confronting more severe air pollution due to intense energy consumption, large-scale demolition, and reconstruction projects, and increased emissions from transportation in the process of industrialization and urbanization.')


with datasets:
    st.header('This research involved five datasets namely:')
    st.sidebar.markdown('Select the datasets accordingly:')
    # Dataset_visual=st.sidebar.checkbox('Display the list of our raw datasets')
    Dataset_list=st.sidebar.selectbox('Select the dataset of your choice:',
    options=['Mortality Rate Dataset',
    'Particulate Matter dataset',
    'The Carbon IV oxide concentration dataset',
    'The Nitrogen Oxide concentration dataset'],index=0)

    # Defining a function to read the datasets
    def Data_frames(type,data):
        if type=='csv':
            My_data=pd.read_csv(data)
            return My_data
        else:
            My_data=pd.read_excel(data,header=1)
            return My_data
    # Function to load the datasets
    def D_datasets(label,df_name,type,data):
        df_name=Data_frames(type,data)
        result=st.text(label)
        result=st.write(df_name.head(5))
        return result
    # Reading the Mortality rate dataset
    if Dataset_list=='Mortality Rate Dataset':
        D_datasets('1.Mortality Rate Dataset','M_data','csv','Death due to respiratory conditions (new).csv')

    # The Particulate Matter dataset
    elif Dataset_list=='Particulate Matter dataset':
        D_datasets('2.Particulate Matter dataset','PM_data','csv','Particulate Matter Concentration world wide...csv')

    # Reading the CO2 concentration dataset
    elif Dataset_list=='The Carbon IV oxide concentration dataset':
        D_datasets('3.The Carbon IV oxide concentration dataset','CO2_data','csv','CO2 Emission in KT. in excel.csv')

    # Reading the NO concentration dataset
    elif Dataset_list=='The Nitrogen Oxide concentration dataset':
        D_datasets('4.The Nitrogen Oxide concentration dataset','NO_dataset','xlsx','Nitogen Oxide Emissions edited.xlsx')
    
    # Denoting the steps of data cleaning

    st.markdown('The stages of cleaning in all datasets involved processes to check the Validity,Accuracy,Completeness,Consistency and uniformity.')
    st.markdown('* **First step:** We removed the null values in all datasets,this was aimed at improving our accuracy during analysis.')
    st.markdown('* **Second step:** We checked for duplicated values and inturn dropped them.')
    st.markdown('* **Third step:** We corrected the column names to enable uniformity and enable merging during analysis.')
    st.markdown('* **Final step:** We filetred out countries in Africa as guided by our objectives.')



with plots:
    st.header('This were the results of our analysis :')
    # Selecting a drop box to select our research questions.
    research_questions=st.sidebar.selectbox('Select the research question of your choice:',
    options=['Which country had the highest Particulate Matter concentration?',
    'Which country had the highest Mortality rates?',
    'Which gender was most affected?',
    'What were the particular causes of death across Africa?'],index=0)
    # Reloading the clean datasets by calling the Dataframe function
    # Loading the Mortality rate dataset and assigning it a variable
    # Data_frames('csv','Clean Mortality rate dataset.csv')
    Clean_Mortality_df=Data_frames('csv','Clean Mortality rate dataset.csv')
    # Loading the clean particulate matter concentration dataset and assigning it a variable
    # Data_frames('csv','Clean_PM.csv')
    Clean_PM=Data_frames('csv','Clean_PM.csv')
    # Loading the The CO2 concentration dataset and assigning it a variable
    # Data_frames('csv','Clean CO2 dataset.csv')
    Clean_CO2=Data_frames('csv','Clean CO2 dataset.csv')
    # Loading the NO dataset and assigning it a variable
    # Data_frames('csv','Clean NO dataset.csv')
    Clean_NO=Data_frames('csv','Clean NO dataset.csv')

    # Defining a function to merge mortality rate dataframe with the various pollutant levels
    def merge1(data1,data2,condition1,condition2):
        merged1_df=pd.merge(data1,data2,left_index=condition1,right_index=condition2)
        return merged1_df
    # Merging the Mortality rate dataset with the CO2 concentration dataset
    CO2_merge=merge1(Clean_Mortality_df,Clean_CO2,True,True)
    # Merging the Mortality rate dataset with the NO dataset 
    NO_merge=merge1(Clean_Mortality_df,Clean_NO,True,True)

    # A display of the respective graphs
    fig = go.Figure()
    # A graph of pollutant concentrations
    if research_questions=='Which country had the highest Particulate Matter concentration?':
        fig.add_trace(go.Scatter(x=Clean_PM.Country, y=Clean_PM.Average_PM_Value,mode='markers',name='Average_PM_value'))
        st.markdown('1. Graph of Average PM concentration against the countries in Africa')
        st.text('Niger had the highest PM concetration of 120.943333')
        st.text('It was followed closely by:')
        st.text('Chad,Mauritania,Nigeria,Carbo Verde and Cameroon ')


    elif research_questions=='Which country had the highest Mortality rates?':
        fig.add_trace(go.Scatter(x=Clean_Mortality_df.Country,y=Clean_Mortality_df.Average_death_Value,mode='markers',name='Average_death_value'))
        st.markdown('2. A graph of Mortality rates against the countries in Africa')
        st.text('Chad has the highest mortality rate') 
        st.text('Egypt,Nigeria,Niger and Cameroon')
        st.text('The countries above are among the "hall of fame" of countries with the highest pollutant levels all together.')
        
    
    elif research_questions=='Which gender was most affected?':
        fig.add_trace(go.Bar(x=Clean_Mortality_df.Gender,y=Clean_Mortality_df.Average_death_Value,name='Average_death_value'))
        st.markdown('3. A graph of mortality rates against the gender')
        st.text('The Male gender was highly affected as compared to the Female gender')
    

    elif research_questions=='What were the particular causes of death across Africa?':
        fig.add_trace(go.Bar(x=Clean_Mortality_df.Cause,y=Clean_Mortality_df.Average_death_Value,name='Average_death_value'))
        st.markdown('4. A graph of mortality rates against the causes of death')
        st.text('Causes of deaths ranged from:')
        st.text('Lower respiratory infections,Ischaemic heart disease,Stroke,COPD,Trachea,bronchus and lung cancers')

    st.plotly_chart(fig, use_container_width=True)                        
        
    