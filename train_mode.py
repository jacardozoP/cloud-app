import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader

# Configuración
DATA_DIR = "dataset_original/train"
BATCH_SIZE = 16
EPOCHS = 15
MODEL_PATH = "models/cloud_model.pth"

# Transformaciones (preparar imágenes)
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(15),
    transforms.ColorJitter(
        brightness=0.3,
        contrast=0.3,
        saturation=0.3
    ),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

# Dataset
dataset = datasets.ImageFolder(DATA_DIR, transform=transform)
dataloader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True, num_workers=0)

# Clases (muy importante)
class_names = dataset.classes
print("Clases detectadas:", class_names)

# Modelo preentrenado
model = models.resnet18(weights="DEFAULT")

# Adaptar última capa al número de clases
num_features = model.fc.in_features
model.fc = nn.Linear(num_features, len(class_names))

# Función de pérdida y optimizador
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.0003)

# Entrenamiento
for epoch in range(EPOCHS):
    running_loss = 0.0
    correct = 0
    total = 0

    for batch_idx, (images, labels) in enumerate(dataloader):
        optimizer.zero_grad()

        outputs = model(images)
        loss = criterion(outputs, labels)

        _, predicted = torch.max(outputs, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

        loss.backward()
        optimizer.step()

        running_loss += loss.item()
        print(f"Epoch {epoch+1}/{EPOCHS} - Batch {batch_idx+1}/{len(dataloader)} - Loss: {loss.item():.4f}")

    avg_loss = running_loss / len(dataloader)
    accuracy = 100 * correct / total

    print(f"Epoch {epoch+1}/{EPOCHS} - Loss: {avg_loss:.4f} - Accuracy: {accuracy:.2f}%")

# Guardar modelo
torch.save({
    "model_state": model.state_dict(),
    "classes": class_names
}, MODEL_PATH)

print("Modelo guardado en:", MODEL_PATH)