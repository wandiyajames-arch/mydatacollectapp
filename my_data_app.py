import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup as bs
from requests import get
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import streamlit as st
import streamlit.components.v1 as components




st.markdown("<h1 style='text-align: center; color: black;'>MY BEST DATA APP</h1>", unsafe_allow_html=True)

st.markdown("""
This app performs webscraping of data from dakar-auto over multiples pages. And we can also
download scraped data from the app directly without scraping them.
* **Python libraries:** base64, pandas, streamlit, requests, bs4
* **Data source:** [Expat-Dakar](https://www.expat-dakar.com/) -- [Dakar-Auto](https://dakar-auto.com/senegal/voitures-4).
""")


# Background function
def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"jpg"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )

# Web scraping of Vehicles data on expat-dakar
@st.cache_data

def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')


def load(dataframe, title, key, key1) :
    # Créer 3 colonnes avec celle du milieu plus large
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if st.button(title, key1):
            st.subheader('Display data dimension')
            st.write('Data dimension: ' + str(dataframe.shape[0]) + ' rows and ' + str(dataframe.shape[1]) + ' columns.')
            st.dataframe(dataframe)

            csv = convert_df(dataframe)

            st.download_button(
                label="Download data as CSV",
                data=csv,
                file_name='Data.csv',
                mime='text/csv',
                key = key)

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# web scraping function villa data
def load_villa_data(n):
    df = pd.DataFrame()
    # loop over pages indexes
    for index in range(1, n+1):
        url = f'https://sn.coinafrique.com/categorie/villas?page={index}'
        res = get(url)
        soup = bs(res.content, 'html.parser' )
        containers = soup.find_all('div', class_ = "col s6 m4 l3")
    # scrape data from all the containers
        data = []

        for container in containers:
            container_url = "https://sn.coinafrique.com" + container.find('a')["href"]
            res_container = get(container_url)
            soup_container = bs(res_container.content, "html.parser")
            try:
                details = soup_container.find('h1',"title title-ad hide-on-large-and-down").text
                price = "".join(soup_container.find('p',"price").text.strip().split()).replace('CFA','')
                address = soup_container.find_all('span','valign-wrapper')[1].text
                p_details = soup_container.find_all('div', class_="details-characteristics")[0]
                j=p_details.find_all('span','qt')
                number_of_rooms = j[0].text.strip() if len(j)>0 else None
                img = soup_container.find('div',class_="swiper-slide slide-clickable")
                style = img.get('style')
                image_link=style.split('url(')[1].split(')')[0].strip('"')

                dic = {
                    "details": details,
                    "price":price,
                    "address":address,
                    "p_details": p_details,
                    "number_of_rooms":number_of_rooms,
                    "image_link": image_link,
                        }
                data.append(dic)
            except:
                pass
    DF = pd.DataFrame(data)
    df = pd.concat([df, DF], axis = 0).reset_index(drop = True)
    return df


# web scraping function terrains data
def load_terrains_data(mul_pages=n):
    # create a empty dataframe df
        df = pd.DataFrame()
        # loop over pages indexes
        for page in range (1,int(mul_pages)+1):
            url = f'https://sn.coinafrique.com/categorie/terrains?page={page}'
            res = get(url)
            soup = bs(res.content, 'html.parser' )
            containers = soup.find_all('div', class_ = "col s6 m4 l3")
        # scrape data from all the containers
        data = []

        for container in containers:
            container_url = "https://sn.coinafrique.com" + container.find('a')["href"]
            res_container = get(container_url)
            soup_container = bs(res_container.content, "html.parser")
            try:
                    details = soup_container.find('h1',"title title-ad hide-on-large-and-down").text
                    surface = details.strip()
                    price = "".join(soup_container.find('p',"price").text.strip().split()).replace('CFA','')
                    address = soup_container.find_all('span','valign-wrapper')[0].text
                    img = soup_container.find('div',class_="swiper-slide slide-clickable")
                    style = img.get('style')
                    image_link=style.split('url(')[1].split(')')[0].strip('"')

                    dic = {
                        "details": details,
                        "price":price,
                        "address":address,
                        "surface":surface,
                        "image_link": image_link,
                    }
                    data.append(dic)
            except:
                pass
        DF = pd.DataFrame(data)
        df = pd.concat([df, DF], axis = 0).reset_index(drop = True)
        
        return df  


