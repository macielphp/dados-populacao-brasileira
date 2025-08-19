import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
from datetime import datetime
import os

# Configuração da página
st.set_page_config(
    page_title="📊 Dashboard - População por Estado",
    page_icon="🇧🇷",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Função para encontrar o caminho correto
def get_data_path():
    """Encontra o caminho correto para os dados"""
    # Tentar diferentes caminhos
    possible_paths = [
        "../data/processed",  # Se executar de src/dashboard/
        "../../data/processed",  # Se executar de src/
        "data/processed",  # Se executar da raiz
        "./data/processed"  # Caminho relativo
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            st.success(f"✅ Dados encontrados em: {path}")
            return path
    
    # Se nenhum caminho funcionar, mostrar erro
    st.error("❌ Não foi possível encontrar a pasta de dados!")
    st.info("Caminhos tentados:")
    for path in possible_paths:
        st.info(f"  - {path}")
    return None

# Carregar dados
@st.cache_data
def load_data():
    """Carrega os dados processados"""
    try:
        data_path = get_data_path()
        if data_path is None:
            return None
            
        files = [f for f in os.listdir(data_path) if f.startswith("cleaned_population") and f.endswith(".csv")]
        
        if files:
            latest_file = max(files, key=lambda x: os.path.getctime(os.path.join(data_path, x)))
            file_path = os.path.join(data_path, latest_file)
            df = pd.read_csv(file_path)
            
            # Adicionar dados de população se não existir
            if 'populacao' not in df.columns:
                population_data = {
                    "São Paulo": 46649132, "Minas Gerais": 21411923, "Rio de Janeiro": 17463349,
                    "Bahia": 14985284, "Paraná": 11797436, "Rio Grande do Sul": 11466630,
                    "Pernambuco": 9674793, "Ceará": 9240580, "Pará": 8777124, "Santa Catarina": 7762154,
                    "Maranhão": 7153262, "Paraíba": 4059905, "Amazonas": 4269995, "Espírito Santo": 4108508,
                    "Goiás": 7206589, "Alagoas": 3365351, "Piauí": 3289290, "Distrito Federal": 3094325,
                    "Mato Grosso do Sul": 2839188, "Mato Grosso": 3567234, "Rio Grande do Norte": 3560903,
                    "Rondônia": 1815278, "Tocantins": 1607363, "Acre": 906876, "Amapá": 877613,
                    "Roraima": 652713, "Sergipe": 2338474
                }
                df['populacao'] = df['nome'].map(population_data)
            
            return df
        else:
            st.error("❌ Nenhum arquivo de dados encontrado!")
            return None
    except Exception as e:
        st.error(f"❌ Erro ao carregar dados: {e}")
        return None

# Carregar insights
@st.cache_data
def load_insights():
    """Carrega os insights salvos"""
    try:
        data_path = get_data_path()
        if data_path is None:
            return None
            
        insights_file = os.path.join(data_path, "insights_analise.json")
        if os.path.exists(insights_file):
            with open(insights_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None
    except:
        return None

# Título principal
st.title("🇧🇷 Dashboard de Análise Populacional")
st.markdown("### Análise da População por Estado do Brasil")
st.markdown("---")

# Carregar dados
df = load_data()
insights = load_insights()

if df is not None:
    # Sidebar com filtros
    st.sidebar.header("🔍 Filtros")
    
    # Filtro por região
    regions = ['Todas'] + df['regiao'].unique().tolist()
    selected_region = st.sidebar.selectbox("Selecione a Região:", regions)
    
    # Filtro por população
    min_pop = int(df['populacao'].min())
    max_pop = int(df['populacao'].max())
    population_range = st.sidebar.slider(
        "Faixa de População (milhões):",
        min_value=min_pop//1000000,
        max_value=max_pop//1000000,
        value=(min_pop//1000000, max_pop//1000000)
    )
    
    # Aplicar filtros
    filtered_df = df.copy()
    if selected_region != 'Todas':
        filtered_df = filtered_df[filtered_df['regiao'] == selected_region]
    
    filtered_df = filtered_df[
        (filtered_df['populacao'] >= population_range[0] * 1000000) &
        (filtered_df['populacao'] <= population_range[1] * 1000000)
    ]
    
    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total de Estados", len(filtered_df))
    
    with col2:
        total_pop = filtered_df['populacao'].sum()
        st.metric("População Total", f"{total_pop:,}")
    
    with col3:
        avg_pop = filtered_df['populacao'].mean()
        st.metric("População Média", f"{avg_pop:,.0f}")
    
    with col4:
        max_state = filtered_df.loc[filtered_df['populacao'].idxmax(), 'nome']
        st.metric("Estado Mais Populoso", max_state)
    
    st.markdown("---")
    
    # Gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Top 10 Estados por População")
        top_10 = filtered_df.nlargest(10, 'populacao')
        fig_bar = px.bar(
            top_10, 
            x='populacao', 
            y='nome',
            orientation='h',
            color='regiao',
            title="Top 10 Estados"
        )
        fig_bar.update_layout(height=400)
        st.plotly_chart(fig_bar, use_container_width=True)
    
    with col2:
        st.subheader("🥧 Distribuição por Região")
        region_pop = filtered_df.groupby('regiao')['populacao'].sum()
        fig_pie = px.pie(
            values=region_pop.values,
            names=region_pop.index,
            title="População por Região"
        )
        fig_pie.update_layout(height=400)
        st.plotly_chart(fig_pie, use_container_width=True)
    
    # Tabela de dados
    st.subheader("📋 Dados Detalhados")
    st.dataframe(
        filtered_df[['nome', 'sigla', 'regiao', 'populacao']].sort_values('populacao', ascending=False),
        use_container_width=True
    )
    
    # Insights
    if insights:
        st.subheader("💡 Insights da Análise")
        col1, col2 = st.columns(2)
        
        with col1:
            st.info(f"**Estado mais populoso:** {insights['estado_mais_populoso']}")
            st.info(f"**Estado menos populoso:** {insights['estado_menos_populoso']}")
        
        with col2:
            st.info(f"**Região com mais estados:** {insights['regiao_mais_estados']}")
            st.info(f"**Total de estados:** {insights['total_estados']}")

else:
    st.error("❌ Não foi possível carregar os dados. Verifique se os arquivos existem.")

# Footer
st.markdown("---")
st.markdown("*Dashboard criado com Streamlit - Fase 4 do projeto*")