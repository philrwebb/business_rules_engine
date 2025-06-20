import sqlite3

DB_NAME = "business_rules.db"


def get_db_connection():
    """Establishes a connection to the SQLite database."""
    return sqlite3.connect(DB_NAME)


def init_db():
    """Initializes the database with the necessary tables."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        # Table for allowed system attributes
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS allowed_attributes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            )
        """
        )
        # Table for business rules
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS business_rules (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_type TEXT NOT NULL,
                rule_text TEXT NOT NULL
            )
        """
        )
        conn.commit()


def add_attribute(name: str):
    """Adds a new allowed attribute to the database."""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO allowed_attributes (name) VALUES (?)", (name,))
            conn.commit()
            print(f"Attribute '{name}' added successfully.")
    except sqlite3.IntegrityError:
        print(f"Attribute '{name}' already exists.")


def get_allowed_attributes() -> set[str]:
    """Retrieves the set of all allowed attribute names from the database."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM allowed_attributes")
        return {row[0] for row in cursor.fetchall()}


def add_rule(event_type: str, rule_text: str):
    """Adds a new business rule to the database."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO business_rules (event_type, rule_string) VALUES (?, ?)",
            (event_type, rule_text),
        )
        conn.commit()
        print(f"Rule for event '{event_type}' added successfully.")


def get_rules_for_event(event_type: str) -> list[str]:
    """Retrieves all rule strings for a given event type."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT rule_string FROM business_rules WHERE event_type = ?", (event_type,)
        )
        return [row[0] for row in cursor.fetchall()]
