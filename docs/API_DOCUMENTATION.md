# 🔌 Documentação das APIs

## 📊 **APIs do IBGE Utilizadas**

### **1. API de Localidades - Estados**

#### **Endpoint:**
```
GET https://servicodados.ibge.gov.br/api/v1/localidades/estados
```

#### **Descrição:**
Retorna informações sobre todos os estados brasileiros, incluindo ID, sigla, nome e região.

#### **Resposta:**
```json
[
  {
    "id": 11,
    "sigla": "RO",
    "nome": "Rondônia",
    "regiao": {
      "id": 1,
      "sigla": "N",
      "nome": "Norte"
    }
  }
]
```

#### **Uso no Projeto:**
```python
# Em src/data/api_client.py
def get_states_info(self):
    """Busca informações dos estados via API de Localidades"""
    url = f"{self.base_url}/localidades/estados"
    response = requests.get(url, timeout=self.timeout)
    response.raise_for_status()
    return response.json()
```

### **2. API de Agregados - População**

#### **Endpoint:**
```
GET https://servicodados.ibge.gov.br/api/v3/agregados/6579/periodos/{year}/variaveis/9324?localidades=N3[all]
```

#### **Parâmetros:**
- `6579`: ID da pesquisa de população
- `{year}`: Ano desejado (2020-2025)
- `9324`: ID da variável população
- `N3[all]`: Todos os estados

#### **Resposta:**
```json
{
  "resultados": [
    {
      "classificacoes": [],
      "series": [
        {
          "localidade": {
            "nivel": {
              "id": 3,
              "nome": "Unidade da Federação"
            },
            "id": "11",
            "nome": "Rondônia"
          },
          "serie": {
            "2022": [
              {
                "valor": "1777225"
              }
            ]
          }
        }
      ]
    }
  ]
}
```

#### **Status:**
⚠️ **Problemas de Disponibilidade:** Esta API frequentemente retorna erros 503/500, por isso implementamos fallback para dados estáticos.

### **3. API de Pesquisas (Alternativa)**

#### **Endpoint:**
```
GET https://servicodados.ibge.gov.br/api/v1/pesquisas/6579/periodos/{year}/indicadores/9324/resultados/BR
```

#### **Status:**
❌ **Indisponível:** Retorna erro 500 consistentemente.

## 🔄 **Sistema de Fallback**

### **Estratégia Implementada:**

1. **Tentativa 1:** API de Agregados
2. **Tentativa 2:** API de Pesquisas  
3. **Tentativa 3:** API de Localidades + Dados Estáticos
4. **Fallback Final:** Dados estáticos completos

### **Dados Estáticos Utilizados:**

```python
# População por estado e ano (2020-2025)
static_population_data = {
    "São Paulo": {
        2020: 46649132, 2021: 46843678, 2022: 47038224,
        2023: 47232770, 2024: 47427316, 2025: 47621862
    },
    "Minas Gerais": {
        2020: 21411923, 2021: 21516477, 2022: 21621031,
        2023: 21725585, 2024: 21830139, 2025: 21934693
    }
    # ... todos os 27 estados
}
```

## 🗄️ **Sistema de Cache**

### **Implementação:**

```python
class DataCache:
    def __init__(self, cache_dir="data/cache"):
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
    
    def save_data(self, key, data):
        """Salva dados no cache"""
        filename = f"{key}.json"
        filepath = os.path.join(self.cache_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def load_data(self, key):
        """Carrega dados do cache"""
        filename = f"{key}.json"
        filepath = os.path.join(self.cache_dir, filename)
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None
```

### **Estrutura do Cache:**
```
data/cache/
├── population_2020.json
├── population_2021.json
├── population_2022.json
├── population_2023.json
├── population_2024.json
├── population_2025.json
└── states_info.json
```

## 🔧 **Tratamento de Erros**

### **Retry Logic:**
```python
def make_request_with_retry(url, max_retries=3):
    """Faz requisição com retry automático"""
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            if attempt == max_retries - 1:
                raise e
            time.sleep(2 ** attempt)  # Exponential backoff
```

### **Códigos de Erro Tratados:**
- **503 Service Unavailable:** API temporariamente indisponível
- **500 Internal Server Error:** Erro interno do servidor
- **Timeout:** Requisição demorou muito
- **Connection Error:** Problemas de conectividade

## 📊 **Monitoramento de Status**

### **Indicadores no Dashboard:**
- ✅ **API Disponível:** "✅ API de Localidades do IBGE Disponível"
- ⚠️ **Usando Cache:** "⚠️ Usando dados em cache"
- ❌ **Usando Fallback:** "⚠️ Usando dados estáticos"

### **Logs de Debug:**
```python
# Exemplo de log
print(f"🔄 Tentativa {i+1}: {url}")
print(f"✅ Dados coletados com sucesso do endpoint {i+1}!")
print(f"❌ Falha no endpoint {i+1}: {e}")
print("⚠️ Todos os endpoints falharam. Usando dados de exemplo...")
```

## 🚀 **Melhorias Futuras**

### **APIs Adicionais Sugeridas:**

1. **IBGE - Indicadores Econômicos:**
   - PIB por estado
   - Taxa de desemprego
   - Índice de desenvolvimento humano

2. **APIs Climáticas:**
   - Temperatura média
   - Precipitação
   - Qualidade do ar

3. **APIs de Transporte:**
   - Dados de migração
   - Fluxo de pessoas entre estados

### **Otimizações de Performance:**
- Cache Redis para melhor performance
- Compressão de dados
- Paginação de resultados
- Rate limiting inteligente

## 📋 **Limitações Atuais**

1. **Dependência de APIs Externas:** IBGE APIs podem estar indisponíveis
2. **Dados Históricos Limitados:** Apenas 2020-2025
3. **Granularidade:** Apenas nível estadual
4. **Frequência de Atualização:** Dados estáticos não se atualizam automaticamente

## 🔍 **Troubleshooting de APIs**

### **Problemas Comuns:**

1. **API Retorna 503:**
   - Aguardar alguns minutos
   - Verificar status do IBGE
   - Usar dados em cache

2. **Timeout de Requisição:**
   - Aumentar timeout
   - Verificar conectividade
   - Implementar retry

3. **Dados Inconsistentes:**
   - Verificar formato da resposta
   - Validar dados antes de salvar
   - Implementar validação

### **Comandos de Debug:**
```bash
# Testar conectividade
curl -I https://servicodados.ibge.gov.br/api/v1/localidades/estados

# Verificar cache
ls -la data/cache/

# Limpar cache
rm -rf data/cache/*
```

---

**📚 Esta documentação deve ser atualizada conforme novas APIs são integradas ao projeto.**
