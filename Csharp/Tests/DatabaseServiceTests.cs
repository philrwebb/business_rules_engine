using BusinessRulesEngine;
using Dapper;
using Microsoft.Data.Sqlite;
using System;
using System.Collections.Generic;
using System.Linq;
using Xunit;

namespace Tests
{
    public class DatabaseServiceTests : IDisposable
    {
        private readonly IDatabaseService _dbService;
        private readonly SqliteConnection _masterConnection;

        public DatabaseServiceTests()
        {
            var connectionString = "Data Source=SharedInMemory;Mode=Memory;Cache=Shared";
            _masterConnection = new SqliteConnection(connectionString);
            _masterConnection.Open();

            _dbService = new DatabaseService(connectionString);
            _dbService.InitDb();
        }

        public void Dispose()
        {
            _masterConnection.Close();
            _masterConnection.Dispose();
            GC.SuppressFinalize(this);
        }

        [Fact]
        public void AddRule_And_GetRules_ShouldWork()
        {
            // Arrange
            _dbService.AddRule("test_event", "true", "test_action");

            // Act
            var rules = _dbService.GetRules("test_event");

            // Assert
            Assert.Single(rules);
            Assert.Equal("test_event", rules[0].EventType);
            Assert.Equal("true", rules[0].Rule);
            Assert.Equal("test_action", rules[0].Action);
        }

        [Fact]
        public void ClearRules_ShouldRemoveAllRulesForAnEventType()
        {
            // Arrange
            _dbService.AddRule("event1", "true", "action1");
            _dbService.AddRule("event2", "false", "action2");

            // Act
            _dbService.ClearRules("event1");

            // Assert
            Assert.Empty(_dbService.GetRules("event1"));
            Assert.NotEmpty(_dbService.GetRules("event2"));
        }

        [Fact]
        public void ClearRules_ShouldRemoveAllRulesWhenNoEventTypeIsProvided()
        {
            // Arrange
            _dbService.AddRule("event1", "true", "action1");
            _dbService.AddRule("event2", "false", "action2");

            // Act
            _dbService.ClearRules();

            // Assert
            Assert.Empty(_dbService.GetRules("event1"));
            Assert.Empty(_dbService.GetRules("event2"));
        }

        [Fact]
        public void InitDb_WithAllowedAttributes_ShouldPopulateTable()
        {
            // Arrange
            var allowedAttributes = new List<string> { "attr1", "attr2" };

            // Act
            _dbService.InitDb(allowedAttributes);

            // Assert
            using (var connection = new SqliteConnection(_masterConnection.ConnectionString))
            {
                connection.Open();
                var attributes = connection.Query<string>("SELECT attribute FROM allowed_attributes").ToList();
                Assert.Equal(2, attributes.Count);
                Assert.Contains("attr1", attributes);
                Assert.Contains("attr2", attributes);
            }
        }
    }
}
