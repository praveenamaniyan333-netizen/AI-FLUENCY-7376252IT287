# Day 2 Analysis
## Reasoning and Acting: Direct Prompting, Chain-of-Thought, and ReAct

## 1. Scenario

### College Library Book Rental

This Day 2 experiment continues the library-based scenario from Day 1.

The scenario uses the following book information:

- AI202: ₹10 per day
- PY101: ₹5 per day

The main questions involve:
- Simple reasoning
- External library information
- Multi-step rental-cost calculation

The purpose is to compare Direct Prompting, Chain-of-Thought (CoT), and ReAct.

---

## 2. Direct Prompting

Direct Prompting asks the model to answer the question directly without giving it access to tools.

### What it can answer

Direct Prompting worked correctly when all the required information was already included in the question.

For example:

> AI202 costs Rs. 10 per day to borrow. If a student borrows it for 3 days, what is the total rental cost?

The model answered:

> Rs. 30

It also correctly solved the multi-step question involving AI202 and PY101 and gave:

> Rs. 40

### What it cannot answer

For the question:

> How much does AI202 cost per day to borrow?

the model responded that it did not have that information.

This is expected because Direct Prompting has no access to the library database or external tools.

### Limitation

Direct Prompting depends on the information available in the prompt or the model's existing knowledge. It cannot directly retrieve the current library rental information.

---

## 3. Chain-of-Thought

Chain-of-Thought prompting asks the model to reason through a problem step by step before giving the answer.

### What it can answer

For the reasoning question, the model calculated:

10 × 3 = 30

and correctly answered:

> Rs. 30

For the multi-step question, it calculated:

- AI202: 10 × 3 = Rs. 30
- PY101: 5 × 2 = Rs. 10
- Total = Rs. 40

Therefore, CoT successfully handled the arithmetic and multi-step reasoning questions when the required information was provided in the prompt.

### What it cannot answer

For the external-information question about the AI202 rental price, CoT also reported that it did not have the required information.

CoT improves the reasoning process, but it does not automatically provide access to external information or tools.

### Limitation

CoT can help with multi-step reasoning, but it cannot retrieve missing information from the library database without a tool.

---

## 4. ReAct Agent

ReAct combines reasoning and action.

The ReAct process used in this experiment is:

**Thought → Action → Observation → Final Answer**

The ReAct agent has access to the Day 1 library tools.

### Tool usage

For the question:

> How much will it cost to borrow AI202 for 3 days?

the agent first used:

`get_book_details("AI202")`

The tool returned the rental price:

> ₹10 per day

The agent then used:

`safe_calculate("3*10")`

The calculation returned:

> 30

The agent then produced the final answer:

> ₹30

### Why ReAct is different

Unlike Direct Prompting and CoT, ReAct can obtain information from an external tool and then use that information in its reasoning.

### Limitation

ReAct requires correctly configured tools and depends on the tool returning reliable information. It also requires additional model/tool calls compared with a simple direct answer.

---

## 5. Comparison Table

| Basis | Direct Prompting | Chain-of-Thought | ReAct Agent |
|---|---|---|---|
| Reasoning depth | Basic/direct reasoning | Step-by-step reasoning | Reasoning combined with actions and observations |
| Tool usage | No tools | No tools | Uses Day 1 library tools |
| Reliability on multi-step questions | Worked for the tested questions | Worked for the tested questions | Can break a task into tool and calculation steps |
| Transparency | Gives a direct answer with no visible reasoning | Provides a reasoning summary before the answer | Shows the ReAct trace through Thought, Action and Observation |
| Speed / cost | Usually fewer processing steps | More reasoning than direct prompting | More steps because of tool calls |
| Consistency across repeated runs | Not specifically tested in this experiment | Self-consistency was tested separately | Depends on the reasoning and tool execution |
| External information | Cannot access the library database | Cannot access the library database | Can retrieve information using tools |

---

## 6. Self-Consistency Observation

The self-consistency experiment used this question:

> AI202 costs Rs. 10 per day to borrow. If a student borrows it for 3 days, what is the total rental cost?

The question was run five times with:

`temperature = 0.7`

### Recorded answers

| Run | Answer |
|---|---:|
| Run 1 | ₹30 |
| Run 2 | ₹30 |
| Run 3 | ₹30 |
| Run 4 | ₹30 |
| Run 5 | ₹30 |

### Majority answer

The majority answer was:

**₹30**

Frequency:

**5 out of 5**

The majority answer was correct.

### Temperature = 0

The same question was then run with:

`temperature = 0`

The answer was again:

**₹30**

The temperature-0 answer was also correct.

### Observation

In this experiment, all five non-zero-temperature runs produced the same correct answer. Therefore, the majority answer was unambiguous.

The temperature-0 result also matched the majority answer.

---

## 7. Suitability Analysis

For the College Library Book Rental scenario, ReAct is suitable when the question requires information from the library tools.

For example, the rental price of AI202 was not supplied to Direct Prompting or Chain-of-Thought in the external-information question. Both approaches correctly stated that they did not have the required information.

ReAct was able to obtain the AI202 rental price using the library tool and then calculate the rental cost.

However, for a simple calculation where all required information is already provided, Direct Prompting is sufficient.

Chain-of-Thought is useful when a problem requires several reasoning steps and all the required information is already available.

Therefore:

- **Direct Prompting** is useful for simple questions where the required information is already available.
- **Chain-of-Thought** is useful for problems requiring careful multi-step reasoning.
- **ReAct** is useful when reasoning must be combined with external information or tools.

---

## 8. Conclusion

This experiment demonstrated the differences between Direct Prompting, Chain-of-Thought, and ReAct using a College Library Book Rental scenario.

Direct Prompting gave direct answers without tool access. It successfully solved questions when the necessary information was included in the prompt.

Chain-of-Thought provided step-by-step reasoning and successfully solved the tested arithmetic and multi-step questions. However, it could not retrieve missing library information because it had no tool access.

ReAct combined reasoning with actions and observations. It used the Day 1 library tools to retrieve the AI202 rental price and then used the calculator tool to calculate the final rental cost.

The self-consistency experiment produced the same correct answer, ₹30, in all five runs at temperature 0.7. The temperature-0 run also produced ₹30.

In general, Direct Prompting is appropriate for straightforward questions, Chain-of-Thought is useful for problems requiring multiple reasoning steps, and ReAct is appropriate when a problem requires both reasoning and interaction with external tools or information sources.