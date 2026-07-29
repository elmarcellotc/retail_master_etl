def update_store_inventory_snapshot(inventory_tables_cursor, inventory_tables_conn, dates_ranges_dictionary):

    from utils.functional.json_files import import_json_file

    from os import listdir

    inventories_files_list = listdir("data_raw/Stores Inventories/")

    for file in inventories_files_list:

        inventory_dict = import_json_file("data_raw/Stores Inventories/"+file)

        import re
        from datetime import datetime

        patron = r"H(?P<hour>\d{2})D(?P<day>\d{2})M(?P<month>\d{2})Y(?P<year>\d{4})"

        for inventory_id, inventory_info in inventory_dict.items():

            coincidences_dict = re.search(patron, inventory_id).groupdict()

            inventory_year = int(coincidences_dict["year"])
            inventory_month = int(coincidences_dict["month"])
            inventory_day = int(coincidences_dict["day"])
            inventory_hour = int(coincidences_dict["hour"])

            inventory_snapshot_datetime = datetime(inventory_year,inventory_month, inventory_day, inventory_hour)

            update_snapshot_lever = False

            if not dates_ranges_dictionary["FirstTime"]:

                if dates_ranges_dictionary["snapshot_start_date"] <= inventory_snapshot_datetime:

                    update_snapshot_lever = True

            else:
                update_snapshot_lever = True

            # Only update registries when the Snapshot dates were well specified.

            if update_snapshot_lever:

                # inventory_id is SnapshotID

                store_id = str(inventory_info["Store"])

                # inventory_snapshot_datetime is SnapshotDatetime

                account_balance = float(inventory_info["Account"])

                if account_balance < 0:
                    raise ValueError(
                        f"Account balance cannot be negative for inventory '{inventory_id}'. "
                        f"Received: {account_balance}"
                    )

                # First register the inventory Snapshot

                elements_list = [
                    inventory_id, store_id, inventory_snapshot_datetime, account_balance
                ]

                query1 = "INSERT INTO StoreInventorySnapshots (SnapshotID, StoreID, SnapshotDatetime, AccountBalance)"

                query2 = "VALUES (" + ", ".join( ["%s"]*len(elements_list) ) + ")"

                query3 = "ON DUPLICATE KEY UPDATE SnapshotID = VALUES(SnapshotID)"

                query = query1 + "\n" + query2 + "\n" + query3

                query_tuple = tuple( elements_list )

                inventory_tables_cursor.execute( query, query_tuple )

                # After the snapshot register the quantities by ID

                for key_name in list(inventory_info.keys()):
                    if key_name not in ["Store","SnapshotDatetime","Account"]:

                        skus_quantity = int(inventory_info[key_name])

                        # StoreInventoryBySnapshotID because here registries are by SKU in each row
                        snapshot_sku_id = "INV"+coincidences_dict["year"]+coincidences_dict["month"]+coincidences_dict["day"]+coincidences_dict["hour"]+store_id+key_name

                        elements_list = [
                                            snapshot_sku_id, inventory_id, key_name, skus_quantity
                                        ]
                        
                        query1 = "INSERT INTO StoreInventoryBySnapshot (StoreInventoryBySnapshotID, SnapshotID, sku, Quantity)"

                        query2 = "VALUES (" + ", ".join( ["%s"]*len(elements_list) ) + ")"

                        query3 = "ON DUPLICATE KEY UPDATE StoreInventoryBySnapshotID = VALUES(StoreInventoryBySnapshotID)"

                        query = query1 + "\n" + query2 + "\n" + query3

                        query_tuple = tuple( elements_list )

                        inventory_tables_cursor.execute( query, query_tuple )

            else:
                continue

    # Commit
    inventory_tables_conn.commit()