def update_locations_table(core_tables_cursor, core_tables_conn):

    from utils.functional.json_files import import_json_file

    locations_dict = import_json_file("data_raw/Core Data/locations.json")

    # Insert locations (if not exists already)
    for location_id, location_info in locations_dict.items():

        column_names = ['sector', 'municipality', 'state']

        elements_list = [location_id]

        for k in column_names:

            if location_info[k]==None:

                raise ValueError(k+" can not be null")
            
            elements_list.append( str( location_info[k] ) )

        query1 = "INSERT INTO Locations (LocationID, Sector, Municipality, StateName)"
        query2 = "VALUES (" + ", ".join( ["%s"]*len(elements_list) ) + ")"
        query3 = "ON DUPLICATE KEY UPDATE LocationID = VALUES(LocationID)"

        query = query1 + "\n" + query2 + "\n" + query3

        query_tuple = tuple(elements_list)

        core_tables_cursor.execute( query, query_tuple )

    # Commit
    core_tables_conn.commit()