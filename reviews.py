import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def rev_plot(data):
    # Create a Streamlit app
    st.title("Google Play Store User Reviews")
    st.markdown('<h2 style="font-size:24px;"> Select an Application </h2>',unsafe_allow_html=True )

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

    total_reviews = data.groupby("App").size().reset_index(name="total_count")

    positives = positives.merge(total_reviews, on="App")
    negatives = negatives.merge(total_reviews, on="App")
    neutrals = neutrals.merge(total_reviews, on="App")

    positives["Percentage"] = (positives["count"] / positives["total_count"]) * 100
    negatives["Percentage"] = (negatives["count"] / negatives["total_count"]) * 100
    neutrals["Percentage"] = (neutrals["count"] / neutrals["total_count"]) * 100

    most_positives = positives.nlargest(3, "Percentage")
    most_negatives = negatives.nlargest(3, "Percentage")
    most_neutrals = neutrals.nlargest(3, "Percentage")

    # Display the results
    st.write("Top 3 apps with the highest percentage of:")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("Positives:")
        for i, row in most_positives.iterrows():
            st.write(f"    - {row['App']} ({int(round(row['Percentage']))}%)")
    with col2:
        st.write("Negatives:")
        for i, row in most_negatives.iterrows():
            st.write(f"    - {row['App']} ({int(round(row['Percentage']))}%)")
    with col3:
        st.write("Neutrals:")
        for i, row in most_neutrals.iterrows():
            st.write(f"    - {row['App']} ({int(round(row['Percentage']))}%)")