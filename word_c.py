from wordcloud import WordCloud, STOPWORDS
import streamlit as st
import matplotlib.pyplot as plt

def plot_word_cloud(df):

    select_sentiment = st.selectbox('Choose a Sentiment', options=['All','Positive','Negative'])

   
    if select_sentiment == 'Positive':
        chosen_rev = df[df["Sentiment"] == "Positive"]   
    elif select_sentiment == 'Negative':
        chosen_rev = df[df["Sentiment"] == "Negative"]
    else:
        chosen_rev = df

    # jamming all the reviews into one long string
    revs = " ".join(chosen_rev["Translated_Review"].dropna().astype(str).tolist())
    #stopwords
    stopwords = set(STOPWORDS)
    stopwords.update(["game", "app",'even','phone','Please'])

    #make word cloud
    wordcloud = WordCloud(stopwords=stopwords,width=800, height=400, background_color='black').generate(revs)

    # Display the word cloud using Matplotlib

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')

# Display the figure using Streamlit
    st.pyplot(fig)
    
   