from database.db import get_connection
from modules.system.app_paths import get_database_path


connection = get_connection()


print(
    "Database location:"
)

print(
    get_database_path()
)


connection.close()