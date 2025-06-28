import * as jsep from 'jsep';
import { Expression } from 'jsep';

// Helper type guards for jsep AST nodes
type IdentifierNode = Expression & { type: 'Identifier'; name?: string };

export class RuleValidator {
  allowedIdentifiers: Set<string>;
  constructor(allowedIdentifiers: string[]) {
    this.allowedIdentifiers = new Set(allowedIdentifiers);
  }

  validate(ast: Expression): void {
    this.walk(ast);
  }

  private walk(node: Expression): void {
    switch (node.type) {
      case 'BinaryExpression':
      case 'LogicalExpression':
        this.walk((node as any).left as Expression);
        this.walk((node as any).right as Expression);
        break;
      case 'UnaryExpression':
        this.walk((node as any).argument as Expression);
        break;
      case 'Identifier': {
        const idNode = node as IdentifierNode;
        if (
          typeof idNode.name !== 'string' ||
          !this.allowedIdentifiers.has(idNode.name)
        ) {
          throw new Error(`Disallowed identifier: ${idNode.name}`);
        }
        break;
      }
      case 'Literal':
        break;
      case 'CallExpression':
        throw new Error('Function calls are not allowed');
      case 'MemberExpression':
        throw new Error('Member expressions are not allowed');
      default:
        throw new Error(`Unsupported AST node: ${node.type}`);
    }
  }
}

export function executeBusinessRule(
  rule: string,
  context: Record<string, any>,
  allowedIdentifiers: string[],
): boolean {
  const ast = jsep.default(rule);
  const validator = new RuleValidator(allowedIdentifiers);
  validator.validate(ast);
  return evalAst(ast, context);
}

function evalAst(node: Expression, context: Record<string, any>): any {
  switch (node.type) {
    case 'BinaryExpression':
      // Handle logical operators parsed as BinaryExpression
      if ((node as any).operator === '&&' || (node as any).operator === '||') {
        return applyLogical(
          (node as any).operator,
          evalAst((node as any).left as Expression, context),
          evalAst((node as any).right as Expression, context),
        );
      }
      return applyOp(
        (node as any).operator,
        evalAst((node as any).left as Expression, context),
        evalAst((node as any).right as Expression, context),
      );
    case 'LogicalExpression':
      return applyLogical(
        (node as any).operator,
        evalAst((node as any).left as Expression, context),
        evalAst((node as any).right as Expression, context),
      );
    case 'UnaryExpression':
      return applyUnary(
        (node as any).operator,
        evalAst((node as any).argument as Expression, context),
      );
    case 'Identifier': {
      const idNode = node as IdentifierNode;
      if (typeof idNode.name !== 'string')
        throw new Error('Invalid identifier');
      return context[idNode.name];
    }
    case 'Literal':
      return (node as any).value;
    default:
      throw new Error(`Unsupported AST node: ${node.type}`);
  }
}

function applyOp(op: string, left: any, right: any): any {
  switch (op) {
    case '==':
      return left == right;
    case '===':
      return left === right;
    case '!=':
      return left != right;
    case '!==':
      return left !== right;
    case '>':
      return left > right;
    case '>=':
      return left >= right;
    case '<':
      return left < right;
    case '<=':
      return left <= right;
    case '+':
      return left + right;
    case '-':
      return left - right;
    case '*':
      return left * right;
    case '/':
      return left / right;
    case '%':
      return left % right;
    case '&&':
      return left && right;
    case '||':
      return left || right;
    default:
      throw new Error(`Unsupported operator: ${op}`);
  }
}

function applyLogical(op: string, left: any, right: any): any {
  switch (op) {
    case '&&':
      return left && right;
    case '||':
      return left || right;
    default:
      throw new Error(`Unsupported logical operator: ${op}`);
  }
}

function applyUnary(op: string, arg: any): any {
  switch (op) {
    case '!':
      return !arg;
    case '+':
      return +arg;
    case '-':
      return -arg;
    default:
      throw new Error(`Unsupported unary operator: ${op}`);
  }
}
