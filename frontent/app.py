import gradio as gr
import requests

API_URL = "http://localhost:8000"

def upload_file(file):
    with open(file.name, "rb") as f:
        response = requests.post(f"{API_URL}/upload", files={"file": f})
    result = response.json()
    return result["summary"], result["content"]

def ask_question(question, content):
    response = requests.post(f"{API_URL}/ask", json={"question": question, "content": content})
    result = response.json()
    return result['answer'], result['justification']

def challenge_me(content):
    response = requests.post(f"{API_URL}/challenge", json={"question": "dummy", "content": content})
    return response.json()['questions']

def evaluate_answers(ans1, ans2, ans3, questions, content):
    answers = [ans1, ans2, ans3]
    payload = {
        "user_answers": answers,
        "questions": questions,
        "content": content
    }
    response = requests.post(f"{API_URL}/evaluate", json=payload)
    feedback = response.json().get('feedback', [])
    feedback_text = "\n\n".join([f"Q: {f['question']}\nYour Answer: {f['your_answer']}\nCorrect: {f['correct']}\nJustification: {f['justification']}" for f in feedback])
    return feedback_text

def main():
    with gr.Blocks() as demo:
        gr.Markdown("# 📚 Smart Document Assistant")

        with gr.Row():
            file_input = gr.File(label="Upload PDF or TXT")
            summary_output = gr.Textbox(label="Auto Summary", lines=4)
        
        content_state = gr.State("")
        question_list = gr.State([])

        file_input.change(upload_file, inputs=[file_input], outputs=[summary_output, content_state])

        with gr.Tab("Ask Anything"):
            question_input = gr.Textbox(label="Your Question")
            answer_output = gr.Textbox(label="Answer")
            justification_output = gr.Textbox(label="Justification")
            ask_btn = gr.Button("Ask")
            ask_btn.click(ask_question, inputs=[question_input, content_state], outputs=[answer_output, justification_output])

        with gr.Tab("Challenge Me"):
            challenge_output = gr.Textbox(label="Generated Questions", lines=6)
            answer1 = gr.Textbox(label="Answer 1")
            answer2 = gr.Textbox(label="Answer 2")
            answer3 = gr.Textbox(label="Answer 3")
            feedback_output = gr.Textbox(label="Feedback", lines=10)

            generate_btn = gr.Button("Generate Questions")
            eval_btn = gr.Button("Evaluate Answers")

            # This function returns questions for the challenge
            def store_questions(content):
                questions = challenge_me(content)
                joined_questions = "\n".join(questions)
                return joined_questions, questions  # returning list explicitly

            # Ensure we pass the correct question list from state to evaluation
            def evaluate_answers_fixed(ans1, ans2, ans3, question_text, content):
                questions = question_text.strip().split("\n")  # split from challenge_output
                return evaluate_answers(ans1, ans2, ans3, questions, content)

            generate_btn.click(store_questions, inputs=[content_state], outputs=[challenge_output, question_list])
            eval_btn.click(evaluate_answers_fixed, inputs=[answer1, answer2, answer3, challenge_output, content_state], outputs=[feedback_output])

    demo.launch()

if __name__ == "__main__":
    main()
