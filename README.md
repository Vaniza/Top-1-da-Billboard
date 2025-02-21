# 🎵 Billboard Top 1 Tracker

Este projeto é uma aplicação **Streamlit** que permite visualizar as músicas mais ouvidas nos EUA (Top 1 da Billboard) em um período selecionado.

## 📌 Funcionalidades
- Seleção de **ano** e **mês** para exibir as músicas número 1 na Billboard Hot 100.
- Exibição de **título da música, artista e data** de cada faixa.
- Links diretos para ouvir no **Spotify**, com tratamento para links inválidos.
- Tratamento de erros para garantir uma experiência fluida.

## 🚀 Como executar o projeto
### 1️⃣ Pré-requisitos
Certifique-se de ter o **Python 3.7+** e as bibliotecas necessárias instaladas:
```sh
pip install streamlit pandas
```

### 2️⃣ Rodando a aplicação
Execute o seguinte comando no terminal dentro do diretório do projeto:
```sh
streamlit run app.py
```

A aplicação abrirá no seu navegador padrão.

## 📂 Estrutura do projeto
```
📂 Billboard Top 1 Tracker
 ┣ 📂 api
 ┃ ┗ 📄 .env (ignorado pelo Git)
 ┣ 📂 data
 ┃ ┗ 📄 billboard_top1_detalhado_1950_2020.csv
 ┣ 📄 app.py
 ┣ 📄 README.md
 ┣ 📄 .gitignore
```

## 📄 Arquivos importantes
- **`app.py`**: Código principal da aplicação Streamlit.
- **`data/billboard_top1_detalhado_1950_2020.csv`**: Base de dados com os rankings da Billboard.
- **`.gitignore`**: Ignora arquivos sensíveis, como `.env`.
- **`README.md`**: Este documento explicativo.

## 🛠 Tecnologias utilizadas
- **Python 3.7+**
- **Streamlit** (para interface interativa)
- **Pandas** (para manipulação de dados)

## 📬 Contato
Caso tenha dúvidas ou sugestões, entre em contato!

---
Feito com ❤️ para facilitar a busca pelas músicas mais populares! 🎶
