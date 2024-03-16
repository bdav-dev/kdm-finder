import shelve

from models.settings_models import EmailConnectionSettings, Settings


SETTINGS_FILENAME = "app_settings"
SETTINGS_SHELVE_KEY = "settings"

def are_email_connection_settings_vaid(email_connection_settings: EmailConnectionSettings) -> bool:
    for _, value in vars(email_connection_settings).items():
        if value is None:
            return False
    return True

def get_settings() -> Settings | None:
    with shelve.open(SETTINGS_FILENAME) as storage:
        if SETTINGS_SHELVE_KEY in storage:
            return storage[SETTINGS_SHELVE_KEY]
        return Settings()

def set_settings(settings: Settings):
    with shelve.open(SETTINGS_FILENAME) as storage:
        storage[SETTINGS_SHELVE_KEY] = settings