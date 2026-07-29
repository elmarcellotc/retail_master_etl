def update_warehouses_payroll_table(payroll_tables_cursor, payroll_tables_conn):

    from utils.functional.json_files import import_json_file

    payroll_dict = import_json_file("data_raw/Core Data/payroll.json")

    workplaces_dict = import_json_file("data_raw/Core Data/workplaces.json")

    for worker_id, worker_info in payroll_dict.items():

        workplace_id = worker_info["workplace_id"]

        workplace_info = workplaces_dict[workplace_id]

        elements_list = []

        if workplace_info["WorkplaceType"] == "Store":
            continue

        elif workplace_info["WorkplaceType"] == "Warehouse":

            store_id = workplace_info["WarehouseID"]

            elements_list = [ worker_id, store_id ]

            query1 = "INSERT INTO WarehouseWorkers (WorkerID, WarehouseID)"

            query2 = "VALUES (" + ", ".join( ["%s"]*len(elements_list) ) + ")"
            query3 = "ON DUPLICATE KEY UPDATE WorkerID = VALUES(WorkerID)"

            query = query1 + "\n" + query2 + "\n" + query3

            query_tuple = tuple( elements_list )
            payroll_tables_cursor.execute( query, query_tuple )

    # Commit
    payroll_tables_conn.commit()