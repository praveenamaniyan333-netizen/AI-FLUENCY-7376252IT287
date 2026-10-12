
"""
Day 4 Task: Context Length and Quantization Observation

Section 3.3 requires:
- Four context-length settings with quantization fixed.
- Four quantization settings with context fixed.
- Weights, KV cache, total memory, and fit verdict.
"""

from memory_estimator import estimate_memory


# Available memory budget.
AVAILABLE_MEMORY_GB = 16.0
RUNTIME_OVERHEAD_GB = 1.0

# Illustrative model architecture.
# Replace these with verified details for your chosen model.
MODEL_NAME = "Example 3B"
PARAMS_B = 3.0
LAYERS = 28
KV_HEADS = 4
HEAD_DIM = 96

# Keep quantization fixed while changing context.
FIXED_QUANTIZATION = "Q4_K_M"
CONTEXT_VALUES = [1024, 2048, 4096, 8192]

# Keep context fixed while changing quantization.
FIXED_CONTEXT = 4096
QUANTIZATION_VALUES = [
    "Q2_K",
    "Q3_K_M",
    "Q4_K_M",
    "Q8_0",
]


def print_row(setting, value, precision, context):
    result = estimate_memory(
        params_b=PARAMS_B,
        precision=precision,
        context_tokens=context,
        layers=LAYERS,
        kv_heads=KV_HEADS,
        head_dim=HEAD_DIM,
        available_memory_gb=AVAILABLE_MEMORY_GB,
        runtime_overhead_gb=RUNTIME_OVERHEAD_GB,
    )

    print(
        f"{setting:<34}"
        f"{str(value):<16}"
        f"{result['weights_gb']:>12.3f}"
        f"{result['kv_cache_gb']:>12.4f}"
        f"{result['total_gb']:>12.3f}"
        f"{'YES' if result['fits'] else 'NO':>8}"
    )


def main():
    print(f"Model: {MODEL_NAME}")
    print(
        f"Available memory: "
        f"{AVAILABLE_MEMORY_GB:.1f} GB"
    )

    print(
        "These are estimates, not actual "
        "Ollama measurements."
    )

    print()

    print(
        f"{'Setting changed':<34}"
        f"{'Value used':<16}"
        f"{'Weights GB':>12}"
        f"{'KV cache GB':>12}"
        f"{'Total GB':>12}"
        f"{'Fits?':>8}"
    )

    print("-" * 94)

    # Experiment 1: vary context length.
    print("\nCONTEXT LENGTH EXPERIMENT")

    for context in CONTEXT_VALUES:
        print_row(
            "Context (same quantization)",
            context,
            FIXED_QUANTIZATION,
            context,
        )

    # Experiment 2: vary quantization.
    print("\nQUANTIZATION EXPERIMENT")

    for precision in QUANTIZATION_VALUES:
        print_row(
            "Quantization (same context)",
            precision,
            precision,
            FIXED_CONTEXT,
        )

    print("\nOBSERVATIONS")
    print(
        "1. With quantization fixed, weights remain "
        "constant as context changes."
    )
    print(
        "2. KV cache grows with context length."
    )
    print(
        "3. With context fixed, changing quantization "
        "changes estimated weight memory."
    )
    print(
        "4. KV cache remains constant in this estimate "
        "when architecture, context, and cache precision "
        "remain unchanged."
    )
    print(
        "5. Lower-bit quantization saves memory but "
        "may reduce model output quality."
    )
    print(
        "6. Select a context that fits with a practical "
        "memory safety margin."
    )


if __name__ == "__main__":
    main()