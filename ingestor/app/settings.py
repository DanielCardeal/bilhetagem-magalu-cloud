from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configurações da aplicação carregadas a partir de variáveis de ambiente.

    Attributes:
        PROJECT_NAME (str): Nome do projeto. Default: "Ingestor".
        VERSION (str): Versão da aplicação. Default: "1.0.0".
        SERVER_HOST (str): Host onde o servidor será executado. Default: "127.0.0.1".
        SERVER_PORT (int): Porta onde o servidor escutará. Default: 80.
        DATABASE_URL (str): URL de conexão com o banco de dados. Default: "sqlite:///ingestor.db".
        DEBUG (bool): Habilita modo de depuração. Default: False.
    """

    PROJECT_NAME: str = "Ingestor"
    VERSION: str = "1.0.0"

    SERVER_HOST: str = "127.0.0.1"
    SERVER_PORT: int = 80

    SQLITE_URL: str = "sqlite:///ingestor.db"

    DEBUG: bool = False
