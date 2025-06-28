import { DBFuncs } from './db_funcs.js';
import fs from 'fs';

describe('DBFuncs', () => {
  const dbPath = 'test_rules.db';
  let db: DBFuncs;
  beforeEach(() => {
    if (fs.existsSync(dbPath)) fs.unlinkSync(dbPath);
    db = new DBFuncs(dbPath);
  });
  afterEach(() => {
    if (fs.existsSync(dbPath)) fs.unlinkSync(dbPath);
  });
  it('should add and get allowed attributes', () => {
    db.addAttribute('foo');
    expect(db.getAllowedAttributes()).toContain('foo');
  });
  it('should add and get rules', () => {
    db.addRule('event', 'foo > 1');
    expect(db.getRulesForEvent('event')).toContain('foo > 1');
  });
  it('should clear rules', () => {
    db.addRule('event', 'foo > 1');
    db.clearRules('event');
    expect(db.getRulesForEvent('event')).toHaveLength(0);
  });
});
