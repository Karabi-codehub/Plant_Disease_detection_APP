import os
import torch
import timm
from torchvision import transforms

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "..", "models", "model.pth")


class PlantModel:
    def __init__(self, model_path=MODEL_PATH, img_size=224):
        self.device = torch.device("cpu")

        self.model = timm.create_model(
            "efficientnet_b0",
            pretrained=False,
            num_classes=38
        )

        # Load checkpoint
        state = torch.load(model_path, map_location=self.device)

        # Remove "backbone." prefix if present
        if any(k.startswith("backbone.") for k in state.keys()):
            state = {k.replace("backbone.", ""): v for k, v in state.items()}

        self.model.load_state_dict(state, strict=True)
        self.model.eval()

        # ✅ MATCHES GRADIO EXACTLY (NO NORMALIZATION)
        self.transform = transforms.Compose([
            transforms.Resize((img_size, img_size)),
            transforms.ToTensor()
        ])


_model = None


def load_model():
    global _model
    if _model is None:
        _model = PlantModel()
    return _model
