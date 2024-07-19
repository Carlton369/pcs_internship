import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def rev_plot(data):
    # Create a Streamlit app
    st.title("Google Play Store User Reviews")

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

    # Display the results in a box with a pink border
    st.markdown("""
        <div style="border: 1.5pt solid pink; padding: 10px; border-radius: 5px; margin-bottom: 20px;">
            <h2 style="font-size:24px; text-align: left;">Top 3 apps with the highest percentage of:</h2>
            <div style="display: flex; justify-content: space-around; text-align: left;">
                <div style="flex: 1;">
                    <h3>Positives:</h3>
                    {}
                </div>
                <div style="flex: 1;">
                    <h3>Negatives:</h3>
                    {}
                </div>
                <div style="flex: 1;">
                    <h3>Neutrals:</h3>
                    {}
                </div>
            </div>
            <div style="height: 30px;"></div>
        </div>
    """.format(
        '<br>'.join([f"- {row['App']} ({int(round(row['Percentage']))}%)" for _, row in most_positives.iterrows()]),
        '<br>'.join([f"- {row['App']} ({int(round(row['Percentage']))}%)" for _, row in most_negatives.iterrows()]),
        '<br>'.join([f"- {row['App']} ({int(round(row['Percentage']))}%)" for _, row in most_neutrals.iterrows()])
    ), unsafe_allow_html=True)

    st.markdown('<h2 style="font-size:24px; text-align: left;">Review of Sentiment Application</h2>', unsafe_allow_html=True)

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

# Example usage (assuming you have a DataFrame named 'data')
# data = pd.read_csv("path_to_your_csv_file.csv")
# rev_plot(data)
