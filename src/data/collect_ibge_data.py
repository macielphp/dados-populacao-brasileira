import requests
import pandas as pd
import json
from datetime import datetime
import os
import time 
from config.data_config import IBGE_POPULATION_URL, IBGE_STATES_URL, RAW_DATA_PATH, PROCESSED_DATA_PATH, EXTERNAL_DATA_PATH, REQUEST_TIMEOUT, MAX_RETRIES, ENCODING, DATE_FORMAT

def collect_population_data():
    """
    Coleta dados de população por estado do IBGE
    """
    print("🔄 Iniciando coleta de dados do IBGE...")
    
    # URL da API do IBGE para população por estado
    endpoints = [
        # 1. Lista de estados (sempre funciona)
        "https://servicodados.ibge.gov.br/api/v1/localidades/estados",
        
        # 2. População por UF - dados agregados (Censo/PNAD)
        "https://servicodados.ibge.gov.br/api/v3/agregados/4714/periodos/2022/variaveis/93?localidades=N3[all]",
        
        # 3. Projeções populacionais por UF
        "https://servicodados.ibge.gov.br/api/v1/projecoes/populacao/BR",
        
        # 4. Dados de população estimada por município (podemos agregar por estado)
        "https://servicodados.ibge.gov.br/api/v3/agregados/6579/periodos/2023/variaveis/9324?localidades=N3[all]"

    ]
    
    for i, url in enumerate(endpoints, 1):
        print(f"\n🌐 Tentando endpoint {i}: {url}")

        try:
            data = make_request_with_retry(url)
            if data: 
                print(f"✅ Dados coletados com sucesso do endpoint {i+1}!")
                save_raw_data(data, f"endpoin_{i}")

                # Processa os dados dependendo do endpoint
                if i == 1: #Estados
                    processed_data = process_states_data(data)
                elif i in [2, 4]: #Dados agregados
                    processed_data = process_aggregated_data(data)
                elif i == 3: #Projeções
                    processed_data = process_projections_data(data)

                if processed_data is not None and len(processed_data) > 0:
                    print(f"✅ Dados processados: {len(processed_data)}")
                    return processed_data
                return processed_data
        except Exception as e:
            print(f"❌ Erro ao coletar dados do endpoint {i}: {str(e)}")
            continue
    # Se todos os endpoints falharem, usar dados de exemplo
    print("❌ Não foi possível coletar dados de nenhum endpoint. Usando dados de exemplo...")
    return use_sample_data()


