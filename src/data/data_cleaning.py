import pandas as pd 
import numpy as np
from datetime import datetime
import os


def clean_population_data(df):
    """Limpeza e valida os dados de população"""
    print("🧹 Iniciando limpeza e validação dos dados de população...")

    # Copia o DataFrame para evitar modificações inadequadas
    df_clean = df.copy()

    # 1. Verificar dados duplicados
    print("🔍 Verificando dados duplicados...")
    duplicates = df_clean.duplicated().sum()
    if duplicates > 0:
        print(f"🚨 Encontradas {duplicates} linhas duplicadas!")
        print(f"✅ Duplicatas removidas")

    # 2. Verificar valores nulos
    print("🔍 Verificando valores nulos...")
    null_counts = df_clean.isnull().sum()
    print("Valores nulos por coluna:")
    print(null_counts)

    # 3. Limpar nomes dos estados
    if "nome" in df_clean.columns:
        print("🔍 Limpeza de nomes de estados...")
        df_clean["nome"] = df_clean["nome"].str.strip()
        df_clean["nome"] = df_clean["nome"].str.strip()

    # 4. Validar população 
    if "populacao" in df_clean.columns:
        print("Validando dados de população...")

        # Remover valores negativos
        negative_pop = (df_clean["populacao"] < 0).sum()
        if negative_pop > 0:
            print(f"🚨 Encontrados {negative_pop} valores negativos de população!")
            df_clean = df_clean[df_clean["populacao"] >= 0]
        
        #Verificar valores extremos (outliers)
        Q1 = df_clean["populacao"].quantile(0.25)
        Q3 = df_clean["populacao"].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        outliers = ((df_clean["populacao"] < lower_bound) | (df_clean["populacao"] > upper_bound)).sum()

        if outliers > 0:
            print(f"🚨 Encontrados {outliers} valores extremos de população!")
            print(f"    Limite inferior: {lower_bound:,.0f}")
            print(f"    Limite superior: {upper_bound:,.0f}")
    
    # 5 Padronizar regiões
    if "regiao" in df_clean.columns: 
        print("🔧 Padronizando regiões...")
        region_mapping = {
            "sudeste": "Sudeste",
            "nordeste": "Nordeste",
            "sul": "Sul",
            "centro-oeste": "Centro-Oeste",
            "norte": "Norte"
        }
        df_clean["regiao"] = df_clean["regiao"]

    # 6. Adicionar metadados de limpeza
    df_clean['data_limpeza'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    df_clean['versao_dados'] = '1.0'

    print("✅ Limpeza concluída!")
    print(f"✅ Dados finais: {len(df_clean)} registros")

    return df_clean

def validate_data_quality(df):
    """Valida a qualidade dos dados após limepeza"""
    print("\n🔍 Validando qualidade dos dados:")
    
    # 1. Verificar se todos os estados estão presentes
    expected_states =  27 # Brasil tem 26 estados + DF
    actual_states = len(df)
    print(f"🔍 Estados esperados: {expected_states}")
    print(f"🔍 Estados encontrados: {actual_states}")

    if actual_states < expected_states:
        print("⚠️ Alguns estados podem estar faltando")

    # 2. Verificar população total
    if "populacao" in df.columns:
        total_pop = df['populacao'].sum()
        print(f"🔍 População total: {total_pop:,}")

        # Verificar se está próximo do esperado (cerca de 214 milhões)
        if 200_000_000 <= total_pop <= 230_000_000:
            print("✅ População total está dentro do esperado")
        else: 
            print("⚠️ População total pode estar incorreta")
        
    # 3. Verificar distribuição por região
    if "regiao" in df.columns:
        print("\nDistribuição por região:")
        region_dist = df['regiao'].value_counts()
        for region, count in region_dist.items():
            print(f"🔍 {region}: {count} estados")
    
    return True

def save_cleaned_data(df, filename=None):
    """Salva os dados limpos"""

    if filename is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%m%S')
        filename = f"data/processed/cleaned_population_{timestamp}.csv"
    
    # Criar pasta se não existir
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    # Salvar dados
    df.to_csv(filename, index=False, encoding='utf-8')
    print(f"✅ Dados salvos em: {filename}")

    return filename

if __name__ == "__main__":
    # Teste da limpeza
    print("🧹 Iniciando teste de limpeza...")
    print("=" * 40)

    # Carregar dados processador mais recentes
    processed_dir = "data/processed"
    if os.path.exists(processed_dir):
        files = [f for f in os.listdir(processed_dir) if f.endswith(".csv")]
        if files:
            latest_file = max(files, key=lambda x: os.path.getctime(os.path.join(processed_dir, x)))
            file_path = os.path.join(processed_dir, latest_file)

            print(f"📂 Carregando: {file_path}")
            df = pd.read_csv(file_path)

            # Aplicar limpeza
            df_clean = clean_population_data(df)

            #Valida qualidade
            validate_data_quality(df_clean)

            # Salvar dados limpos
            save_cleaned_data(df_clean)

        else:
            print("🔍 Nenhum arquivo processado encontrado")
    else:
        print("🔍 Diretório de dados processados não encontrado")