import streamlit as st
import pandas as pd
import preprocessor,helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff

df=pd.read_csv(r'C:\Users\Niraj Patil\OneDrive\Desktop\AllAboutOlympics\athlete_events.csv')
region_df=pd.read_csv(r'C:\Users\Niraj Patil\OneDrive\Desktop\AllAboutOlympics\noc_regions.csv')

df = preprocessor.preprocess(df,region_df)

st.sidebar.title("Summer Olympics Analysis")
st.sidebar.image(r'https://png.pngtree.com/png-vector/20220611/ourmid/pngtree-olympic-rings-colorful-rings-on-a-white-background-png-image_4825904.png')
user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally','Overall Analysis','Country-wise analysis','Athlete wise analysis')
)

if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years,country = helper.country_year_list(df)

    selected_year = st.sidebar.selectbox("Select Year",years)
    selected_country = st.sidebar.selectbox("Select Country", country)

    medal_tally = helper.fetch_medal_tally(df,selected_year,selected_country)

    if selected_year == 'Overall' and selected_country == 'All the Countries':
        st.title('Overall Tally')
    if selected_year != 'Overall' and selected_country == 'All the Countries':
        st.title('Medal Tally in ' + str(selected_year))
    if selected_year == 'Overall' and selected_country != 'All the Countries':
        st.title(selected_country+'\'s Overall Performance')
    if selected_year != 'Overall' and selected_country != 'All the Countries':
        st.title(selected_country+'\'s Performance in the Year '+ str(selected_year))
    st.table(medal_tally)

if user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title("Top Statistics")

    col1,col2,col3 = st.columns(3)
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
        st.header("Nations")
        st.title(nations)
    with col3:
        st.header("Athletes")
        st.title(athletes)

    nations_over_time = helper.participating_nations_over_time(df)
    fig = px.line(nations_over_time, x='Edition', y='No. of Countries')
    st.title("Participating Nations over the Years")
    st.plotly_chart(fig)

    events_over_time = helper.number_of_events_over_time(df)
    fig = px.line(events_over_time, x='Edition', y='Event')
    st.title("Events over the Years")
    st.plotly_chart(fig)

    athletes_over_time = helper.number_of_athletes_over_time(df)
    fig = px.line(athletes_over_time, x='Edition', y='No. of Athletes')
    st.title("No. of Athletes over the Years")
    st.plotly_chart(fig)

    st.title('No. of Events over time (Every Sport)')
    fig,ax = plt.subplots(figsize=(50,50))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),annot=True)
    st.pyplot(fig)


if user_menu == 'Country-wise analysis':

    st.sidebar.title('Country-wise Analysis')

    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()
    selected_country = st.sidebar.selectbox('Select a Country',country_list)

    country_df = helper.yearwise_medal_tally(df,selected_country)
    fig = px.line(country_df,x='Year',y='Medal')
    st.title(selected_country +'\'s Medal Tally over the years')
    st.plotly_chart(fig)

    st.title(selected_country + '\'s Sportwise Analaysis over the Years')
    pt = helper.country_event_heatmap(df,selected_country)
    fig,ax = plt.subplots(figsize=(20,20))
    if pt.size == 0:
        st.header(selected_country + ' has won no medals')
    else:
        ax = sns.heatmap(pt, annot=True)
        st.pyplot(fig)

if user_menu == 'Athlete wise analysis':
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],show_hist=False, show_rug=False)

    fig.update_layout(autosize=False,width=950,height=540)
    st.title("Distribution of Age")
    st.plotly_chart(fig)

    x = []
    name = []
    famous_sports = ['Basketball','Judo','Football','Tug-of-war','Athletics','Swimming','Badminton','Sailing','Gymnastics',
                'Art Competitions','Handball','Weightlifting','Wrestling','Water Polo','Hockey','Rowing','Fencing',
                'Shooting','Boxing','Taekwondo','Cycling','Diving','Canoeing','Tennis','Golf','Softball','Archery',
                'Rhythmic Gymnastics','Rugby Sevens','Beach Volleyball','Triathlon','Rugby','Polo','Ice Hockey','Cricket']

    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        gold_ages = temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna()
        if not gold_ages.empty:
            x.append(gold_ages)
            name.append(sport)
    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=950, height=540)
    st.title("Distribution of Age wrt Sport (only for Gold Medal winners)")
    st.plotly_chart(fig)

    st.title('Height vs Weight')
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')
    selected_sport = st.selectbox('Select a Sport', sport_list)
    temp_df = helper.weight_v_height(df,selected_sport)
    fig,ax = plt.subplots()
    ax = sns.scatterplot(x='Weight', y='Height', data=temp_df,hue=temp_df['Medal'],style=temp_df['Sex'],s=75)
    st.pyplot(fig)

    st.title('Men VS Women Participation over the Years')
    final = helper.men_vs_women(df)
    fig = px.line(final, x='Year', y=['Male', 'Female'])
    fig.update_layout(autosize=False, width=950, height=540)
    st.plotly_chart(fig)


