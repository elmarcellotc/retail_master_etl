def update_store_prices_table(infrastructure_tables_cursor, infrastructure_tables_conn):

    from utils.functional.json_files import import_json_file

    stores_dict = import_json_file("data_raw/Core Data/stores.json")

    items_dict = import_json_file("data_raw/Core Data/items.json")

    # Insert items (if not exists already)
    for store_id, store_info in stores_dict.items():

        column_names = ['Prices']

        

        for k in column_names:

            if store_info[k] == None:

                raise ValueError(k+" can not be null")
                
            elif k == "Prices":

                for item_id in store_info[k]:

                    
                    
                    if item_id not in items_dict.keys():
                        raise ValueError(store_info[k] + " must be an item from Items registry")

                    if not isinstance(store_info[k][item_id], float):
                        raise ValueError(store_info[k] + " must be a positive decimal number")
                    
                    elif store_info[k][item_id] <= 0:
                        raise ValueError(store_info[k] + " must be a positive decimal number")
                    
                    elements_list = [ store_id+item_id ]

                    elements_list.append(store_id)
                    
                    elements_list.append(item_id)
                    
                    elements_list.append(store_info[k][item_id])
            
                    query1 = "INSERT INTO StorePrices (StorePriceID, StorePricesStoreID, StorePricesSKU, StorePricesPrice)"
                    query2 = "VALUES (" + ", ".join( ["%s"]*len(elements_list) ) + ")"
                    query3 = "ON DUPLICATE KEY UPDATE StorePriceID = VALUES(StorePriceID)"

                    query = query1 + "\n" + query2 + "\n" + query3

                    query_tuple = tuple( elements_list )

                    infrastructure_tables_cursor.execute( query, query_tuple )

    # Commit
    infrastructure_tables_conn.commit()