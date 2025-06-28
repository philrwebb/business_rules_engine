import { DBFuncs } from './db_funcs.js';
import { executeBusinessRule } from './business_rules.js';

const db = new DBFuncs('business_rules.db');

// Only seed if the DB is empty
if (
  db.getAllowedAttributes().length === 0 &&
  db.getRulesForEvent('order').length === 0
) {
  db.addAttribute('amount');
  db.addAttribute('customerType');
  db.addRule('order', 'amount > 100 && customerType === "VIP"');
  db.addRule('order', 'amount <= 100 && customerType === "Regular"');
}

const eventContext = { amount: 150, customerType: 'VIP' };
const allowed = db.getAllowedAttributes();
const rules = db.getRulesForEvent('order');

for (const rule of rules) {
  try {
    const result = executeBusinessRule(rule, eventContext, allowed);
    console.log(`Rule: ${rule} => ${result}`);
  } catch (e) {
    console.error(`Rule: ${rule} => ERROR: ${(e as Error).message}`);
  }
}
