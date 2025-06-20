import unittest
import ast
from business_rules import RuleValidator, execute_business_rule, SAFE_NODE_TYPES


class TestRuleValidator(unittest.TestCase):

    def test_valid_simple_expression(self):
        rule = "user_age > 18"
        tree = ast.parse(rule, mode="eval")
        validator = RuleValidator(
            allowed_attribute_names={"user_age"}, allowed_node_types=SAFE_NODE_TYPES
        )
        validator.visit(tree)
        self.assertTrue(validator.is_valid)
        self.assertEqual(len(validator.errors), 0)

    def test_disallowed_variable(self):
        rule = "credit_score > 700"
        tree = ast.parse(rule, mode="eval")
        validator = RuleValidator(
            allowed_attribute_names={"user_age"}, allowed_node_types=SAFE_NODE_TYPES
        )
        validator.visit(tree)
        self.assertFalse(validator.is_valid)
        self.assertIn(
            "Disallowed attribute/variable: 'credit_score'", validator.errors[0]
        )

    def test_disallowed_node_type(self):
        # Using an f-string which is an ast.JoinedStr, not in SAFE_NODE_TYPES
        rule = "f'hello'"
        # ast.parse for f-string in 'eval' mode creates a JoinedStr node.
        tree = ast.parse(rule, mode="eval")
        validator = RuleValidator(
            allowed_attribute_names=set(), allowed_node_types=SAFE_NODE_TYPES
        )
        validator.visit(tree)
        self.assertFalse(validator.is_valid)
        self.assertIn("Disallowed node type: JoinedStr", validator.errors[0])

        # Let's try another disallowed type that is valid in 'eval' mode, like a lambda
        rule = "lambda: True"
        tree = ast.parse(rule, mode="eval")
        validator = RuleValidator(
            allowed_attribute_names=set(), allowed_node_types=SAFE_NODE_TYPES
        )
        validator.visit(tree)
        self.assertFalse(validator.is_valid)
        self.assertIn("Disallowed node type: Lambda", validator.errors[0])

    def test_disallowed_attribute_access(self):
        rule = "'hello'.upper()"
        tree = ast.parse(rule, mode="eval")
        validator = RuleValidator(
            allowed_attribute_names=set(),
            allowed_node_types=SAFE_NODE_TYPES,
            allowed_call_names={"upper"},
        )
        validator.visit(tree)
        self.assertFalse(validator.is_valid)
        # The visitor will first complain about the complex call, then about the attribute access.
        self.assertIn("Disallowed complex function call target", validator.errors[0])
        self.assertIn("Disallowed attribute access ('.')", validator.errors[1])

    def test_disallowed_function_call(self):
        rule = "open('file.txt')"
        tree = ast.parse(rule, mode="eval")
        validator = RuleValidator(
            allowed_attribute_names=set(),
            allowed_node_types=SAFE_NODE_TYPES,
            allowed_call_names={"print"},
        )
        validator.visit(tree)
        self.assertFalse(validator.is_valid)
        self.assertIn("Disallowed function call: 'open'", validator.errors[0])

    def test_allowed_function_call(self):
        rule = "len('hello') > 3"
        tree = ast.parse(rule, mode="eval")
        # We need to allow 'len' in the validator's allowed_call_names
        validator = RuleValidator(
            allowed_attribute_names=set(),
            allowed_node_types=SAFE_NODE_TYPES,
            allowed_call_names={"len"},
        )
        # But the validator also checks for names in SAFE_GLOBALS, and 'len' is not there by default in the call check.
        # The execute_business_rule function handles this by merging globals.
        # For a direct validator test, let's assume 'len' is an allowed attribute for simplicity.
        validator_with_len = RuleValidator(
            allowed_attribute_names={"len"}, allowed_node_types=SAFE_NODE_TYPES
        )
        # This is not quite right. The validator's visit_Name will fail 'len' if it's not an allowed attribute.
        # The visit_Call is what checks the function name. Let's re-test with a proper allowed call name.
        validator_calls = RuleValidator(
            allowed_attribute_names=set(),
            allowed_node_types=SAFE_NODE_TYPES,
            allowed_call_names={"len"},
        )
        validator_calls.visit(tree)
        self.assertTrue(validator_calls.is_valid)


class TestExecuteBusinessRule(unittest.TestCase):

    def setUp(self):
        self.allowed_attrs = {"user_age", "order_total", "user_country"}
        self.context = {"user_age": 25, "order_total": 150.0, "user_country": "US"}

    def test_execute_simple_true(self):
        rule = "user_age > 18"
        result, error = execute_business_rule(rule, self.context, self.allowed_attrs)
        self.assertTrue(result)
        self.assertIsNone(error)

    def test_execute_simple_false(self):
        rule = "order_total > 200"
        result, error = execute_business_rule(rule, self.context, self.allowed_attrs)
        self.assertFalse(result)
        self.assertIsNone(error)

    def test_execute_complex_rule_true(self):
        rule = "user_age > 20 and order_total < 200 and user_country in ('US', 'CA')"
        result, error = execute_business_rule(rule, self.context, self.allowed_attrs)
        self.assertTrue(result)
        self.assertIsNone(error)

    def test_execute_syntax_error(self):
        rule = "user_age >"  # This is a real syntax error
        result, error = execute_business_rule(rule, self.context, self.allowed_attrs)
        self.assertFalse(result)
        self.assertIn("Syntax error", error)

    def test_execute_validation_error_disallowed_name(self):
        rule = "credit_score > 700"
        result, error = execute_business_rule(rule, self.context, self.allowed_attrs)
        self.assertFalse(result)
        self.assertIn("Invalid rule", error)
        self.assertIn("Disallowed attribute/variable: 'credit_score'", error)

    def test_execute_validation_error_disallowed_node(self):
        rule = "lambda: user_age > 18"
        result, error = execute_business_rule(rule, self.context, self.allowed_attrs)
        self.assertFalse(result)
        self.assertIn("Invalid rule", error)
        self.assertIn("Disallowed node type: Lambda", error)

    def test_execute_runtime_error(self):
        # Add a division attribute and test division by zero
        attrs = self.allowed_attrs.copy()
        attrs.add("divisor")
        context = self.context.copy()
        context["divisor"] = 0
        rule = "order_total / divisor > 1"
        result, error = execute_business_rule(rule, context, attrs)
        self.assertFalse(result)
        self.assertIn("Error executing rule", error)
        self.assertIn("division by zero", error)

    def test_execute_missing_context_variable(self):
        # Rule is valid, but the context is missing a variable
        # The variable should evaluate to None or cause an error.
        # In the current implementation, it will cause a NameError during eval.
        rule = "item_count > 0"
        result, error = execute_business_rule(
            rule, self.context, self.allowed_attrs | {"item_count"}
        )
        self.assertFalse(result)
        self.assertIn("Error executing rule", error)
        self.assertIn("is not defined", error)


if __name__ == "__main__":
    unittest.main(verbosity=2)
