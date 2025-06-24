using BusinessRulesEngine;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using System;
using System.Collections.Generic;

namespace App
{
    class Program
    {
        static void Main(string[] args)
        {
            var host = CreateHostBuilder(args).Build();
            var serviceProvider = host.Services;

            var dbService = serviceProvider.GetRequiredService<IDatabaseService>();

            // Initialize the database
            var allowedAttributes = new List<string> { "user_role", "purchase_total", "item_category" };
            dbService.InitDb(allowedAttributes);

            // Clear existing rules for a clean run
            dbService.ClearRules();

            // Add some business rules
            dbService.AddRule("purchase", "user_role == \"gold\" and purchase_total > 100", "apply_10_percent_discount");
            dbService.AddRule("purchase", "item_category == \"electronics\"", "offer_extended_warranty");

            Console.WriteLine("Business rules loaded.");

            // Simulate a purchase event
            var purchaseData = new Dictionary<string, object>
            {
                { "user_role", "gold" },
                { "purchase_total", 150 },
                { "item_category", "books" }
            };

            Console.WriteLine("\nEvaluating rules for a purchase...");
            var rules = dbService.GetRules("purchase");
            foreach (var rule in rules)
            {
                if (rule.Rule is not null)
                {
                    // Correctly pass parameters to the evaluator
                    var parameters = new[] { new KeyValuePair<string, object>("data", purchaseData) };
                    bool result = RuleEvaluator.Evaluate(rule.Rule, purchaseData);
                    Console.WriteLine($"Rule: {rule.Rule}, Action: {rule.Action}, Result: {result}");
                }
            }
        }

        static IHostBuilder CreateHostBuilder(string[] args)
        {
            return Host.CreateDefaultBuilder(args)
                .ConfigureServices((_, services) =>
                {
                    services.AddSingleton<IDatabaseService>(new DatabaseService("Data Source=csharp_business_rules.db"));
                });
        }
    }
}
