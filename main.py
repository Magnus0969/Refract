from llm import call_qwen_model, build_react_prompt
from tools import execute_action
from report_utils import save_pdf_report, save_markdown_report
from datetime import datetime

def summarize_partial_history(topic, history):
    summary_prompt = f"""
You are an AI assistant. The user asked you to research a topic: "{topic}".
You were able to gather the following thoughts and partial observations but ran out of time.

Please write a short summary based on what was collected so far.

Partial Transcript:
{history}

Summary:""".strip()

    return call_qwen_model(summary_prompt)


def run_agent(topic):
    history = ""
    final_answer = ""
    step_count = 0
    max_steps = 10  # safer limit

    while step_count < max_steps:
        prompt = build_react_prompt(topic, history)
        output = call_qwen_model(prompt)

        print("🧠 Prompt sent to LLM:")
        print(prompt)
        print("🧾 LLM Output:")
        print(output)

        if "Final Answer:" in output:
            final_answer = output.split("Final Answer:")[-1].strip()
            history += f"\nFinal Answer: {final_answer}"
            break

        for line in output.strip().split("\n"):
            line = line.strip()
            if line.startswith("Thought:"):
                history += f"{line}\n"
            elif line.startswith("Action:"):
                action = line.split("Action:")[1].strip()
                print(f"🔧 Executing: {action} ...")
                obs = execute_action(action)
                cleaned_obs = obs.strip().replace("\n", " ").replace("  ", " ")[:500]
                print("📥 Observation received.")
                history += f"Action: {action}\nObservation: {cleaned_obs}...\n"
                break  # exit loop to prompt again
        else:
            step_count += 1

    if not final_answer:
      print("⚠️ Step limit reached. Generating partial summary...")
      
      # Step 1: summarize based on history
      partial_summary_prompt = f"""
  You were assisting a user researching the topic: "{topic}".

  Here is the information collected so far:

  {history}

  Please write a concise summary of what has been learned based on the above thoughts and observations.
  """
      partial_summary = call_qwen_model(partial_summary_prompt)

      # Step 2: verify the summary
      verify_prompt = f"""
The following text is a summary of the topic "{topic}" generated from multiple partial reasoning steps. 

Please:
1. Check whether it accurately defines *foundation models* (not just machine learning algorithms).
2. Rewrite the summary to be accurate, concise, and technically sound.
3. Keep the tone informative and suitable for a research summary.

Here is the current summary:
{partial_summary}

Your revised and verified version:
"""
      final_answer = call_qwen_model(verify_prompt)
      history += f"\nFinal Answer (Verified Summary): {final_answer}"


    return final_answer, history


def main():
    topic = input("🔍 What would you like to research? (e.g., Quantum Entanglement): ").strip()
    if not topic:
        print("❌ Please enter a valid topic.")
        return

    print("\n🚀 Running Agent... Please wait.\n")
    final_answer, history = run_agent(topic)

    print("\n✅ Research Completed!\n")
    print("📝 Final Summary:\n")
    print(final_answer)
    print("\n🔎 Full Thought Process:\n")
    print(history)

    # Save reports
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    session_id = f"research_{topic.replace(' ', '_')}_{now}"
    research_summary = f"# Research Summary: {topic}\n\n## Final Answer:\n{final_answer}\n\n## Reasoning Trace:\n{history}"

    pdf_path = f"{session_id}.pdf"
    save_pdf_report(research_summary, pdf_path)
    print(f"\n📄 PDF Report saved to: {pdf_path}")

    md_path = save_markdown_report(research_summary, f"{session_id}.md")
    print(f"📝 Markdown Report saved to: {md_path}")

if __name__ == "__main__":
    main()
