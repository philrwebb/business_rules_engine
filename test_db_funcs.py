import unittest
from unittest.mock import patch
import sqlite3
from db_funcs import (
    init_db,
    add_attribute,
    get_allowed_attributes,
    add_rule,
    get_rules_for_event,
    clear_rules,
)


class TestDbFuncs(unittest.TestCase):

    conn = None
    get_db_connection_patcher = None

    @classmethod
    def setUpClass(cls):
        """Create an in-memory database and patch the connection getter."""
        # Create a single, persistent in-memory database connection
        cls.conn = sqlite3.connect(":memory:")

        # Patch the get_db_connection function to always return our single connection
        cls.get_db_connection_patcher = patch('db_funcs.get_db_connection')
        mock_get_db_connection = cls.get_db_connection_patcher.start()
        mock_get_db_connection.return_value = cls.conn

        # Now that the patching is active, initialize the schema once
        init_db()

    @classmethod
    def tearDownClass(cls):
        """Stop the patcher and close the database connection."""
        cls.get_db_connection_patcher.stop()
        cls.conn.close()

    def tearDown(self):
        """Clear all data from the tables after each test to ensure isolation."""
        # Use the connection directly to clear tables within a transaction
        with self.conn:
            self.conn.execute("DELETE FROM business_rules")
            self.conn.execute("DELETE FROM allowed_attributes")

    def test_init_with_attributes(self):
        """Test that init_db can populate attributes."""
        init_db(allowed_attributes=["a", "b"])
        self.assertEqual(get_allowed_attributes(), {"a", "b"})

    def test_add_and_get_attributes(self):
        """Test that we can add and retrieve allowed attributes."""
        self.assertEqual(get_allowed_attributes(), set())
        add_attribute("user_age")
        add_attribute("order_total")
        self.assertEqual(get_allowed_attributes(), {"user_age", "order_total"})
        add_attribute("user_age")  # test duplicate
        self.assertEqual(get_allowed_attributes(), {"user_age", "order_total"})

    def test_add_and_get_rules(self):
        """Test that we can add and retrieve business rules for a given event type."""
        self.assertEqual(get_rules_for_event("new_order"), [])
        rule1 = "user_age > 18"
        rule2 = "order_total < 1000"
        add_rule("new_order", rule1)
        add_rule("new_order", rule2)
        retrieved_rules = get_rules_for_event("new_order")
        self.assertIn(rule1, retrieved_rules)
        self.assertIn(rule2, retrieved_rules)
        self.assertEqual(len(retrieved_rules), 2)
        add_rule("user_signup", "user_country == 'US'")
        self.assertEqual(len(get_rules_for_event("new_order")), 2)
        self.assertEqual(get_rules_for_event("user_signup"), ["user_country == 'US'"])

    def test_clear_rules(self):
        """Test that we can clear rules."""
        add_rule("event1", "rule1")
        add_rule("event2", "rule2")
        self.assertEqual(len(get_rules_for_event("event1")), 1)
        clear_rules("event1")
        self.assertEqual(len(get_rules_for_event("event1")), 0)
        self.assertEqual(len(get_rules_for_event("event2")), 1)
        clear_rules()  # Clear all
        self.assertEqual(len(get_rules_for_event("event2")), 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
