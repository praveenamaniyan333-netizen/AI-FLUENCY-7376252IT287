# Day 3 - From Prompt to Action: Understanding LLMs, Tools, and Agents

## 1. Scenario

For this task, I selected a library book availability scenario.

The library contains the following books:

- PY101 - Python Programming - 4 copies
- AI202 - Artificial Intelligence - 2 copies
- DB303 - Database Systems - 5 copies

The purpose of this scenario is to compare a plain LLM prompt with the same LLM when it has access to one external tool.

The current library stock is information that the LLM cannot reliably know from its own trained knowledge. Therefore, the `lookup_book` tool is provided to obtain the current library information.

The three questions used in the experiment were:

1. What is a variable in Python?
2. What is the current number of available copies of AI202 in our library?
3. What is the purpose of a database?

Questions 1 and 3 are general knowledge questions, while Question 2 requires current information from the library.

---

## 2. Explanation of Concepts

### 2.1 What is a Large Language Model?

A Large Language Model (LLM) is a model trained on a large amount of text that can understand and generate natural language.

In this scenario, the LLM can answer general knowledge questions such as:

"What is a variable in Python?"

It can answer this using its learned knowledge.

However, the LLM does not automatically know the current number of copies available in our library. When asked:

"What is the current number of available copies of AI202 in our library?"

the plain LLM correctly stated that it did not have access to the library's current information instead of inventing a number.

This shows that a plain LLM can be useful for general knowledge but cannot automatically access new external information.

---

### 2.2 What is an Agent?

An agent is an LLM-based system that can use tools or take actions to complete a task.

A plain chat response generates an answer directly from the model.

An agent can identify that additional information is required, select an appropriate tool, call that tool, receive its result, and then use the result to produce the final answer.

In this scenario, the tool-enabled LLM recognised that the current availability of AI202 required information from the library and called the `lookup_book` tool.

---

### 2.3 What is a Tool and a Tool Call?

A tool is an external function that an LLM can use to obtain information or perform an operation.

The tool used in this project is:

`lookup_book`

The tool schema describes the tool to the model. It contains:

- The name of the tool
- A description of what the tool does
- The parameters required by the tool

The model needs this information so that it can understand when the tool is useful and what information it must provide when calling it.

For example, when the user asks about the current availability of AI202, the model can decide to call:

`lookup_book("AI202")`

A tool call is the request made by the model to execute the external function.

---

### 2.4 Step-by-Step Tool Call Flow

The tool call in this project follows these steps:

1. The user asks for the current number of available copies of AI202.
2. The LLM receives the question.
3. The LLM determines that current library information is required.
4. The LLM selects the `lookup_book` tool.
5. The LLM provides `AI202` as the tool parameter.
6. The tool checks the library data.
7. The tool returns the result.
8. The result is sent back to the LLM.
9. The LLM uses the tool result to produce the final answer.

The actual tool call in the experiment was:

`lookup_book({"book_code":"AI202"})`

The tool returned:

- Book: Artificial Intelligence
- Code: AI202
- Copies available: 2
- Available: Yes

The final answer was that there are 2 copies of AI202 available in the library.

---

### 2.5 Why Should a Tool Return Its Result as Plain Text?

A tool should return its result as plain text even when something goes wrong.

For example, if an unknown book code is requested, the tool can return a message such as:

"Book code XYZ999 was not found in the library."

The LLM can then understand the result and provide an appropriate response.

Returning a text result allows the model to receive information from the tool and continue the interaction instead of stopping the whole program because of an error.

---

## 3. Comparison Table

| Basis for comparison | Plain LLM prompt | LLM with one tool |
|---|---|---|
| Source of the answer | The model's trained knowledge | The model's knowledge plus the external tool |
| Can it fetch or compute information outside its own memory? | No | Yes, through the available tool |
| Reliability on factual or numeric questions | Suitable for general knowledge, but cannot reliably know current library information | More reliable when the required current information is available through the tool |
| Transparency | The generated answer does not involve an external operation | The tool call and tool result can be recorded |
| Speed / cost of getting an answer | No additional tool execution is required | Requires an additional tool call when the tool is needed |

---

## 4. Observations

### Question 1: What is a variable in Python?

#### Plain LLM

The plain LLM answered the question directly using its own knowledge.

It did not need access to the library tool.

#### Tool-enabled LLM

The tool-enabled LLM also answered the question without calling the `lookup_book` tool.

#### Observation

The tool was unnecessary because this was a general knowledge question.

---

### Question 2: What is the current number of available copies of AI202 in our library?

#### Plain LLM

The plain LLM stated that it did not have information about the library's current holdings.

It did not invent a number.

#### Tool-enabled LLM

The tool-enabled LLM called:

`lookup_book({"book_code":"AI202"})`

The tool returned:

`Copies available: 2`

The LLM then used the tool result and answered that there are 2 copies of AI202 available in the library.

#### Observation

This question genuinely required the external tool because the current library information was not available from the LLM's own knowledge.

---

### Question 3: What is the purpose of a database?

#### Plain LLM

The plain LLM answered the question using its own knowledge.

#### Tool-enabled LLM

The tool-enabled LLM answered the question without calling the library tool.

#### Observation

The tool was unnecessary because the question could be answered using general knowledge.

---

## 5. Suitability

The plain LLM was sufficient for questions involving general knowledge, such as the meaning of a Python variable and the purpose of a database.

However, the external tool became necessary for the question about the current number of available copies of AI202. The LLM itself did not have access to the library's current information, while the tool could retrieve it.

Therefore, a tool is not required for every question. It becomes useful when the task requires information or an operation that is outside the LLM's available knowledge.

---

## 6. Conclusion

This experiment demonstrated the difference between a plain LLM and an LLM with access to one external tool.

The plain LLM could answer general knowledge questions directly. When asked for current library information, it did not have access to that information and therefore could not provide a reliable number.

After providing the `lookup_book` tool, the LLM could recognise when the tool was necessary, call it with the correct book code, receive the result, and use that result in its final answer.

The experiment therefore shows that a plain LLM can be sufficient for many general knowledge and language tasks, while an external tool is useful when a problem requires current external information or an operation that the model cannot reliably perform on its own.