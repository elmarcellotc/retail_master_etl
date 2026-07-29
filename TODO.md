# 🚀 RetailMasterDB TODO

---

## 🐍 ETL Tasks

### 🔴 Populate Empty Tables (Highest Priority)

1. **Populate all remaining empty tables**

   * Storesales and StoreAcquisitionEvents
   * Create corresponding ETL functions
   * Follow the existing ETL pattern:

   ```
   update_<table_name>_table()
   ```

   * Export outputs to the `tests/` directory

2. **Verify ETL population order**

   ```
   Core Tables
   → Infrastructure Tables
   → Operational Tables
   ```