import mysql.connector
import configparser
import os
import sys


CONFIG_PATH = os.path.join("config", "config.ini")


def get_connection():
    if not os.path.exists(CONFIG_PATH):
        print("Chyba konfigurace:")
        print(f"Soubor {CONFIG_PATH} neexistuje.")
        sys.exit(1)

    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)

    if "database" not in config:
        print("Chyba konfigurace:")
        print("V config.ini chybí sekce [database].")
        sys.exit(1)

    try:
        db_cfg = config["database"]

        return mysql.connector.connect(
            host=db_cfg.get("host"),
            port=db_cfg.getint("port"),
            user=db_cfg.get("user"),
            password=db_cfg.get("password"),
            database=db_cfg.get("database"),
        )

    except mysql.connector.Error as e:
        print("Chyba připojení k databázi:")
        print(e)
        sys.exit(1)
