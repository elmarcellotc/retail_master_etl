def update_payroll():

    from utils.functional.sql_conn import initialize_conn
    from utils.payroll.tables.main_payroll import update_main_payroll_table
    from utils.payroll.tables.stores_payroll import update_stores_payroll_table
    from utils.payroll.tables.warehouses_payroll import update_warehouses_payroll_table

    payroll_tables_conn = initialize_conn()
    payroll_tables_cursor = payroll_tables_conn.cursor()

    update_main_payroll_table(payroll_tables_cursor, payroll_tables_conn)
    update_stores_payroll_table(payroll_tables_cursor, payroll_tables_conn)
    update_warehouses_payroll_table(payroll_tables_cursor, payroll_tables_conn)

    # Close cursor
    payroll_tables_cursor.close()

    import pandas as pd

    core_tables_names = [
        "Payroll", "StoreWorkers", "WarehouseWorkers"
    ]

    for c in core_tables_names:

        testingdf = pd.read_sql("SELECT * FROM "+c, payroll_tables_conn).sample(5)

        testingdf.to_csv(f'tests/Payroll/{c}.txt', sep="\t", encoding="utf-8", index=False)
        print(testingdf)

    # Close connection
    payroll_tables_conn.close()