# Business Rules Engine (Python and C#)

This project implements a dynamic, database-driven business rules engine. It allows for the safe execution of user-defined rules against a given data context. The project includes two equivalent implementations: one in Python and one in C#.

# Python Business Rules Engine

This project implements a dynamic, database-driven business rules engine in Python. It allows for the safe execution of user-defined rules against a given data context.

## Core Components

### `rules.py`

This is the main application file and serves as the entry point and orchestrator. Its primary responsibilities are:

- **Initialization**: Sets up the database by calling `db_funcs.init_db()` and passing in the initial list of allowed attributes.
- **Data Seeding**: Populates the database with business rules for demonstration purposes.
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

- **`init_db(allowed_attributes=None)`**: Creates the SQLite database file and the necessary tables. If a list of attribute names is provided, it populates the `allowed_attributes` table.
- **`add_attribute()` / `get_allowed_attributes()`**: Functions to manage the list of attributes that are permissible for use in business rules.
- **`add_rule()` / `get_rules_for_event()`**: Functions to add new business rules to the database and retrieve all rules associated with a specific event type.
- **`clear_rules(event_type=None)`**: Deletes rules from the database. If an `event_type` is provided, it deletes only the rules for that event. If omitted, it deletes all rules.

### `test_business_rules.py`

This file contains unit tests for the `business_rules.py` module. It uses Python's built-in `unittest` framework to verify the correctness of the rule validation and execution logic. The tests cover:

- Valid and invalid rule syntax.
- Usage of allowed and disallowed attributes and functions.
- Correct execution and boolean outcomes of rules.
- Handling of runtime errors during rule evaluation.

### `test_db_funcs.py`

This file contains unit tests for the `db_funcs.py` module. It uses an in-memory SQLite database to test the database functions in isolation, ensuring that creating, reading, and deleting attributes and rules works as expected without affecting the main development database.

## Getting Started

To get this project up and running on your local machine, follow these steps:

1.  **Clone the Repository**

    ```bash
    git clone <your-repository-url>
    cd <repository-directory>
    ```

2.  **Create and Activate a Python Virtual Environment**

    It is highly recommended to use a virtual environment to manage project dependencies.

    ```bash
    # Create the virtual environment
    python3 -m venv venv

    # Activate the environment (on macOS/Linux)
    source venv/bin/activate

    # On Windows, use:
    # .\venv\Scripts\activate
    ```

3.  **Install Dependencies**

    This project currently has no external dependencies, as it only uses Python's standard library. However, if any were added, you would install them using the `requirements.txt` file:

    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Application**

    Execute the main `rules.py` script to see the business rules engine in action. It will create the `business_rules.db` file, populate it with sample data, and run a simulation.

    ```bash
    python3 rules.py
    ```

5.  **Run the Tests**

    To verify that all components are working correctly, you can run the unit tests:

    ```bash
    python3 -m unittest discover
    # For more verbose output:
    python3 -m unittest discover -v
    ```

# C# Business Rules Engine

This is a C# implementation of the same business rules engine, located in the `Csharp/` subdirectory. It uses .NET, the Dapper micro-ORM for database access, and the `System.Linq.Dynamic.Core` library for safe, dynamic rule evaluation.

## Core Components (C#)

The C# solution (`CSharpBusinessRules.sln`) is organized into three projects:

-   **`BusinessRulesEngine`**: A class library containing the core logic.
    -   **`BusinessRule.cs`**: A simple record defining the data structure for a rule.
    -   **`IDatabaseService.cs`**: An interface defining the contract for database operations.
    -   **`DatabaseService.cs`**: The implementation of `IDatabaseService` using Dapper and `Microsoft.Data.Sqlite` to interact with the `business_rules.db` SQLite database.
    -   **`RuleEvaluator.cs`**: Contains the `Evaluate` method, which safely parses and evaluates rule strings against a given data object using the `System.Linq.Dynamic.Core` library. This prevents arbitrary code execution.
-   **`App`**: A console application that serves as the entry point and orchestrator. It demonstrates how to initialize the database, add rules, and evaluate them against a sample `Order` object.
-   **`Tests`**: An xUnit test project containing unit tests for the `DatabaseService` and `RuleEvaluator`. It uses an in-memory SQLite database to ensure test isolation.

## Getting Started (C#)

To get the C# project up and running, you will need the [.NET SDK](https://dotnet.microsoft.com/download) installed.

1.  **Navigate to the C# Directory**

    All commands should be run from within the `Csharp` subdirectory.

    ```bash
    cd Csharp
    ```

2.  **Restore Dependencies**

    This command restores the NuGet packages defined in the project files (e.g., Dapper, xUnit, etc.).

    ```bash
    dotnet restore
    ```

3.  **Build the Solution**

    Compile all the projects in the solution.

    ```bash
    dotnet build
    ```

4.  **Run the Application**

    Execute the main console application. It will create/update the `business_rules.db` file in the `Csharp/` directory, populate it with sample data, and run the simulation.

    ```bash
    dotnet run --project App
    ```

5.  **Run the Tests**

    To verify that all components are working correctly, run the unit tests.

    ```bash
    dotnet test
    ```
