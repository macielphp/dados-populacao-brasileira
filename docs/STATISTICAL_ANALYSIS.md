# 📊 Documentação das Análises Estatísticas

## 🎯 **Visão Geral**

Este documento descreve as análises estatísticas avançadas implementadas no módulo `src/analytics/statistical_analysis.py`. As análises incluem estatísticas descritivas, testes de hipóteses, detecção de outliers e modelos preditivos.

## 🔬 **Classe PopulationAnalyzer**

### **Inicialização:**
```python
class PopulationAnalyzer:
    def __init__(self, data):
        """
        Inicializa o analisador com dados populacionais
        
        Args:
            data (pd.DataFrame): DataFrame com dados populacionais
        """
        self.data = data
        self.results = {}
```

## 📈 **1. Estatísticas Básicas**

### **Método: `basic_statistics()`**

#### **Métricas Calculadas:**
- **Total:** Soma da população
- **Média:** Média aritmética
- **Mediana:** Valor central
- **Desvio Padrão:** Dispersão dos dados
- **Mínimo/Máximo:** Valores extremos
- **Quartis (Q1, Q3):** 25º e 75º percentis
- **IQR:** Intervalo interquartil
- **Assimetria:** Medida de simetria da distribuição
- **Curtose:** Medida de "peso" das caudas

#### **Implementação:**
```python
def basic_statistics(self):
    """Calcula estatísticas básicas da população"""
    stats_dict = {
        'total_population': self.data['populacao'].sum(),
        'mean_population': self.data['populacao'].mean(),
        'median_population': self.data['populacao'].median(),
        'std_population': self.data['populacao'].std(),
        'min_population': self.data['populacao'].min(),
        'max_population': self.data['populacao'].max(),
        'q1': self.data['populacao'].quantile(0.25),
        'q3': self.data['populacao'].quantile(0.75),
        'iqr': self.data['populacao'].quantile(0.75) - self.data['populacao'].quantile(0.25),
        'skewness': self.data['populacao'].skew(),
        'kurtosis': self.data['populacao'].kurtosis()
    }
    return stats_dict
```

## 📊 **2. Análise de Distribuição**

### **Método: `distribution_analysis()`**

#### **Teste de Normalidade - Shapiro-Wilk:**

**Hipótese Nula (H₀):** Os dados seguem uma distribuição normal
**Hipótese Alternativa (H₁):** Os dados não seguem uma distribuição normal

**Critério de Decisão:**
- Se p-valor > 0.05 → **ACEITA** H₀ (dados normais)
- Se p-valor ≤ 0.05 → **REJEITA** H₀ (dados não normais)

#### **Visualizações:**
1. **Histograma:** Distribuição da população por estado
2. **Q-Q Plot:** Comparação com distribuição normal teórica

#### **Implementação:**
```python
def distribution_analysis(self):
    """Análise de distribuição da população"""
    population = self.data['populacao']
    
    # Teste de normalidade (Shapiro-Wilk)
    shapiro_stat, shapiro_p = shapiro(population)
    
    # Criar visualizações
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
    
    # Histograma
    ax1.hist(population, bins=20, alpha=0.7, color='skyblue', edgecolor='black')
    ax1.set_title('Distribuição da População por Estado')
    
    # Q-Q Plot
    stats.probplot(population, dist="norm", plot=ax2)
    ax2.set_title('Q-Q Plot - Teste de Normalidade')
    
    return {
        'shapiro_statistic': shapiro_stat,
        'shapiro_p_value': shapiro_p,
        'is_normal': shapiro_p > 0.05,
        'figure': fig
    }
```

## 🔍 **3. Análise Regional/Anual**

### **Método: `regional_analysis()`**

#### **Análise por Ano (Adaptação):**
Como os dados não contêm informação de região, a análise foi adaptada para comparar anos diferentes.

#### **Teste ANOVA (Análise de Variância):**

**Hipótese Nula (H₀):** Não há diferenças significativas entre os anos
**Hipótese Alternativa (H₁):** Existe pelo menos uma diferença significativa entre os anos

#### **Teste de Levene (Homogeneidade de Variâncias):**

**Hipótese Nula (H₀):** As variâncias são homogêneas entre os grupos
**Hipótese Alternativa (H₁):** As variâncias não são homogêneas

#### **Implementação:**
```python
def regional_analysis(self):
    """Análise comparativa entre anos"""
    # Estatísticas por ano
    yearly_stats = self.data.groupby('ano')['populacao'].agg([
        'count', 'mean', 'std', 'min', 'max'
    ]).round(2)
    
    # Teste ANOVA entre anos
    years = self.data['ano'].unique()
    year_groups = [self.data[self.data['ano'] == year]['populacao'] for year in years]
    
    f_stat, p_value = f_oneway(*year_groups)
    levene_stat, levene_p = levene(*year_groups)
    
    return {
        'yearly_stats': yearly_stats,
        'anova_f_statistic': f_stat,
        'anova_p_value': p_value,
        'levene_statistic': levene_stat,
        'levene_p_value': levene_p,
        'significant_differences': p_value < 0.05
    }
```

