def update_infrastructure_tables():

    from utils.functional.sql_conn import initialize_conn
    from utils.infrastructure.tables.warehouses_table import update_warehouses_table
    from utils.infrastructure.tables.stores_table import update_stores_table
    from utils.infrastructure.tables.store_prices_table import update_store_prices_table


    infrastructure_tables_conn = initialize_conn()
    infrastructure_tables_cursor = infrastructure_tables_conn.cursor()

    update_stores_table(infrastructure_tables_cursor, infrastructure_tables_conn)
    update_warehouses_table(infrastructure_tables_cursor, infrastructure_tables_conn)
    update_store_prices_table(infrastructure_tables_cursor, infrastructure_tables_conn)

    # Close cursor
    infrastructure_tables_cursor.close()

    import pandas as pd

    # core_tables_names = [
    #     "Warehouses", "Stores", "StorePrices"
    # ]

    core_tables_names = [
        "Stores", "Warehouses"
    ]

    data_tables_names = [
        "StorePrices"
    ]

    for c in core_tables_names:

        testingdf = pd.read_sql("SELECT * FROM "+c, infrastructure_tables_conn)

        testingdf.to_csv(f'tests/Infrastructure Tables/{c}.txt', sep="\t", encoding="utf-8", index=False)
        print(testingdf)

    for c in data_tables_names:

        # For future versions with too many items, this must be a sample selection

        testingdf = pd.read_sql("SELECT * FROM "+c, infrastructure_tables_conn)

        testingdf.to_csv(f'tests/Infrastructure Tables/{c}.txt', sep="\t", encoding="utf-8", index=False)
        print(testingdf)

    # Close connection
    infrastructure_tables_conn.close()