# web scraping function appartements data
def load_ppartements_data(mul_pages=n):
    # create a empty dataframe df
    df = pd.DataFrame()
    # loop over pages indexes
    for index in range(1, n):
        url = f'https://sn.coinafrique.com/categorie/appartements?page={index}'
        res = get(url)
        soup = bs(res.content, 'html.parser' )
        containers = soup.find_all('div', class_ = "col s6 m4 l3")

        # scrape data from all the containers
        data = []

        for container in containers:
            container_url = "https://sn.coinafrique.com/" + container.find('a')["href"]
            res_container = get(container_url)
            soup_container = bs(res_container.content, "html.parser")
            try:
                details = soup_container.find('h1',"title title-ad hide-on-large-and-down").text
                price = "".join(soup_container.find('p',"price").text.strip().split()).replace('CFA','')
                address = soup_container.find_all('span','valign-wrapper')[1].text
                a_details = soup_container.find_all('div', class_="details-characteristics")[0]
                j=a_details.find_all('span','qt') # a_details stand for apartment details
                number_of_rooms = j[0].text.strip() if len(j)>0 else None
                img = soup_container.find('div',class_="swiper-slide slide-clickable")
                style = img.get('style')
                image_link=style.split('url(')[1].split(')')[0].strip('"')

                dic = {
                    "details": details,
                    "price":price,
                    "address":address,
                    "a_details": a_details,
                    "number_of_rooms":number_of_rooms,
                    "image_link": image_link,
                    }
                data.append(dic)
            except:
                pass
        DF = pd.DataFrame(data)
        df = pd.concat([df, DF], axis = 0).reset_index(drop = True)

        #clean data 
        return df


st.sidebar.header('User Input Features')
Pages = st.sidebar.selectbox('Pages indexes', list([int(p) for p in np.arange(2, 600)]))
Choices = st.sidebar.selectbox('Options', ['Scrape data using beautifulSoup', 'Download scraped data', 'Dashbord of the data', 'Evaluate the App'])



add_bg_from_local('img_file3.jpg') 

local_css('style.css')  

if Choices=='Scrape data using beautifulSoup':

    villa_data_mul_pag = load_villa_data(Pages)
    terrains_data_mul_pag = load_terrains_data(Pages)
    appartements_data_mul_pag = load_ppartements_data(Pages)
    
    load(villa_data_mul_pag, 'Villa data', '1', '101')
    load(terrains_data_mul_pag, 'Terrains data', '2', '102')
    load(appartements_data_mul_pag, 'Appartements data', '3', '103')

elif Choices == 'Download scraped data': 
    villa = pd.read_csv('Villa_data(2).csv')
    terrains = pd.read_csv('terrains_data.csv') 
    appartements = pd.read_csv('appartements_data.csv')

    load(villa, 'Villa data', '1', '101')
    load(terrains, 'Terrains data', '2', '102')
    load(appartements, 'Appartements data', '3', '103')

elif  Choices == 'Dashbord of the data': 
    df1 = pd.read_csv('villa_clean_data.csv')
    df2 = pd.read_csv('terrains_clean_data.csv')
    df3 = pd.read_csv('appartements_clean_data.csv')

    col1, col2= st.columns(2)

    with col1:
        plot1= plt.figure(figsize=(11,7))
        color = (0.2, # redness
                 0.4, # greenness
                 0.2, # blueness
                 0.6 # transparency
                 )
        plt.bar(df1.marque.value_counts()[:5].index, df1.marque.value_counts()[:5].values, color = color)
        plt.title("Top five most sold villas")
        plt.xlabel('price')
        st.pyplot(plot1)

    with col2:
        plot2 = plt.figure(figsize=(11,7))
        color = (0.5, # redness
         0.7, # greenness
         0.9, # blueness
         0.6 # transparency
         )
        plt.bar(df2.marque.value_counts()[:5].index, df2.marque.value_counts()[:5].values, color = color)
        plt.title('Top five most sold terrains')
        plt.xlabel('price')
        st.pyplot(plot2)
    
    col3, col4= st.columns(2)

    with col3:
        plot3= plt.figure(figsize=(11,7))
        sns.lineplot(data=df1, x="year", y="price", hue="status")
        plt.title('Price variation by year for villa categories')
        st.pyplot(plot3)

    with col4:
        plot4 = plt.figure(figsize=(11,7))
        sns.lineplot(data=df2, x="year", y="price", hue="status")
        plt.title('Price variation by year for terrain categories')
        st.pyplot(plot4)



else :
    # components.html("""
    # <iframe src="https://ee.kobotoolbox.org/i/y3pfGxMz" width="800" height="1100"></iframe>
    # """,height=1100,width=800)
    st.markdown("<h3 style='text-align: center;'>Give your Feedback</h3>", unsafe_allow_html=True)

    # centrer les deux boutons
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Kobo Evaluation Form"):
            st.markdown(
                '<meta http-equiv="refresh" content="0; url=https://ee.kobotoolbox.org/i/y3pfGxMz">',
                unsafe_allow_html=True
            )

    with col2:
        if st.button("Google Forms Evaluation"):
            st.markdown(
                '<meta http-equiv="refresh" content="0; url=https://docs.google.com/forms/d/e/XXXXXXXXX/viewform?usp=sf_link">',
                unsafe_allow_html=True
            )







 











