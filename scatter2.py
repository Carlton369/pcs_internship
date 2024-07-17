import pandas as pd
import altair as alt
import streamlit as st
import numpy as np

def scatter_plot(apps_df,reviews_df):
    # Calculate the average rating for each app
    avg_ratings = apps_df.groupby("App")["Rating"].mean().reset_index()

    # Calculate the average sentiment polarity for each app
    avg_sentiments = reviews_df.groupby("App")["Sentiment_Polarity"].mean().reset_index()

    # Merge the two datasets on the app name
    merged_df = pd.merge(avg_ratings, avg_sentiments, on="App")
    merged_df = merged_df.dropna()

    scatter = alt.Chart(merged_df).mark_point().encode(
        x=alt.X("Rating", scale=alt.Scale(domain=[2.6, 5])),  
        y="Sentiment_Polarity",
        tooltip=["App", "Rating", "Sentiment_Polarity"]
    )

    # Create a regression line chart
    regression = alt.Chart(merged_df).mark_line(color="lime").transform_regression(
        "Rating", "Sentiment_Polarity"
    ).encode(
        x="Rating",
        y="Sentiment_Polarity"
    )

    # Layer the scatterplot and regression line
    chart = alt.layer(scatter, regression)
    
    # Create a Streamlit app
    st.title("Average Rating vs Average Sentiment Polarity")
    st.write("This scatter plot shows the relationship between the average rating and average sentiment polarity for each app.")
    st.altair_chart(chart, use_container_width=True)

    corr_matrix = np.corrcoef(merged_df['Rating'], merged_df['Sentiment_Polarity'])
    corr = corr_matrix[0,1]
    R_sq = corr**2
    
    st.write(f'R-value: {R_sq}')
    st.write('Very weak positive linear correlation between Sentiment Polarity and Rating')