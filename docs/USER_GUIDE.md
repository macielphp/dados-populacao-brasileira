# 👤 Guia do Usuário - Dashboard de Análise de Dados

## 🎯 **Bem-vindo ao Dashboard!**

Este guia irá ajudá-lo a navegar e utilizar todas as funcionalidades do dashboard de análise de dados populacionais do Brasil.

## 🚀 **Primeiros Passos**

### **1. Acessando o Dashboard**

```bash
# No terminal, navegue até a pasta do projeto
cd dados-populacao-brasileira

# Ative o ambiente virtual
.venv\Scripts\activate  # Windows
# ou
source .venv/bin/activate  # Linux/Mac

# Execute o dashboard
streamlit run src/dashboard/app.py
```

### **2. Abrindo no Navegador**

Após executar o comando, o dashboard abrirá automaticamente em:
- **URL Local:** http://localhost:8501
- **URL da Rede:** http://192.168.x.x:8501

## 📊 **Navegando pelo Dashboard**

### **🏠 Página Principal**

O dashboard está organizado em seções principais:

1. **📋 Cabeçalho:** Título e informações do projeto
2. **🎛️ Barra Lateral:** Filtros e controles
3. **📈 Área Principal:** Visualizações e análises
4. **📊 Seção de Análises:** Estatísticas avançadas

## 🎛️ **Usando os Filtros**

### **Filtro por Região**

**Localização:** Barra lateral esquerda

**Opções disponíveis:**
- **Todas as Regiões:** Mostra dados de todo o Brasil
- **Norte:** Estados da região Norte
- **Nordeste:** Estados da região Nordeste
- **Sudeste:** Estados da região Sudeste
- **Sul:** Estados da região Sul
- **Centro-Oeste:** Estados da região Centro-Oeste

**Como usar:**
1. Clique no seletor "Região"
2. Escolha a região desejada
3. Os dados e gráficos serão atualizados automaticamente

### **Filtro por Ano**

**Localização:** Barra lateral esquerda

**Opções disponíveis:**
- **2020 a 2025:** Dados históricos e projeções

**Como usar:**
1. Clique no seletor "Ano"
2. Escolha o ano desejado
3. Os dados serão filtrados para mostrar apenas o ano selecionado

### **Indicador de Fonte de Dados**

**Localização:** Barra lateral esquerda

**Status possíveis:**
- ✅ **"API de Localidades do IBGE Disponível"** - Dados reais da API
- ⚠️ **"Usando dados em cache"** - Dados salvos localmente
- ⚠️ **"Usando dados estáticos"** - Dados de backup

## 📈 **Explorando as Visualizações**

### **1. Métricas Principais**

**Localização:** Área principal, parte superior

**Métricas exibidas:**
- **Total de Estados:** Número de estados no filtro atual
- **População Total:** Soma da população dos estados filtrados
- **População Média:** Média populacional dos estados
- **Estado Mais Populoso:** Estado com maior população
- **Estado Menos Populoso:** Estado com menor população

### **2. Gráfico de Barras - Top 10 Estados**

**Localização:** Área principal, primeira linha

**O que mostra:**
- Os 10 estados mais populosos
- População de cada estado
- Cores diferentes para cada estado

**Interatividade:**
- Passe o mouse sobre as barras para ver detalhes
- Clique e arraste para zoom
- Use os controles para navegar

### **3. Gráfico de Pizza - Distribuição por Região**

**Localização:** Área principal, segunda linha

**O que mostra:**
- Distribuição percentual da população por região
- Proporção de cada região no total

**Interatividade:**
- Passe o mouse sobre as fatias para ver percentuais
- Clique em uma fatia para destacá-la
- Use a legenda para mostrar/ocultar regiões

### **4. Tabela de Dados**

**Localização:** Área principal, parte inferior

**Funcionalidades:**
- **Ordenação:** Clique nos cabeçalhos para ordenar
- **Busca:** Use a caixa de busca para filtrar estados
- **Paginação:** Navegue entre páginas de resultados
- **Exportação:** Baixe os dados em CSV

