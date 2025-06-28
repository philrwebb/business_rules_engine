import Database from 'better-sqlite3';

export class DBFuncs {
  db: Database.Database;
  constructor(dbPath: string) {
    this.db = new Database(dbPath);
    this.initDB();
  }

  initDB() {
    this.db.exec(`
      CREATE TABLE IF NOT EXISTS allowed_attributes (
        name TEXT PRIMARY KEY
      );
      CREATE TABLE IF NOT EXISTS rules (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        event_type TEXT,
        rule TEXT
      );
    `);
  }

  addAttribute(name: string) {
    this.db
      .prepare('INSERT OR IGNORE INTO allowed_attributes (name) VALUES (?)')
      .run(name);
  }

  getAllowedAttributes(): string[] {
    return this.db
      .prepare('SELECT name FROM allowed_attributes')
      .all()
      .map((row: any) => row.name);
  }

  addRule(eventType: string, rule: string) {
    this.db
      .prepare('INSERT INTO rules (event_type, rule) VALUES (?, ?)')
      .run(eventType, rule);
  }

  getRulesForEvent(eventType: string): string[] {
    return this.db
      .prepare('SELECT rule FROM rules WHERE event_type = ?')
      .all(eventType)
      .map((row: any) => row.rule);
  }

  clearRules(eventType?: string) {
    if (eventType) {
      this.db.prepare('DELETE FROM rules WHERE event_type = ?').run(eventType);
    } else {
      this.db.prepare('DELETE FROM rules').run();
    }
  }
}
