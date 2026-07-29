def update_warehouses_table(infrastructure_tables_cursor, infrastructure_tables_conn):

    from utils.functional.json_files import import_json_file

    warehouses_dict = import_json_file("data_raw/Core Data/warehouses.json")

    building_types_dict = import_json_file("data_raw/Core Data/buildings.json")

    locations_dict = import_json_file("data_raw/Core Data/locations.json")

    # Insert items (if not exists already)
    for warehouse_id, warehouse_info in warehouses_dict.items():

        column_names = ['Building Model', 'Location']

        elements_list = [ warehouse_id ]

        for k in column_names:

            if warehouse_info[k] == None:

                raise ValueError(k+" can not be null")
            
            if k == "Building Model":

                if warehouse_info[k] not in building_types_dict.keys():

                    raise ValueError(warehouse_info[k] + " must be a Building type from buildings registry")
                
            if k == "Location":

                if warehouse_info[k] not in locations_dict.keys():

                    raise ValueError(warehouse_info[k] + " must be a location from locations registry")
            
            elements_list.append( str( warehouse_info[k] ) )
            
        query1 = "INSERT INTO Warehouses (WarehouseID, WarehouseBuildingModel, WarehouseLocation)"
        query2 = "VALUES (" + ", ".join( ["%s"]*len(elements_list) ) + ")"
        query3 = "ON DUPLICATE KEY UPDATE WarehouseID = VALUES(WarehouseID)"

        query = query1 + "\n" + query2 + "\n" + query3

        query_tuple = tuple( elements_list )

        # -------- Insert workplace --------

        workplace_id = "WPLCS" + warehouse_id

        workplace_elements_list = [
            workplace_id,
            "Warehouse",
            warehouse_id
        ]

        query1 = "INSERT INTO Workplaces (WorkplaceID, WorkplaceType, WarehouseID)"
        query2 = "VALUES (" + ", ".join(["%s"] * len(workplace_elements_list)) + ")"
        query3 = "ON DUPLICATE KEY UPDATE WorkplaceID = VALUES(WorkplaceID)"

        workplace_query = query1 + "\n" + query2 + "\n" + query3

        workplace_query_tuple = tuple(workplace_elements_list)

        infrastructure_tables_cursor.execute(workplace_query, workplace_query_tuple)        

        infrastructure_tables_cursor.execute( query, query_tuple )

    # Commit
    infrastructure_tables_conn.commit()