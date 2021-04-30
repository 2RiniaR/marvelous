import os

discord_token: str = os.environ.get("DISCORD_TOKEN")
run_environment: str = os.environ.get("RUN_ENVIRONMENT")

mysql_host: str = os.environ.get("MYSQL_HOST")
mysql_port: str = os.environ.get("MYSQL_PORT")
mysql_user: str = os.environ.get("MYSQL_USER")
mysql_password: str = os.environ.get("MYSQL_PASSWORD")
mysql_database: str = os.environ.get("MYSQL_DATABASE")
mysql_pool_size: int = int(os.environ.get("MYSQL_POOL_SIZE"))
