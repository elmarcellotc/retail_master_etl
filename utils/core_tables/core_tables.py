def update_core_tables():

    from utils.functional.sql_conn import initialize_conn

    import pandas as pd

    from utils.core_tables.tables.items import update_items_table
    from utils.core_tables.tables.locations import update_locations_table
    from utils.core_tables.tables.employing_categories import update_employing_categories_table
    from utils.core_tables.tables.building_types import update_building_table, update_building_stock_capacity_table, building_type_minimum_employees_table

    core_tables_conn = initialize_conn()

    core_tables_cursor = core_tables_conn.cursor()

    # Update tables here:

    update_items_table(core_tables_cursor, core_tables_conn)
    update_locations_table(core_tables_cursor, core_tables_conn)
    update_employing_categories_table(core_tables_cursor, core_tables_conn)
    update_building_table(core_tables_cursor, core_tables_conn)
    update_building_stock_capacity_table(core_tables_cursor, core_tables_conn)
    building_type_minimum_employees_table(core_tables_cursor, core_tables_conn)
    
    # Close cursor
    core_tables_cursor.close()

    core_tables_names = [
        "SKU", "Locations", "EmployingCategories", "BuildingTypes", "BuildingTypeStockCapacity",
        "BuildingTypeMinimumEmployees"
    ]

    for c in core_tables_names:

        testingdf = pd.read_sql("SELECT * FROM "+c, core_tables_conn)

        testingdf.to_csv(f'tests/Core Tables/{c}.txt', sep="\t", encoding="utf-8", index=False)
        print(testingdf)

    # Close connection
    core_tables_conn.close()