using Dapper;
using Microsoft.Data.Sqlite;
using System.Collections.Generic;
using System.Linq;

namespace BusinessRulesEngine
{
    public class DatabaseService : IDatabaseService
    {
        private readonly string _connectionString;

        public DatabaseService(string connectionString)
        {
            _connectionString = connectionString;
        }

        public void InitDb(List<string>? allowedAttributes = null)
        {
            using (var connection = new SqliteConnection(_connectionString))
            {
                connection.Open();

                var tableCommand = """
                CREATE TABLE IF NOT EXISTS business_rules (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_type TEXT NOT NULL,
                    rule TEXT NOT NULL,
                    action TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS allowed_attributes (
                    attribute TEXT PRIMARY KEY
                );
                """;
                connection.Execute(tableCommand);

                if (allowedAttributes != null)
                {
                    var existingAttributes = connection.Query<string>("SELECT attribute FROM allowed_attributes").ToList();
                    var newAttributes = allowedAttributes.Except(existingAttributes);
                    foreach (var attribute in newAttributes)
                    {
                        connection.Execute("INSERT INTO allowed_attributes (attribute) VALUES (@attribute)", new { attribute });
                    }
                }
            }
        }

        public void AddRule(string eventType, string rule, string action)
        {
            using (var connection = new SqliteConnection(_connectionString))
            {
                connection.Open();
                connection.Execute("INSERT INTO business_rules (event_type, rule, action) VALUES (@eventType, @rule, @action)",
                    new { eventType, rule, action });
            }
        }

        public List<BusinessRule> GetRules(string eventType)
        {
            using (var connection = new SqliteConnection(_connectionString))
            {
                connection.Open();
                return connection.Query<BusinessRule>("SELECT id, event_type as EventType, rule, action FROM business_rules WHERE event_type = @eventType", new { eventType }).ToList();
            }
        }

        public void ClearRules(string? eventType = null)
        {
            using (var connection = new SqliteConnection(_connectionString))
            {
                connection.Open();
                if (eventType != null)
                {
                    connection.Execute("DELETE FROM business_rules WHERE event_type = @eventType", new { eventType });
                }
                else
                {
                    connection.Execute("DELETE FROM business_rules");
                }
            }
        }
    }
}
