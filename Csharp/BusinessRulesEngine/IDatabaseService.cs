using System.Collections.Generic;

namespace BusinessRulesEngine
{
    public interface IDatabaseService
    {
        void InitDb(List<string>? allowedAttributes = null);
        void AddRule(string eventType, string rule, string action);
        List<BusinessRule> GetRules(string eventType);
        void ClearRules(string? eventType = null);
    }
}
