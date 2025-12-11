class SeverityScorer:
    """
    Converts model probabilities into a 0-100 severity score.
    """
    def __init__(self):
        # Optional: weights for different categories
        self.text_weights = {
            "toxic": 1.0,
            "severe_toxic": 1.2,
            "obscene": 0.8,
            "threat": 1.5,
            "insult": 1.0,
            "identity_hate": 1.2
        }

        self.image_weights = {
            "nsfw": 1.5,
            "normal": 1.0
        }

    def text_severity(self, text_probs):
        score = 0.0
        for label, prob in text_probs.items():
            weight = self.text_weights.get(label, 1.0)
            score += prob * weight
        # normalize to 0-100
        score = min(max(score * 50, 0), 100)
        return round(score, 2)

    def image_severity(self, image_probs):
        score = 0.0
        for label, prob in image_probs.items():
            weight = self.image_weights.get(label, 1.0)
            score += prob * weight
        # normalize to 0-100
        score = min(max(score * 50, 0), 100)
        return round(score, 2)
