import csv
import json
import sqlite3


# Function to validate client data
def is_valid_client(name, email, age):
    if not name or not email:
        return False
    try:
        age = int(age)
        return age > 0
    except ValueError:
        return False


# create a log file for invalid rows
def log_error(row, file_path="error_log.txt"):
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(f"[ERROR] invalid row: {row}\n")


# Function to save valid clients to a CSV file
def save_valid_clients(valid_clients, output_path="valid_clients.csv"):
    fieldnames = ["name", "email", "age"]
    with open(output_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for client in valid_clients:
            writer.writerow(client)


# Function to save valid clients to a JSON file
def save_clients_to_jason(valid_clients, output_path="valid_clients.json"):
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(valid_clients, f, indent=2)


#
def save_clients_to_sqlite(valid_clients, db_path="valid_clients.sqlite"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute(
        """
                    Create table if not exists clients(
                        name TEXT,
                        email TEXT UNIQUE,
                        age INTIGER
                    )
                    """
    )
    for client in valid_clients:
        try:
            cursor.execute(
                """
                INSERT INTO clients (name, email, age) VALUES (?, ?, ?)
            """,
                (client["name"], client["email"], client["age"]),
            )
        except sqlite3.IntegrityError:
            pass  # Skip duplicates

    conn.commit()
    conn.close()


# Function to import clients from a CSV file
def import_clients(csv_path):
    valid_clients = []
    invalid_clients = []
    seen_emails = set()  # To track unique emails

    # Clear the log file before starting
    open("error_log.txt", "w").close()

    with open(csv_path, newline="", encoding="cp1250") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            name = row.get("name", "").strip()
            email = row.get("email", "").strip()
            age = row.get("age", "").strip()

            # validation
            if not is_valid_client(name, email, age):
                invalid_clients.append(row)
                log_error(row)
                continue

            # check for duplicate emails
            if email in seen_emails:
                invalid_clients.append(row)
                log_error(row)
                continue

            # passed all checks
            seen_emails.add(email)
            valid_clients.append({"name": name, "email": email, "age": int(age)})

    return valid_clients, invalid_clients


# Example usage
if __name__ == "__main__":
    try:
        valid, invalid = import_clients("clients.csv")

        # save results
        save_valid_clients(valid)
        save_clients_to_jason(valid)
        save_clients_to_sqlite(valid)

        print("Valid clients:")
        for client in valid:
            print(client)

        print("\nInvalid clients:")
        for bad in invalid:
            print(bad)

        print(
            "\n save valid clients to 'valid_clients.csv', 'valid_clients.json' and 'valid_clients.sqlite'"
        )
        print("Total valid clients:", len(valid))
        print("Errors logged in 'error_log.txt'")
        print("Total invalid clients:", len(invalid))

        # Uncomment the following lines to see the results in console
        # print("OK!, valid clients:", valid)
        # print("NO!, invalida clients:", invalid)
    except FileNotFoundError:
        print("File not found: clients.csv")