**Colunas disponíveis:**
- **Estado:** Nome do estado
- **Sigla:** Sigla do estado
- **População:** População atual
- **Ano:** Ano dos dados
- **Fonte:** Origem dos dados

## 🔬 **Análises Estatísticas Avançadas**

### **Acessando as Análises**

**Localização:** Final da página principal

**Como usar:**
1. Role até a seção "📊 Análises Estatísticas Avançadas"
2. Clique no botão "🔬 Executar Análises Estatísticas"
3. Aguarde o processamento (pode levar alguns segundos)

### **Resultados das Análises**

#### **1. Métricas Estatísticas**

**Exibidas automaticamente:**
- **Total de Estados:** Número de estados analisados
- **População Total:** Soma total da população
- **Média:** Média aritmética da população
- **Mediana:** Valor central da distribuição
- **Desvio Padrão:** Medida de dispersão
- **Assimetria:** Medida de simetria da distribuição
- **Curtose:** Medida do "peso" das caudas

#### **2. Testes de Hipóteses**

**Resultados exibidos:**
- **Teste de Normalidade (Shapiro-Wilk):**
  - p-valor e interpretação
  - Se os dados seguem distribuição normal

- **Análise de Variância (ANOVA):**
  - p-valor e interpretação
  - Se há diferenças significativas entre anos

- **Correlação (Pearson):**
  - Coeficiente de correlação
  - Se há correlação significativa entre população e ano

#### **3. Detecção de Outliers**

**Informações exibidas:**
- **Método IQR:** Estados identificados como outliers
- **Método Z-Score:** Confirmação dos outliers
- **Total de Outliers:** Número de estados atípicos

#### **4. Modelos Preditivos**

**Resultados exibidos:**
- **Regressão Linear:** R² e RMSE
- **Random Forest:** R² e RMSE
- **Melhor Modelo:** Comparação entre os modelos

#### **5. Gráficos Avançados**

**Visualizações geradas:**
- **Boxplot por Ano:** Distribuição da população por ano
- **Scatter Plot:** População vs Ano
- **Histograma:** Distribuição geral da população
- **Gráfico de Barras:** População média por ano

### **Relatório Detalhado**

**Localização:** Expander "📋 Relatório Completo"

**Como acessar:**
1. Clique no expander "📋 Relatório Completo"
2. Role para ver todas as informações detalhadas

**Conteúdo incluído:**
- Resumo executivo
- Resultados completos dos testes
- Interpretações estatísticas
- Recomendações

## 🔍 **Interpretando os Resultados**

### **Estatísticas Básicas**

**O que observar:**
- **Assimetria > 0:** Distribuição com cauda à direita (estados muito populosos)
- **Curtose > 3:** Caudas mais pesadas que a normal
- **Desvio Padrão alto:** Grande variação entre estados

### **Teste de Normalidade**

**Interpretação:**
- **p-valor > 0.05:** Dados normais (pouco provável para população)
- **p-valor ≤ 0.05:** Dados não normais (esperado para população)

### **Análise de Variância**

**Interpretação:**
- **p-valor > 0.05:** Sem diferenças significativas entre anos
- **p-valor ≤ 0.05:** Diferenças significativas entre anos

### **Correlação**

**Interpretação:**
- **|r| > 0.7:** Correlação forte
- **0.3 < |r| < 0.7:** Correlação moderada
- **|r| < 0.3:** Correlação fraca

### **Outliers**

**Estados típicos identificados:**
- São Paulo (mais populoso)
- Minas Gerais
- Rio de Janeiro
- Bahia
- Paraná
- Rio Grande do Sul

### **Modelos Preditivos**

**Interpretação:**
- **R² próximo de 1:** Modelo explica bem a variância
- **R² próximo de 0:** Modelo não explica bem a variância
- **R² negativo:** Modelo pior que usar a média

## 🛠️ **Solução de Problemas**

### **Dashboard não carrega**

**Possíveis causas:**
1. **Porta ocupada:** Feche outros aplicativos usando a porta 8501
2. **Dependências não instaladas:** Execute `pip install -r requirements.txt`
3. **Ambiente virtual não ativado:** Ative o ambiente virtual

