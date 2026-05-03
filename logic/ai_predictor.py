import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image


MODEL_PATH = "models/cloud_model.pth"

_model = None
_classes = None


def load_model():
    global _model, _classes

    if _model is not None:
        return _model, _classes

    checkpoint = torch.load(MODEL_PATH, map_location="cpu")

    _classes = checkpoint["classes"]

    model = models.resnet18(weights=None)
    num_features = model.fc.in_features
    model.fc = nn.Linear(num_features, len(_classes))

    model.load_state_dict(checkpoint["model_state"])
    model.eval()

    _model = model
    return _model, _classes


def predict_cloud(image_path):
    model, classes = load_model()

    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor()
    ])

    image = Image.open(image_path).convert("RGB")
    image = transform(image).unsqueeze(0)

    with torch.no_grad():
        outputs = model(image)
        probabilities = torch.softmax(outputs, dim=1)[0]

    top_probs, top_indices = torch.topk(probabilities, 3)

    top_predictions = []

    for prob, index in zip(top_probs, top_indices):
        top_predictions.append({
            "code": classes[index.item()],
            "confidence": prob.item()
        })

    return {
        "code": top_predictions[0]["code"],
        "confidence": top_predictions[0]["confidence"],
        "top_3": top_predictions
    }