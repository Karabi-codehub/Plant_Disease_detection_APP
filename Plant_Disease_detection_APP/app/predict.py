import json
import torch
import numpy as np
from PIL import Image
import os

from app.model import load_model
from app.utils import clean_name, risk_from_prob, generate_leaf_report


# 🔥 CORRECT PATH (ROOT classes.json)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CLASSES_PATH = os.path.join(BASE_DIR, "..", "classes.json")



with open(CLASSES_PATH, "r") as f:
   CLASS_NAMES = json.load(f)



model = load_model()


def predict_pil_image(pil_image: Image.Image):
   img = pil_image.convert("RGB")
   input_tensor = model.transform(img).unsqueeze(0)



   with torch.no_grad():
       logits = model.model(input_tensor)
       probs = torch.softmax(logits, dim=1)[0].cpu().numpy()



   pred_idx = int(np.argmax(probs))
   pred_name = clean_name(CLASS_NAMES[pred_idx])
   confidence = round(float(probs[pred_idx]) * 100, 2)



   risk = risk_from_prob(probs[pred_idx])
   description, treatment = generate_leaf_report(pred_name)



   top5_idx = probs.argsort()[-5:][::-1]
   top5 = [
       {
           "class": clean_name(CLASS_NAMES[i]),
           "probability": float(probs[i])
       }
       for i in top5_idx
   ]



   return {
       "prediction": pred_name,
       "confidence": confidence,
       "risk": risk,
       "description": description,
       "treatment": treatment,
       "top5": top5
   }
