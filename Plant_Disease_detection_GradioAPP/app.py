import gradio as gr
import torch
from torchvision import transforms
from PIL import Image
import timm
import os
import json

# ------------------------------------------------
# CONFIG
# ------------------------------------------------
MODEL_PATH = "model.pth"
CLASSES_FILE = "classes.json"
MODEL_NAME = "efficientnet_b0"
IMG_SIZE = 224


# ------------------------------------------------
# LOAD CLASS NAMES
# ------------------------------------------------
def load_classes(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"{path} missing in Space")

    with open(path, "r") as f:
        classes = json.load(f)

    cleaned = []
    for c in classes:
        cleaned.append(c.replace("___", " ").replace("__", " ").replace("_", " "))
    return cleaned


try:
    class_names = load_classes(CLASSES_FILE)
    num_classes = len(class_names)
except:
    class_names = ["Error"]
    num_classes = 1


# ------------------------------------------------
# DISEASE SHORT DESCRIPTIONS
# ------------------------------------------------
disease_info = {
    "Leaf Scorch": "Brown burned edges caused by heat or fungal infection.",
    "Early Blight": "Circular brown spots with yellow halo.",
    "Late Blight": "Water-soaked patches, very harmful.",
    "Leaf Spot": "Small brown/black round scattered spots.",
    "Healthy": "No harmful signs detected."
}

def get_description(disease):
    for key in disease_info:
        if key.lower() in disease.lower():
            return disease_info[key]
    return "No description available."


# ------------------------------------------------
# LOAD MODEL
# ------------------------------------------------
def load_model():
    model = timm.create_model(MODEL_NAME, pretrained=False, num_classes=num_classes)
    state = torch.load(MODEL_PATH, map_location="cpu")

    clean_state = {k.replace("backbone.", ""): v for k, v in state.items()}
    model.load_state_dict(clean_state, strict=True)
    model.eval()
    return model


try:
    model = load_model()
except:
    model = None


# ------------------------------------------------
# TRANSFORM
# ------------------------------------------------
transform = transforms.Compose([
    transforms.Resize((IMG_SIZE, IMG_SIZE)),
    transforms.ToTensor(),
])


# ------------------------------------------------
# RISK COLOR LOGIC
# ------------------------------------------------
def get_risk_color(prob):
    if prob >= 0.70:
        return "🔴 **High Risk**"
    elif prob >= 0.30:
        return "🟡 **Moderate Risk**"
    else:
        return "🟢 Low Risk"


# ------------------------------------------------
# PREDICT
# ------------------------------------------------
def predict(img):
    if img is None:
        return "Upload an image", ""

    if model is None:
        return "Model failed to load", ""

    image = Image.fromarray(img).convert("RGB")
    image = transform(image).unsqueeze(0)

    with torch.no_grad():
        out = model(image)
        probs = torch.softmax(out, dim=1)[0]

    conf = {cls: float(probs[i]) for i, cls in enumerate(class_names)}

    # TOP 5
    top5 = sorted(conf.items(), key=lambda x: x[1], reverse=True)[:5]

    # Make HTML cards
    cards_html = ""
    for disease, prob in top5:
        percent = round(prob * 100, 2)
        desc = get_description(disease)
        risk = get_risk_color(prob)

        card = f"""
        <div style="
            background:#ffffffdd; 
            padding:15px; 
            border-radius:15px; 
            margin-bottom:10px;
            box-shadow:0 4px 10px rgba(0,0,0,0.15);
        ">
            <h3 style="margin:0;">{disease}</h3>
            <p style="margin:4px 0;">Confidence: <b>{percent}%</b></p>
            <p style="margin:4px 0;">{risk}</p>
            <p style="opacity:0.8;">{desc}</p>
        </div>
        """
        cards_html += card

    return top5[0][0], cards_html


# ------------------------------------------------
# UI
# ------------------------------------------------
with gr.Blocks() as demo:

    # Inject custom CSS
    gr.HTML("""
        <style>
        body { background: linear-gradient(to bottom right,#e2f7e2,#ffffff); }
        </style>
    """)

    gr.HTML("""
        <h1 style='text-align:center;'>🌱 Plant Disease Detector</h1>
        <p style='text-align:center;'>AI Model with Top-5 Risk Colored Predictions</p>
    """)

    with gr.Row():
        with gr.Column():
            input_img = gr.Image(type="numpy", label="Upload Leaf Image")
            analyze = gr.Button("🔍 Analyze")

        with gr.Column():
            result = gr.Textbox(label="Most Likely Disease", interactive=False)
            cards = gr.HTML()

    analyze.click(predict, inputs=input_img, outputs=[result, cards])

demo.launch()
