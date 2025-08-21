# 👨‍💻 Guia de Desenvolvimento

## 🎯 **Visão Geral**

Este guia é destinado a desenvolvedores que desejam contribuir, modificar ou estender o projeto de dashboard de análise de dados.

## 🏗️ **Arquitetura do Projeto**

### **Estrutura de Módulos:**

```
src/
├── data/                    # Camada de dados
│   ├── collect_ibge_data.py    # Coleta de dados
│   ├── data_cleaning.py        # Limpeza de dados
│   └── api_client.py           # Cliente de APIs
├── analytics/              # Camada de análise
│   └── statistical_analysis.py # Análises estatísticas
└── dashboard/              # Camada de apresentação
    └── app.py              # Dashboard Streamlit
```

### **Padrões de Design:**

1. **Separação de Responsabilidades:** Cada módulo tem uma responsabilidade específica
2. **Injeção de Dependências:** Módulos são independentes e testáveis
3. **Configuração Externa:** Configurações centralizadas
4. **Tratamento de Erros:** Fallbacks e retry logic

## 🚀 **Configuração do Ambiente de Desenvolvimento**

### **1. Pré-requisitos:**

```bash
# Python 3.8+
python --version

# Git
git --version

# Editor recomendado: VS Code com extensões Python
```

### **2. Configuração Inicial:**

```bash
# Clone o repositório
git clone <url-do-repositorio>
cd dados-populacao-brasileira

# Crie ambiente virtual
python -m venv .venv

# Ative o ambiente
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Instale dependências
pip install -r requirements.txt

# Instale dependências de desenvolvimento
pip install pytest black flake8 mypy
```

### **3. Configuração do Editor:**

**VS Code Settings (`.vscode/settings.json`):**
```json
{
    "python.defaultInterpreterPath": "./.venv/Scripts/python.exe",
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.formatting.provider": "black",
    "python.testing.pytestEnabled": true,
    "python.testing.unittestEnabled": false,
    "python.testing.pytestArgs": ["tests"]
}
```

## 📝 **Padrões de Código**

### **1. Style Guide (PEP 8):**

```python
# ✅ Bom
def calculate_population_stats(data: pd.DataFrame) -> dict:
    """Calcula estatísticas populacionais.
    
    Args:
        data: DataFrame com dados populacionais
        
    Returns:
        Dicionário com estatísticas calculadas
    """
    total = data['populacao'].sum()
    mean = data['populacao'].mean()
    return {'total': total, 'mean': mean}

# ❌ Ruim
def calc_pop_stats(data):
    total=data['populacao'].sum()
    mean=data['populacao'].mean()
    return {'total':total,'mean':mean}
```

### **2. Type Hints:**

```python
from typing import Dict, List, Optional, Union
import pandas as pd

def process_data(
    raw_data: List[Dict[str, Union[str, int]]],
    config: Optional[Dict[str, str]] = None
) -> pd.DataFrame:
    """Processa dados brutos em DataFrame."""
    pass
```

### **3. Docstrings:**

```python
def analyze_population_trends(
    data: pd.DataFrame,
    years: List[int]
) -> Dict[str, float]:
    """
    Analisa tendências populacionais ao longo dos anos.
    
    Args:
        data: DataFrame com dados populacionais
        years: Lista de anos para análise
        
    Returns:
        Dicionário com métricas de tendência
        
    Raises:
        ValueError: Se years estiver vazio
        KeyError: Se coluna 'populacao' não existir
        
    Example:
        >>> df = pd.DataFrame({'populacao': [100, 110, 120]})
        >>> result = analyze_population_trends(df, [2020, 2021, 2022])
        >>> print(result['growth_rate'])
        0.10
    """
    if not years:
        raise ValueError("Lista de anos não pode estar vazia")
    
    if 'populacao' not in data.columns:
        raise KeyError("Coluna 'populacao' não encontrada")
    
    # Implementação...
    return {'growth_rate': 0.10}
```

### **4. Tratamento de Erros:**

```python
import logging
from typing import Optional

logger = logging.getLogger(__name__)

def safe_api_call(url: str, timeout: int = 30) -> Optional[dict]:
    """
    Faz chamada segura para API com retry e logging.
    
    Args:
        url: URL da API
        timeout: Timeout em segundos
        
    Returns:
        Dados da API ou None se falhar
    """
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        logger.warning(f"Timeout na chamada para {url}")
        return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Erro na chamada para {url}: {e}")
        return None
    except Exception as e:
        logger.error(f"Erro inesperado: {e}")
        return None
```

## 🧪 **Testes**

### **1. Estrutura de Testes:**

