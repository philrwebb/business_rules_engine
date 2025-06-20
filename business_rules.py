import ast

SAFE_GLOBALS: dict[str, object] = {
    "len": len,
    "print": print,
    # Add any safe built-ins you want to allow, e.g.:
    # "len": len,
}

SAFE_NODE_TYPES = {
    ast.Expression,
    ast.Compare,
    ast.BinOp,
    ast.UnaryOp,
    ast.BoolOp,
    ast.Constant,
    ast.Name,
    ast.Load,
    ast.And,
    ast.Or,
    ast.Not,
    ast.Eq,
    ast.NotEq,
    ast.Lt,
    ast.LtE,
    ast.Gt,
    ast.GtE,
    ast.In,
    ast.NotIn,
    ast.Add,
    ast.Sub,
    ast.Mult,
    ast.Div,
    ast.Mod,
    ast.Pow,
    ast.USub,
    ast.UAdd,
    ast.Tuple,
    ast.List,
}


class RuleValidator(ast.NodeVisitor):
    def __init__(
        self, allowed_attribute_names, allowed_node_types, allowed_call_names=None
    ):
        self.allowed_attribute_names = set(allowed_attribute_names)
        self.allowed_node_types = set(allowed_node_types)
        self.allowed_call_names = (
            set(allowed_call_names) if allowed_call_names else set()
        )
        self.is_valid = True
        self.errors = []

    def generic_visit(self, node):
        if type(node) not in self.allowed_node_types:
            self.is_valid = False
            self.errors.append(
                f"Disallowed node type: {type(node).__name__} at line {getattr(node, 'lineno', 'N/A')}"
            )
            return
        super().generic_visit(node)

    def visit_Name(self, node: ast.Name):
        if (
            node.id not in self.allowed_attribute_names
            and node.id not in SAFE_GLOBALS
            and node.id not in ["True", "False", "None"]
        ):
            self.is_valid = False
            self.errors.append(
                f"Disallowed attribute/variable: '{node.id}' at line {node.lineno}"
            )

    def visit_Call(self, node: ast.Call):
        if isinstance(node.func, ast.Name):
            if node.func.id not in self.allowed_call_names:
                self.is_valid = False
                self.errors.append(
                    f"Disallowed function call: '{node.func.id}' at line {node.lineno}"
                )
        else:
            self.is_valid = False
            self.errors.append(
                f"Disallowed complex function call target at line {node.lineno}"
            )
        super().generic_visit(node)

    def visit_Attribute(self, node: ast.Attribute):
        self.is_valid = False
        self.errors.append(
            f"Disallowed attribute access ('.') at line {node.lineno}. Only direct system attributes are allowed."
        )


def execute_business_rule(
    rule_str: str, current_context_values: dict, allowed_attributes: set
) -> tuple[bool, str | None]:
    """
    Parses, validates, and executes a single business rule string.
    allowed_attributes: A set of attribute names that are permitted in the rule.
    Returns: (bool_result, error_message_or_None)
    """
    try:
        rule_ast = ast.parse(rule_str, mode="eval")
    except SyntaxError as e:
        return False, f"Syntax error in rule: {e}"

    validator = RuleValidator(allowed_attributes, SAFE_NODE_TYPES)
    validator.visit(rule_ast)

    if not validator.is_valid:
        return False, f"Invalid rule: {'; '.join(validator.errors)}"

    try:
        compiled_rule = compile(rule_ast, "<user_rule>", "eval")

        execution_locals = {
            k: v for k, v in current_context_values.items() if k in allowed_attributes
        }
        execution_globals = SAFE_GLOBALS.copy()

        result = eval(compiled_rule, execution_globals, execution_locals)
        return bool(result), None
    except Exception as e:
        return False, f"Error executing rule: {e} (Context: {execution_locals})"
