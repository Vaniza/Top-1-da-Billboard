import streamlit as st
import pandas as pd
import os

st.title("Top 1 da Billboard")

csv_file_path = r"billboard_top1_detalhado_1950_2020.csv"

try:
    
    if not os.path.exists(csv_file_path):
        st.error("Arquivo de dados não encontrado. Certifique-se de que o CSV está no diretório correto.")
    else:
       
        df = pd.read_csv(csv_file_path)
        
       
        required_columns = {'chart_week', 'current_week', 'title', 'performer', 'spotify_link'}
        if not required_columns.issubset(df.columns):
            st.error("O arquivo CSV não contém as colunas esperadas.")
        else:
            
            df['chart_week'] = pd.to_datetime(df['chart_week'], errors='coerce')
            
            
            df['Ano'] = df['chart_week'].dt.year
            df['Mês'] = df['chart_week'].dt.strftime('%B')
            
            
            anos = sorted(df['Ano'].dropna().unique())
            meses = df['Mês'].dropna().unique().tolist()

            
            ano_selecionado = st.selectbox("Selecione o ano:", anos, index=anos.index(1985) if 1985 in anos else 0)
            mes_selecionado = st.selectbox("Selecione o mês:", meses, index=meses.index("October") if "October" in meses else 0)

            
            if st.button("Pesquisar"):
                
                df_filtrado = df[(df['Ano'] == ano_selecionado) & (df['Mês'] == mes_selecionado)]
                
                if not df_filtrado.empty:
                    st.write(f"Músicas que foram número 1 na Billboard Hot 100 em {mes_selecionado} de {ano_selecionado}:")
                    
                    
                    for index, row in df_filtrado.iterrows():
                        st.subheader(f"{row['title']} - {row['performer']}")
                        st.write(f"📅 Data: {row['chart_week'].strftime('%d/%m/%Y')}")
                        st.markdown(f"🎵 [Ouça no Spotify]({row['spotify_link']})")
                        st.write("---")
                else:
                    st.warning("Nenhuma música encontrada para o período selecionado.")
except Exception as e:
    st.error(f"Ocorreu um erro ao carregar os dados: {e}")
