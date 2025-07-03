################################################ DIVVY BIKES DASHABOARD #####################################################

################################################ Libraries Import #####################################################

import streamlit as st
import pandas as pd 
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from streamlit_keplergl import keplergl_static 
from keplergl import KeplerGl
from datetime import datetime as dt 
from numerizer import numerize
from PIL import Image
import humanize
import seaborn as sns
import plotly.express as px

########################### Initial settings for the dashboard ##################################################################
st.set_page_config(page_title = 'New York 2022 Divvy Bikes Strategy Dashboard', layout='wide')
st.title("New York 2022 Divvy Bikes Strategy Dashboard")
st.markdown("The dashboard will help with the expansion problems Divvy currently faces")


# Define side bar
st.sidebar.title("Aspect Selector")
page = st.sidebar.selectbox('Select an aspect of the analysis',
  ["Intro page","Weather component and bike usage",
   "Most popular stations",
    "Interactive map with aggregated bike trips","Top 10 Ride Durations by Rideable Type", "Recommendations"])
########################## Import data ###########################################################################################

df = pd.read_csv('reduced_data_to_plot.csv')
top20 = pd.read_csv('top20.csv', index_col = 0)


# ######################################### DEFINE THE PAGES #####################################################################
### Intro page

if page == "Intro page":
    st.markdown("#### This dashboard aims at providing helpful insights on the expansion problems Divvy Bikes currently faces.")
    st.markdown("Right now, Divvy bikes runs into a situation where customers complain about bikes not being available at certain times. This analysis will look at the potential reasons behind this. The dashboard is separated into 5 sections:")
    st.markdown("- Weather component and bike usage")
    st.markdown("- Most popular stations")
    st.markdown("- Interactive map with aggregated bike trips")
    st.markdown("- Top 10 Ride Durations by Rideable Type")
    st.markdown("- Recommendations")
    st.markdown("The dropdown menu on the left 'Aspect Selector' will take you to the different aspects of the analysis our team looked at.")

    myImage = Image.open("new_york_bike.jpg") #source: https://www.freepik.com/free-ai-image/rainbow-end-road-landscape_225568023.htm#fromView=search&page=1&position=17&uuid=33cedaed-0091-4218-8adc-ebe48e4c0929&query=new+york+bike
    st.image(myImage)

# ######################################### Weather component and bike usage #####################################################################
### Create the dual axis line chart page ###
    
elif page == 'Weather component and bike usage':

    fig_2 = make_subplots(specs = [[{"secondary_y": True}]])

    fig_2.add_trace(
    go.Scatter(x = df['date'], y = df['bike_rides_daily'], name = 'Daily bike rides', marker={'color': df['bike_rides_daily'],'color': 'blue'}),
    secondary_y = False
    )

    fig_2.add_trace(
    go.Scatter(x=df['date'], y = df['temp'], name = 'Daily temperature', marker={'color': df['temp'],'color': 'red'}),
    secondary_y=True
    )

    fig_2.update_layout(
    title = 'Daily bike trips and temperatures in 2022',
    height = 400
    )

    st.plotly_chart(fig_2, use_container_width=True)
    st.markdown("The dual-axis line chart shows daily bike trips and temperatures throughout 2022. It reveals a clear relationship between    temperature and bike usage. During the colder months—January, February, November, and December—daily temperatures often drop below 0°C, and bike usage tends to increase, peaking on days when temperatures are especially low. This suggests that in cold weather, people may prefer biking over walking to reduce exposure time to uncomfortable conditions.")

    st.markdown("In contrast, from April to October, when daily temperatures rise and often stay above 15–20°C and in some cases above 30°C, there is a noticeable decline in bike trips. This trend indicates that in warmer conditions, people may favor walking instead of biking, as cycling requires more physical effort and generates additional body heat, which can be uncomfortable during hot weather. Overall, the chart suggests an inverse correlation between temperature and bike usage: bike trips rise as temperatures fall and decrease as temperatures climb.")
    st.markdown("How much would you recommend scaling bikes back between November and April?")

# ######################################### Most popular stations #####################################################################

### Create the season variable

