import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def rev_plot(data):
    # Create a Streamlit app
    st.title("Google Play Store User Reviews")
    st.header("Select an application")

    # Get a list of unique applications
    apps = data["App"].unique()

    # Create a selectbox to select an application
    app_name = st.selectbox("Select an application", apps)

    # Filter the data for the selected application
    app_data = data[data["App"] == app_name]

    # Filter out null values in the Sentiment column
    app_data = app_data[app_data["Sentiment"].notna()]

    # Count the number of reviews for each sentiment
    sentiment_counts = app_data["Sentiment"].value_counts().reset_index()
    sentiment_counts.columns = ["Sentiment", "Count"]

    # Create a bar chart using Plotly
    fig = go.Figure()
    for sentiment, count in sentiment_counts.values:
        color = "blue" if sentiment == "Positive" else "red" if sentiment == "Negative" else "gray"
        fig.add_bar(x=[sentiment], y=[count], name=sentiment,
                    text=[str(count)], textposition='outside', marker_color=color,
                    textfont=dict(size=15))  # Adjust the font size here

    # Adjust the layout to provide more space for the text labels
    fig.update_layout(
        title=f"Number of Reviews for {app_name}",
        legend=dict(itemsizing="constant", orientation="h"),
        showlegend=True,
        barmode="group",
        xaxis=dict(title="Sentiment"),
        yaxis=dict(title="Count"),
        margin=dict(t=25)  # Increase the top margin to provide more space for text labels
    )

    # Display the chart
    st.plotly_chart(fig)

    # Calculate the app with the most number of positives, negatives, and neutrals
    positives = data[data["Sentiment"] == "Positive"].groupby("App").size().reset_index(name="count")
    negatives = data[data["Sentiment"] == "Negative"].groupby("App").size().reset_index(name="count")
    neutrals = data[data["Sentiment"] == "Neutral"].groupby("App").size().reset_index(name="count")

    most_positives = positives.loc[positives["count"].idxmax()]
    most_negatives = negatives.loc[negatives["count"].idxmax()]
    most_neutrals = neutrals.loc[neutrals["count"].idxmax()]

    # Display the results
    st.write("App with the most number of:")
    st.write(f"  - Positives: {most_positives['App']} ({most_positives['count']})")
    st.write(f"  - Negatives: {most_negatives['App']} ({most_negatives['count']})")
    st.write(f"  - Neutrals: {most_neutrals['App']} ({most_neutrals['count']})")