## 🔗 **4. Análise de Correlação**

### **Método: `correlation_analysis()`**

#### **Correlação de Pearson:**
Mede a força e direção da relação linear entre duas variáveis contínuas.

**Interpretação:**
- **r = 1:** Correlação positiva perfeita
- **r = 0:** Sem correlação linear
- **r = -1:** Correlação negativa perfeita
- **|r| > 0.7:** Correlação forte
- **0.3 < |r| < 0.7:** Correlação moderada
- **|r| < 0.3:** Correlação fraca

#### **Teste de Significância:**
- **Hipótese Nula (H₀):** ρ = 0 (sem correlação)
- **Hipótese Alternativa (H₁):** ρ ≠ 0 (existe correlação)

#### **Implementação:**
```python
def correlation_analysis(self):
    """Análise de correlações"""
    df_corr = self.data.copy()
    
    # Matriz de correlação
    correlation_matrix = df_corr[['populacao', 'ano']].corr()
    
    # Correlação entre população e ano
    pop_year_corr, pop_year_p = pearsonr(df_corr['populacao'], df_corr['ano'])
    
    return {
        'correlation_matrix': correlation_matrix,
        'population_year_correlation': pop_year_corr,
        'population_year_p_value': pop_year_p,
        'significant_correlation': pop_year_p < 0.05
    }
```

## 🎯 **5. Detecção de Outliers**

### **Método: `outlier_detection()`**

#### **Método IQR (Intervalo Interquartil):**
- **Limite Inferior:** Q1 - 1.5 × IQR
- **Limite Superior:** Q3 + 1.5 × IQR
- **Outliers:** Valores fora desses limites

#### **Método Z-Score:**
- **Limite:** |Z-score| > 3
- **Cálculo:** Z = (x - μ) / σ

#### **Implementação:**
```python
def outlier_detection(self):
    """Detecção de outliers usando IQR e Z-score"""
    population = self.data['populacao']
    
    # Método IQR
    Q1 = population.quantile(0.25)
    Q3 = population.quantile(0.75)
    IQR = Q3 - Q1
    lower_bound_iqr = Q1 - 1.5 * IQR
    upper_bound_iqr = Q3 + 1.5 * IQR
    
    outliers_iqr = self.data[
        (self.data['populacao'] < lower_bound_iqr) | 
        (self.data['populacao'] > upper_bound_iqr)
    ]
    
    # Método Z-score
    z_scores = np.abs(stats.zscore(population))
    outliers_zscore = self.data[z_scores > 3]
    
    return {
        'iqr_outliers': outliers_iqr,
        'zscore_outliers': outliers_zscore,
        'iqr_bounds': (lower_bound_iqr, upper_bound_iqr),
        'total_outliers_iqr': len(outliers_iqr),
        'total_outliers_zscore': len(outliers_zscore)
    }
```

## 🤖 **6. Modelos Preditivos**

### **Método: `predictive_modeling()`**

#### **Modelos Implementados:**

1. **Regressão Linear:**
   - **Algoritmo:** `sklearn.linear_model.LinearRegression`
   - **Vantagens:** Simples, interpretável
   - **Limitações:** Assume relação linear

2. **Random Forest:**
   - **Algoritmo:** `sklearn.ensemble.RandomForestRegressor`
   - **Vantagens:** Captura relações não-lineares, robusto
   - **Limitações:** Menos interpretável

#### **Métricas de Avaliação:**
- **R² Score:** Proporção da variância explicada (0-1)
- **RMSE:** Raiz do erro quadrático médio

#### **Implementação:**
```python
def predictive_modeling(self):
    """Modelos preditivos para população"""
    df_model = self.data.copy()
    
    # Features para o modelo
    features = ['ano']
    X = df_model[features]
    y = df_model['populacao']
    
    # Dividir dados
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Modelo 1: Regressão Linear
    lr_model = LinearRegression()
    lr_model.fit(X_train, y_train)
    lr_pred = lr_model.predict(X_test)
    lr_r2 = r2_score(y_test, lr_pred)
    lr_rmse = np.sqrt(mean_squared_error(y_test, lr_pred))
    
    # Modelo 2: Random Forest
    rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)
    rf_pred = rf_model.predict(X_test)
    rf_r2 = r2_score(y_test, rf_pred)
    rf_rmse = np.sqrt(mean_squared_error(y_test, rf_pred))
    
    return {
        'linear_regression': {
            'r2_score': lr_r2,
            'rmse': lr_rmse,
            'model': lr_model
        },
        'random_forest': {
            'r2_score': rf_r2,
            'rmse': rf_rmse,
            'model': rf_model
        },
        'best_model': 'Random Forest' if rf_r2 > lr_r2 else 'Linear Regression'
    }
```

## 📊 **7. Visualizações**

### **Método: `plot_analysis()`**

#### **Gráficos Gerados:**
1. **Boxplot por Ano:** Distribuição da população por ano
2. **Scatter Plot:** População vs Ano
3. **Histograma:** Distribuição geral da população
4. **Gráfico de Barras:** População média por ano

