import streamlit as st
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup

def load_env():
    load_dotenv()
    return spotipy.Spotify(auth_manager=SpotifyClientCredentials(
        client_id=os.getenv("SPOTIPY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIPY_CLIENT_SECRET")
    ))

def get_billboard_top1(year, month):
    url = f"https://en.wikipedia.org/wiki/List_of_Billboard_Hot_100_number_ones_of_{year}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    try:
        tables = soup.find_all("table", class_="wikitable")
        if not tables:
            st.error("Nenhuma tabela encontrada na Wikipedia.")
            return []
        
        songs = []
        for table in tables:
            rows = table.find_all("tr")[1:]
            for row in rows:
                cols = row.find_all("td")
                if len(cols) >= 3:
                    date_range = cols[0].text.strip()
                    song = cols[1].text.strip().strip('"')
                    artist = cols[2].text.strip()
                    if month.lower() in date_range.lower():
                        songs.append({"song": song, "artist": artist})
        return songs
    except Exception as e:
        st.error(f"Erro ao buscar dados da Billboard: {e}")
        return []

def get_spotify_links(sp, songs):
    updated_songs = []
    for song in songs:
        query = f"{song['song']} {song['artist']}"
        try:
            results = sp.search(q=query, type="track", limit=1)
            if results['tracks']['items']:
                song["spotify_url"] = results['tracks']['items'][0]['external_urls']['spotify']
            else:
                song["spotify_url"] = "N/A"
        except Exception as e:
            song["spotify_url"] = "N/A"
            st.error(f"Erro ao buscar {query}: {e}")
        updated_songs.append(song)
    return updated_songs

def main():
    st.title("Top 1 da Billboard nos EUA com Links Spotify")
    year = st.number_input("Ano", min_value=1950, max_value=2025, value=1985)
    months_dict = {
        "Janeiro": "January", "Fevereiro": "February", "Março": "March", "Abril": "April", 
        "Maio": "May", "Junho": "June", "Julho": "July", "Agosto": "August", 
        "Setembro": "September", "Outubro": "October", "Novembro": "November", "Dezembro": "December"
    }
    month_pt = st.selectbox("Mês", list(months_dict.keys()))
    month = months_dict[month_pt]  # Converte para inglês
    
    if st.button("Buscar Músicas"):
        sp = load_env()
        songs = get_billboard_top1(year, month)
        
        if not songs:
            st.error("Nenhuma música encontrada para o período selecionado.")
            return
        
        # Exibe as músicas encontradas antes da requisição ao Spotify
        st.subheader("Músicas encontradas na Billboard:")
        df_songs = pd.DataFrame(songs)
        if not df_songs.empty:
            st.dataframe(df_songs)  # Exibe a tabela de músicas encontradas
        else:
            st.warning("Nenhuma música encontrada para exibição.")
        
        songs_with_links = get_spotify_links(sp, songs)
        df = pd.DataFrame(songs_with_links)
        
        if "spotify_url" in df.columns:
            df["spotify_url"] = df["spotify_url"].apply(lambda x: f'<a href="{x}" target="_blank">Ouvir no Spotify</a>' if x != "N/A" else "Não encontrado")
            st.write(df.to_html(escape=False), unsafe_allow_html=True)
            
            # Adiciona opção de download como CSV e JSON
            csv = df.to_csv(index=False).encode('utf-8')
            json_data = df.to_json(orient="records", indent=4).encode('utf-8')
            
            st.download_button("Baixar CSV", csv, "billboard_top1.csv", "text/csv")
            st.download_button("Baixar JSON", json_data, "billboard_top1.json", "application/json")
        else:
            st.error("Erro ao obter os links do Spotify.")

if __name__ == "__main__":
    main()
