from modules.system.app_paths import (
    initialize_application_directories,
    get_application_directory,
    get_database_path,
    get_backup_directory,
    get_receipts_directory,
    get_logs_directory,
    get_settings_path
)


initialize_application_directories()


print(
    "Application:",
    get_application_directory()
)

print(
    "Database:",
    get_database_path()
)

print(
    "Backups:",
    get_backup_directory()
)

print(
    "Receipts:",
    get_receipts_directory()
)

print(
    "Logs:",
    get_logs_directory()
)

print(
    "Settings:",
    get_settings_path()
)