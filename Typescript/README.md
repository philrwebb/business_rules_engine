# TypeScript Business Rules Engine

This is a TypeScript implementation of a dynamic, database-driven business rules engine, inspired by the Python AST-based version. It uses AST parsing for rule validation and safe evaluation, and SQLite for persistence.

## Structure

- `rules.ts`: Main entry point and orchestrator
- `business_rules.ts`: Rule parsing, validation, and execution
- `db_funcs.ts`: Database functions (using better-sqlite3)
- `test_business_rules.ts`, `test_db_funcs.ts`: Unit tests

## Getting Started

1. Install dependencies:
   ```sh
   npm install
   ```
2. Build the project:
   ```sh
   npm run build
   ```
3. Run the main app:
   ```sh
   npm start
   ```
4. Run tests:
   ```sh
   npm test
   ```