**Solução:**
```bash
# Parar processos na porta 8501
netstat -ano | findstr :8501
taskkill /PID <PID> /F

# Reinstalar dependências
pip install -r requirements.txt

# Executar novamente
streamlit run src/dashboard/app.py
```

### **Dados não aparecem**

**Possíveis causas:**
1. **APIs indisponíveis:** IBGE APIs podem estar fora do ar
2. **Arquivos de dados corrompidos:** Cache pode estar corrompido
3. **Filtros muito restritivos:** Nenhum dado atende aos critérios

**Solução:**
1. Verifique o indicador de fonte de dados na barra lateral
2. Limpe o cache: `rm -rf data/cache/*`
3. Redefina os filtros para "Todas as Regiões" e "2023"

### **Análises estatísticas não funcionam**

**Possíveis causas:**
1. **Dados insuficientes:** Poucos estados no filtro atual
2. **Módulo não encontrado:** Problema de importação
3. **Memória insuficiente:** Dados muito grandes

**Solução:**
1. Use filtros mais amplos (ex: "Todas as Regiões")
2. Verifique se o módulo `statistical_analysis.py` existe
3. Reduza o número de anos selecionados

### **Gráficos não carregam**

**Possíveis causas:**
1. **Plotly não instalado:** `pip install plotly`
2. **Dados vazios:** Nenhum dado para visualizar
3. **Erro de JavaScript:** Problema no navegador

**Solução:**
1. Reinstale o Plotly: `pip install plotly --upgrade`
2. Verifique se há dados nos filtros
3. Tente outro navegador (Chrome, Firefox, Edge)

## 📱 **Dicas de Uso**

### **Para Análise Rápida:**
1. Use "Todas as Regiões" e ano atual
2. Observe as métricas principais
3. Explore o gráfico de barras dos top 10
4. Execute análises estatísticas básicas

### **Para Análise Comparativa:**
1. Compare diferentes regiões
2. Analise a evolução temporal (diferentes anos)
3. Use a tabela para ordenar por população
4. Execute análises estatísticas completas

### **Para Análise Detalhada:**
1. Foque em uma região específica
2. Compare anos consecutivos
3. Identifique outliers
4. Analise correlações e tendências

### **Para Apresentações:**
1. Use filtros específicos para seu público
2. Capture screenshots dos gráficos
3. Use o relatório detalhado para insights
4. Exporte dados para análises externas

## 🎯 **Casos de Uso Comuns**

### **1. Análise Regional**
- **Objetivo:** Comparar regiões do Brasil
- **Passos:**
  1. Selecione uma região específica
  2. Observe as métricas principais
  3. Compare com outras regiões
  4. Execute análises estatísticas

### **2. Análise Temporal**
- **Objetivo:** Verificar evolução populacional
- **Passos:**
  1. Compare diferentes anos
  2. Observe tendências nos gráficos
  3. Analise correlações temporais
  4. Verifique significância estatística

### **3. Identificação de Outliers**
- **Objetivo:** Encontrar estados atípicos
- **Passos:**
  1. Execute análises estatísticas
  2. Observe a seção de outliers
  3. Compare com a média nacional
  4. Analise as causas possíveis

### **4. Análise Preditiva**
- **Objetivo:** Entender capacidade preditiva dos modelos
- **Passos:**
  1. Execute análises estatísticas
  2. Observe os R² dos modelos
  3. Compare Linear Regression vs Random Forest
  4. Interprete os resultados

## 📞 **Suporte**

### **Problemas Técnicos:**
- Verifique a documentação em `docs/`
- Consulte o troubleshooting acima
- Verifique logs no terminal

### **Dúvidas sobre Análises:**
- Leia `docs/STATISTICAL_ANALYSIS.md`
- Consulte a interpretação dos resultados
- Use o relatório detalhado

### **Melhorias e Sugestões:**
- Abra uma issue no repositório
- Descreva o problema detalhadamente
- Inclua screenshots se possível

---

**🎉 Agora você está pronto para explorar todos os recursos do dashboard!**
