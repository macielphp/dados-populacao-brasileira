import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
from datetime import datetime
import os
import sys

# Adicionar diretório atual ao path para importações
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Importar o novo sistema de APIs
try:
    from src.data.api_client import get_data_with_fallback, get_available_years
    API_AVAILABLE = True
except ImportError as e:
    API_AVAILABLE = False
    st.warning(f"⚠️ Sistema de APIs não disponível: {e}")

# Importar análises estatísticas da Fase 6
try:
    from src.analytics.statistical_analysis import PopulationAnalyzer
    ANALYTICS_AVAILABLE = True
except ImportError as e:
    ANALYTICS_AVAILABLE = False
    st.warning(f"⚠️ Módulo de análises não disponível: {e}")


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
    """Carrega dados com sistema de APIs e fallback"""
    try:
        data_path = get_data_path()
        if data_path is None:
            return None
            
        # Tentar usar API se disponível
        if API_AVAILABLE:
            # Carregar dados básicos dos estados
            files = [f for f in os.listdir(data_path) if f.startswith("cleaned_population") and f.endswith(".csv")]
            
            if files:
                latest_file = max(files, key=lambda x: os.path.getctime(os.path.join(data_path, x)))
                file_path = os.path.join(data_path, latest_file)
                df_base = pd.read_csv(file_path)
                
                # Criar DataFrame com dados históricos
                historical_df = []
                
                for ano in range(2020, 2026):
                    # Tentar API para cada ano
                    api_data = get_data_with_fallback(ano)
                    
                    if api_data:
                        # Usar dados da API
                        for item in api_data:
                            estado_data = df_base[df_base['nome'] == item['nome']].iloc[0].copy()
                            estado_data['ano'] = ano
                            estado_data['populacao'] = item['populacao']
                            estado_data['fonte'] = item['fonte']
                            historical_df.append(estado_data)
                    else:
                        # Usar dados estáticos
                        for estado in df_base['nome'].unique():
                            estado_data = df_base[df_base['nome'] == estado].iloc[0].copy()
                            estado_data['ano'] = ano
                            estado_data['populacao'] = get_static_population(estado, ano)
                            estado_data['fonte'] = 'Dados Estáticos'
                            historical_df.append(estado_data)
                
                return pd.DataFrame(historical_df)
        
        # Fallback para dados estáticos originais
        return load_static_data()
        
    except Exception as e:
        st.error(f"❌ Erro ao carregar dados: {e}")
        return load_static_data()

def get_static_population(estado, ano):
    """Retorna população estática para um estado e ano"""
    static_data = {
        "São Paulo": {2020: 45919049, 2021: 46289133, 2022: 46649132, 2023: 47009131, 2024: 47369130, 2025: 47729129},
        "Minas Gerais": {2020: 21168791, 2021: 21290357, 2022: 21411923, 2023: 21533489, 2024: 21655055, 2025: 21776621},
        "Rio de Janeiro": {2020: 17264943, 2021: 17366189, 2022: 17463349, 2023: 17560499, 2024: 17657649, 2025: 17754799},
        "Bahia": {2020: 14873064, 2021: 14961684, 2022: 15050284, 2023: 15138884, 2024: 15227484, 2025: 15316084},
        "Paraná": {2020: 11516840, 2021: 11597440, 2022: 11677936, 2023: 11758436, 2024: 11838936, 2025: 11919436},
        "Rio Grande do Sul": {2020: 11377239, 2021: 11422987, 2022: 11468735, 2023: 11514483, 2024: 11560231, 2025: 11605979},
        "Pernambuco": {2020: 9557071, 2021: 9616621, 2022: 9676171, 2023: 9735721, 2024: 9795271, 2025: 9854821},
        "Ceará": {2020: 9132078, 2021: 9187105, 2022: 9242132, 2023: 9297159, 2024: 9352186, 2025: 9407213},
        "Pará": {2020: 8602865, 2021: 8690745, 2022: 8778625, 2023: 8866505, 2024: 8954385, 2025: 9042265},
        "Santa Catarina": {2020: 7164788, 2021: 7226894, 2022: 7289000, 2023: 7351106, 2024: 7413212, 2025: 7475318},
        "Maranhão": {2020: 7075181, 2021: 7123917, 2022: 7172653, 2023: 7221389, 2024: 7270125, 2025: 7318861},
        "Goiás": {2020: 7018354, 2021: 7079187, 2022: 7140020, 2023: 7200853, 2024: 7261686, 2025: 7322519},
        "Amazonas": {2020: 4144597, 2021: 4186907, 2022: 4229217, 2023: 4271527, 2024: 4313837, 2025: 4356147},
        "Espírito Santo": {2020: 4018650, 2021: 4046785, 2022: 4074920, 2023: 4103055, 2024: 4131190, 2025: 4159325},
        "Paraíba": {2020: 4018127, 2021: 4039777, 2022: 4061427, 2023: 4083077, 2024: 4104727, 2025: 4126377},
        "Rio Grande do Norte": {2020: 3506853, 2021: 3529353, 2022: 3551853, 2023: 3574353, 2024: 3596853, 2025: 3619353},
        "Mato Grosso": {2020: 3484466, 2021: 3526220, 2022: 3567974, 2023: 3609728, 2024: 3651482, 2025: 3693236},
        "Alagoas": {2020: 3337357, 2021: 3351543, 2022: 3365729, 2023: 3379915, 2024: 3394101, 2025: 3408287},
        "Piauí": {2020: 3273227, 2021: 3289290, 2022: 3305353, 2023: 3321416, 2024: 3337479, 2025: 3353542},
        "Distrito Federal": {2020: 3055149, 2021: 3088671, 2022: 3122193, 2023: 3155715, 2024: 3189237, 2025: 3222759},
        "Mato Grosso do Sul": {2020: 2778986, 2021: 2804144, 2022: 2829302, 2023: 2854460, 2024: 2879618, 2025: 2904776},
        "Sergipe": {2020: 2298696, 2021: 2318822, 2022: 2338948, 2023: 2359074, 2024: 2379200, 2025: 2399326},
        "Rondônia": {2020: 1777225, 2021: 1796460, 2022: 1815695, 2023: 1834930, 2024: 1854165, 2025: 1873400},
        "Tocantins": {2020: 1572866, 2021: 1590248, 2022: 1607630, 2023: 1625012, 2024: 1642394, 2025: 1659776},
        "Acre": {2020: 881935, 2021: 894470, 2022: 907005, 2023: 919540, 2024: 932075, 2025: 944610},
        "Amapá": {2020: 845731, 2021: 857735, 2022: 869739, 2023: 881743, 2024: 893747, 2025: 905751},
        "Roraima": {2020: 605761, 2021: 612783, 2022: 619805, 2023: 626827, 2024: 633849, 2025: 640871}
    }
    
    return static_data.get(estado, {}).get(ano, 0)

