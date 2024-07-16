import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import re 
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="yeet",page_icon="chart_with_upwards_trend", layout="wide", initial_sidebar_state="auto", menu_items=None)

#importing functions from other files 

import charts as cr
import reviews as rv
import multivariable as mv
import scatter2 as sc

def decrement_slider_value():
    st.session_state.slider_value -= 1

def increment_slider_value():
    st.session_state.slider_value += 1

def init_slider():
    if 'slider_value' not in st.session_state:
        st.session_state.slider_value = 10

    # Create a column layout
    col1, col2, col3 = st.columns([2, 25, 2])

    # Create the '-' button
    with col1:
        st.button(':heavy_minus_sign:', on_click=decrement_slider_value)
    
    # Create the slider bar
    with col2:
        st.session_state.slider_value = st.slider('Select Value', 1, 33, value=st.session_state.slider_value)
 
    # Create the '+' button
    with col3:
        st.button(':heavy_plus_sign:', on_click=increment_slider_value)

def top_n_barchart(cat_df) -> None:
    """
    Visualize the top N categories by number of apps in a bar chart.
    """
    # Create Streamlit widgets
    init_slider()
    top_n = st.session_state.slider_value
    # Group the data by Category and count the number of apps in each category

    selected_variable = st.selectbox("Select variable", cat_df.columns[1:])
    # Sort the categories by count in descending order and get the top N
    top_categories = cat_df.sort_values(selected_variable, ascending=False).head(top_n)
    var_min = min(top_categories[selected_variable])
    var_max = max(top_categories[selected_variable])

    # Create the bar chart
    fig = px.bar(top_categories, x="Category", y=selected_variable, color="Category", 
                category_orders={"Category": top_categories["Category"].tolist()}, 
                title=f"Top {top_n} Categories by {selected_variable}")

    # Customize the layout
    fig.update_layout(
        dragmode=False,
        selectdirection = "h",
        width=900,
        height=600,
        xaxis=dict(
            title="Category",
            tickangle=80,
            tickfont=dict(size=12)
        ),
        yaxis=dict(
            title=selected_variable,
            range=[var_min - (var_min*0.01), var_max + (var_max*0.01)]
        )
    )

    # Define the function to call when a bar is clicked
   
    if 'selected_category' not in st.session_state:
        st.session_state.selected_category = None

    def handle_click(trace, points, state):
        if points.point_inds:
            category = points.points[0].x
            st.session_state.selected_category = category

    fig.data[0].on_click(handle_click)

    if st.session_state.selected_category:
        #top_apps = get_top_apps(st.session_state.selected_category)
        st.subheader(f"Top 10 apps in {st.session_state.selected_category}")
        st.write(cat_df[selected_variable])
    # Display the chart in Streamlit
    st.plotly_chart(fig, use_container_width=True)

def piechart(df):
    init_slider()
    # Access the slider value
    current_slider_value = st.session_state.slider_value

    top_categories = df.groupby('Category')['Installs'].sum().nlargest(current_slider_value)
    top_categories_df = df[df['Category'].isin(top_categories.index)]
    
    # Aggregate installs per category
    installs_per_category = top_categories_df.groupby('Category')['Installs'].sum().reset_index()

    fig = px.sunburst(top_categories_df, path=['Type', 'Category', 'Content Rating'], values='Installs', color='Content Rating',   color_discrete_sequence=px.colors.qualitative.Set2)
    
    fig.update_layout(width=800, height=600)  # adjust the size as needed

    st.plotly_chart(fig,use_container_width=True)

def linegraph(df):
    init_slider()
    top_n = st.session_state.slider_value
    # Calculate Rating Frequency by Category
    rating_counts = df.groupby(['Category', 'Rating']).size().reset_index(name='Count')

    # Step 2: Get top 10 categories by count
    top_categories = df['Category'].value_counts().nlargest(top_n).index

    # Filter rating_counts for top 10 categories
    rating_counts = rating_counts[rating_counts['Category'].isin(top_categories)]

    # Create Line Chart using Altair
    line_chart = alt.Chart(rating_counts).mark_line().encode(
        x='Rating:Q',
        y='Count:Q',
        color='Category:N',
        tooltip=['Category:N', 'Rating:Q', 'Count:Q']
    ).properties(
        width=1000,
        height=400,
    )
    st.altair_chart(line_chart)