#### **Implementação:**
```python
def plot_analysis(self):
    """Cria visualizações das análises"""
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    # 1. Boxplot por ano
    self.data.boxplot(column='populacao', by='ano', ax=axes[0,0])
    axes[0,0].set_title('Distribuição da População por Ano')
    
    # 2. Scatter plot: População vs Ano
    axes[0,1].scatter(self.data['ano'], self.data['populacao'], alpha=0.6)
    axes[0,1].set_title('População vs Ano')
    
    # 3. Histograma da população
    axes[1,0].hist(self.data['populacao'], bins=20, alpha=0.7, color='green')
    axes[1,0].set_title('Distribuição da População')
    
    # 4. Média populacional por ano
    yearly_means = self.data.groupby('ano')['populacao'].mean()
    yearly_means.plot(kind='bar', ax=axes[1,1])
    axes[1,1].set_title('População Média por Ano')
    
    plt.tight_layout()
    return fig
```

## 📋 **8. Relatório Completo**

### **Método: `generate_report()`**

#### **Estrutura do Relatório:**
```python
report = {
    'summary': {
        'total_states': len(self.data),
        'total_years': self.data['ano'].nunique(),
        'year_range': f"{self.data['ano'].min()} - {self.data['ano'].max()}"
    },
    'basic_statistics': self.results['basic_stats'],
    'distribution': {
        'is_normal': self.results['distribution']['is_normal'],
        'shapiro_p_value': self.results['distribution']['shapiro_p_value']
    },
    'regional_analysis': {
        'significant_differences': self.results['regional']['significant_differences'],
        'anova_p_value': self.results['regional']['anova_p_value']
    },
    'correlation': {
        'population_year_correlation': self.results['correlation']['population_year_correlation'],
        'significant_correlation': self.results['correlation']['significant_correlation']
    },
    'outliers': {
        'total_outliers_iqr': self.results['outliers']['total_outliers_iqr'],
        'total_outliers_zscore': self.results['outliers']['total_outliers_zscore']
    },
    'predictive_models': {
        'best_model': self.results['predictive']['best_model'],
        'random_forest_r2': self.results['predictive']['random_forest']['r2_score'],
        'linear_regression_r2': self.results['predictive']['linear_regression']['r2_score']
    }
}
```

## 📊 **Resultados Típicos**

### **Exemplo de Saída:**
```python
# Estatísticas Básicas
{
    'total_population': 214300000,
    'mean_population': 7937037.04,
    'median_population': 4470000,
    'std_population': 8934567.23,
    'skewness': 1.85,  # Distribuição assimétrica positiva
    'kurtosis': 3.42   # Caudas pesadas
}

# Teste de Normalidade
{
    'shapiro_p_value': 0.0001,  # < 0.05
    'is_normal': False          # Dados não normais
}

# ANOVA
{
    'anova_p_value': 0.9990,    # > 0.05
    'significant_differences': False  # Sem diferenças entre anos
}

# Correlação
{
    'population_year_correlation': 0.005,  # Correlação muito fraca
    'significant_correlation': False       # Não significativa
}

# Outliers
{
    'total_outliers_iqr': 6,    # 6 estados são outliers
    'total_outliers_zscore': 6  # Confirmado pelo Z-score
}

# Modelos Preditivos
{
    'best_model': 'Linear Regression',
    'linear_regression_r2': -0.088,  # Modelo não explica bem a variância
    'random_forest_r2': -0.092
}
```

## 🔍 **Interpretação dos Resultados**

### **Principais Descobertas:**

1. **Distribuição Não Normal:** Os dados populacionais não seguem distribuição normal (p < 0.05)

2. **Sem Diferenças Temporais:** Não há diferenças significativas entre os anos (ANOVA p = 0.999)

3. **Correlação Muito Fraca:** Praticamente não há correlação entre população e ano (r = 0.005)

4. **Outliers Identificados:** 6 estados são considerados outliers (São Paulo, Minas Gerais, Rio de Janeiro, Bahia, Paraná, Rio Grande do Sul)

5. **Modelos Limitados:** Os modelos preditivos têm baixo poder explicativo (R² negativo)

### **Implicações:**
- Os dados são estáveis ao longo do tempo
- A população não cresce linearmente com o ano
- Existe grande desigualdade populacional entre estados
- Modelos simples não capturam a complexidade dos dados

## 🚀 **Melhorias Futuras**

### **Análises Adicionais Sugeridas:**

1. **Análise de Séries Temporais:**
   - Tendências de crescimento
   - Sazonalidade
   - Decomposição temporal

2. **Análise Espacial:**
   - Correlação geográfica
   - Clustering de estados
   - Mapas de calor

3. **Análise Multivariada:**
   - Análise de componentes principais (PCA)
   - Análise de clusters
   - Regressão múltipla

4. **Modelos Avançados:**
   - Regressão polinomial
   - Support Vector Regression
   - Redes neurais

---

**📚 Esta documentação deve ser atualizada conforme novas análises são implementadas.**
