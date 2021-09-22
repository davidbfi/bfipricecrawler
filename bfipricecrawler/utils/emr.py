from datetime import datetime
from pyhive import hive
from config import hive_config

host_name = hive_config['host_name']
port = hive_config['port']
user = hive_config['user']
password = hive_config['password']
database = hive_config['database']

hive_connector = hive.Connection(host=host_name, port=port, username=user, password=password, database=database, auth='CUSTOM')


def create_external_table(connector, database_name, table_name, columns, bucket_name, external_path, dt):

    cursor = connector.cursor()
    columns = columns.replace('[', '').replace(']', '').replace('\'', '')
    query_create = "CREATE EXTERNAL TABLE IF NOT EXISTS {}.{} ({}) PARTITIONED BY (dt string) STORED AS JSON LOCATION 'oss://{}/{}'".format(bucket_name, database_name, table_name, columns, external_path)
    query_alter = "ALTER TABLE {}.{}  ADD  IF NOT EXISTS PARTITION (dt = {}) location 'oss://{}/{}/{}/dt={}'".format(database_name, table_name.lower(), table_name.lower(), table_name.lower(), str(dt), bucket_name,dt)

    try:
        cursor.execute(query_create)
        cursor.execute(query_alter)
    except Exception as e:
        print("Error", str(e))
    cursor.close()
    return "table {} created".format(table_name)





