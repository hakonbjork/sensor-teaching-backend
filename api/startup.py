from .empatica import EmpaticaConnection

def init_backend():
    """ Connects to empatica and starts the master backend"""

    print("starting master backend...")
    connection = EmpaticaConnection()

    connection.connect()