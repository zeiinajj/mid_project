import calendar
import streamlit as st
import pandas as pd 
import plotly.express as px 
from plotly.subplots import make_subplots

#set page layout
st.set_page_config(layout='wide')

st.title("Billboard Hot 100 Analysis")

df=pd.read_csv("billboard_complete.csv")
df["chart_week"] =pd.to_datetime(df["chart_week"])

df["Month"] = df["chart_week"].dt.month
df["Year"] = df["chart_week"].dt.year
df['Month'] = df['Month'].apply(lambda x: calendar.month_name[x])

# dropping inaccurate rows
df = df[~df['Year'].isin([1976, 1977])]

sequence=['hotpink','rebeccapurple']


years=list(df['Year'].unique())




def page1():
    st.header('Visualization results')
    tab1 , tab2  = st.tabs(['genres' , 'duration' ])
    
    # start put charts in each tab 
    
    with tab1:
    
        genres=['country','r&b','pop','christmas','rap','trap','k-pop','hip hop',
        'drill','edm','afrobeats','rock','punk rock','latin']
        genre=st.selectbox("Select a genre",genres)
        st.write(genre)
        df['genre(s)'].fillna(" ")
        x=df[df['genre(s)'].str.contains(genre, case=False, regex=False, na=False)]
        xx=x[x['current_week']<=10]
        st.plotly_chart(px.histogram(data_frame=xx , x = 'Month' , text_auto=True ))

            
    with tab2:
    
        mask=df[df['duration-ms']<=500000] # to ignore outliers
        st.plotly_chart(px.histogram(mask, x='duration-ms', title='Distribution of Song Durations',labels={'duration-ms': 'Duration (ms)'}))
    
    
    # with tab3:
    
    #     st.plotly_chart(px.scatter(data_frame=df , x = 'genre(s)' , y = 'tempo' , color = 'explicit'))
    

def page2():
    st.header('Percentage of explicit songs in the top 100')
    fig = make_subplots(
    rows=3, 
    cols=2, 
    specs=[
        [{"type": "domain"}, {"type": "domain"}],  
        [{"type": "domain"}, {"type": "domain"}],  
        [{"type": "domain"}, {"type": "domain"}]   
    ],
    subplot_titles=[
        "2025 Explicit Tracks", "2024 Explicit Tracks",
        "2023 Explicit Tracks", "2022 Explicit Tracks",
        "2021 Explicit Tracks", "2020 Explicit Tracks"
    ]
    )

    # Helper function to add pie charts
    def add_pie(fig, year, row, col, sequence):
        mask = df[df['Year'] == year]
        pie = px.pie(
            data_frame=mask, 
            names='explicit', 
            color_discrete_sequence=sequence,
            title=f"Explicit Tracks in {year}",
            hole=0.3
        )
        fig.add_trace(pie.data[0], row=row, col=col)

    
    add_pie(fig, 2025, 1, 1, sequence)
    add_pie(fig, 2024, 1, 2, sequence)
    add_pie(fig, 2023, 2, 1, sequence)
    add_pie(fig, 2022, 2, 2, sequence)
    add_pie(fig, 2021, 3, 1, sequence)
    add_pie(fig, 2020, 3, 2, sequence)


    fig.update_layout(
    height=1000,  
    title_text="Percentage of Explicit Tracks by Year",
    showlegend=False  
    )
    st.plotly_chart(fig)
    




def page3():
    st.header("Audio features affecting track's position in the top 100")
    tab1 , tab2  = st.tabs(['correlation' , 'scatterplots' ])
    with tab1:
        audio_features = df[['loudness', 'energy', 'danceability', 'tempo', 'duration-ms']]

        corr = audio_features.corr()

        st.plotly_chart(px.imshow(
            corr, 
            text_auto=True, 
            title='Correlation Matrix of Audio Features',
            labels=dict(x="Feature", y="Feature", color_continuous_scale="RdBu")
        ))
    
    with tab2:
        years=list(df['Year'].unique())
        audio_features = ['loudness', 'energy', 'danceability', 'tempo', 'duration-ms']
        year=st.select_slider('select year',years)
        st.write(year)
        feature=st.radio('select feature',audio_features)
        st.write(feature)
        
        mask=df[df['Year']==year]
        st.plotly_chart(px.scatter(
            mask,  x='current_week',  y=feature, 
            title=f'{feature} vs. Chart Position',
            labels={'current_week': 'Current Week Position'}
        ))
    

pages = {
    'Genres' : page1,
    'Explicitness' : page2,
    'Audio features' : page3
}

pg = st.sidebar.radio('Navigate between pages' , pages.keys())

pages[pg]()
