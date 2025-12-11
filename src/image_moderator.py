from transformers import AutoFeatureExtractor, AutoModelForImageClassification
from PIL import Image
import torch
from io import BytesIO
import requests

class ImageModerator:
    def __init__(self):
        self.model_name = "Falconsai/nsfw_image_detection"
        self.extractor = AutoFeatureExtractor.from_pretrained(self.model_name)
        self.model = AutoModelForImageClassification.from_pretrained(self.model_name)

        self.labels = self.model.config.id2label

    def predict(self, image_path):

        if image_path.startswith("http://") or image_path.startswith("https://"):
            response = requests.get(image_path)
            img = Image.open(BytesIO(response.content))
        else:
            img = Image.open(image_path).convert("RGB")

        inputs = self.extractor(images=img, return_tensors="pt")

        with torch.no_grad():
            outputs = self.model(**inputs)
        
        prob = torch.softmax(outputs.logits, dim=1)[0].tolist()
        result = {
            self.labels[i]: round(float(p), 4)
            for i, p in enumerate(prob)
        }

        return result
    
if __name__ == "__main__":
    image_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRLSr9br6ucD00bgDT-DrXfs8MRUe3JNEAiag&s"
    
    m = ImageModerator()
    print(m.predict(image_url))