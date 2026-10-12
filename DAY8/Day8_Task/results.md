# Day 8 Lab Results

## 1. Model Configuration

| Setting | Value |
|---|---|
| LLM Provider | Groq |
| LLM Model | `openai/gpt-oss-120b` |
| Embedding Provider | `hash` |
| Embedding Dimensions | 256 |
| Vector Store | Chroma |
| Collection Name | `college_handbook` |
| Maximum Distance | `0.9` (configured value to verify in `task_agent.py`) |

## 2. Document Ingestion

- Six handbook documents were loaded.
- A total of 27 chunks were stored in the Chroma vector store.
- Chunk size: 300 characters.
- Chunk overlap: 50 characters.
- The `placement_policy.md` document was successfully stored as three chunks.

## 3. Retrieval and Distance Score Tests

| Query | Relevant Document | Best Relevant Distance | Result |
|---|---|---:|---|
| How much is the late fee for paying fees after the due date? | `fee_policy.md` | 0.370 | Relevant content retrieved |
| What time should hostel students return? | `hostel_rules.md` | 0.716 | Relevant content retrieved |
| Can I write the exam with 70% attendance? | `exam_regulations.md` | 0.614 | Relevant content retrieved |
| What CGPA do I need to be eligible for placements? | `placement_policy.md` | 0.838 | Relevant content retrieved |
| What is the capital of France? | No relevant document | 0.490 for the closest returned chunk | Unrelated content returned by retrieval |

**Observation:** Lower cosine distance indicates a closer match. The hash embedding retrieval results do not reliably separate relevant and irrelevant queries using a single distance threshold. For example, the placement query's relevant chunk has a distance of 0.838, while the unrelated France query returns a chunk with a distance of 0.490.

## 4. Handbook Filtering Test

- Filter used: `source = library.md`
- Result: Only chunks from `library.md` were returned.
- Status: Passed.

## 5. Exam Eligibility Tool Test

| Attendance | Expected Tool Result | Status |
|---:|---|---|
| 82% | Eligible to write the exam | Passed |
| 70% | Condonation of Rs. 500 per course | Passed |
| 50% | Not eligible to write the exam | Passed |
| 120% | Error: Attendance must be between 0 and 100 | Passed |

## 6. Agent Question Results

| No. | Question | Tools Called | Answer / Result | Correct |
|---:|---|---|---|---|
| 1 | What CGPA do I need to be eligible for placements? | `search_handbook` | CGPA of 6.5 or above and no standing arrears | Yes |
| 2 | My attendance is 70%. Can I write the exam? | `check_exam_eligibility` | Condonation available for Rs. 500 per course | Yes |
| 3 | What is the total of the CS101 fee, the AI202 fee and the maximum late fee? | `get_course_fee` × 2, `search_handbook`, `calculator` | Rs. 32,000 | Yes |
| 4 | And if I pay only 5 days late instead? | `search_handbook`, `calculator` | Rs. 30,500 | Yes |
| 5 | What is the capital of France? | No tools called | "I don't know. This is not covered in the college handbook." | Answer correct; verify required tool behavior |

## 7. Observations and Conclusion

1. The ingestion script stored all six documents and 27 chunks.
2. Handbook retrieval returned relevant information for the late-fee, hostel, attendance and placement questions.
3. The source filter for `library.md` worked correctly.
4. The exam eligibility tool handled eligible, condonation, ineligible and invalid attendance values.
5. The agent produced the expected answers for all five questions, including the expected totals of Rs. 32,000 and Rs. 30,500.
6. The France question received the required refusal response. However, no tool was called, so verify whether the task requires `search_handbook` to return `NO_MATCH`.
7. Distance thresholding alone is insufficient to distinguish relevant from irrelevant results with the current hash embeddings.

**Overall status:** The ingestion, retrieval, filtering and tool tests ran successfully. The agent's five final answers matched the expected answers. The distance-threshold and Question 5 tool-call behavior should be reviewed before final submission.