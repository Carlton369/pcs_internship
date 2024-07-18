import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
import plotly.express as px

# Convert the Installs column to a numeric type
def convert_installs_to_numeric(installs):
    try:
        if ',' in installs:
            installs = installs.replace(',', '')
        if '+' in installs:
            installs = installs.replace('+', '')
        return float(installs)
    except ValueError:
        return np.nan
#df['Installs'] = df['Installs'].apply(convert_installs_to_numeric)

# Convert the Size column to a numeric type
def convert_size_to_numeric(size):
    if 'M' in size:
        return float(size.replace('M', '')) / 1024
    elif 'k' in size:
        return float(size.replace('k', '')) /(1024 * 1024)
    elif size == 'Varies with device':
        return float('nan')
    else:
        return float(size)

#df['Size'] = df['Size'].apply(convert_size_to_numeric)

# Convert the Price column to a numeric type
def convert_price_to_numeric(price):
    if '$' in price:
        price = price.replace('$', '')
    if ',' in price:
        price = price.replace(',', '')
    return float(price)

#df['Price'] = df['Price'].apply(convert_price_to_numeric)

def plot_multivariate(df):
    # Display the header
    st.markdown('<h2 style="font-size:24px;"> Scatter Graph </h2>',unsafe_allow_html=True )
    # Create a dictionary to map category names to their corresponding columns
    category_cols = {
        "Rating": "Rating",
        "Reviews": "Reviews",
        "Size": "Size",
        "Installs": "Installs",
        "Price": "Price"
    }
    # Create a selectbox for x-axis and y-axis
    x_axis = st.selectbox("Select x-axis", list(category_cols.keys()))
    y_axis = st.selectbox("Select y-axis", list(category_cols.keys()))

    # Calculate the average values for each category
    avg_df = df.groupby("Category").agg({category_cols[x_axis]: "mean", category_cols[y_axis]: "mean"}).reset_index()

    # Create an Altair scatter plot
    chart = alt.Chart(avg_df).mark_point().encode(
        x=alt.X(f"{x_axis}:Q", title=f"{x_axis} {'(MB)' if x_axis == 'Size' else ''}",
                scale=alt.Scale(domain=[3.9, 4.5] if x_axis == 'Rating' else alt.Undefined)),
        y=alt.Y(f"{y_axis}:Q", title=f"{y_axis} {'(MB)' if y_axis == 'Size' else ''}",
                scale=alt.Scale(domain=[3.9, 4.5] if y_axis == 'Rating' else alt.Undefined)),
        color=alt.Color("Category:N", title="Category")
    ).properties(width=600, height=400)

    st.altair_chart(chart, use_container_width=True)

# Display the chart
def display_results(df):
     # Calculate the average values for each category
    avg_rating = df.groupby("Category")["Rating"].mean().reset_index()
    avg_rating = avg_rating.rename(columns={"Rating": "Average Rating"}).sort_values(by="Average Rating", ascending=False)

    avg_size = df.groupby("Category")["Size"].mean().reset_index()
    avg_size = avg_size.rename(columns={"Size": "Average Size"}).sort_values(by="Average Size", ascending=False)

    avg_price = df[df["Price"] > 0].groupby("Category")["Price"].mean().reset_index()
    avg_price["Price"] = avg_price["Price"].round(2)
    avg_price = avg_price.rename(columns={"Price": "Average Price"}).sort_values(by="Average Price", ascending=False)

    avg_reviews = df.groupby("Category")["Reviews"].mean().reset_index()
    avg_reviews = avg_reviews.rename(columns={"Reviews": "Average Reviews"}).sort_values(by="Average Reviews", ascending=False)

    avg_installs = df.groupby("Category")["Installs"].mean().reset_index()
    avg_installs = avg_installs.rename(columns={"Installs": "Average Installs"}).sort_values(by="Average Installs", ascending=False)

    # Create a selectbox for selecting the options
    option = st.selectbox("Select an option", ["Average Rating", "Average Size", "Average Price", "Average Reviews", "Average Installs"])

    if option == "Average Rating":
        st.write("Average Rating by Category:")
        st.write(avg_rating)
        st.write(f"Top category: {avg_rating.iloc[0]['Category']} with an average rating of {avg_rating.iloc[0]['Average Rating']:.2f}")
        st.write(f"Bottom category: {avg_rating.iloc[-1]['Category']} with an average rating of {avg_rating.iloc[-1]['Average Rating']:.2f}")

    elif option == "Average Size":
        fig = px.pie(avg_size, names="Category", values="Average Size")
        fig.update_traces(hovertemplate="<br>".join([
            "Category: %{label}<br>",
            "Average Size: %{value:.2f} MB<br>"
        ]))
        st.plotly_chart(fig, use_container_width=True)
        st.write(f"Largest category: {avg_size.iloc[0]['Category']} with an average size of {avg_size.iloc[0]['Average Size']:.2f} MB")
        st.write(f"Smallest category: {avg_size.iloc[-1]['Category']} with an average size of {avg_size.iloc[-1]['Average Size']:.2f} MB")

    elif option == "Average Price":
        fig = px.pie(avg_price, names="Category", values="Average Price")
        fig.update_traces(hovertemplate="<br>".join([
            "Category: %{label}<br>",
            "Average Price: $%{value:.2f}<br>"
        ]))
        st.plotly_chart(fig, use_container_width=True)
        st.write(f"Most expensive category: {avg_price.iloc[0]['Category']} with an average price of ${avg_price.iloc[0]['Average Price']:.2f}")
        st.write(f"Cheapest category: {avg_price.iloc[-1]['Category']} with an average price of ${avg_price.iloc[-1]['Average Price']:.2f}")

    elif option == "Average Reviews":
        fig = px.bar(avg_reviews, x="Category", y="Average Reviews", color="Average Reviews", color_continuous_scale="Viridis")
        fig.update_traces(hovertemplate="<br>".join([
            "Category: %{x}<br>",
            "Average Reviews: %{y:.2f}<br>"
        ]))
        st.plotly_chart(fig, use_container_width=True)
        st.write(f"Category with most reviews: {avg_reviews.iloc[0]['Category']} with an average of {avg_reviews.iloc[0]['Average Reviews']:.2f} reviews")
        st.write(f"Category with least reviews: {avg_reviews.iloc[-1]['Category']} with an average of {avg_reviews.iloc[-1]['Average Reviews']:.2f} reviews")

    elif option == "Average Installs":
        fig = px.bar(avg_installs, x="Category", y="Average Installs", color="Average Installs", color_continuous_scale="Viridis")
        fig.update_traces(hovertemplate="<br>".join([
            "Category: %{x}<br>",
            "Average Installs: %{y:.2f}<br>"
        ]))
        st.plotly_chart(fig, use_container_width=True)
        st.write(f"Category with most installs: {avg_installs.iloc[0]['Category']} with an average of {avg_installs.iloc[0]['Average Installs']:.2f} installs")
        st.write(f"Category with least installs: {avg_installs.iloc[-1]['Category']} with an average of {avg_installs.iloc[-1]['Average Installs']:.2f} installs")
