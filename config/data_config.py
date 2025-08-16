# Configurações para coleta de dados

# URLs das APIs
IBGE_POPULATION_URL = "https://servicodados.ibge.gov.br/api/v1/projecoes/populacao"
IBGE_STATES_URL = "https://servicodados.ibge.gov.br/api/v1/localidades/estados"

# Configurações de arquivos
RAW_DATA_PATH = "data/raw"
PROCESSED_DATA_PATH = "data/processed"
EXTERNAL_DATA_PATH = "data/external"

# Configurações de requisições
REQUEST_TIMEOUT = 30  # segundos
MAX_RETRIES = 3

# Configurações de dados
ENCODING = "utf-8"
DATE_FORMAT = "%Y%m%d_%H%M%S"