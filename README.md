# LLM Cost Optimization Gateway

A policy-based routing prototype that estimates request cost and selects a model from a catalog using required capabilities, cost ceilings, latency ceilings, and a routing objective.

## Included
- Token-based cost estimation using configured per-million-token rates.
- Capability, availability, cost, and latency filtering.
- Cost-first, latency-first, and normalized balanced selection policies.
- Explicit no-candidate response rather than silently bypassing policy.
- Unit tests and a synthetic model catalog.

## Important boundary
This repository does **not** call model providers, measure live latency, tokenize prompts, or verify current pricing. Model metadata is supplied by you and should be refreshed from provider contracts before any real routing decision. The balanced objective is a simple demo heuristic, not a universal optimization function.

## Quick start
Requires Python 3.10+.

```bash
python - <<'PY'
import json
from app import models_from_dicts, route_request
models = models_from_dicts(json.load(open("examples/models.json", encoding="utf-8")))
print(route_request(models, capabilities={"chat"}, input_tokens=1200, output_tokens=300,
                    max_cost_usd=0.02, max_latency_ms=1000, objective="balanced"))
PY
```

## Tests
`python -m unittest discover -s tests -v`

## Before production
Add provider adapters, retries and timeouts, streaming support, per-tenant budgets, secret management, rate limiting, live telemetry, pricing refresh, and fallback tests. Never log prompts or credentials by default.

## Explore more

- [AI Lead Qualification Agent](https://github.com/HardikPaghdar/ai-lead-qualification-agent) — transparent rule-based lead triage.
- [Production RAG Pipeline](https://github.com/HardikPaghdar/production-rag-pipeline) — retrieval, reranking, citations, and evaluation.
- [More projects on my portfolio](https://hardikpaghdar.netlify.app/).
