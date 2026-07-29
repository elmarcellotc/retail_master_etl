def update_employing_categories_table(core_tables_cursor, core_tables_conn):

    from utils.functional.json_files import import_json_file

    employing_categories_dict = import_json_file("data_raw/Core Data/employes_charges.json")

    # Insert locations (if not exists already)
    for categories_id, categories_info in employing_categories_dict.items():

        column_names = [
            'Employ Category', 'Maximum hiring days allowed', 'Maximum hiring daily hours allowed',
            'Minimum Hourly Payment ($)', 'Maximum Hourly Payment ($)'
            ]
        
        str_columns = ['Employ Category']

        elements_list = [categories_id]

        for k in column_names:

            if categories_info[k] == None:

                raise ValueError(k+" can not be null")
            
            if categories_info[k] is str_columns:

                if not isinstance(categories_info[k], str):
                    
                    raise ValueError(k+" must be string type")
                
 
            # Rules to consider
            value = categories_info[k]

            if k == "Maximum hiring days allowed":
                if not isinstance(value, int):
                    raise TypeError(f"Expected integer for '{k}' in {categories_id}, got {type(value).__name__}")
                if value < 2 or value > 5:
                    raise ValueError(f"'{k}' value for {categories_id} is out of boundaries. It must be between 2 and 5 → [2; 5]")

            elif k == "Maximum hiring daily hours allowed":
                if not isinstance(value, int):
                    raise TypeError(f"Expected integer for '{k}' in {categories_id}, got {type(value).__name__}")
                if value < 4 or value > 8:
                    raise ValueError(f"'{k}' value for {categories_id} is out of boundaries. It must be between 4 and 8 → [4; 8]")

            elif k == "Minimum Hourly Payment":
                if not isinstance(value, (float, int)):
                    raise TypeError(f"Expected float or int for '{k}' in {categories_id}, got {type(value).__name__}")
                if value < 2.00:
                    raise ValueError(f"'{k}' for {categories_id} is below the minimum allowed. It must be at least 2.00")

            elif k == "Maximum Hourly Payment":
                if not isinstance(value, (float, int)):
                    raise TypeError(f"Expected float or int for '{k}' in {categories_id}, got {type(value).__name__}")
                if value > 50.00:
                    raise ValueError(f"'{k}' for {categories_id} exceeds the maximum allowed. It must not exceed 50.00")

            # Append value to list as string            
            elements_list.append( str( categories_info[k] ) )

        query11 = "INSERT INTO EmployingCategories (EmployCategoryID, CategoryName, MaxHiringDaysAllowed,"
        query12 = " MaxHiringDailyHoursAllowed, MinHourlyPayment, MaxHourlyPayment)"
        query1 = query11 + query12
        query2 = "VALUES (" + ", ".join( ["%s"]*len(elements_list) ) + ")"
        query3 = "ON DUPLICATE KEY UPDATE EmployCategoryID = VALUES(EmployCategoryID)"

        query = query1 + "\n" + query2 + "\n" + query3

        query_tuple = tuple(elements_list)

        core_tables_cursor.execute(query, query_tuple )

    # Commit
    core_tables_conn.commit()