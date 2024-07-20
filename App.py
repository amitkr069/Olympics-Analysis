import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import  seaborn as sns
import preprocess, helper
import plotly.figure_factory as ff
df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

df = preprocess.preprocessor(df, region_df)
st.sidebar.title("Olympics Analysis")
st.sidebar.image("earth-1585817_1280.jpg")
user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally', 'Overall Analysis', 'Country-wise Analysis', 'Athelete wise Analysis')
)

# st.dataframe(df)

if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")

    years, country = helper.country_year_list(df)
    selected_year = st.sidebar.selectbox("Select Year", years)
    selected_country = st.sidebar.selectbox("Select Country", country)

    medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country)
    st.dataframe(medal_tally)

if user_menu == 'Overall Analysis':
    editions = df['Year'].nunique() -1
    cities = df['City'].nunique()
    sports = df['Sport'].nunique()
    events = df['Event'].nunique()
    athletes = df['Name'].nunique()
    nations = df['region'].nunique()

    st.title("Top statistics")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Athletes")
        st.title(athletes)
    with col3:
        st.header("nations")
        st.title(nations)

    nations_over_time = helper.participating_nations_over_time(df)
    fig = px.line(nations_over_time, x='Edition', y='No_of_countries')
    st.title("Participating nations over the years")
    st.plotly_chart(fig)

    events_over_time = helper.all_events_over_time(df)
    fig = px.line(events_over_time, x='Edition', y='No_of_Events')
    st.title("All the Events over the years")
    st.plotly_chart(fig)

    athletes_over_time = helper.all_athletes_over_time(df)
    fig = px.line(athletes_over_time, x='Edition', y='No_of_Athletes')
    st.title("Athletes Participating over the years")
    st.plotly_chart(fig)

    st.title("No. of Events over time(Every Sport)")
    fig, ax = plt.subplots(figsize=(25, 25))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'), annot=True)
    st.pyplot(fig)

    st.title("Most Successful Atheletes")
    sport_list = df['Sport'].unique().tolist()  # sport waale column ka saara unique nikalke list me daal diye
    sport_list.sort()
    sport_list.insert(0, 'Overall')
    selected_sport = st.selectbox('Select a Sport', sport_list)
    x = helper.most_successful(df, selected_sport)
    st.table(x)


if user_menu == 'Country-wise Analysis':

    st.sidebar.title('Country-wise Analysis')

    # country_list = df['region'].unique().tolist() # isme nan values v hai to usko v hatana h
    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()
    selected_country = st.sidebar.selectbox('Select a country', country_list)
    country_df = helper.year_wise_medal_tally(df, selected_country)
    fig = px.line(country_df, x='Year', y='Medal')
    st.title(selected_country + "'s Medal Tally over the years")
    st.plotly_chart(fig)


    st.title(selected_country + " excels in the following sports")
    pt = helper.country_event_heatmap(df, selected_country)
    fig, ax = plt.subplots(figsize=(20, 20))
    ax = sns.heatmap(pt, annot=True)
    st.pyplot(fig)


    st.title("Top 10 athletes of " + selected_country)
    top10_df = helper.most_successful_ath(df, selected_country)
    st.table(top10_df)



if user_menu == 'Athelete wise Analysis':
    athelete_df = df.drop_duplicates(subset=['Name', 'region'])
    x1 = athelete_df['Age'].dropna()
    x2 = athelete_df[athelete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athelete_df[athelete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athelete_df[athelete_df['Medal'] == 'Bronze']['Age'].dropna()
    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title('Distribution of Age')
    st.plotly_chart(fig)

    famous_sports1 = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics', 'Swimming']
    x = []
    name = []
    for sport in famous_sports1:
        temp_df = athelete_df[athelete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title('Distribution of Age wrt sports(Gold medalist)')
    st.plotly_chart(fig)

    sport_list = df['Sport'].unique().tolist()  # sport waale column ka saara unique nikalke list me daal diye
    sport_list.sort()
    sport_list.insert(0, 'Overall')
    st.title("Height vs Weight")
    selected_sport = st.selectbox('Select a Sport', sport_list)
    temp_df = helper.weight_v_height(df, selected_sport)

    fig, ax = plt.subplots()
    ax = sns.scatterplot(x='Weight', y='Height', hue='Medal', data=temp_df, style=temp_df['Sex'], s=60)

    st.pyplot(fig)

    st.title("Men vs Women participatoin")
    final = helper.men_vs_women(df)
    fig = px.line(final, x='Year', y=['Male', 'Female'])
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)
