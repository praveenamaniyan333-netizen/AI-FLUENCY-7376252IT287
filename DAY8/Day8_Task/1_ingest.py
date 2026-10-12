
"""Day 8 Part A: load, split, embed and store handbook documents."""

import shutil
from pathlib import Path

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from lc_config import DB_DIR, EMBED_PROVIDER, get_vectorstore

DATA_DIR = Path(__file__).resolve().parent / "data"

docs = []

for path in sorted(DATA_DIR.glob("*.md")):
    docs.append(
        Document(
            page_content=path.read_text(encoding="utf-8"),
            metadata={"source": path.name},
        )
    )

print(f"Loaded {len(docs)} documents")

if len(docs) != 6:
    raise ValueError(
        f"Expected 6 Markdown documents, but found {len(docs)}. "
        "Check the data folder."
    )

splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=50,
)

chunks = splitter.split_documents(docs)

print(
    f"Split into {len(chunks)} chunks "
    "(chunk_size=300, overlap=50)"
)

if len(chunks) > 4:
    print(
        "Example chunk ->",
        repr(chunks[4].page_content[:120]),
        chunks[4].metadata,
    )

# Remove the previous database and create a fresh one.
shutil.rmtree(DB_DIR, ignore_errors=True)

store = get_vectorstore()
ids = store.add_documents(chunks)

print(
    f"Stored {len(ids)} vectors in ./{DB_DIR.name} "
    f"using EMBED_PROVIDER={EMBED_PROVIDER}"
)
print(
    "Vector length:",
    len(store.embeddings.embed_query("test")),
)