
from genai_application.utils.postgresql_service import PostgreSQLService

if __name__ == "__main__":
    postgres_client = PostgreSQLService()
    postgres_client.connect()