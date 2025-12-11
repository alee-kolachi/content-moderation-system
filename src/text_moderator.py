from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

class TextModerator:
    def __init__(self):
        self.model_name = "microsoft/xtremedistil-l6-h256-uncased"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name)
        
        self.labels = [
            "toxic",
            "severe_toxic",
            "obsence",
            "threat",
            "insult",
            "identity_hate"
        ]
    
    def predict(self, text):
        inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True)
        with torch.no_grad():
            outputs = self.model(**inputs)

        probs = torch.softmax(outputs.logits, dim=1)[0].tolist()

        result = {}
        for label, p in zip(self.labels, probs):
            result[label] = round(float(p), 4)

        return result
    

