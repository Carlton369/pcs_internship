import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration
#st.set_page_config(page_title="Google Play Store App Analysis", page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)

# App title
st.title("Google Play Store App Analysis")

# Load the data
df = pd.read_csv('googleplaystore.csv')

# Create Streamlit widgets for user input
top_n_options = [i for i in range(1, 34)]  # Define the options for the dropdown box
top_n = st.selectbox('Select the number of top categories:', top_n_options, index=14)

# Group the data by Category and count the number of apps in each category
category_counts = df.groupby('Category').size().reset_index(name='Count')

# Sort the categories by count in descending order and get the top N
top_categories = category_counts.sort_values('Count', ascending=False).head(top_n)

# Create the bar chart with Plotly
bar_chart = px.bar(
    top_categories,
    x='Category',
    y='Count',
    color='Category',
    title=f'Top {top_n} Categories by Number of Apps',
    labels={'Count': 'Number of Apps'},
    height=500
)

# Update layout for better readability
bar_chart.update_layout(
    xaxis_title='Category', 
    yaxis_title='Number of Apps', 
    xaxis_tickangle=-45
)

# Display the chart in Streamlit
st.plotly_chart(bar_chart, use_container_width=True)

# Create a dropdown to select a category from the top N categories
if 'selected_category' not in st.session_state:
    st.session_state.selected_category = top_categories['Category'].iloc[0]

selected_category = st.selectbox(
    'Select a category:',
    top_categories['Category'],
    index=top_categories['Category'].tolist().index(st.session_state.selected_category)
)

# Update session state with the selected category
st.session_state.selected_category = selected_category

# Function to display top 10 apps for the selected category
def display_top_apps(category: str):
    category_df = df[df['Category'] == category]
    top_apps = category_df.sort_values('Rating', ascending=False).head(10)
    st.write(f'**Top 10 Apps in {category} based on Ratings:**')
    st.write(top_apps[['App', 'Rating']])

# Display the top 10 apps for the selected category
display_top_apps(st.session_state.selected_category)