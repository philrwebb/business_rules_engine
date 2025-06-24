using System;
using System.Collections.Generic;
using System.Linq;
using System.Linq.Dynamic.Core;
using System.Linq.Expressions;

namespace BusinessRulesEngine
{
    public static class RuleEvaluator
    {
        public static bool Evaluate(string rule, Dictionary<string, object> data)
        {
            try
            {
                var parameterExpressions = data.Keys.Select(key => Expression.Parameter(data[key].GetType(), key)).ToArray();
                var lambda = DynamicExpressionParser.ParseLambda(parameterExpressions, typeof(bool), rule);

                var values = data.Values.ToArray();
                var result = lambda.Compile().DynamicInvoke(values);
                return (bool)(result ?? false);
            }
            catch (Exception)
            {
                return false;
            }
        }
    }
}