elif page == 'Most popular stations':
    
    # Create the filter on the side bar
    
    with st.sidebar:
        season_filter = st.multiselect(label= 'Select the season', options=df['season'].unique(),
    default=df['season'].unique())

    df1 = df.query('season == @season_filter')
    
    # Define the total rides
    total_rides = float(df1['bike_rides_daily'].sum())    
    st.metric(label = 'Total Bike Rides', value= humanize.intword(total_rides))
    
    # Bar chart

    df1['value'] = 1 
    df_groupby_bar = df1.groupby('start_station_name', as_index = False).agg({'value': 'sum'})
    top20 = df_groupby_bar.nlargest(20, 'value')
    fig = go.Figure(go.Bar(x = top20['start_station_name'], y = top20['value']))

    fig = go.Figure(go.Bar(x = top20['start_station_name'], y = top20['value'], marker={'color':top20['value'],'colorscale': 'Blues'}))
    fig.update_layout(
    title = 'Top 20 most popular bike stations in New York 2022',
    xaxis_title = 'Start stations',
    yaxis_title ='Sum of trips',
    width = 900, height = 600
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("Based on the analysis of the bar chart, the top 20 most common bike stations in New York during 2022 are primarily located in Manhattan. The top three stations are 11 Ave & W 41 St, E 20 St & 2 Ave, and W 27 St & 7 Ave. This suggests that most riders begin or end their trips within Manhattan. Although there are stations in New Jersey and Brooklyn, they appear far less frequently among the most popular locations. This finding can be cross-referenced with the interactive map.")
    st.markdown("What are some ideas for ensuring bikes are always stocked at the most popular stations?")

# ######################################### Interactive map with aggregated bike trips #####################################################################
elif page == 'Interactive map with aggregated bike trips': 

    ### Create the map ###

    st.write("Interactive map showing aggregated bike trips over New York 2022")

    path_to_html = "kepler.gl.html" 

    # Read file and keep in variable
    with open(path_to_html,'r') as f: 
        html_data = f.read()

    ## Show in webpage
    st.header("Aggregated Bike Trips in New York 2022")
    st.components.v1.html(html_data,height=1000)
    st.markdown("## Key Insights of Trips with over 1000 counts.")
    st.markdown("#### High-Density Bike Corridors in Manhattan:")
    st.markdown("The majority of high-volume bike trips start and end within Manhattan.")
    st.markdown("Especially dense activity appears between Midtown Manhattan, Lower Manhattan, and East Village areas.")
    st.markdown("This suggests a strong commuting pattern or tourist-heavy bike usage in central locations.")
    st.markdown("#### Popular Start & End Zones:")
    st.markdown("Central Park South and the Hudson River Greenway area show dense clusters of green and red dots, implying frequent usage.")
    st.markdown("Battery Park and Brooklyn Bridge entry/exit points also show high trip termination or origin.")
    st.markdown("#### Absence of Trips in Some Boroughs")
    st.markdown("The Bronx, Queens, and much of Brooklyn are underrepresented in this filtered data (due to the 1,000-trip threshold), indicating these routes see less frequent use or more distributed trip paths.")
    st.markdown("How could you determine how many more stations to add along the water?")

 # ######################################### Top 10 Ride Durations by Rideable Type #####################################################################

elif page == 'Top 10 Ride Durations by Rideable Type':   

    st.header("Top 10 Ride Durations by Rideable Type")
    # FacetGrids for Bike Type and ride duration
# Get the top 10 ride durations
    top_10 = df['ride_duration'].value_counts().nlargest(10).index
    df_top10 = df[df['ride_duration'].isin(top_10)]
    
# Plot with Plotly Express histogram
    fig = px.histogram(
    df_top10,
    x='ride_duration',
    color='rideable_type',
    facet_col='rideable_type',
    facet_col_wrap=2,
    nbins=10,  # same as bins=10 in seaborn
    opacity=0.8,
    color_discrete_sequence=['#1f77b4', '#2ca02c']  # adjust colors if you like
)

    fig.update_layout(
    title='Top 10 Ride Durations by Rideable Type',
    xaxis_title='ride_duration',
    yaxis_title='Count',
    width=900,
    height=600
)

    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))  # Remove 'rideable_type='

    st.plotly_chart(fig, use_container_width=True)
    st.markdown("## Duration of rides (filtered to only the top 10 most common durations).")
    st.markdown("#### Shape of distribution.")
    st.markdown("Both types have a roughly bell-like distribution and a right skew within the filtered top 10 durations.")
    st.markdown("This means that for both classic and electric bikes, most rides cluster around mid-range durations, around 5–7 minutes.")
    st.markdown("#### Counts.")
    st.markdown("The counts are high for classic bikes, slightly lower for electric bikes.")
    st.markdown("This suggests classic bikes might be used more frequently overall, or have more rides that fall into these top durations.")
    st.markdown("#### Summary.")
    st.markdown("The histogram shows that most rides cluster around short, specific durations for both classic and electric bikes, with classic bikes having slightly more rides overall for these durations. Riders appear to prefer similar trip lengths regardless of bike type.")

 # ######################################### Conclusions and recommendations #####################################################################
else:
    
    st.header("Conclusions and recommendations")
    st.markdown("## Possible next steps by Aspect:")
    st.markdown("#### Weather component and bike usage")
    st.markdown("Consider increasing bike availability during the colder months (November through March) to meet potential demand.")
    st.markdown("#### Most popular stations")
    st.markdown("Focus on maintaining and expanding bike availability and station capacity in Manhattan, especially near the top three stations, to meet high demand and improve rider convenience.")
    st.markdown("#### Interactive map with aggregated bike trips")
    st.markdown("Enhance bike infrastructure and station capacity in Midtown, Lower Manhattan, and the East Village to support heavy demand, while exploring opportunities to expand service and promote usage in underrepresented areas like the Bronx, Queens, and outer Brooklyn.")
    st.markdown("#### Top 10 Ride Durations by Rideable Type")
    st.markdown("Since classic bikes account for more rides within the most common short trip durations, prioritize maintaining and expanding the classic bike fleet to meet this higher demand. Ensure stations are well-stocked with classic bikes, especially in high-traffic areas, to align with riders’ clear preference for this bike type on short to mid-range trips.")
    bikes = Image.open("bike_ny.jpg")  #source: https://www.freepik.com/free-ai-image/man-front-empire-state-building_72608481.htm#fromView=search&page=1&position=4&uuid=d45880f8-01f8-4b31-844a-84c82841fc26&query=new+york+city+bike
    st.image(bikes)