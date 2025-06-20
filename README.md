# Python Business Rules Engine

This project implements a dynamic, database-driven business rules engine in Python. It allows for the safe execution of user-defined rules against a given data context.

## Core Components

### `rules.py`

This is the main application file and serves as the entry point and orchestrator. Its primary responsibilities are:

- **Initialization**: Sets up the database by calling `db_funcs.init_db()`.
- **Data Seeding**: Populates the database with initial allowed attributes and business rules for demonstration purposes.
- **Event Simulation**: Simulates a runtime event (e.g., a new order) with a specific data context.
- **Rule Execution**: Fetches the relevant rules and allowed attributes from the database, then uses `business_rules.execute_business_rule()` to evaluate each rule against the event's context.
- **Reporting**: Prints the validation and execution results to the console.

### `business_rules.py`

This module contains the core logic for parsing, validating, and executing the business rules safely.

- **`RuleValidator`**: An `ast.NodeVisitor` subclass that traverses the Abstract Syntax Tree (AST) of a rule string. It ensures that the rule only contains allowed nodes (e.g., comparisons, boolean operations) and only references attributes from a predefined safe list. This is the primary mechanism for preventing malicious or unsafe code execution.
- **`execute_business_rule()`**: The main function that takes a rule string, a data context, and the set of allowed attributes. It orchestrates the process of:
  1.  Parsing the rule string into an AST.
  2.  Validating the AST using `RuleValidator`.
  3.  Compiling the validated AST into executable Python bytecode.
  4.  Executing the bytecode in a restricted environment using `eval()` with carefully controlled global and local scopes.
  5.  Returning the boolean result of the rule and any validation or execution errors.

### `db_funcs.py`

This module encapsulates all database interactions, using Python's built-in `sqlite3` library. It provides a clean API for the rest of the application to manage the persistence of rules and attributes.

- **`init_db()`**: Creates the SQLite database file and the necessary tables (`allowed_attributes`, `business_rules`) if they don't already exist.
- **`add_attribute()` / `get_allowed_attributes()`**: Functions to manage the list of attributes that are permissible for use in business rules.
- **`add_rule()` / `get_rules_for_event()`**: Functions to add new business rules to the database and retrieve all rules associated with a specific event type (e.g., 'new_order').
