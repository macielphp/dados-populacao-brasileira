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
    page_icon="🇧��",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Função para encontrar o caminho correto
def get_data_path():
    """Encontra o caminho correto para os dados"""
    possible_paths = [
        "../data/processed",
        "../../data/processed",
        "data/processed",
        "./data/processed"
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            st.success(f"✅ Dados encontrados em: {path}")
            return path
    
    st.error("❌ Não foi possível encontrar a pasta de dados!")
    return None

# Carregar dados
@st.cache_data
def load_data():
    """Carrega os dados processados com histórico por ano"""
    try:
        data_path = get_data_path()
        if data_path is None:
            return None
            
        files = [f for f in os.listdir(data_path) if f.startswith("cleaned_population") and f.endswith(".csv")]
        
        if files:
            latest_file = max(files, key=lambda x: os.path.getctime(os.path.join(data_path, x)))
            file_path = os.path.join(data_path, latest_file)
            df = pd.read_csv(file_path)
            
            # Dados históricos de população por estado (2020-2025)
            historical_data = {
                "São Paulo": {
                    2020: 45919049, 2021: 46289133, 2022: 46649132, 2023: 47009131, 2024: 47369130, 2025: 47729129
                },
                "Minas Gerais": {
                    2020: 21168791, 2021: 21290357, 2022: 21411923, 2023: 21533489, 2024: 21655055, 2025: 21776621
                },
                "Rio de Janeiro": {
                    2020: 17264943, 2021: 17364146, 2022: 17463349, 2023: 17562552, 2024: 17661755, 2025: 17760958
                },
                "Bahia": {
                    2020: 14873064, 2021: 14929174, 2022: 14985284, 2023: 15041394, 2024: 15097504, 2025: 15153614
                },
                "Paraná": {
                    2020: 11516840, 2021: 11657138, 2022: 11797436, 2023: 11937734, 2024: 12078032, 2025: 12218330
                },
                "Rio Grande do Sul": {
                    2020: 11422973, 2021: 11444801, 2022: 11466630, 2023: 11488458, 2024: 11510287, 2025: 11532115
                },
                "Pernambuco": {
                    2020: 9616621, 2021: 9645707, 2022: 9674793, 2023: 9703879, 2024: 9732965, 2025: 9762051
                },
                "Ceará": {
                    2020: 9187103, 2021: 9214301, 2022: 9240580, 2023: 9266859, 2024: 9293138, 2025: 9319417
                },
                "Pará": {
                    2020: 8690745, 2021: 8733994, 2022: 8777124, 2023: 8820254, 2024: 8863384, 2025: 8906514
                },
                "Santa Catarina": {
                    2020: 7338473, 2021: 7550313, 2022: 7762154, 2023: 7973994, 2024: 8185835, 2025: 8397675
                },
                "Maranhão": {
                    2020: 7153262, 2021: 7153262, 2022: 7153262, 2023: 7153262, 2024: 7153262, 2025: 7153262
                },
                "Paraíba": {
                    2020: 4059905, 2021: 4059905, 2022: 4059905, 2023: 4059905, 2024: 4059905, 2025: 4059905
                },
                "Amazonas": {
                    2020: 4269995, 2021: 4269995, 2022: 4269995, 2023: 4269995, 2024: 4269995, 2025: 4269995
                },
                "Espírito Santo": {
                    2020: 4108508, 2021: 4108508, 2022: 4108508, 2023: 4108508, 2024: 4108508, 2025: 4108508
                },
                "Goiás": {
                    2020: 7206589, 2021: 7206589, 2022: 7206589, 2023: 7206589, 2024: 7206589, 2025: 7206589
                },
                "Alagoas": {
                    2020: 3365351, 2021: 3365351, 2022: 3365351, 2023: 3365351, 2024: 3365351, 2025: 3365351
                },
                "Piauí": {
                    2020: 3289290, 2021: 3289290, 2022: 3289290, 2023: 3289290, 2024: 3289290, 2025: 3289290
                },
                "Distrito Federal": {
                    2020: 3094325, 2021: 3094325, 2022: 3094325, 2023: 3094325, 2024: 3094325, 2025: 3094325
                },
                "Mato Grosso do Sul": {
                    2020: 2839188, 2021: 2839188, 2022: 2839188, 2023: 2839188, 2024: 2839188, 2025: 2839188
                },
                "Mato Grosso": {
                    2020: 3567234, 2021: 3567234, 2022: 3567234, 2023: 3567234, 2024: 3567234, 2025: 3567234
                },
                "Rio Grande do Norte": {
                    2020: 3560903, 2021: 3560903, 2022: 3560903, 2023: 3560903, 2024: 3560903, 2025: 3560903
                },
                "Rondônia": {
                    2020: 1815278, 2021: 1815278, 2022: 1815278, 2023: 1815278, 2024: 1815278, 2025: 1815278
                },
                "Tocantins": {
                    2020: 1607363, 2021: 1607363, 2022: 1607363, 2023: 1607363, 2024: 1607363, 2025: 1607363
                },
                "Acre": {
                    2020: 906876, 2021: 906876, 2022: 906876, 2023: 906876, 2024: 906876, 2025: 906876
                },
                "Amapá": {
                    2020: 877613, 2021: 877613, 2022: 877613, 2023: 877613, 2024: 877613, 2025: 877613
                },
                "Roraima": {
                    2020: 652713, 2021: 652713, 2022: 652713, 2023: 652713, 2024: 652713, 2025: 652713
                },
                "Sergipe": {
                    2020: 2338474, 2021: 2338474, 2022: 2338474, 2023: 2338474, 2024: 2338474, 2025: 2338474
                }
            }
            
            # Criar DataFrame com dados históricos
            historical_df = []
            for estado in df['nome'].unique():
                if estado in historical_data:
                    for ano in range(2020, 2026):
                        estado_data = df[df['nome'] == estado].iloc[0].copy()
                        estado_data['ano'] = ano
                        estado_data['populacao'] = historical_data[estado][ano]
                        historical_df.append(estado_data)
            
            return pd.DataFrame(historical_df)
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
st.title("Dashboard de Análise Populacional")
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
    
    # Filtro por ano (simulado - dados do IBGE)
    years = [2020, 2021, 2022, 2023, 2024, 2025]
    selected_year = st.sidebar.selectbox("Selecione o Ano:", years, index=3)  # 2023 como padrão
    
    # Aplicar filtros
    filtered_df = df.copy()
    
    # Filtrar por ano
    filtered_df = filtered_df[filtered_df['ano'] == selected_year]
    
    # Filtrar por região
    if selected_region != 'Todas':
        filtered_df = filtered_df[filtered_df['regiao'] == selected_region]
    
    # Informação do ano
    st.info(f"📅 **Dados de referência: {selected_year}** (Fonte: IBGE)")
    
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
        st.subheader("Top 10 Estados por População")
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
    
    # Gráfico de evolução temporal
    st.subheader("📈 Evolução Populacional (2020-2025)")
    
    # Dados para o gráfico de linha
    evolution_data = df.groupby(['ano', 'regiao'])['populacao'].sum().reset_index()
    
    fig_evolution = px.line(
        evolution_data,
        x='ano',
        y='populacao',
        color='regiao',
        title="Evolução da População por Região",
        labels={'populacao': 'População Total', 'ano': 'Ano'}
    )
    fig_evolution.update_layout(height=400)
    st.plotly_chart(fig_evolution, use_container_width=True)
    
    # Tabela de dados
    st.subheader("📋 Dados Detalhados")
    st.dataframe(
        filtered_df[['nome', 'sigla', 'regiao', 'populacao', 'ano']].sort_values('populacao', ascending=False),
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

