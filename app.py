import pandas as pd
import streamlit as st
import preprocessor
import helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import plotly.figure_factory as ff

df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv') 
df = preprocessor.preprocess(df,region_df)

st.sidebar.title("Olympic Analysis upto 2016")
st.sidebar.image('olympic.png')
user_menu = st.sidebar.radio(
    'Select an option',
    ('Medal Tally','Overall Analysis','Country-wise Analysis','Athelete-wise Analysis')
)

#st.dataframe(df)

if user_menu == 'Medal Tally':
    st.sidebar.header('Medal Tally')
    years , countries = helper.country_year_list(df)
    selected_year = st.sidebar.selectbox("Select Year" , years)
    selected_country = st.sidebar.selectbox("Select Country" , countries)
    medal_df = helper.medal_tally(df) 
    x = helper.fetch(selected_year,selected_country,df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal']))

    if selected_country == 'All' and selected_year =='Overall':
        st.title("Overall Medal Analysis")
    if selected_country == 'All' and selected_year !='Overall':
        st.title(f"Year-wise Analysis for {selected_country}")
    if selected_country != 'All' and selected_year =='Overall':
        st.title(f"Country-wise Analysis for {selected_year}")
    if selected_country != 'All' and selected_year !='Overall':
        st.title(f"{selected_country} performance in {selected_year}")
    st.table(x)

if user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0]-1
    hosts = df['City'].unique().shape[0]
    sports =df['Sport'].unique().shape[0]
    event = df['Event'].unique().shape[0]
    atheletes = df['Name'].unique().shape[0]
    countries = df['region'].unique().shape[0]
    medal_df = helper.medal_tally(df) 
    gold = medal_df['Gold'].sum()
    silver = medal_df['Silver'].sum()
    bronze = medal_df['Bronze'].sum()
    total = medal_df['Total'].sum()

    st.title("Major stats")
    col1 , col2 , col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(hosts)
    with col3:
        st.header("Sports")
        st.title(sports)

    col1 , col2 , col3 = st.columns(3)
    with col1:
        st.header("Event")
        st.title(event)
    with col2:
        st.header("Atheletes")
        st.title(atheletes)
    with col3:
        st.header("Countries")
        st.title(countries)

    col1 , col2 , col3 ,col4= st.columns(4)
    with col1:
        st.header("Gold")
        st.title(gold)
    with col2:
        st.header("Silver")
        st.title(silver)
    with col3:
        st.header("Bronze")
        st.title(bronze)
    with col4:
        st.header("Total")
        st.title(total)

    st.title("Participating nations over the years")
    nation_over_time = df.drop_duplicates(subset=['Year','region'])['Year'].value_counts().reset_index().sort_values('Year')
    fig = px.line(nation_over_time,x='Year',y='count',labels={'Year' : "Edition" , 'count' : "Nations"})
    st.plotly_chart(fig)

    st.title("No. of events over the years")
    event_over_time = df.drop_duplicates(subset=['Year','Event'])['Year'].value_counts().reset_index().sort_values('Year')
    fig = px.line(event_over_time,x='Year',y='count',labels={'Year' : "Edition" , 'count' : "Events"})
    st.plotly_chart(fig)

    st.title("No. of atheletes over the years")
    event_over_time = df.drop_duplicates(subset=['Year','Name'])['Year'].value_counts().reset_index().sort_values('Year')
    fig = px.line(event_over_time,x='Year',y='count',labels={'Year' : "Edition" , 'count' : "Atheletes"})

    st.plotly_chart(fig)

    st.title("No. of events under each sport over the years")
    fig , ax = plt.subplots(figsize=(15,15))
    kind_of_events_over_time = df.drop_duplicates(subset=['Year','Sport','Event'])
    sns.heatmap(kind_of_events_over_time.pivot_table(index='Sport', columns='Year', values='Event',aggfunc='count' ).fillna(0).astype('int'),annot=True)
    st.pyplot(fig)

    col1 , col2 = st.columns(2)
    with col1:
        st.title("Most successful atheletes")
    with col2:
        sport = np.unique(df['Sport'].dropna().values).tolist()
        sport.sort()
        sport.insert(0,'All')
        selected_sport = st.selectbox("Select the sport",options=sport)
    temp=helper.most_success(df,selected_sport)
    st.table(temp)

if user_menu == "Country-wise Analysis":
    st.sidebar.title(f"Country-wise Analysis")
    years , countries = helper.country_year_list(df)
    s_country = st.sidebar.selectbox('Select country',countries)
    final = helper.countrywise_medal(df,s_country)
    fig = px.line(final,x='Year',y='Medal')
    st.title(f"Medal over the years for {s_country}")
    st.plotly_chart(fig)

    st.title(s_country + " excels in the following sports")
    pt = helper.country_event_heatmap(df,s_country)
    fig, ax = plt.subplots(figsize=(20, 20))
    sns.heatmap(pt,annot=True)
    st.pyplot(fig)

    st.title("Top 10 athletes of " + s_country)
    top10_df = helper.most_successful_countrywise(df,s_country)
    st.table(top10_df)

if user_menu == 'Athelete-wise Analysis':
    
    athelete_df = df.drop_duplicates(subset=['Name','region'])
    medal = athelete_df['Age'].dropna()
    gold_medal = athelete_df[athelete_df['Medal'] == 'Gold']['Age'].dropna()
    silver_medal = athelete_df[athelete_df['Medal'] == 'Silver']['Age'].dropna()
    bronze_medal = athelete_df[athelete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([medal,gold_medal,silver_medal,bronze_medal],['Overall Age','Gold medalist','Silver medalist','Bronze medalist'],show_hist=False,show_rug=False)
    fig.update_layout(autosize=False,width=1000,height=500)
    st.title('Probability Distribution of medal winning odds against Age')
    st.plotly_chart(fig)

    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War',            'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    x = []
    name = []
    for sport in famous_sports:
        temp = athelete_df[athelete_df['Sport'] == sport]
        x.append(temp[(temp['Medal'] == 'Gold') | (temp['Medal'] == 'Silver') |(temp['Medal'] == 'Bronze')]['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x,name,show_hist=False,show_rug=False)
    fig.update_layout(autosize=False,width=1000,height=500)
    st.title('Probability Distribution of medal winning odds in each sport against Age')
    st.plotly_chart(fig)

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    st.title('Height Vs Weight')
    selected_sport = st.selectbox('Select a Sport', sport_list)
    selected_gender = st.selectbox('Select a Gender', ['All','M','F'])

    temp_df = helper.weight_v_height(df,selected_sport,selected_gender)
    fig , ax = plt.subplots()
    sns.scatterplot(x=temp_df['Weight'],y=temp_df['Height'],hue=temp_df['Medal'],style=temp_df['Sex'],s=30).set_xlabel('Weight in lbs')
    st.pyplot(fig)

    st.title("Men Vs Women Participation Over the Years")
    final = helper.men_vs_women(df)
    fig = px.line(final, x="Year", y=["Male", "Female"])
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)