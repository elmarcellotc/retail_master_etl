def update_stores_table(infrastructure_tables_cursor, infrastructure_tables_conn):

    from utils.functional.json_files import import_json_file

    stores_dict = import_json_file("data_raw/Core Data/stores.json")

    building_types_dict = import_json_file("data_raw/Core Data/buildings.json")

    locations_dict = import_json_file("data_raw/Core Data/locations.json")

    # Insert items (if not exists already)
    for store_id, store_info in stores_dict.items():

        column_names = ['Store Model', 'Location']

        elements_list = [ store_id ]

        for k in column_names:

            if store_info[k] == None:

                raise ValueError(k+" can not be null")
            
            if k == "Store Model":

                if store_info[k] not in building_types_dict.keys():

                    raise ValueError(store_info[k] + " must be a Building type from buildings registry")
                
            elif k == "Location":

                if store_info[k] not in locations_dict.keys():

                    raise ValueError(store_info[k] + " must be a location from locations registry")
            
            elements_list.append( str( store_info[k] ) )

        # -------- Store Table --------
            
        query1 = "INSERT INTO Stores (StoreID, StoreModel, StoreLocation)"
        query2 = "VALUES (" + ", ".join( ["%s"]*len(elements_list) ) + ")"
        query3 = "ON DUPLICATE KEY UPDATE StoreID = VALUES(StoreID)"

        query = query1 + "\n" + query2 + "\n" + query3

        query_tuple = tuple( elements_list )

        infrastructure_tables_cursor.execute( query, query_tuple )

        # -------- Insert workplace --------

        workplace_id = "WPLCS" + store_id

        workplace_elements_list = [
            workplace_id,
            "Store",
            store_id
        ]

        query1 = "INSERT INTO Workplaces (WorkplaceID, WorkplaceType, StoreID)"
        query2 = "VALUES (" + ", ".join(["%s"] * len(workplace_elements_list)) + ")"
        query3 = "ON DUPLICATE KEY UPDATE WorkplaceID = VALUES(WorkplaceID)"

        workplace_query = query1 + "\n" + query2 + "\n" + query3

        workplace_query_tuple = tuple(workplace_elements_list)

        infrastructure_tables_cursor.execute(workplace_query, workplace_query_tuple)

    # Commit
    infrastructure_tables_conn.commit()