def make_request_with_retry(url, max_retries=MAX_RETRIES):
    """Faz requisição com tentativas múltiplas e headers apropriados"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json',
        'Accept-Encoding': 'gzip, deflate'
    }
    """Faz requisição com tentativas múltiplicas"""
    for attempt in range(max_retries):
        try: 
            print(f"Tentativa {attempt +1}/{max_retries}...")
            response = requests.get(url, timeout=REQUEST_TIMEOUT)
            print(f"  📊 Status Code: {response.status_code}")
            print(f"  📊 Headers: {response.headers}")
            
            if response.status_code == 503:
                print("  ⚠️  Serviço temporariamente indisponível (503)")
                raise requests.exceptions.RequestException("Service unavailable")

            response.raise_for_status()
            data = response.json()

            if data:
                print(f"Respostas recebidas: {len(data) if isinstance(data, list) else 1} item(s)")
                return data
            else:
                print("⚠️ Resposta vazia")
        except requests.exceptions.RequestException as e:
            print(f"Tentativa {attempt + 1} falhou: {str(e)}")
            if attempt < max_retries - 1:
                print(f"  ⏳ Aguardando 2 segundos antes da próxima tentativa...")
                time.sleep(2)
            else: 
                raise e
    
def process_states_data(data):
    """Processa dados básicos dos estados"""
    print("🔧 Processando dados dos estados...")

    states_data = []
    for state in data:
        states_data.append({
            'id': state.get('id'),
            'sigla': state.get('sigla'),
            'nome': state.get('nome'),
            'regiao': state.get('regiao', {}).get('nome', 'N/A'),
            'data_coleta': datetime.now().strftime('%Y-%m-%d %H-:%M:%S')
        })
    return states_data

def process_aggregated_data(data):
    """Processa dados agregados de população por estado"""
    print("🔧 Processando dados agregados...")

    population_data = []
    try: 
        for item in data:
            if 'localidade' in item:
                for localidade in item['localidades']:
                    nome = localidade.get('localidade', {}).get('nome', 'N/A')

                    # Pega o valor da série
                    serie_value = None
                    if 'series' in localidade:
                        for series in localidade['series']:
                            if '2022' in series or '2023' in series:
                                values = list(series.values())
                                if values and values[0] != '-':
                                    serie_value = values[0]
                                    break
                    if serie_value:
                        population_data.append({
                            'nome': nome,
                            'populacao': int(str(serie_value).replace('.', '').replace(',', '')),
                            'data_coleta': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        })

    except Exception as e:
        print(f"❌ Erro ao processar dados agregados: {str(e)}")
        return None

    return population_data

def process_projections_data(data):
    """Processa dados de projeções populacionais por estado"""
    print("🔧 Processando dados de projeções...")

    # A API de projeções tem estrutura diferente
    # Retorna dados agregados para usar como fallback
    return None

def use_sample_data():
    """Usa dados de exemplo se a coleta falhar"""
    print("🔄 Usando dados de exemplo...")

    # Dados de população por estado(exemplo)
    sample_data = [
        {"nome": "São Paulo", "populacao": 46649132, "regiao": "Sudeste"},
        {"nome": "Minas Gerais", "populacao": 21411923, "regiao": "Sudeste"},
        {"nome": "Rio de Janeiro", "populacao": 17463349, "regiao": "Sudeste"},
        {"nome": "Bahia", "populacao": 14985284, "regiao": "Nordeste"},
        {"nome": "Paraná", "populacao": 11797436, "regiao": "Sul"},
        {"nome": "Rio Grande do Sul", "populacao": 11466630, "regiao": "Sul"},
        {"nome": "Pernambuco", "populacao": 9674793, "regiao": "Nordeste"},
        {"nome": "Ceará", "populacao": 9240580, "regiao": "Nordeste"},
        {"nome": "Pará", "populacao": 8777124, "regiao": "Norte"},
        {"nome": "Santa Catarina", "populacao": 7762154, "regiao": "Sul"},
        {"nome": "Maranhão", "populacao": 7153262, "regiao": "Nordeste"},
        {"nome": "Paraíba", "populacao": 4059905, "regiao": "Nordeste"},
        {"nome": "Amazonas", "populacao": 4269995, "regiao": "Norte"},
        {"nome": "Espírito Santo", "populacao": 4108508, "regiao": "Sudeste"},
        {"nome": "Goiás", "populacao": 7206589, "regiao": "Centro-Oeste"},
        {"nome": "Alagoas", "populacao": 3365351, "regiao": "Nordeste"},
        {"nome": "Piauí", "populacao": 3289290, "regiao": "Nordeste"},
        {"nome": "Distrito Federal", "populacao": 3094325, "regiao": "Centro-Oeste"},
        {"nome": "Mato Grosso do Sul", "populacao": 2839188, "regiao": "Centro-Oeste"},
        {"nome": "Mato Grosso", "populacao": 3567234, "regiao": "Centro-Oeste"},
        {"nome": "Rio Grande do Norte", "populacao": 3560903, "regiao": "Nordeste"},
        {"nome": "Rondônia", "populacao": 1815278, "regiao": "Norte"},
        {"nome": "Tocantins", "populacao": 1607363, "regiao": "Norte"},
        {"nome": "Acre", "populacao": 906876, "regiao": "Norte"},
        {"nome": "Amapá", "populacao": 877613, "regiao": "Norte"},
        {"nome": "Roraima", "populacao": 652713, "regiao": "Norte"},
        {"nome": "Sergipe", "populacao": 2338474, "regiao": "Nordeste"}
    ]

    for item in sample_data:
        item['data_coleta'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    print(f"Dados de exemplo criados com {len(sample_data)} estados.")
    return sample_data

def save_raw_data(data, source="api"):
    """
    Salva os dados brutos em formato JSON
    """
    # Criando pasta se não existir
    os.makedirs("data/raw", exist_ok=True)
    
    # Nome do arquivo com timestamp
    timestamp = datetime.now().strftime(DATE_FORMAT)
    filename = f"{RAW_DATA_PATH}/ibge_population_{source}_{timestamp}.json"

    with open(filename, "w", encoding=ENCODING) as f: 
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Dados salvos em: {filename}")

def process_and_save_final_data(data):
    """Processa e salva os dados finais"""
    print("🔧 Processamento final dos dados...")
    
    # Cria DataFrame
    df = pd.DataFrame(data)
    
    # Informações básicas
    print(f"📋 Colunas disponíveis: {list(df.columns)}")
    print(f"📊 Primeiras 5 linhas:")
    print(df.head())
    print(f"📈 Total de registros: {len(df)}")
    
    if 'populacao' in df.columns:
        total_pop = df['populacao'].sum()
        print(f"👥 População total: {total_pop:,}")
        
        # Adiciona percentual
        df['percentual_populacional'] = (df['populacao'] / total_pop * 100).round(2)
    
    # Salva dados processados
    save_processed_data(df)
    
    return df

def save_processed_data(df):
    """
    Salva os dados processados em CSV
    """
    # Criando pasta se não existir
    os.makedirs(PROCESSED_DATA_PATH, exist_ok=True)
    
    # Nome do arquivo com timestamp
    timestamp = datetime.now().strftime(DATE_FORMAT)
    filename = f"{PROCESSED_DATA_PATH}/ibge_population_{timestamp}.csv"
    
    # Salvando arquivo
    df.to_csv(filename, index=False, encoding=ENCODING)
    
    print(f"💾 Dados processados salvos em: {filename}")

if __name__ == "__main__":
    print("🇧🇷 IBGE Data Collector - População por Estado")
    print("=" * 50)
    
    # Executa a coleta
    population_data = collect_population_data()
    
    if population_data:
        final_df = process_and_save_final_data(population_data)
        print("\n🎉 Coleta concluída com sucesso!")
        print(f"📊 Total de registros processados: {len(final_df)}")
        
        if 'populacao' in final_df.columns:
            top_states = final_df.nlargest(5, 'populacao')[['nome', 'populacao']]
            print("\n🏆 Top 5 estados por população:")
            for idx, row in top_states.iterrows():
                print(f"  {row['nome']}: {row['populacao']:,} habitantes")
    else:
        print("❌ Falha na coleta de dados")
