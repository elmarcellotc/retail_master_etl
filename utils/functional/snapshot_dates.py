def get_snapshot_date_range(cursor, table_name, snapshot_date_column, days_back=21):

    from datetime import timedelta
    
    """
    Determines the snapshot date range that should be regenerated.

    Parameters
    ----------
    cursor : mysql.connector.cursor.MySQLCursor
        Cursor connected to the database.
    table_name : str
        Name of the snapshot table.
    snapshot_date_column : str
        Name of the snapshot datetime column.
    days_back : int, default=21
        Number of days before the latest snapshot that should be regenerated.

    Returns
    -------
    dict
        {
            "FirstTime": bool,
            "snapshot_start_date": datetime or None,
            "snapshot_end_date": datetime or None
        }
    """

    query = f"""
        SELECT MAX({snapshot_date_column})
        FROM {table_name}
    """

    cursor.execute(query)

    result = cursor.fetchone()

    latest_snapshot = result[0]

    # Table is empty
    if latest_snapshot is None:
        return {
            "FirstTime": True,
            "snapshot_start_date": None,
            "snapshot_end_date": None
        }

    snapshot_end_date = latest_snapshot
    snapshot_start_date = snapshot_end_date - timedelta(days=days_back)

    return {
        "FirstTime": False,
        "snapshot_start_date": snapshot_start_date
    }