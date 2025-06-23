import unittest
import sqlite3
from db_funcs import (
    init_db,
    add_attribute,
    get_allowed_attributes,
    add_rule,
    get_rules_for_event,
)


class TestDbFuncs(unittest.TestCase):

    def setUp(self):
        """Set up a temporary in-memory database for each test."""
        self.db_name = ":memory:"
        init_db(self.db_name)

    def test_add_and_get_attributes(self):
        """Test that we can add and retrieve allowed attributes."""
        # Initially, the attributes should be empty
        self.assertEqual(get_allowed_attributes(self.db_name), set())

        # Add some attributes
        add_attribute("user_age", self.db_name)
        add_attribute("order_total", self.db_name)

        # Verify they are present
        self.assertEqual(
            get_allowed_attributes(self.db_name), {"user_age", "order_total"}
        )

        # Test that adding a duplicate attribute doesn't cause an error or change the set
        add_attribute("user_age", self.db_name)
        self.assertEqual(
            get_allowed_attributes(self.db_name), {"user_age", "order_total"}
        )

    def test_add_and_get_rules(self):
        """Test that we can add and retrieve business rules for a given event type."""
        # Initially, there should be no rules for this event
        self.assertEqual(get_rules_for_event("new_order", self.db_name), [])

        # Add some rules
        rule1 = "user_age > 18"
        rule2 = "order_total < 1000"
        add_rule("new_order", rule1, self.db_name)
        add_rule("new_order", rule2, self.db_name)

        # Verify the rules are retrieved correctly
        retrieved_rules = get_rules_for_event("new_order", self.db_name)
        self.assertIn(rule1, retrieved_rules)
        self.assertIn(rule2, retrieved_rules)
        self.assertEqual(len(retrieved_rules), 2)

        # Add a rule for a different event type
        add_rule("user_signup", "user_country == 'US'", self.db_name)

        # Verify that the original event's rules are unchanged
        self.assertEqual(len(get_rules_for_event("new_order", self.db_name)), 2)

        # Verify the new event's rule is present
        self.assertEqual(
            get_rules_for_event("user_signup", self.db_name), ["user_country == 'US'"]
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
