import logging

from modules.system.app_paths import (
    get_logs_directory
)


def setup_logging():

    log_file = (
        get_logs_directory()
        /
        "application.log"
    )


    logging.basicConfig(

        filename=str(log_file),

        level=logging.INFO,

        format=(
            "%(asctime)s "
            "%(levelname)s "
            "%(message)s"
        )
    )



def write_log(message):

    logging.info(message)