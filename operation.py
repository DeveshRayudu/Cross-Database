def table_creation(table_name, column_defs, des_cur, db_type):

    if not column_defs:
        raise ValueError("Table is empty.")
    

    names = []
    types = []

    for col_name, col_type in column_defs:
        names.append(col_name)
        types.append(map_data_type(col_type, db_type))
    
    columns = ', '.join(f"{name} {typ}" for name, typ in zip(names, types))    

    if db_type == 'mysql':
        create_table_query = f"CREATE TABLE {table_name} ({columns})"
    
    elif db_type == 'postgresql':
        create_table_query = f"CREATE TABLE {table_name} ({columns})"
    
    elif db_type == 'oracle':
        create_table_query = f"CREATE TABLE {table_name} ({columns})"

    else:
        raise ValueError(f"Unsupported database type: {db_type}")
    
    des_cur.execute(create_table_query)
    

def transfer_data(src_cur, des_cur, conn, source_table, destination_table, dest_type):
    try:
        
        src_cur.execute(f"SELECT * FROM {source_table}")
        rows = src_cur.fetchall()

        for row in rows:
            if dest_type == 'oracle':
                placeholders = ', '.join([f":{i+1}" for i in range(len(row))])
            else:
                placeholders = ', '.join(['%s'] * len(row))
            
            insert_query = f"INSERT INTO {destination_table} VALUES ({placeholders})"
            
            des_cur.execute(insert_query, row)
        
        conn.commit()
        print(f"Data transferred from {source_table} to {destination_table} successfully.")

    except Exception as err:
        print(f"Error: {err}")
        conn.rollback()  
    

def map_data_type(data_type, db_type):
    data_type = data_type.lower()

    mysql_types = {
        'int': 'INT',
        'varchar': 'VARCHAR(255)',
        'text': 'TEXT',
        'decimal': 'DECIMAL(10,2)',
        'float': 'FLOAT',
        'date': 'DATE',
        'timestamp': 'DATETIME',
        'boolean': 'BOOLEAN'
    }

    postgresql_types = {
        'int': 'INTEGER',
        'varchar': 'VARCHAR(255)',
        'text': 'TEXT',
        'decimal': 'NUMERIC(10,2)',
        'float': 'REAL',
        'date': 'DATE',
        'timestamp': 'TIMESTAMP',
        'boolean': 'BOOLEAN'
    }

    oracle_types = {
        'int': 'NUMBER',
        'varchar': 'VARCHAR2(255)',
        'text': 'CLOB',
        'decimal': 'NUMBER(10,2)',
        'float': 'BINARY_FLOAT',
        'date': 'DATE',
        'timestamp': 'TIMESTAMP',
        'boolean': 'CHAR(1)'
    }

    type_maps = {
        'mysql': mysql_types,
        'postgresql': postgresql_types,
        'oracle': oracle_types
    }

    for key in type_maps[db_type]:
        if key in data_type:
            return type_maps[db_type][key]

    return type_maps[db_type]['varchar'] 
