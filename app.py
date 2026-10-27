"""Policy-based model routing demo using provider metadata, not live provider calls."""
from dataclasses import dataclass
from typing import Iterable

@dataclass(frozen=True)
class Model:
    name: str
    input_usd_per_million: float
    output_usd_per_million: float
    latency_ms: int
    capabilities: frozenset[str]
    available: bool = True

def estimate_cost(model: Model, input_tokens: int, output_tokens: int) -> float:
    if input_tokens < 0 or output_tokens < 0:
        raise ValueError("token counts must be non-negative")
    return (input_tokens * model.input_usd_per_million + output_tokens * model.output_usd_per_million) / 1_000_000

def route_request(models: Iterable[Model], *, capabilities: set[str], input_tokens: int,
                  output_tokens: int, max_cost_usd: float, max_latency_ms: int,
                  objective: str = "balanced") -> dict:
    if objective not in {"cost", "latency", "balanced"}:
        raise ValueError("objective must be cost, latency, or balanced")
    candidates = []
    for model in models:
        cost = estimate_cost(model, input_tokens, output_tokens)
        if not model.available or not capabilities.issubset(model.capabilities):
            continue
        if cost > max_cost_usd or model.latency_ms > max_latency_ms:
            continue
        candidates.append((model, cost))
    if not candidates:
        return {"selected": None, "reason": "No available model meets the capability, cost, and latency policy."}
    if objective == "cost":
        chosen, cost = min(candidates, key=lambda pair: (pair[1], pair[0].latency_ms))
    elif objective == "latency":
        chosen, cost = min(candidates, key=lambda pair: (pair[0].latency_ms, pair[1]))
    else:
        max_cost = max((c for _, c in candidates), default=1) or 1
        max_latency = max((m.latency_ms for m, _ in candidates), default=1) or 1
        chosen, cost = min(candidates, key=lambda pair: pair[1]/max_cost + pair[0].latency_ms/max_latency)
    return {"selected": chosen.name, "estimated_cost_usd": round(cost, 8),
            "estimated_latency_ms": chosen.latency_ms, "objective": objective,
            "candidates_considered": len(candidates)}

def models_from_dicts(items: list[dict]) -> list[Model]:
    return [Model(name=x["name"], input_usd_per_million=float(x["input_usd_per_million"]),
        output_usd_per_million=float(x["output_usd_per_million"]), latency_ms=int(x["latency_ms"]),
        capabilities=frozenset(x["capabilities"]), available=bool(x.get("available", True))) for x in items]
