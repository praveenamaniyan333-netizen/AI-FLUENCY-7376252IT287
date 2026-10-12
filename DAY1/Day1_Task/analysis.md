# Analysis - College Library AI Systems

## 1. Introduction

This project demonstrates three different approaches for handling questions related to a college library: a plain chatbot, a rule-based workflow, and an AI agent.

The private library data used in this project contains information about three books:

- PY101 - Python Programming: 4 copies, ₹5 fine per day
- AI202 - Artificial Intelligence: 2 copies, ₹10 fine per day
- DB303 - Database Systems: 5 copies, ₹7 fine per day

The same set of questions was tested on all three systems to compare their behavior.

## 2. Plain Chatbot

The plain chatbot sends the user's question directly to the language model.

It does not have access to the private library database or any external tools. Therefore, when asked about the number of copies or fines, it cannot provide the private library information.

For example, for the question "How many copies of AI202 are available?", the chatbot responds that it does not have access to the private library data.

For a general question such as writing a welcome message, the chatbot can generate an appropriate response.

## 3. Rule-Based Workflow

The rule-based workflow uses predefined Python rules and the library data stored in the program.

It does not depend on the language model to decide what action to perform. The program directly checks the question and applies the appropriate rule.

The workflow can answer questions such as:

- AI202 has 2 available copies.
- The fine for 5 days for AI202 is ₹50.
- DB303 has 3 more copies than AI202.
- It can also provide a predefined welcome message.

This approach gives predictable results because the rules are explicitly defined.

## 4. AI Agent

The AI agent combines a language model with tools.

The agent can decide when it needs to use a tool to answer a question. The tools used in this project are:

- `get_book_details` - retrieves private library information.
- `safe_calculate` - performs arithmetic calculations safely.

For example, when asked for the fine for 5 days for AI202, the agent can first retrieve the fine per day using `get_book_details` and then use `safe_calculate` to calculate the total fine.

The agent also displays the tools it uses, providing a trace of the actions taken to produce the answer.

## 5. Comparison

| Feature | Plain Chatbot | Rule-Based Workflow | AI Agent |
|---|---|---|---|
| Flexibility | High for general questions | Low | High |
| Decision-making | LLM generates response | Fixed Python rules | LLM decides actions |
| Tool usage | No | No | Yes |
| Private-data access | No | Yes | Yes through tools |
| Multi-step tasks | Limited | Only predefined steps | Can perform multiple tool calls |
| Automation | Limited | High for predefined tasks | High |
| Reliability | Depends on model response | Predictable for defined rules | Depends on model and tools |

## 6. Suitability

The plain chatbot is suitable for general conversation and tasks that do not require private data or external tools.

The rule-based workflow is suitable when the required operations are known in advance and predictable results are important.

The AI agent is suitable when a task requires the system to decide which tools to use and perform multiple steps. In this project, the agent can retrieve private library information and perform calculations using tools.

## 7. Conclusion

The three systems demonstrate different levels of capability.

The plain chatbot can generate responses but cannot access the private library data. The rule-based workflow can reliably process predefined library operations using fixed rules. The AI agent combines language-model reasoning with tool usage, allowing it to retrieve private data and perform calculations based on the question.

This comparison shows how adding tools and decision-making capabilities can extend a basic chatbot into a more capable AI agent.