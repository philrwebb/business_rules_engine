import { executeBusinessRule } from './business_rules.js';

describe('Business Rule Engine', () => {
  const allowed = ['amount', 'customerType'];
  it('should allow valid rules', () => {
    expect(executeBusinessRule('amount > 100', { amount: 150 }, allowed)).toBe(
      true,
    );
    expect(executeBusinessRule('amount < 100', { amount: 50 }, allowed)).toBe(
      true,
    );
    expect(
      executeBusinessRule(
        'customerType === "VIP"',
        { customerType: 'VIP' },
        allowed,
      ),
    ).toBe(true);
  });
  it('should reject disallowed identifiers', () => {
    expect(() =>
      executeBusinessRule('foo > 100', { foo: 1 }, allowed),
    ).toThrow();
  });
  it('should reject function calls', () => {
    expect(() => executeBusinessRule('alert(1)', {}, allowed)).toThrow();
  });
});
