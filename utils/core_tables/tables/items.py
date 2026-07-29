def update_items_table(core_tables_cursor, core_tables_conn):

    from utils.functional.json_files import import_json_file

    items_dict = import_json_file("data_raw/Core Data/items.json")

    # Insert items (if not exists already)
    for item_id, item_info in items_dict.items():

        column_names = ['item', 'units']

        elements_list = [ item_id ]

        for k in column_names:

            if item_info[k] == None:

                raise ValueError(k+" can not be null")
            
            elements_list.append( str( item_info[k] ) )
            
        query1 = "INSERT INTO SKU (sku, ItemName, Unit)"
        query2 = "VALUES (" + ", ".join( ["%s"]*len(elements_list) ) + ")"
        query3 = "ON DUPLICATE KEY UPDATE sku = VALUES(sku)"

        query = query1 + "\n" + query2 + "\n" + query3

        query_tuple = tuple(elements_list )

        core_tables_cursor.execute( query, query_tuple )

    # Commit
    core_tables_conn.commit()