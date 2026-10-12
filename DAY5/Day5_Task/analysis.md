
# Day 5 Task: Serving Models Your Way

## 1. Scenario

My scenario is a personal coding helper that runs locally on my computer. It explains programming concepts in simple English, gives short code examples, and redirects questions unrelated to programming.

I created a custom Ollama model named `coding-helper` using a Modelfile. I used Python to access the model through the Ollama REST API and the OpenAI-compatible endpoint.

My goal is to understand how Ollama serves a model, how a Modelfile defines default behavior, how API requests can change that behavior, and why a server such as vLLM may be more suitable when many users access a model simultaneously.

## 2. Explanation of Concepts

### 2.1 What Is Ollama?

Ollama is a tool for downloading, running, and serving language models locally. It provides a server that applications can access through multiple interfaces.

The three parts relevant to this project are the Ollama command-line interface, the Ollama server, and the model/runtime layer.

The command-line interface allows me to download models, create custom models, inspect model information, and run prompts. The server receives requests through HTTP API endpoints. The model/runtime layer loads the selected model and performs inference to generate responses.

Ollama model files are normally stored in a user-specific model directory. The exact location depends on the operating system and configuration. On Windows, the default model directory is generally under the user's profile, in `.ollama/models`.

When I send a request, the server receives the request and identifies the requested model. If necessary, it loads the model into memory, processes the prompt, generates a response, and sends the result back to the client. The model may remain loaded for subsequent requests, depending on its keep-alive settings and available resources.

In my scenario, I use the command line to create and test `coding-helper`, then use Python to send API requests.

### 2.2 What Is a Modelfile?

A Modelfile describes how to create a custom Ollama model from a base model and configuration instructions.

My Modelfile uses `FROM llama3.2` to select the base model. It uses `PARAMETER temperature 0.2` to make responses less random, `PARAMETER num_ctx 2048` to configure the context length, and `PARAMETER num_predict 200` to limit the generated output. Its `SYSTEM` instruction defines the coding-helper role and the rules the model should follow.

I created the custom model with:

`ollama create coding-helper -f Modelfile`

A custom model created this way is primarily a configuration and behavior definition associated with the selected base model. It does not normally train a new model or download a second complete set of weights when the base model is already present. The base model must, however, be available locally; pulling it is necessary if it has not been downloaded.

For my project, this means I can package a consistent coding-helper behavior without training a language model from scratch.

### 2.3 Which System Prompt Wins?

The Modelfile provides the default system behavior for my custom model. An API request can supply its own system prompt, which can override the default for that request when the endpoint supports it.

I tested this using the OpenAI-compatible chat endpoint. My Modelfile tells the model to act as a coding assistant, while the program supplies a different system prompt asking it to act as a study assistant and answer in exactly three short bullet points.

