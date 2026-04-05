def get_tables(cursor, db_type):
    if db_type == 'mysql':
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        return [table[0] for table in tables]
    
    elif db_type == 'postgresql':
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public';
        """)
        tables = cursor.fetchall()
        return [table[0] for table in tables]
    
    elif db_type == 'oracle':
        cursor.execute("SELECT table_name FROM user_tables")
        tables = [table[0] for table in cursor.fetchall()]

        filtered_tables = [
            t for t in tables 
            if not ('$' in t or t.startswith('LOGMNR') or t.startswith('MVIEW$') or t.startswith('AQ$') 
                    or t.startswith('REPCAT$') or t.startswith('DEF$') or t.startswith('LOGSTDBY$') 
                    or t in {'SQLPLUS_PRODUCT_PROFILE', 'HELP'})
        ]

        return filtered_tables


    else:
        raise ValueError(f"Unsupported database type: {db_type}")
    
def get_table_schema(cursor, db_type, table_name):
    if db_type == 'mysql':
        cursor.execute(f"DESCRIBE {table_name}")
        return [(col[0], col[1]) for col in cursor.fetchall()]

    elif db_type == 'postgresql':
        cursor.execute(f"""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = '{table_name}'
            ORDER BY ordinal_position;
        """)
        
        return [(col[0], col[1]) for col in cursor.fetchall()]

    elif db_type == 'oracle':
        cursor.execute(f"""
            SELECT column_name, data_type 
            FROM user_tab_columns 
            WHERE table_name = '{table_name.upper()}'
        """)
        return [(col[0], col[1]) for col in cursor.fetchall()]

def table_exists(cursor, db_type, table_name):
    if db_type == 'mysql':
        cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
        return cursor.fetchone() is not None

    elif db_type == 'postgresql':
        cursor.execute(f"""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = '{table_name}'
            AND table_schema = 'public'
        """)
        result = cursor.fetchone()
        return result is not None

    elif db_type == 'oracle':
        cursor.execute(f"""
            SELECT table_name FROM user_tables 
            WHERE table_name = '{table_name.upper()}'
        """)
        return cursor.fetchone() is not None
