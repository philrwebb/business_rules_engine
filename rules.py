import sqlite3
from business_rules import (
    RuleValidator,
    SAFE_GLOBALS,
    SAFE_NODE_TYPES,
    execute_business_rule,
)
from db_funcs import (
    DB_NAME,
    init_db,
    get_allowed_attributes,
    add_rule,
    get_rules_for_event,
    clear_rules,
)

# --- Example Runtime Usage with Database ---
if __name__ == "__main__":
    # 1. Initialize and populate the database
    init_db(["user_age", "order_total", "user_country", "item_count"])

    # Add some business rules for different events
    print("Populating business rules...")
    # Clear existing rules for this event to make the example idempotent
    clear_rules("new_order")

    add_rule("new_order", "user_age > 18")
    add_rule("new_order", "order_total < 1000")
    add_rule("new_order", "user_country in ('US', 'CA', 'GB')")
    add_rule("new_order", "item_count > 0")
    print("\n--- Simulating a 'new_order' event ---")

    # In a real app, this data would come from the order being processed
    order_data_context = {
        "user_age": 25,
        "order_total": 150.75,
        "user_country": "US",
        "item_count": 2,
    }
    print(f"Event data context: {order_data_context}")

    # 3. Fetch configuration from the database
    allowed_attrs_from_db = get_allowed_attributes()
    rules_for_event = get_rules_for_event("new_order")

    print(
        f"\nFound {len(rules_for_event)} rules for event 'new_order'. Executing them..."
    )
    all_rules_passed = True

    # 4. Execute the rules
    for i, rule_expression in enumerate(rules_for_event):
        print(f'  - Rule {i+1}: "{rule_expression}"')  # Corrected this line
        is_rule_true, error_message = execute_business_rule(
            rule_str=rule_expression,
            current_context_values=order_data_context,
            allowed_attributes=allowed_attrs_from_db,
        )

        if error_message:
            print(f"    Result: FAILED VALIDATION -> {error_message}")
            all_rules_passed = False
        else:
            print(f"    Result: {'PASS' if is_rule_true else 'FAIL'}")
            if not is_rule_true:
                all_rules_passed = False

    print(
        f"\nFinal Result for 'new_order' event: {'All rules passed.' if all_rules_passed else 'One or more rules failed.'}"
    )
