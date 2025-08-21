#!/usr/bin/env python3
"""
Módulo de Análises Estatísticas Avançadas - Fase 6
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.stats import shapiro, levene, f_oneway, ttest_ind, pearsonr
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import warnings
warnings.filterwarnings('ignore')

class PopulationAnalyzer:
    """Analisador estatístico avançado para dados populacionais"""
    
    def __init__(self, data):
        """
        Inicializa o analisador com dados populacionais
        
        Args:
            data (pd.DataFrame): DataFrame com dados populacionais
        """
        self.data = data
        self.results = {}
        
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
        
        self.results['basic_stats'] = stats_dict
        return stats_dict
    
    def distribution_analysis(self):
        """Análise de distribuição da população"""
        population = self.data['populacao']
        
        # Teste de normalidade (Shapiro-Wilk)
        shapiro_stat, shapiro_p = shapiro(population)
        
        # Histograma e densidade
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
        
        # Histograma
        ax1.hist(population, bins=20, alpha=0.7, color='skyblue', edgecolor='black')
        ax1.set_title('Distribuição da População por Estado')
        ax1.set_xlabel('População')
        ax1.set_ylabel('Frequência')
        
        # Q-Q Plot
        stats.probplot(population, dist="norm", plot=ax2)
        ax2.set_title('Q-Q Plot - Teste de Normalidade')
        
        plt.tight_layout()
        
        distribution_results = {
            'shapiro_statistic': shapiro_stat,
            'shapiro_p_value': shapiro_p,
            'is_normal': shapiro_p > 0.05,
            'figure': fig
        }
        
        self.results['distribution'] = distribution_results
        return distribution_results
    
    def regional_analysis(self):
        """Análise comparativa entre anos (já que não temos região)"""
        # Criar análise por ano em vez de região
        yearly_stats = self.data.groupby('ano')['populacao'].agg([
            'count', 'mean', 'std', 'min', 'max'
        ]).round(2)
        
        # Teste ANOVA entre anos
        years = self.data['ano'].unique()
        year_groups = [self.data[self.data['ano'] == year]['populacao'] for year in years]
        
        f_stat, p_value = f_oneway(*year_groups)
        
        # Teste de homogeneidade de variâncias (Levene)
        levene_stat, levene_p = levene(*year_groups)
        
        regional_results = {
            'yearly_stats': yearly_stats,
            'anova_f_statistic': f_stat,
            'anova_p_value': p_value,
            'levene_statistic': levene_stat,
            'levene_p_value': levene_p,
            'significant_differences': p_value < 0.05
        }
        
        self.results['regional'] = regional_results
        return regional_results
    
    def correlation_analysis(self):
        """Análise de correlações"""
        # Criar variáveis numéricas para correlação
        df_corr = self.data.copy()
        
        # Calcular correlações apenas com as colunas disponíveis
        correlation_matrix = df_corr[['populacao', 'ano']].corr()
        
        # Correlação entre população e ano
        pop_year_corr, pop_year_p = pearsonr(df_corr['populacao'], df_corr['ano'])
        
        correlation_results = {
            'correlation_matrix': correlation_matrix,
            'population_year_correlation': pop_year_corr,
            'population_year_p_value': pop_year_p,
            'significant_correlation': pop_year_p < 0.05
        }
        
        self.results['correlation'] = correlation_results
        return correlation_results
    
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
        
        outlier_results = {
            'iqr_outliers': outliers_iqr,
            'zscore_outliers': outliers_zscore,
            'iqr_bounds': (lower_bound_iqr, upper_bound_iqr),
            'total_outliers_iqr': len(outliers_iqr),
            'total_outliers_zscore': len(outliers_zscore)
        }
        
        self.results['outliers'] = outlier_results
        return outlier_results
    
    def predictive_modeling(self):
        """Modelos preditivos para população"""
        # Preparar dados
        df_model = self.data.copy()
        
        # Features para o modelo (apenas ano por enquanto)
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
        
        # Feature importance
        feature_importance = pd.DataFrame({
            'feature': features,
            'importance': rf_model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        model_results = {
            'linear_regression': {
                'r2_score': lr_r2,
                'rmse': lr_rmse,
                'model': lr_model
            },
            'random_forest': {
                'r2_score': rf_r2,
                'rmse': rf_rmse,
                'model': rf_model,
                'feature_importance': feature_importance
            },
            'best_model': 'Random Forest' if rf_r2 > lr_r2 else 'Linear Regression'
        }
        
        self.results['predictive'] = model_results
        return model_results
    
    def generate_report(self):
        """Gera relatório completo das análises"""
        # Executar todas as análises
        self.basic_statistics()
        self.distribution_analysis()
        self.regional_analysis()
        self.correlation_analysis()
        self.outlier_detection()
        self.predictive_modeling()
        
        # Criar relatório
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
        
        return report
    
    def plot_analysis(self):
        """Cria visualizações das análises"""
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # 1. Boxplot por ano
        self.data.boxplot(column='populacao', by='ano', ax=axes[0,0])
        axes[0,0].set_title('Distribuição da População por Ano')
        axes[0,0].set_xlabel('Ano')
        axes[0,0].set_ylabel('População')
        
        # 2. Scatter plot: População vs Ano
        axes[0,1].scatter(self.data['ano'], self.data['populacao'], alpha=0.6)
        axes[0,1].set_title('População vs Ano')
        axes[0,1].set_xlabel('Ano')
        axes[0,1].set_ylabel('População')
        
        # 3. Histograma da população
        axes[1,0].hist(self.data['populacao'], bins=20, alpha=0.7, color='green')
        axes[1,0].set_title('Distribuição da População')
        axes[1,0].set_xlabel('População')
        axes[1,0].set_ylabel('Frequência')
        
        # 4. Média populacional por ano
        yearly_means = self.data.groupby('ano')['populacao'].mean()
        yearly_means.plot(kind='bar', ax=axes[1,1])
        axes[1,1].set_title('População Média por Ano')
        axes[1,1].set_xlabel('Ano')
        axes[1,1].set_ylabel('População Média')
        axes[1,1].tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        return fig

def run_complete_analysis(data):
    """Função principal para executar análise completa"""
    analyzer = PopulationAnalyzer(data)
    report = analyzer.generate_report()
    return analyzer, report
