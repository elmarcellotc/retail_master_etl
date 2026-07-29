def update_inventory_tables():

    from utils.functional.sql_conn import initialize_conn

    from utils.inventory.store_inventory_snapshot import update_store_inventory_snapshot

    from utils.functional.snapshot_dates import get_snapshot_date_range


    inventory_tables_conn = initialize_conn()
    inventory_tables_cursor = inventory_tables_conn.cursor()

    dates_ranges_dictionary = get_snapshot_date_range(inventory_tables_cursor,"StoreInventorySnapshots","SnapshotDatetime",21)

    update_store_inventory_snapshot(inventory_tables_cursor, inventory_tables_conn, dates_ranges_dictionary)

    # Close cursor
    inventory_tables_cursor.close()

    import pandas as pd

    inventory_tables = [
        "StoreInventorySnapshots", "StoreInventoryBySnapshot"
    ]

    for c in inventory_tables:

        testingdf = pd.read_sql("SELECT * FROM "+c+" ORDER BY RAND() LIMIT 10;", inventory_tables_conn)

        testingdf.to_csv(f'tests/Inventory Tables/{c}.txt', sep="\t", encoding="utf-8", index=False)
        print(testingdf)

    # Close connection
    inventory_tables_conn.close()