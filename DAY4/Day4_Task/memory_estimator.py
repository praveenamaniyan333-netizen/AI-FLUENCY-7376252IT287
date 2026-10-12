
"""
Day 4 Task: Memory Estimator

Estimates:
1. Model weights memory
2. KV cache memory
3. Total memory including runtime overhead
4. Whether the model fits in available memory

Memory formula:
Weights = Parameters x Bytes per parameter

KV cache =
2 x Layers x KV heads x Head dimension
x Context tokens x Cache bytes

Total = Weights + KV cache + Runtime overhead

GB uses decimal units:
1 GB = 1,000,000,000 bytes
"""

BYTES_PER_PARAMETER = {
    "FP32": 4.0,
    "FP16": 2.0,
    "BF16": 2.0,
    "Q8_0": 8.5 / 8.0,
    "Q6_K": 6.6 / 8.0,
    "Q5_K_M": 5.7 / 8.0,
    "Q4_K_M": 4.89 / 8.0,
    "Q4": 0.5,
    "Q3_K_M": 3.9 / 8.0,
    "Q2_K": 3.35 / 8.0,
}


def estimate_memory(
    params_b,
    precision,
    context_tokens,
    layers,
    kv_heads,
    head_dim,
    available_memory_gb,
    runtime_overhead_gb=1.0,
    cache_bytes=2.0,
):
    """Calculate memory estimates and return a fit verdict."""

    if precision not in BYTES_PER_PARAMETER:
        raise ValueError(
            f"Unknown precision: {precision}. "
            f"Choose from {list(BYTES_PER_PARAMETER)}"
        )

    if (
        params_b <= 0
        or context_tokens <= 0
        or layers <= 0
        or kv_heads <= 0
        or head_dim <= 0
        or available_memory_gb <= 0
    ):
        raise ValueError("Model and memory inputs must be positive.")

    if runtime_overhead_gb < 0 or cache_bytes <= 0:
        raise ValueError(
            "Runtime overhead cannot be negative, "
            "and cache bytes must be positive."
        )

    # Estimate model weights.
    weights_gb = (
        params_b * BYTES_PER_PARAMETER[precision]
    )

    # Estimate KV cache.
    kv_bytes = (
        2
        * layers
        * kv_heads
        * head_dim
        * context_tokens
        * cache_bytes
    )

    kv_cache_gb = kv_bytes / 1_000_000_000

    # Estimate total memory.
    total_gb = (
        weights_gb
        + kv_cache_gb
        + runtime_overhead_gb
    )

    fits = total_gb <= available_memory_gb

    return {
        "weights_gb": weights_gb,
        "kv_cache_gb": kv_cache_gb,
        "overhead_gb": runtime_overhead_gb,
        "total_gb": total_gb,
        "fits": fits,
    }


def main():
    # Scenario: local coding helper.
    # Available memory budget: 16 GB.
    available_memory_gb = 16.0
    runtime_overhead_gb = 1.0

    # Illustrative architecture values.
    # Replace these with verified values for your chosen model.
    configurations = [
        {
            "model": "Example 3B",
            "params_b": 3.0,
            "precision": "Q4_K_M",
            "context": 2048,
            "layers": 28,
            "kv_heads": 4,
            "head_dim": 96,
        },
        {
            "model": "Example 3B",
            "params_b": 3.0,
            "precision": "Q4_K_M",
            "context": 8192,
            "layers": 28,
            "kv_heads": 4,
            "head_dim": 96,
        },
        {
            "model": "Example 3B",
            "params_b": 3.0,
            "precision": "Q8_0",
            "context": 4096,
            "layers": 28,
            "kv_heads": 4,
            "head_dim": 96,
        },
        {
            "model": "Example 3B",
            "params_b": 3.0,
            "precision": "FP16",
            "context": 4096,
            "layers": 28,
            "kv_heads": 4,
            "head_dim": 96,
        },
    ]

    print(
        f"Available memory: "
        f"{available_memory_gb:.2f} GB"
    )

    print(
        "Total memory includes the configured "
        "runtime overhead."
    )

    print("-" * 105)

    print(
        f"{'Model':<16}"
        f"{'Params(B)':>10}"
        f"{'Precision':>12}"
        f"{'Context':>10}"
        f"{'Weights(GB)':>13}"
        f"{'KV(GB)':>10}"
        f"{'Total(GB)':>12}"
        f"{'Fits?':>8}"
    )

    print("-" * 105)

    for item in configurations:
        result = estimate_memory(
            params_b=item["params_b"],
            precision=item["precision"],
            context_tokens=item["context"],
            layers=item["layers"],
            kv_heads=item["kv_heads"],
            head_dim=item["head_dim"],
            available_memory_gb=available_memory_gb,
            runtime_overhead_gb=runtime_overhead_gb,
        )

        print(
            f"{item['model']:<16}"
            f"{item['params_b']:>10.2f}"
            f"{item['precision']:>12}"
            f"{item['context']:>10}"
            f"{result['weights_gb']:>13.2f}"
            f"{result['kv_cache_gb']:>10.3f}"
            f"{result['total_gb']:>12.2f}"
            f"{'YES' if result['fits'] else 'NO':>8}"
        )


if __name__ == "__main__":
    main()