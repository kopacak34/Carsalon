import csv
import json
import os
from db import get_connection

class ImportService:

    def import_customers_csv(self, path):
        if not os.path.exists(path):
            print(f"Soubor {path} neexistuje.")
            return

        conn = get_connection()
        cur = conn.cursor()

        try:
            with open(path, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    cur.execute(
                        "INSERT INTO customer (name, email, active) VALUES (%s, %s, %s)",
                        (row["name"], row["email"], bool(int(row["active"])))
                    )
            conn.commit()
            print("Import zákazníků dokončen")
        except Exception as e:
            conn.rollback()
            print("Chyba při importu:", e)
        finally:
            conn.close()



    def import_cars_json(self, path):
        if not os.path.exists(path):
            print(f"Soubor {path} neexistuje.")
            return

        conn = get_connection()
        cur = conn.cursor()

        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)

            for car in data:
                cur.execute(
                    """
                    INSERT INTO car (brand, model, price, fuel, available)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (
                        car["brand"],
                        car["model"],
                        car["price"],
                        car["fuel"],
                        car.get("available", True)
                    )
                )

            conn.commit()
            print("Import aut dokončen")

        except Exception as e:
            conn.rollback()
            print("Chyba při importu aut:", e)

        finally:
            conn.close()
