def update_main_payroll_table(payroll_tables_cursor, payroll_tables_conn):

    from utils.functional.json_files import import_json_file

    payroll_dict = import_json_file("data_raw/Core Data/payroll.json")
    employees_categories = import_json_file("data_raw/Core Data/employes_charges.json")
    workplaces = import_json_file("data_raw/Core Data/workplaces.json")


    for worker_id, worker_info in payroll_dict.items():

        column_names = [
            "worker_category", "id_card_number", "last_name1", "last_name2",
            "name1", "name2", "gender", "ethnic", "age", "dependents", "workplace_id",
            "hourly_salary"
        ]

        can_be_null = ["last_name2", "name2", "ethnic"]

        elements_list = [ worker_id ]

        for c in column_names:

            value = worker_info[c]

            if value is None and c not in can_be_null:
                raise ValueError(f"Field '{c}' cannot be null for worker {worker_id}")

            if c == "id_card_number":
                if not isinstance(value, int):
                    raise ValueError(f"'id_card_number' must be int for worker {worker_id}")

            elif c == "age":
                if not isinstance(value, int) or value < 16:
                    raise ValueError(f"'age' must be int and ≥ 16 for worker {worker_id}")

            elif c == "dependents":
                if not isinstance(value, int) or value < 0:
                    raise ValueError(f"'dependents' must be int and ≥ 0 for worker {worker_id}")

            elif c == "hourly_salary":
                if not isinstance(value, (float, int)) or value < 5:
                    raise ValueError(f"'hourly_salary' must be float or int and ≥ 5 for worker {worker_id}")

            elif c == "gender":
                if value not in ["male", "female"]:
                    raise ValueError(f"'gender' must be 'male' or 'female' for worker {worker_id}")
                
            elif c == "worker_category":
                if value not in employees_categories.keys():
                    raise ValueError(f"'worker_category' must be a category from Employingcategories for worker {worker_id}")
                
            elif c == "workplace_id":
                if value not in workplaces.keys():
                    raise ValueError(f"'workplace_id' must be registered in  Workplaces for worker {worker_id}")

            elements_list.append( str(value) )

        query11 = "INSERT INTO Payroll (worker_id, worker_category, id_card_number"
        query12 = ", last_name1, last_name2, name1, name2, gender, ethnic, age"
        query13 = ", dependents, workplace_id, hourly_salary)"

        query1 = query11+query12+query13
        query2 = "VALUES (" + ", ".join( ["%s"]*len(elements_list) ) + ")"
        query3 = "ON DUPLICATE KEY UPDATE worker_id = VALUES(worker_id)"

        query = query1 + "\n" + query2 + "\n" + query3

        query_tuple = tuple( elements_list )
        payroll_tables_cursor.execute( query, query_tuple )

    # Commit
    payroll_tables_conn.commit()