# from utils.core_tables.core_tables import update_core_tables

# from utils.infrastructure.infrastructure import update_infrastructure_tables
from utils.payroll.payroll import update_payroll

from utils.inventory.update_inventory import update_inventory_tables

# update_core_tables()
# update_infrastructure_tables()
update_payroll()
update_inventory_tables()