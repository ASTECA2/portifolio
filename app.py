import streamlit as st
import pandas as pd
import re
import streamlit.components.v1 as components

# --- CONFIGURAÇÕES DA PÁGINA ---
st.set_page_config(
    page_title="Dashboard do Meu Portfólio",
    page_icon="🎨",
    layout="wide"
)

# --- FUNÇÃO PARA PEGAR A THUMBNAIL DO YOUTUBE ---
def get_youtube_thumbnail(url):
    video_id = None
    regex = r"(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})"
    
    match = re.search(regex, url)
    if match:
        video_id = match.group(1)
        return f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
    
    return "https://via.placeholder.com/480x360.png?text=Link+Inválido"

# --- BANCO DE DADOS (SIMULADO DE FORMA SEGURA) ---
@st.cache_data
def carregar_dados():
    dados_portfolio = [
        {
            "titulo": "Orion Hunter ASMR",
            "tipo": "Vídeo",
            "descricao": "Trabalho feito pela Orion.",
            "link": "https://www.youtube.com/watch?v=kF3fRGerlwc",
            "imagem_thumbnail": ""
        },
        {
            "titulo": "Pulverizador Overlander Headshot",
            "tipo": "Vídeo",
            "descricao": "Trabalho feito para incomagri",
            "link": "https://youtu.be/YERB4rPunag",
            "imagem_thumbnail": "" 
        },
        {
            "titulo": "Lavadora de alta pressão",
            "tipo": "Vídeo",
            "descricao": "Trabalho feito para JactoClean",
            "link": "https://youtu.be/JiAyrHQK5qM",
            "imagem_thumbnail": ""
        },
        {
            "titulo": "Carrosséis Instagram",
            "tipo": "Imagem",
            "descricao": "Criação de carrosséis",
            "link": "https://www.behance.net/gallery/232803187/Carrossis-Instagram/modules/1335979025",
            "imagem_thumbnail": "assets/carrosseisinstagram.png"
        },
        {
            "titulo": "Uma produção familiar",
            "tipo": "Vídeo",
            "descricao": "Trabalho feito para Toplanting",
            "link": "https://youtu.be/0RRnfdNXVHQ",
            "imagem_thumbnail": "" # Deixe vazio, o código gera a thumb do YouTube
        },
        {
            "titulo": "Diagramação",
            "tipo": "Imagem",
            "descricao": "Diagramação de manuais",
            "link": "https://www.behance.net/gallery/232801933/Diagramacao-de-manuais-de-instrucoes",
            "imagem_thumbnail": "assets/diagramacao.png"
        },
        {
            "titulo": "Compostador de Resíduos Orgânicos",
            "tipo": "Vídeo",
            "descricao": "Diagramação de manuais",
            "link": "https://youtu.be/8SWodzkQruU",
            "imagem_thumbnail": ""
        },
        {
            "titulo": "Emocentro - Marilia",
            "tipo": "Vídeo",
            "descricao": "Trabalho feito para Orion",
            "link": "https://www.instagram.com/reel/DNlG-8ZugCf/",
            "imagem_thumbnail": "assets/rodrigoalandia.png"
        },
        {
            "titulo": "Lavadora de Alta pressão",
            "tipo": "Vídeo",
            "descricao": "Trabalho feito para JactoClean",
            "link": "https://www.youtube.com/watch?v=6Kj-4KhYYr4",
            "imagem_thumbnail": ""
        },
        {
            "titulo": "Lançamento J7400",
            "tipo": "Vídeo",
            "descricao": "Trabalho feito para JactoClean",
            "link": "https://www.instagram.com/p/DN37Kcwibh_/",
            "imagem_thumbnail": "assets/thumbc.png"
        },
        {
            "titulo": "Post Veneto Agricultura",
            "tipo": "Imagem",
            "descricao": "Post",
            "link": "https://www.instagram.com/p/DOJp4kck7XL/?img_index=1",
            "imagem_thumbnail": "assets/print.png"
        },
                {
            "titulo": "Post Agral",
            "tipo": "Imagem",
            "descricao": "Post",
            "link": "https://www.instagram.com/p/DPOvmKdjU9a/",
            "imagem_thumbnail": "assets/agjet.png"
        },
    ]

    df = pd.DataFrame(dados_portfolio)

    for index, row in df.iterrows():
        if row['tipo'] == 'Vídeo' and not row['imagem_thumbnail']:
            df.at[index, 'imagem_thumbnail'] = get_youtube_thumbnail(row['link'])
            
    return df

# --- INÍCIO DA EXECUÇÃO DO APP ---
try:
    df = carregar_dados()
except Exception as e:
    st.error(f"Ocorreu um erro ao carregar os dados do portfólio. Verifique a estrutura dos dados no código.")
    st.error(f"Erro técnico: {e}")
    st.stop()

# --- INTERFACE DA APLICAÇÃO ---
st.title("Portfólio Interativo")
st.markdown("Navegue pelos trabalhos da nossa agência usando o filtro na barra lateral.")

st.sidebar.title("Filtros")
if not df.empty and 'tipo' in df.columns:
    categorias_sidebar = ['Todos'] + list(df['tipo'].unique())
    categoria_selecionada = st.sidebar.radio(
        'Selecione uma categoria:',
        categorias_sidebar
    )

    if categoria_selecionada == 'Todos':
        df_filtrado = df
    else:
        df_filtrado = df[df['tipo'] == categoria_selecionada]
else:
    st.warning("Não foi possível encontrar a coluna 'tipo' ou o portfólio está vazio.")
    df_filtrado = pd.DataFrame() 

st.header(f"Mostrando: {categoria_selecionada}", divider='rainbow')

if df_filtrado.empty:
    st.warning("Nenhum item encontrado para esta categoria.")
else:
    num_colunas = 3
    colunas = st.columns(num_colunas)
    for i, (index, item) in enumerate(df_filtrado.iterrows()):
        with colunas[i % num_colunas]:
            st.subheader(item['titulo'])
            st.image(item['imagem_thumbnail'], use_container_width=True)
            
            with st.expander("Ver detalhes"):
                st.write(item['descricao'])
                if item['tipo'] == 'Vídeo':
                    if "instagram.com" in item['link']:
                        instagram_embed = f"""
                        <blockquote class="instagram-media" data-instgrm-permalink="{item['link']}" data-instgrm-version="14"></blockquote>
                        <script async src="//www.instagram.com/embed.js"></script>
                        """
                        components.html(instagram_embed, height=500)
                    else:
                        st.video(item['link'])
                else:
                    st.markdown(f"[🔗 Ver projeto completo]({item['link']})")

                    