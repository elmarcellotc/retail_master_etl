def update_building_table(core_tables_cursor, core_tables_conn):

    from utils.functional.json_files import import_json_file

    building_dict = import_json_file("data_raw/Core Data/buildings.json")

    column_names = ['Building Model', 'Customers Daily Capacity']
    
    str_columns = ['Building Model']

    for building_id, building_info in building_dict.items():

        elements_list = [building_id]

        for k in column_names:

            if building_info[k]==None:

                raise ValueError(k+" can not be null")
            
            if building_info[k] is str_columns:

                if not isinstance(building_info[k], str):
                    
                    raise ValueError(k+" must be string type")
                
 
            # Rules to consider
            value = building_info[k]

            if k == "Customers Daily Capacity":
                if not isinstance(value, int):
                    raise TypeError(f"Expected integer for '{k}' in {building_id}, got {type(value).__name__}")

            # Append value to list as string            
            elements_list.append( str( building_info[k] ) )

        query1 = "INSERT INTO BuildingTypes (BuildingTypeID, BuildingModel, CustomersDailyCapacity)"
        query2 = "VALUES (" + ", ".join( ["%s"]*len(elements_list) ) + ")"
        query3 = "ON DUPLICATE KEY UPDATE BuildingTypeID = VALUES(BuildingTypeID)"

        query = query1 + "\n" + query2 + "\n" + query3

        query_tuple = tuple(elements_list)

        core_tables_cursor.execute(query, query_tuple )
        
    core_tables_conn.commit()

def update_building_stock_capacity_table(core_tables_cursor, core_tables_conn):

    from utils.functional.json_files import import_json_file

    building_dict = import_json_file("data_raw/Core Data/buildings.json")

    items_dict = import_json_file("data_raw/Core Data/items.json")

    for building_id, building_info in building_dict.items():

        stocks_dict = building_info['Stock Capacity']

        if not isinstance(stocks_dict, dict):

            raise ValueError("Stock Capacity must be dictionary, review registry: "+building_id)
        
        for stock_id in stocks_dict.keys():

            elements_list = [building_id]

            if stock_id not in items_dict.keys():
                raise ValueError("Stock ID must be in items table. Review registry: "+building_id)

            elements_list.append(stock_id)  

            stock_capacity = stocks_dict[stock_id]

            if not isinstance(stock_capacity,(int,float)):

                raise ValueError("Stock capacity must be nummeric type, review registry: "+building_id)
            
            if stock_capacity<0:
                raise ValueError("Stock capacity must be non negative, review registry: "+building_id)
            
            elements_list.append(stock_capacity)
            
            query1 = "INSERT INTO BuildingTypeStockCapacity (BuildingTypeID, SKU, CapacityAmount)"
            query2 = "VALUES (" + ", ".join( ["%s"]*len(elements_list) ) + ")"
            query3 = "ON DUPLICATE KEY UPDATE BuildingTypeID = VALUES(BuildingTypeID)"

            query = query1 + "\n" + query2 + "\n" + query3

            query_tuple = tuple(elements_list)
            core_tables_cursor.execute(query, query_tuple )
            
    core_tables_conn.commit()

def building_type_minimum_employees_table(core_tables_cursor, core_tables_conn):

    from utils.functional.json_files import import_json_file

    building_dict = import_json_file("data_raw/Core Data/buildings.json")

    employing_categories_dict = import_json_file("data_raw/Core Data/employes_charges.json")

    for building_id, building_info in building_dict.items():

        employes_dict = building_info['Employes']

        if not isinstance(employes_dict, dict):

            raise ValueError("Employes Capacity must be dictionary, review registry: "+building_id)
        
        for employes_id in employes_dict.keys():

            elements_list = [building_id]

            if employes_id not in employing_categories_dict.keys():
                raise ValueError("Employes Category ID must be in employes categories table. Review registry: "+building_id)

            elements_list.append(employes_id)  

            employes_capacity = employes_dict[employes_id]

            if not isinstance(employes_capacity,(int,float)):

                raise ValueError("Employes capacity must be nummeric type, review registry: "+building_id)
            
            if employes_capacity<0:
                raise ValueError("Employes capacity must be non negative, review registry: "+building_id)
            
            elements_list.append(employes_capacity)
            
            query1 = "INSERT INTO BuildingTypeMinimumEmployees (BuildingTypeID, EmployCategoryID, MinimumRequired)"
            query2 = "VALUES (" + ", ".join( ["%s"]*len(elements_list) ) + ")"
            query3 = "ON DUPLICATE KEY UPDATE BuildingTypeID = VALUES(BuildingTypeID)"

            query = query1 + "\n" + query2 + "\n" + query3

            query_tuple = tuple(elements_list)
    
            core_tables_cursor.execute(query, query_tuple )

    core_tables_conn.commit()