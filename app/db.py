import psycopg2

def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="vehicle_inventory",
        user="postgres",
        password="root"
    )
