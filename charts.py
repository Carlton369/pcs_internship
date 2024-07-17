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

def top_n_barchart_2(df,top_n) -> None:

    st.markdown('<h2 style="font-size:24px;"> Comparison between 2 selected variables </h2>',unsafe_allow_html=True )
    if 'selected_var1' not in st.session_state:
        st.session_state.selected_var1 = None
    if 'selected_var2' not in st.session_state:
        st.session_state.selected_var2 = None


    keys_list =  list(category_cols.keys())
    # Display the charts in Streamlit
    col1, col2 = st.columns(2)
    with col1:
        var2 = st.session_state.selected_var2
        available_keys_var1 = [key for key in keys_list if key != var2]
        var1 = st.selectbox("Select the variable 1", available_keys_var1, key="var1", on_change=lambda: st.session_state.update({"selected_var1": st.session_state.var1}))

        if var1:
            category_avg1 = df.groupby('Category')[var1].mean().reset_index(name=f'Average {var1}')
            top_categories1 = category_avg1.sort_values(f'Average {var1}', ascending=False).head(top_n)

            bar_chart1 = alt.Chart(top_categories1).mark_bar().encode(
                x=alt.X('Category:N', 
                        axis=alt.Axis(
                            labelAngle=280,
                            labelFontSize=8
                        ),
                        sort='-y'  # Sort the categories in descending order
                    ),
                y=alt.Y(f'Average {var1}:Q', title=f'Average {var1}' + (' (GB)' if var1 == 'Size' else '')),
                color=alt.Color('Category:N', scale=alt.Scale(scheme='category20'))
            ).properties(
                title=f'Top {top_n} Categories by Average {var1}',
                width=1000,
                height=500
            )

            st.altair_chart(bar_chart1, use_container_width=True)

    with col2:
        var1 = st.session_state.selected_var1
        available_keys_var2 = [key for key in keys_list if key != var1]
        var2 = st.selectbox("Select the variable 2", available_keys_var2, index = 1,key="var2", on_change=lambda: st.session_state.update({"selected_var2": st.session_state.var2}))

        if var2:
            category_avg2 = df.groupby('Category')[var2].mean().reset_index(name=f'Average {var2}')
            top_categories2 = category_avg2.sort_values(f'Average {var2}', ascending=False).head(top_n)

            bar_chart2 = alt.Chart(top_categories2).mark_bar().encode(
                x=alt.X('Category:N', 
                        axis=alt.Axis(
                            labelAngle=280,
                            labelFontSize=8
                        ),
                        sort='-y'  # Sort the categories in descending order
                    ),
                y=alt.Y(f'Average {var2}:Q', title=f'Average {var2}' + (' (GB)' if var2 == 'Size' else '')),
                color=alt.Color('Category:N', scale=alt.Scale(scheme='category20'))
            ).properties(
                title=f'Top {top_n} Categories by Average {var2}',
                width=1000,
                height=500
            )

            st.altair_chart(bar_chart2, use_container_width=True)
