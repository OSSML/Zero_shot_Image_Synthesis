from PIL import Image

from models.pretrained.SD2Inpainting import SD2Inpainting
import gradio as gr

model = SD2Inpainting(device="cuda")

def run(image, prompt, direction, similar_color, num_images):
    # num_images = int(num_images)
    image = Image.fromarray(image)
    outputs = [image]*num_images
    for i in range(num_images):
        for dire in direction:
            outputs[i] = model.inference(image=outputs[i], direction=dire, prompt=prompt, similar_color=similar_color)
    return outputs

# app = gr.Interface(
#     fn=run,
#     inputs=[gr.Image(), "text", gr.Dropdown(['left', 'right', 'top', 'bottom']), "checkbox"],
#     outputs=gr.Gallery()
#     )

with gr.Blocks(fill_width=True) as app:
    with gr.Row():
        with gr.Column(min_width=300):
            image = gr.Image()
        with gr.Column(min_width=300):
            prompt = gr.Textbox(label="prompt")
            direction = gr.Dropdown(['left', 'right', 'top', 'bottom'], label="direction", multiselect=True)
            similar_color = gr.Checkbox(label="Similar Color", value=True)
            num_images = gr.Number(label="Number of images", minimum=1, maximum=4)
            submit_btn = gr.Button("Submit")

    outputs = gr.Gallery(preview=True)

    submit_btn.click(
        run,
        [image, prompt, direction, similar_color, num_images],
        outputs
    )

app.launch()