import time
from typing import Optional,Any, List, Dict
import gradio as gr
from gradio import ChatMessage

def azure_enterprise_chat(user_message: str, history: List[dict]):
    conversation = []
    #for msg_dict in history:
    #    conversation.append(convert_dict_to_chatmessage(msg_dict))

    # Append the user's new message
    conversation.append(ChatMessage(role="user", content=user_message))

    answer = ChatMessage(
        role="assistant", 
        content="This is a placeholder response.",
        metadata={
                "title": "myFunction",
                "status": "pending",
                "id": "tool-123"
            }
        )
    conversation.append(answer)
    yield conversation, ""
    
    time.sleep(5)  # Simulate processing time
    answer.metadata["status"] = "done"


    # Immediately yield two outputs to clear the textbox
    yield conversation, ""

brand_theme = gr.themes.Default(
    primary_hue="blue",
    secondary_hue="blue",
    neutral_hue="gray",
    font=["Segoe UI", "Arial", "sans-serif"],
    font_mono=["Courier New", "monospace"],
    text_size="lg",
).set(
    button_primary_background_fill="#0f6cbd",
    button_primary_background_fill_hover="#115ea3",
    button_primary_background_fill_hover_dark="#4f52b2",
    button_primary_background_fill_dark="#5b5fc7",
    button_primary_text_color="#ffffff",
    button_secondary_background_fill="#e0e0e0",
    button_secondary_background_fill_hover="#c0c0c0",
    button_secondary_background_fill_hover_dark="#a0a0a0",
    button_secondary_text_color="#000000",
    body_background_fill="#f5f5f5",
    block_background_fill="#ffffff",
    body_text_color="#242424",
    body_text_color_subdued="#616161",
    block_border_color="#d1d1d1",
    block_border_color_dark="#333333",
    input_background_fill="#ffffff",
    input_border_color="#d1d1d1",
    input_border_color_focus="#0f6cbd",
)

with gr.Blocks(theme=brand_theme, css="footer {visibility: hidden;}", fill_height=True) as demo:

    def clear_thread():
        global thread
        #thread = project_client.agents.create_thread() do later
        return []

    def on_example_clicked(evt: gr.SelectData):
        return evt.value["text"]  # Fill the textbox with that example text

    gr.HTML("<h1 style=\"text-align: center;\">Azure AI Agent Service</h1>")

    chatbot = gr.Chatbot(
        type="messages",
        examples=[
            {"text": "What's my company's remote work policy?"},
            {"text": "Check if it will rain tomorrow?"},
            {"text": "How is Contoso's stock doing today?"},
            {"text": "Send my direct report a summary of the HR policy."},
        ],
        show_label=False,
        scale=1,
    )

    textbox = gr.Textbox(
        show_label=False,
        lines=1,
        submit_btn=True,
    )

    # Populate textbox when an example is clicked
    chatbot.example_select(fn=on_example_clicked, inputs=None, outputs=textbox)

    # On submit: call azure_enterprise_chat, then clear the textbox
    (textbox
     .submit(
         fn=azure_enterprise_chat,
         inputs=[textbox, chatbot],
         outputs=[chatbot, textbox],
     )
     .then(
         fn=lambda: "",
         outputs=textbox,
     )
    )

    # A "Clear" button that resets the thread and the Chatbot
    chatbot.clear(fn=clear_thread, outputs=chatbot)

# Launch your Gradio app
if __name__ == "__main__":
    demo.launch()