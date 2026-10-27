import unittest
from app import Model, estimate_cost, route_request

MODELS = [Model("cheap", .2, .4, 800, frozenset({"chat"})),
          Model("fast", 1, 2, 100, frozenset({"chat","json"})),
          Model("offline", .1, .1, 50, frozenset({"chat"}), False)]

class GatewayTests(unittest.TestCase):
    def test_cost_estimate(self):
        self.assertAlmostEqual(estimate_cost(MODELS[0], 1000, 500), .0004)
    def test_capability_and_policy_filtering(self):
        result = route_request(MODELS, capabilities={"json"}, input_tokens=1000, output_tokens=500,
                               max_cost_usd=1, max_latency_ms=500)
        self.assertEqual(result["selected"], "fast")
    def test_no_candidate_is_explicit(self):
        result = route_request(MODELS, capabilities={"vision"}, input_tokens=1, output_tokens=1,
                               max_cost_usd=1, max_latency_ms=5000)
        self.assertIsNone(result["selected"])
    def test_negative_tokens_rejected(self):
        with self.assertRaises(ValueError): estimate_cost(MODELS[0], -1, 0)

if __name__ == "__main__": unittest.main()