def load_static_data():
    """Carrega dados estáticos (função original)"""
    try:
        # Dados estáticos dos estados brasileiros
        estados_data = [
            {"id": 11, "sigla": "RO", "nome": "Rondônia", "regiao": "Norte"},
            {"id": 12, "sigla": "AC", "nome": "Acre", "regiao": "Norte"},
            {"id": 13, "sigla": "AM", "nome": "Amazonas", "regiao": "Norte"},
            {"id": 14, "sigla": "RR", "nome": "Roraima", "regiao": "Norte"},
            {"id": 15, "sigla": "PA", "nome": "Pará", "regiao": "Norte"},
            {"id": 16, "sigla": "AP", "nome": "Amapá", "regiao": "Norte"},
            {"id": 17, "sigla": "TO", "nome": "Tocantins", "regiao": "Norte"},
            {"id": 21, "sigla": "MA", "nome": "Maranhão", "regiao": "Nordeste"},
            {"id": 22, "sigla": "PI", "nome": "Piauí", "regiao": "Nordeste"},
            {"id": 23, "sigla": "CE", "nome": "Ceará", "regiao": "Nordeste"},
            {"id": 24, "sigla": "RN", "nome": "Rio Grande do Norte", "regiao": "Nordeste"},
            {"id": 25, "sigla": "PB", "nome": "Paraíba", "regiao": "Nordeste"},
            {"id": 26, "sigla": "PE", "nome": "Pernambuco", "regiao": "Nordeste"},
            {"id": 27, "sigla": "AL", "nome": "Alagoas", "regiao": "Nordeste"},
            {"id": 28, "sigla": "SE", "nome": "Sergipe", "regiao": "Nordeste"},
            {"id": 29, "sigla": "BA", "nome": "Bahia", "regiao": "Nordeste"},
            {"id": 31, "sigla": "MG", "nome": "Minas Gerais", "regiao": "Sudeste"},
            {"id": 32, "sigla": "ES", "nome": "Espírito Santo", "regiao": "Sudeste"},
            {"id": 33, "sigla": "RJ", "nome": "Rio de Janeiro", "regiao": "Sudeste"},
            {"id": 35, "sigla": "SP", "nome": "São Paulo", "regiao": "Sudeste"},
            {"id": 41, "sigla": "PR", "nome": "Paraná", "regiao": "Sul"},
            {"id": 42, "sigla": "SC", "nome": "Santa Catarina", "regiao": "Sul"},
            {"id": 43, "sigla": "RS", "nome": "Rio Grande do Sul", "regiao": "Sul"},
            {"id": 50, "sigla": "MS", "nome": "Mato Grosso do Sul", "regiao": "Centro-Oeste"},
            {"id": 51, "sigla": "MT", "nome": "Mato Grosso", "regiao": "Centro-Oeste"},
            {"id": 52, "sigla": "GO", "nome": "Goiás", "regiao": "Centro-Oeste"},
            {"id": 53, "sigla": "DF", "nome": "Distrito Federal", "regiao": "Centro-Oeste"}
        ]
        
        # Criar DataFrame com dados históricos
        historical_df = []
        
        for estado in estados_data:
            for ano in range(2020, 2026):
                estado_data = estado.copy()
                estado_data['ano'] = ano
                estado_data['populacao'] = get_static_population(estado['nome'], ano)
                estado_data['fonte'] = 'Dados Estáticos'
                estado_data['data_coleta'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                estado_data['data_limpeza'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                estado_data['versao_dados'] = '1.0'
                historical_df.append(estado_data)
        
        return pd.DataFrame(historical_df)
        
    except Exception as e:
        st.error(f"❌ Erro ao carregar dados estáticos: {e}")
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
    
    # Filtro por ano - usar anos disponíveis da API ou fallback
    if API_AVAILABLE:
        try:
            available_years = get_available_years()
            if available_years:
                years = available_years
                default_index = len(years) - 1  # Último ano disponível
            else:
                years = [2020, 2021, 2022, 2023, 2024, 2025]
                default_index = 3
        except:
            years = [2020, 2021, 2022, 2023, 2024, 2025]
            default_index = 3
    else:
        years = [2020, 2021, 2022, 2023, 2024, 2025]
        default_index = 3
    
    selected_year = st.sidebar.selectbox("Selecione o Ano:", years, index=default_index)
    
    # Indicador de fonte de dados
    st.sidebar.markdown("---")
    st.sidebar.subheader("🌐 Fonte de Dados")
    
    if API_AVAILABLE:
        try:
            available_years = get_available_years()
            if available_years:
                st.sidebar.success("✅ API de Localidades do IBGE Disponível")
                st.sidebar.info(f"📅 Anos disponíveis: {min(available_years)}-{max(available_years)}")
                st.sidebar.info("🔄 Estados via API + População Estática")
            else:
                st.sidebar.warning("⚠️ API disponível mas sem dados")
                st.sidebar.info("📊 Usando dados estáticos")
        except:
            st.sidebar.warning("⚠️ Erro ao conectar com API")
            st.sidebar.info("📊 Usando dados estáticos")
    else:
        st.sidebar.warning("⚠️ API não disponível")
        st.sidebar.info("📊 Dados históricos simulados")
    
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
    
    # Seção de Análises Estatísticas Avançadas (Fase 6)
    if ANALYTICS_AVAILABLE:
        st.markdown("---")
        st.header("📊 Análises Estatísticas Avançadas")
        
        # Botão para executar análises
        if st.button("🔬 Executar Análises Estatísticas"):
            with st.spinner("Executando análises estatísticas..."):
                try:
                    # Criar analisador
                    analyzer = PopulationAnalyzer(df)
                    
                    # Executar análises
                    basic_stats = analyzer.basic_statistics()
                    regional_analysis = analyzer.regional_analysis()
                    correlation_analysis = analyzer.correlation_analysis()
                    outlier_analysis = analyzer.outlier_detection()
                    
                    # Exibir resultados
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("📈 Estatísticas Básicas")
                        st.metric("População Total", f"{basic_stats['total_population']:,}")
                        st.metric("Média", f"{basic_stats['mean_population']:,.0f}")
                        st.metric("Mediana", f"{basic_stats['median_population']:,.0f}")
                        st.metric("Desvio Padrão", f"{basic_stats['std_population']:,.0f}")
                    
                    with col2:
                        st.subheader("🔍 Análise Regional")
                        st.metric("Diferenças Significativas", 
                                "✅ Sim" if regional_analysis['significant_differences'] else "❌ Não")
                        st.metric("P-valor ANOVA", f"{regional_analysis['anova_p_value']:.4f}")
                        st.metric("Correlação Pop-Ano", f"{correlation_analysis['population_year_correlation']:.3f}")
                        st.metric("Outliers Detectados", outlier_analysis['total_outliers_iqr'])
                    
                    # Gráficos avançados
                    st.subheader("📊 Visualizações Avançadas")
                    fig = analyzer.plot_analysis()
                    st.pyplot(fig)
                    
                    # Relatório detalhado
                    with st.expander("📋 Relatório Detalhado"):
                        st.write("### Estatísticas por Ano")
                        st.dataframe(regional_analysis['yearly_stats'])
                        
                        st.write("### Matriz de Correlação")
                        st.dataframe(correlation_analysis['correlation_matrix'])
                        
                        if outlier_analysis['total_outliers_iqr'] > 0:
                            st.write("### Outliers Detectados")
                            st.dataframe(outlier_analysis['iqr_outliers'][['nome', 'populacao', 'ano']])
                    
                    st.success("✅ Análises estatísticas concluídas!")
                    
                except Exception as e:
                    st.error(f"❌ Erro ao executar análises: {e}")
    else:
        st.warning("⚠️ Módulo de análises estatísticas não disponível")

else:
    st.error("❌ Não foi possível carregar os dados. Verifique se os arquivos existem.")

# Footer
st.markdown("---")

