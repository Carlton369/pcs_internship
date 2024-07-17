import streamlit as st
import pandas as pd
import altair as alt
import numpy as np

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
    st.title("Scatter graph")

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
    # Display the results

    col1, col2, col3 = st.columns(3)

    with col1:
        st.write("Average Rating by Category:")
        avg_rating = df.groupby("Category")["Rating"].mean().reset_index()
        avg_rating = avg_rating.sort_values(by="Rating", ascending=False)
        st.write(avg_rating)

        st.write("\nAverage Reviews by Category:")
        avg_reviews = df.groupby("Category")["Reviews"].mean().reset_index()
        avg_reviews = avg_reviews.sort_values(by="Reviews", ascending=False)
        st.write(avg_reviews)
    
    with col2:
        st.write("\nAverage Size by Category:")
        avg_size = df.groupby("Category")["Size"].mean().reset_index()
        avg_size = avg_size.sort_values(by="Size", ascending=False)
        st.write(avg_size)

        st.write("\nAverage Installs by Category:")
        avg_installs = df.groupby("Category")["Installs"].mean().reset_index()
        avg_installs = avg_installs.sort_values(by="Installs", ascending=False)
        st.write(avg_installs)

    with col3:
        st.write("\nAverage Price by Category:")
        avg_price = df.groupby("Category")["Price"].mean().reset_index()
        avg_price = avg_price.sort_values(by="Price", ascending=False).reset_index()
        st.write(avg_price)