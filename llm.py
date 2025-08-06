from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

model_id = "Qwen/Qwen1.5-1.8B-Chat"

tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
tokenizer.pad_token = tokenizer.eos_token
model = AutoModelForCausalLM.from_pretrained(model_id, trust_remote_code=True).eval()

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)

def call_qwen_model(prompt: str) -> str:
    messages = [
        {"role": "system", "content": "You are an AI research assistant. Use tools like Search or Scrape to explore the topic and answer the query in ReAct format."},
        {"role": "user", "content": prompt}
    ]
    inputs = tokenizer.apply_chat_template(messages, return_tensors="pt").to(device)
    attention_mask = inputs.ne(tokenizer.pad_token_id).long()

    with torch.no_grad():
        output = model.generate(
            input_ids=inputs,
            attention_mask=attention_mask,
            max_new_tokens=1024,
            do_sample=False
        )

    response = tokenizer.decode(output[0][inputs.shape[-1]:], skip_special_tokens=True)
    return response.strip()

def build_react_prompt(topic: str, history: str = "") -> str:
    return f"""
"You are an expert AI research assistant. Your goal is to provide clear, accurate, and academically sound explanations using reliable sources. Use the ReAct format to break down the topic, gather insights using Search/Scrape, and summarize with precise terminology. Avoid generalizations or outdated definitions."

Topic: {topic}

Break the topic into key subtopics. For each subtopic, use tools like [Search] or [Scrape] to collect insights. After exploring all subtopics, give a comprehensive summary of what the user should learn to fully understand and research the main topic.

Format:
Thought: I need to break down the topic into subtopics...
Action: Search[{topic}]
Observation: (search result or content)
...
Final Answer: (summary)


Previous turns:
{history}
""".strip()


