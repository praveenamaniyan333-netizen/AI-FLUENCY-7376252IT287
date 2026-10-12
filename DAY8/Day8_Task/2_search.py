
"""Day 8 Parts A and C: test retrieval and relevance scores."""

from lc_config import get_vectorstore

# Connect to the existing Chroma vector store
store = get_vectorstore()

# Part A: Test retrieval for different questions
questions = [
    "How much is the late fee for paying fees after the due date?",
    "What time should hostel students return?",
    "Can I write the exam with 70% attendance?",
    "What CGPA do I need to be eligible for placements?",
]

for query in questions:
    print(f"\nQ: {query}")

    # Retrieve the 10 closest chunks for diagnosis
    results = store.similarity_search_with_score(query, k=10)

    for doc, score in results:
        source = doc.metadata.get("source", "unknown")
        print(
            f"  {score:.3f} [{source}] "
            f"{doc.page_content[:100]!r}"
        )

# Part C: Compare a relevant query with an unrelated query
threshold_queries = [
    "What CGPA do I need to be eligible for placements?",
    "What is the capital of France?",
]

for query in threshold_queries:
    print(f"\nThreshold evidence: {query}")

    results = store.similarity_search_with_score(query, k=10)

    for doc, score in results:
        print(
            f"  {score:.3f} "
            f"[{doc.metadata.get('source', 'unknown')}]"
        )

# Test metadata filtering
print("\nFiltered to library.md:")

library_docs = store.similarity_search(
    "fine for late return",
    k=2,
    filter={"source": "library.md"},
)

for doc in library_docs:
    print(
        " ",
        doc.metadata.get("source", "unknown"),
        "->",
        doc.page_content[:100].replace("\n", " "),
    )

# Diagnostic: verify placement policy chunks exist
print("\nChecking whether placement_policy.md is stored:")

placement_docs = store.get(
    where={"source": "placement_policy.md"}
)

placement_ids = placement_docs.get("ids", [])
placement_contents = placement_docs.get("documents") or []
placement_metadatas = placement_docs.get("metadatas") or []

print("Placement chunks found:", len(placement_ids))

for content, metadata in zip(
    placement_contents,
    placement_metadatas,
):
    print(f"\nSource: {metadata.get('source', 'unknown')}")
    print(content[:300])
