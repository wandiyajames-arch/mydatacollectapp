import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup as bs
from requests import get

#   SCRAPING FUNCTIONS


def load_villa_data(n):
    df = pd.DataFrame()
    progress = st.empty()   
    
    for index in range(1, n + 1):
        progress.write(f"🔎 Scraping villa page {index} ...")

        url = f'https://sn.coinafrique.com/categorie/villas?page={index}'
        res = get(url)
        soup = bs(res.content, 'html.parser')
        containers = soup.find_all('div', class_="col s6 m4 l3")

        data = []
        for c in containers:
            try:
                link = "https://sn.coinafrique.com" + c.find('a')["href"]
                res2 = get(link)
                soup2 = bs(res2.content, "html.parser")

                details = soup2.find('h1', "title title-ad hide-on-large-and-down").text
                price = "".join(soup2.find('p', "price").text.strip().split()).replace("CFA", "")
                address = soup2.find_all('span', 'valign-wrapper')[1].text

                block = soup2.find('div', class_="details-characteristics")
                rooms = block.find_all('span', 'qt')
                number_of_rooms = rooms[0].text.strip() if len(rooms) else None

                img = soup2.find('div', class_="swiper-slide slide-clickable")
                style = img.get("style")
                image_link = style.split('url(')[1].split(')')[0].strip('"')

                data.append({
                    "type": "villa",
                    "details": details,
                    "price": price,
                    "address": address,
                    "rooms": number_of_rooms,
                    "image": image_link,
                })
            except:
                pass

        df = pd.concat([df, pd.DataFrame(data)], ignore_index=True)

    progress.write("Villa scraping completed!")
    return df


def load_terrains_data(n):
    df = pd.DataFrame()
    progress = st.empty()

    for index in range(1, n + 1):
        progress.write(f"🔎 Scraping terrain page {index} ...")

        url = f'https://sn.coinafrique.com/categorie/terrains?page={index}'
        res = get(url)
        soup = bs(res.content, 'html.parser')
        containers = soup.find_all('div', class_="col s6 m4 l3")

        data = []
        for c in containers:
            try:
                link = "https://sn.coinafrique.com" + c.find('a')["href"]
                res2 = get(link)
                soup2 = bs(res2.content, "html.parser")

                details = soup2.find('h1', "title title-ad hide-on-large-and-down").text
                price = "".join(soup2.find('p', "price").text.strip().split()).replace("CFA", "")
                address = soup2.find_all('span', 'valign-wrapper')[0].text
                surface = details.strip()

                img = soup2.find('div', class_="swiper-slide slide-clickable")
                style = img.get("style")
                image_link = style.split('url(')[1].split(')')[0].strip('"')

                data.append({
                    "type": "terrain",
                    "details": details,
                    "price": price,
                    "address": address,
                    "surface": surface,
                    "image": image_link,
                })
            except:
                pass

        df = pd.concat([df, pd.DataFrame(data)], ignore_index=True)

    progress.write("✔️ Terrain scraping completed!")
    return df

def load_appartements_data(n):
    df = pd.DataFrame()
    progress = st.empty()

    for index in range(1, n + 1):
        progress.write(f"🔎 Scraping appartement page {index} ...")

        url = f'https://sn.coinafrique.com/categorie/appartements?page={index}'
        res = get(url)
        soup = bs(res.content, 'html.parser')
        containers = soup.find_all('div', class_="col s6 m4 l3")

        data = []
        for c in containers:
            try:
                link = "https://sn.coinafrique.com" + c.find('a')["href"]
                res2 = get(link)
                soup2 = bs(res2.content, "html.parser")

                details = soup2.find('h1', "title title-ad hide-on-large-and-down").text
                price = "".join(soup2.find('p', "price").text.strip().split()).replace("CFA", "")
                address = soup2.find_all('span', 'valign-wrapper')[1].text

                block = soup2.find('div', class_="details-characteristics")
                rooms = block.find_all('span', 'qt')
                number_of_rooms = rooms[0].text.strip() if len(rooms) else None

                img = soup2.find('div', class_="swiper-slide slide-clickable")
                style = img.get("style")
                image_link = style.split('url(')[1].split(')')[0].strip('"')

                data.append({
                    "type": "appartement",
                    "details": details,
                    "price": price,
                    "address": address,
                    "rooms": number_of_rooms,
                    "image": image_link,
                })
            except:
                pass

        df = pd.concat([df, pd.DataFrame(data)], ignore_index=True)

    progress.write("Apartement scraping completed!")
    return df




#   STREAMLIT PAGE


def run():
    st.title("🏠 Welcome to my data scraping")

  
    # FILE UPLOAD SECTION
   
    st.subheader("📁 Import existing scraped data")
    uploaded = st.file_uploader("Upload .csv or .xlsx", type=["csv", "xlsx"])

    if uploaded:
        if uploaded.name.endswith(".csv"):
            df = pd.read_csv(uploaded)
        else:
            df = pd.read_excel(uploaded)

        st.success("File imported successfully!")
        st.dataframe(df)
        st.write(f"Total rows: **{len(df)}**")

    st.write("---")


    # SCRAPING SECTION

    st.subheader("🕷️ Scrape data")

    choice = st.selectbox("Choose category", ["villa", "terrain", "appartement"])
    pages = st.number_input("Number of pages to scrape", min_value=1, max_value=50, value=2)

    if st.button("Start scraping"):
        with st.spinner("Scraping in progress..."):

            if choice == "villa":
                df = load_villa_data(pages)
            elif choice == "terrain":
                df = load_terrains_data(pages)
            else:
                df = load_appartements_data(pages)

            st.success(f"Scraping completed for **{choice}**!")
            st.write(f"Total items: **{len(df)}**")
            st.dataframe(df)

            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                "Download CSV",
                csv,
                f"{choice}_data.csv",
                "text/csv"
            )