def bubble_plot(cat_df):
    fig = go.Figure(data=[go.Scatter(
    x=cat_df['Average Size (MB)'],
    y=cat_df['Total Installs (M)'],
    mode='markers',
    marker=dict(
        size=cat_df['Average Rating'] - 3.9,
        sizemin=5,  # minimum size of the bubbles
        sizeref=2.*max(cat_df['Average Rating'])/(30.**2),  # scale factor for the bubble sizes
        color=cat_df['Average Rating'],  # color by average rating
        colorscale='Viridis',  # set color scale to Viridis
        showscale=True,  # show color bar
    ),
    hovertemplate="<br>".join([
        "Category: %{customdata[0]}",
        "Average Rating: %{marker.size:.2f}",
        "Total Installs (M): %{y:.0f}",
        "Average Size (MB): %{x:.2f}"
    ]) + "<extra></extra>",
    customdata=cat_df[['Category']]  # pass the Category column as custom data
    )])

    fig.update_layout(
        autosize=False,
        width=1000, 
        height=700,  
    )
        

    st.plotly_chart(fig)

def box_plot(df):
    selected_variables = st.multiselect('Select variables', df['Category'].unique(),default='ART_AND_DESIGN')
    filtered_df = df[df['Category'].isin(selected_variables)]
    Q1 = np.percentile(filtered_df['Rating'], 25)
    Q3 = np.percentile(filtered_df['Rating'], 75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    # Create the boxplot
    chart = alt.Chart(filtered_df).mark_boxplot(color='#3B7EEB', clip = True).encode(
        x='Category:N',
        y=alt.Y('Rating:Q',scale=alt.Scale(domain=[lower_bound,upper_bound]))
    )
    chart = chart.properties(
    title="Rating Distribution by Category",
    width=400,
    height=600
)
    # Display the chart 
    st.altair_chart(chart, use_container_width=True)

def compat_plot(df):
    df['Android Ver'] = df['Android Ver'].str[:3].replace('and up','')
    df = df.dropna(subset=['Android Ver'])
    df = df[~df['Android Ver'].str.contains('Var', na=False)]
    df['Android Ver'] = df['Android Ver'].astype(float)
   
    fig = px.scatter(df,x="Android Ver", y="Installs")
    st.plotly_chart(fig, use_container_width=True)

# read in the data
df = pd.read_csv('googleplaystore.csv')
rev_df =  pd.read_csv("googleplaystore_user_reviews.csv")

# format "installs" into strings for numerical analysis
df['Installs'] = df['Installs'].str.replace('+','').str.replace(',','')
df['Installs'] = df['Installs'].astype(int)

# format "size"
df.dropna(inplace=True)

def convert_size_to_mb(size_str):
    match = re.search(r'(\d+(?:\.\d+)?)', size_str)  # extract numeric part
    if match:
        value = float(match.group(1))
        if size_str.endswith('k'):
            return value / 1024
        elif size_str.endswith('M'):
            return value
        else:
            return value
    else:
        return np.nan  # or some other default value
    
df['Size'] = df['Size'].apply(convert_size_to_mb)
df['Price'] = df['Price'].apply(mv.convert_price_to_numeric)

# create new data frame holding the following variables 
data = {
    'Average Rating': df.groupby('Category')['Rating'].mean(),
    'Average Size (MB)': df.groupby('Category')['Size'].mean(),
    'Total Installs (M)': df.groupby('Category')['Installs'].sum()/1000000,
    'Number of Apps': df.groupby('Category').size(),
    'Number of Reviews': df.groupby('Category')['Reviews'].sum()
    }


cat_df = pd.DataFrame(data).reset_index()
cat_df.columns = ['Category'] + list(data.keys())

# Create tabs for different visualizations

st.sidebar.image("pcss.png")
col1,col2=st.sidebar.columns(2)
with col1:
    st.image('steve_photo.jpg')
with col2:
    st.image('reynard_photo.jpg')

tab_selection = st.sidebar.radio(
    'Select Visualization', 
    ['Distribution of Installs across Categories',
     'Bubble Plot',
     'Box Plot',
     'Scatter Plot',
     'Reviews',
     'Multivariate',
     'Two Charts',
     'Check DFs'])


#if tab_selection == 'Analysis of Rating Frequency':
#    st.header('Analysis of Rating Frequency')
#    linegraph(df)
if tab_selection == 'Distribution of Installs across Categories':
    st.header('Distribution of Installs across Categories')
    piechart(df)
#elif tab_selection == 'Comparison between Categories':
#   st.header('Comparison between Categories')
#  top_n_barchart(cat_df)
elif tab_selection == 'Bubble Plot':
    st.header('Bubble Plot')
    bubble_plot(cat_df)
elif tab_selection == 'Box Plot':
    box_plot(df)
#elif tab_selection == 'Compatibility':
#    compat_plot(df)
elif tab_selection == 'Scatter Plot':
    sc.scatter_plot(df,rev_df)
elif tab_selection == 'Reviews':
    rv.rev_plot(rev_df)
elif tab_selection == 'Multivariate':
    mv.plot_multivariate(df)
    mv.display_results(df)
elif tab_selection == 'Two Charts':
    cr.top_n_barchart_2(df)
elif tab_selection == 'Check DFs':
    st.write(df)
    st.write(cat_df)