I observed the following result: [Record whether the response followed the program's three-bullet instruction or the Modelfile behavior.]

This behavior is useful for agent development. A developer can define a reusable default role in the Modelfile while supplying task-specific instructions for an individual request. The actual behavior must still be verified with the selected model and endpoint.

### 2.4 Difference Between /api/generate and /api/chat

The `/api/generate` endpoint is designed for generating a response from a prompt. My Python script uses it to send a prompt and receive generated text.

The `/api/chat` endpoint is designed for conversational messages, including message roles such as system, user, and assistant. It is more convenient when an application maintains a conversation history.

Ollama also provides an OpenAI-compatible endpoint, such as `/v1/chat/completions`. This allows applications written for the OpenAI chat-completions interface to communicate with a compatible local model server with relatively small code changes.

In my scenario, I used `/api/generate` for direct REST testing and `/v1/chat/completions` to test a custom system prompt. An OpenAI-compatible interface can make it easier to migrate an application to another compatible server, although model names, supported features, and behavior may still differ.

### 2.5 Streaming, TTFT, and Total Time

Streaming means that generated response text is returned in chunks while the model is still generating. Without streaming, the client normally waits for the complete response before displaying it.

TTFT means time to first token. In my script, it is measured as the elapsed time from the beginning of a streaming request until the first non-empty text chunk is received. This is a practical measurement of time to first visible output, rather than an exact measurement of an individual model token.

Total time is the elapsed wall-clock time from sending the request until the response finishes. Tokens per second is calculated from the generated-token count and Ollama's reported generation duration.

Streaming can make an answer feel faster because the user sees the beginning earlier. It does not necessarily reduce the total time needed to generate the complete answer.

My measured TTFT was [value] seconds and my total time was [value] seconds. The difference indicates [explain your observation].

### 2.6 num_ctx, OLLAMA_KEEP_ALIVE, and OLLAMA_NUM_PARALLEL

`num_ctx` controls the context window used for a model request or model configuration. A larger context allows more tokens to be considered, but can increase KV-cache memory usage.

`OLLAMA_KEEP_ALIVE` controls how long Ollama keeps a model loaded after a request. Keeping a model loaded can avoid repeated loading delays, but uses memory even when the model is idle.

`OLLAMA_NUM_PARALLEL` controls the number of parallel requests Ollama can process for a model. More parallel requests can improve concurrency, but may increase memory requirements because each request can require its own KV-cache allocation.

These settings matter in my coding-helper scenario because longer prompts and repeated requests affect memory and response time. They become more important if several people use the service at the same time.

### 2.7 PagedAttention and Prefix Caching

A simple serving system can waste memory when it allocates KV-cache space for requests using fixed maximum lengths or reserves space that is not actually needed. Different requests have different sequence lengths, so static allocation can leave memory unused.

PagedAttention manages KV-cache data in fixed-size blocks rather than requiring one large contiguous allocation for each sequence. A block table maps the logical token sequence to its physical cache blocks. This helps reduce fragmentation and improves memory utilization.

Prefix caching can reuse previously computed attention information for a shared prefix. For example, an agent may send the same system prompt with many requests. Reusing the cached prefix can avoid recomputing that part of the prompt, subject to the server's cache behavior and compatibility requirements.

These techniques are valuable for deployments that serve many requests and need to use accelerator memory efficiently.

### 2.8 Static Batching and Continuous Batching

Static batching groups requests into a batch and processes that batch together. A request that finishes early may leave unused capacity while the other requests continue.

Continuous batching allows new requests to join the running workload as other requests finish. This can improve accelerator utilization and throughput when requests have different prompt and generation lengths.

Throughput measures how much work the server completes over time, often in generated tokens per second across requests.

TTFT measures how long a user waits for the first output. TPOT means time per output token after generation begins. P95 latency is the latency below which 95 percent of measured requests complete.

Increasing batch size or maximizing throughput can increase waiting time for individual requests. The best configuration depends on the balance between throughput, TTFT, TPOT, and P95 latency.

For my personal coding helper, simplicity matters more than serving many concurrent users. For a shared service, scheduling and memory efficiency become much more important.

## 3. Ollama Versus vLLM Comparison

| Basis for comparison | Ollama | vLLM |
|---|---|---|
| Built for (who and how many users) | Convenient local use, development, and smaller deployments | High-throughput serving for concurrent requests |
| Hardware it needs | Runs on supported local CPU/GPU hardware | Commonly deployed on suitable accelerator hardware for high-throughput inference |
| How it handles several requests at once | Provides configurable parallel request handling | Uses continuous batching and serving optimizations |
| How it manages memory | Loads models and manages inference memory through its runtime | Uses PagedAttention and block-based KV-cache management |
| Setup effort and model format | Simple local installation; supports Ollama model packaging | More serving configuration; supports supported model architectures and formats |
| Your choice if only you use the scenario, and why | Ollama, because it is straightforward to install and test locally | Not necessary for this small personal scenario |
| Your choice if 100 people use it at once, and why | May be less suitable depending on workload and hardware | vLLM, or a comparable production server, because concurrency, batching, and memory efficiency matter |

## 4. Observation

I created the custom model and tested it with three different prompts. I also repeated the first prompt to compare the consecutive runs.

| Run | Prompt | Modelfile behavior followed? | TTFT | Tokens/second | Total time | Model already loaded? |
|---|---|---|---|---|---|---|
| 1 | Explain a Python variable | [Observation] | [Measured] | [Measured] | [Measured] | [Yes/No] |
| 2 | Explain a Python for loop | [Observation] | [Measured] | [Measured] | [Measured] | [Yes/No] |
| 3 | What is the capital of France? | [Observation] | [Measured] | [Measured] | [Measured] | [Yes/No] |
| 4 | Repeat the Python variable prompt | [Observation] | [Measured] | [Measured] | [Measured] | [Yes/No] |
| 5 | Explain a Python function using the program's different system prompt | [Observation] | [Measured] | [Measured] | [Measured] | [Yes/No] |

I checked whether the model was loaded using `ollama ps` or the `/api/ps` endpoint.

On the repeated prompt, the model was [already loaded / not loaded]. The first run took [value] seconds and the repeated run took [value] seconds. The measured TTFT changed from [value] to [value] seconds.

My main observation was [describe the actual result]. TTFT was [shorter than / close to / a large part of] the total time, which means [explain what you observed]. When the program supplied its own system prompt, the response [followed the new prompt / retained the default behavior / showed mixed behavior].

Any difference between runs may be related to model loading, warm-up, prompt length, generation length, hardware, or runtime scheduling. These are possible explanations, not conclusions unless supported by the measurements.

## 5. Suitability and Conclusion

Ollama was suitable for my personal coding-helper scenario because it allowed me to create a custom model, define default behavior with a Modelfile, and access the model through command-line and HTTP interfaces.

The REST API made it possible to integrate model responses into a Python program. Streaming improved responsiveness by allowing output to appear before the complete response was generated. The OpenAI-compatible endpoint demonstrated how a client can supply task-specific instructions and use an interface that is also supported by other serving systems.

A shared deployment for 100 concurrent users has different requirements. It must manage request scheduling, KV-cache memory, throughput, and latency across many simultaneous requests. vLLM or a similar production inference server may be more suitable because continuous batching and PagedAttention are designed to improve serving efficiency.

In general, local Ollama is sufficient for learning, personal assistants, prototyping, and smaller workloads. Modelfiles package default behavior, while REST APIs let other applications call the model programmatically. When concurrency, accelerator-memory utilization, throughput, and latency become central requirements, a server designed for high-throughput multi-user inference is often the better choice.