```
tests/
├── __init__.py
├── test_data_collection.py
├── test_data_cleaning.py
├── test_api_client.py
├── test_statistical_analysis.py
└── test_dashboard.py
```

### **2. Exemplo de Teste:**

```python
# tests/test_statistical_analysis.py
import pytest
import pandas as pd
import numpy as np
from src.analytics.statistical_analysis import PopulationAnalyzer

class TestPopulationAnalyzer:
    """Testes para a classe PopulationAnalyzer."""
    
    @pytest.fixture
    def sample_data(self):
        """Dados de exemplo para testes."""
        return pd.DataFrame({
            'populacao': [1000000, 2000000, 3000000, 4000000, 5000000],
            'ano': [2020, 2021, 2022, 2023, 2024],
            'nome': ['Estado A', 'Estado B', 'Estado C', 'Estado D', 'Estado E']
        })
    
    def test_basic_statistics(self, sample_data):
        """Testa cálculo de estatísticas básicas."""
        analyzer = PopulationAnalyzer(sample_data)
        stats = analyzer.basic_statistics()
        
        assert 'total_population' in stats
        assert 'mean_population' in stats
        assert stats['total_population'] == 15000000
        assert stats['mean_population'] == 3000000
    
    def test_outlier_detection(self, sample_data):
        """Testa detecção de outliers."""
        analyzer = PopulationAnalyzer(sample_data)
        outliers = analyzer.outlier_detection()
        
        assert 'total_outliers_iqr' in outliers
        assert 'total_outliers_zscore' in outliers
        assert isinstance(outliers['total_outliers_iqr'], int)
    
    def test_empty_data(self):
        """Testa comportamento com dados vazios."""
        empty_df = pd.DataFrame()
        
        with pytest.raises(KeyError):
            analyzer = PopulationAnalyzer(empty_df)
            analyzer.basic_statistics()
```

### **3. Executando Testes:**

```bash
# Executar todos os testes
pytest

# Executar com cobertura
pytest --cov=src --cov-report=html

# Executar testes específicos
pytest tests/test_statistical_analysis.py::TestPopulationAnalyzer::test_basic_statistics

# Executar com verbose
pytest -v
```

## 🔧 **Ferramentas de Desenvolvimento**

### **1. Formatação de Código:**

```bash
# Black (formatação automática)
black src/ tests/

# Flake8 (linting)
flake8 src/ tests/

# MyPy (verificação de tipos)
mypy src/
```

### **2. Pre-commit Hooks:**

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 22.3.0
    hooks:
      - id: black
        language_version: python3
  - repo: https://github.com/pycqa/flake8
    rev: 4.0.1
    hooks:
      - id: flake8
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.2.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
```

### **3. Configuração do Black:**

```toml
# pyproject.toml
[tool.black]
line-length = 88
target-version = ['py38']
include = '\.pyi?$'
extend-exclude = '''
/(
  # directories
  \.eggs
  | \.git
  | \.hg
  | \.mypy_cache
  | \.tox
  | \.venv
  | build
  | dist
)/
'''
```

## 📦 **Adicionando Novas Funcionalidades**

### **1. Estrutura para Novos Módulos:**

```python
# src/new_feature/__init__.py
"""
Módulo para nova funcionalidade.

Este módulo implementa...
"""

from .core import NewFeature

__version__ = "1.0.0"
__all__ = ["NewFeature"]
```

```python
# src/new_feature/core.py
"""
Implementação principal da nova funcionalidade.
"""

import logging
from typing import Dict, Any
import pandas as pd

logger = logging.getLogger(__name__)

class NewFeature:
    """Implementa nova funcionalidade."""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Inicializa a nova funcionalidade.
        
        Args:
            config: Configurações da funcionalidade
        """
        self.config = config
        self._validate_config()
    
    def _validate_config(self):
        """Valida configurações."""
        required_keys = ['key1', 'key2']
        for key in required_keys:
            if key not in self.config:
                raise ValueError(f"Configuração obrigatória '{key}' não encontrada")
    
    def process(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Processa dados com a nova funcionalidade.
        
        Args:
            data: Dados de entrada
            
        Returns:
            Dados processados
        """
        logger.info("Iniciando processamento com nova funcionalidade")
        
        try:
            # Implementação da funcionalidade
            result = data.copy()
            # ... processamento ...
            
            logger.info("Processamento concluído com sucesso")
            return result
            
        except Exception as e:
            logger.error(f"Erro no processamento: {e}")
            raise
```

### **2. Integração com Dashboard:**

```python
# src/dashboard/app.py (adição)
try:
    from src.new_feature import NewFeature
    NEW_FEATURE_AVAILABLE = True
except ImportError as e:
    NEW_FEATURE_AVAILABLE = False
    st.warning(f"⚠️ Nova funcionalidade não disponível: {e}")

