using BusinessRulesEngine;
using System.Collections.Generic;
using Xunit;

namespace Tests
{
    public class RuleEvaluatorTests
    {
        [Fact]
        public void Evaluate_ShouldReturnTrue_WhenRuleIsTrue()
        {
            // Arrange
            var rule = "user_role == \"admin\"";
            var data = new Dictionary<string, object> { { "user_role", "admin" } };

            // Act
            var result = RuleEvaluator.Evaluate(rule, data);

            // Assert
            Assert.True(result);
        }

        [Fact]
        public void Evaluate_ShouldReturnFalse_WhenRuleIsFalse()
        {
            // Arrange
            var rule = "user_role == \"admin\"";
            var data = new Dictionary<string, object> { { "user_role", "guest" } };

            // Act
            var result = RuleEvaluator.Evaluate(rule, data);

            // Assert
            Assert.False(result);
        }

        [Fact]
        public void Evaluate_ShouldHandleComplexRules()
        {
            // Arrange
            var rule = "user_role == \"gold\" and purchase_total > 100";
            var data = new Dictionary<string, object>
            {
                { "user_role", "gold" },
                { "purchase_total", 150 }
            };

            // Act
            var result = RuleEvaluator.Evaluate(rule, data);

            // Assert
            Assert.True(result);
        }

        [Fact]
        public void Evaluate_ShouldReturnFalse_ForInvalidRule()
        {
            // Arrange
            var rule = "invalid rule";
            var data = new Dictionary<string, object>();

            // Act
            var result = RuleEvaluator.Evaluate(rule, data);

            // Assert
            Assert.False(result);
        }
    }
}
