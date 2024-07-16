import streamlit as st
import pandas as pd
import altair as alt
import numpy as np

# Create a dictionary to map category names to their corresponding columns
category_cols = {
    "Rating": "Rating",
    "Reviews": "Reviews",
    "Size": "Size",
    "Installs": "Installs",
    "Price": "Price"
}

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

def top_n_barchart_2(df) -> None:

    st.title("Comparison between 2 variables")

    top_n_options = [i for i in range (1,34)]
    top_n = st.selectbox('Select the number of top categories:', top_n_options)

    # Group the data by Category and calculate the average of the chosen variables
    # category_avg1 = df.groupby('Category')[var1].mean().reset_index(name=f'Average {var1}')
    # category_avg2 = df.groupby('Category')[var2].mean().reset_index(name=f'Average {var2}')

    # Sort the categories by average in descending order and get the top N
    # top_categories1 = category_avg1.sort_values(f'Average {var1}', ascending=False).head(top_n)
    # top_categories2 = category_avg2.sort_values(f'Average {var2}', ascending=False).head(top_n)

    # Create the bar charts
    # bar_chart1 = alt.Chart(top_categories1).mark_bar().encode(
    #     x=alt.X('Category:N', 
    #         axis=alt.Axis(
    #             labelAngle=80,
    #             labelFontSize=10
    #         ),
    #         sort='-y'  # Sort the categories in descending order
    #     ),
    #     y=alt.Y(f'Average {var1}:Q', title=f'Average {var1}' + (' (GB)' if var1 == 'Size' else '')),
    #     #scale=alt.Scale(domain=[top_categories1[f'Average {var1}'].min(), top_categories1[f'Average {var1}'].max()]))),
    #     color=alt.Color('Category:N', scale=alt.Scale(scheme='category20'))
    # ).properties(
    #     title=f'Top {top_n} Categories by Average {var1}',
    #     width=1000,
    #     height=500
    #     )

    # bar_chart2 = alt.Chart(top_categories2).mark_bar().encode(
    #     x=alt.X('Category:N', 
    #         axis=alt.Axis(
    #             labelAngle=80,
    #             labelFontSize=10
    #         ),
    #         sort='-y'  # Sort the categories in descending order
    #     ),
    #     y=alt.Y(f'Average {var2}:Q', title=f'Average {var2}' + (' (GB)' if var2 == 'Size' else '')),
    #     #scale=alt.Scale(domain=[top_categories2[f'Average {var2}'].min(), top_categories2[f'Average {var2}'].max()]))),
    #     color=alt.Color('Category:N', scale=alt.Scale(scheme='category20'))
    # ).properties(
    #     title=f'Top {top_n} Categories by Average {var2}',
    #     width=1000,
    #     height


    # Display the charts in Streamlit
    col1, col2 = st.columns(2)
    with col1:
        var1 = st.selectbox("Select the variable 1", list(category_cols.keys()), key="var1")
        category_avg1 = df.groupby('Category')[var1].mean().reset_index(name=f'Average {var1}')
        top_categories1 = category_avg1.sort_values(f'Average {var1}', ascending=False).head(top_n)

        bar_chart1 = alt.Chart(top_categories1).mark_bar().encode(
        x=alt.X('Category:N', 
                axis=alt.Axis(
                    labelAngle=80,
                    labelFontSize=10
                ),
                sort='-y'  # Sort the categories in descending order
            ),
        y=alt.Y(f'Average {var1}:Q', title=f'Average {var1}' + (' (GB)' if var1 == 'Size' else '')),
            #scale=alt.Scale(domain=[top_categories1[f'Average {var1}'].min(), top_categories1[f'Average {var1}'].max()])),
            color=alt.Color('Category:N', scale=alt.Scale(scheme='category20'))
        ).properties(
            title=f'Top {top_n} Categories by Average {var1}',
            width=1000,
            height=500
        )

        st.altair_chart(bar_chart1, use_container_width=True)
    with col2:
        var2 = st.selectbox("Select the variable 2", list(category_cols.keys()), key="var2")
        category_avg2 = df.groupby('Category')[var2].mean().reset_index(name=f'Average {var2}')
        top_categories2 = category_avg2.sort_values(f'Average {var2}', ascending=False).head(top_n)

        bar_chart2 = alt.Chart(top_categories2).mark_bar().encode(
        x=alt.X('Category:N', 
            axis=alt.Axis(
                labelAngle=80,
                labelFontSize=10
            ),
            sort='-y'  # Sort the categories in descending order
        ),
        y=alt.Y(f'Average {var2}:Q', title=f'Average {var2}' + (' (GB)' if var2 == 'Size' else '')),
            #scale=alt.Scale(domain=[top_categories2[f'Average {var2}'].min(), top_categories2[f'Average {var2}'].max()])),
            color=alt.Color('Category:N', scale=alt.Scale(scheme='category20'))
        ).properties(
            title=f'Top {top_n} Categories by Average {var2}',
            width=1000,
            height=500
        )
        

        st.altair_chart(bar_chart2, use_container_width=True)