# Na interface
if NEW_FEATURE_AVAILABLE:
    st.header("🆕 Nova Funcionalidade")
    if st.button("🚀 Executar Nova Funcionalidade"):
        with st.spinner("Executando nova funcionalidade..."):
            try:
                feature = NewFeature(config={'key1': 'value1'})
                result = feature.process(df)
                st.success("✅ Nova funcionalidade executada com sucesso!")
                st.dataframe(result)
            except Exception as e:
                st.error(f"❌ Erro: {e}")
```

### **3. Testes para Nova Funcionalidade:**

```python
# tests/test_new_feature.py
import pytest
import pandas as pd
from src.new_feature import NewFeature

class TestNewFeature:
    """Testes para nova funcionalidade."""
    
    def test_initialization(self):
        """Testa inicialização da nova funcionalidade."""
        config = {'key1': 'value1', 'key2': 'value2'}
        feature = NewFeature(config)
        assert feature.config == config
    
    def test_invalid_config(self):
        """Testa inicialização com configuração inválida."""
        config = {'key1': 'value1'}  # Falta key2
        with pytest.raises(ValueError, match="key2"):
            NewFeature(config)
    
    def test_process_data(self):
        """Testa processamento de dados."""
        config = {'key1': 'value1', 'key2': 'value2'}
        feature = NewFeature(config)
        
        data = pd.DataFrame({'col1': [1, 2, 3], 'col2': [4, 5, 6]})
        result = feature.process(data)
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == len(data)
```

## 🔄 **Fluxo de Desenvolvimento**

### **1. Git Workflow:**

```bash
# 1. Criar branch para nova funcionalidade
git checkout -b feature/nova-funcionalidade

# 2. Fazer alterações
# ... editar arquivos ...

# 3. Adicionar e commitar
git add .
git commit -m "feat: adiciona nova funcionalidade de análise"

# 4. Executar testes
pytest

# 5. Verificar qualidade do código
black src/ tests/
flake8 src/ tests/
mypy src/

# 6. Push e criar Pull Request
git push origin feature/nova-funcionalidade
```

### **2. Convenções de Commit:**

```
feat: nova funcionalidade
fix: correção de bug
docs: atualização de documentação
style: formatação de código
refactor: refatoração de código
test: adição de testes
chore: tarefas de manutenção
```

### **3. Pull Request Template:**

```markdown
## 📝 Descrição
Breve descrição das mudanças implementadas.

## 🎯 Tipo de Mudança
- [ ] Bug fix
- [ ] Nova funcionalidade
- [ ] Breaking change
- [ ] Documentação

## 🧪 Testes
- [ ] Testes unitários passando
- [ ] Testes de integração passando
- [ ] Cobertura de testes adequada

## 📋 Checklist
- [ ] Código segue padrões do projeto
- [ ] Documentação atualizada
- [ ] Testes adicionados/atualizados
- [ ] Build passando localmente

## 🔍 Como Testar
Instruções para testar as mudanças.

## 📸 Screenshots (se aplicável)
Screenshots das mudanças na interface.
```

## 🚀 **Deploy e Distribuição**

### **1. Build do Projeto:**

```bash
# Instalar build tools
pip install build twine

# Criar distribuição
python -m build

# Verificar distribuição
twine check dist/*
```

### **2. Deploy Local:**

```bash
# Executar dashboard localmente
streamlit run src/dashboard/app.py

# Executar com configurações específicas
streamlit run src/dashboard/app.py --server.port 8502 --server.address 0.0.0.0
```

### **3. Deploy em Produção:**

```bash
# Docker (exemplo)
docker build -t dashboard-analise .
docker run -p 8501:8501 dashboard-analise

# Heroku
heroku create dashboard-analise
git push heroku main
```

## 📚 **Recursos Adicionais**

### **1. Documentação:**

- [PEP 8 - Style Guide](https://www.python.org/dev/peps/pep-0008/)
- [Type Hints](https://docs.python.org/3/library/typing.html)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)

### **2. Ferramentas:**

- [Black](https://black.readthedocs.io/) - Formatação de código
- [Flake8](https://flake8.pycqa.org/) - Linting
- [MyPy](https://mypy.readthedocs.io/) - Verificação de tipos
- [Pytest](https://docs.pytest.org/) - Framework de testes

### **3. Boas Práticas:**

- [Clean Code](https://www.amazon.com/Clean-Code-Handbook-Software-Craftsmanship/dp/0132350884)
- [Effective Python](https://effectivepython.com/)
- [Python Testing with pytest](https://pytest.org/)

---

**🎉 Agora você está pronto para contribuir com o projeto!**
