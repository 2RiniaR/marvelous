from client import MarvelousClient
from data_context import DataContext
from json_repository import JsonRepository
from console_logger import ConsoleLogger
import os
from os.path import join, dirname
from dotenv import load_dotenv

load_dotenv(verbose=True)
dotenv_path = join(dirname(__file__), '../.env')
data_filepath = join(dirname(__file__), '../data/data.json')
load_dotenv(dotenv_path)
TOKEN = os.environ.get("DISCORD_TOKEN")


if __name__ == '__main__':
    print('''
    ===============================
    ||    Marvelous started!!    ||
    ===============================
    ''')

    logger = ConsoleLogger()
    repository = JsonRepository(data_filepath)
    context = DataContext(repository, logger)
    client = MarvelousClient(logger, context)
    client.run(TOKEN)
