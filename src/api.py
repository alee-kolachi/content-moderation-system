from fastapi import FastAPI, File, UploadFile
from src.text_moderator import TextModerator
from src.image_moderator import ImageModerator
from src.scorer import SeverityScorer
from PIL import Image
import io

app = FastAPI()

text_model = TextModerator()
image_model = ImageModerator()
scorer = SeverityScorer()

@app.post("/moderator/text")
async def moderate_text(text: str):
    text_result = text_model.predict(text)
    severity = scorer.text_severity(text_result)
    return {"text_result": text_result, "severity": severity}

@app.post("/moderate/image")
async def moderate_image(file: UploadFile = File(...)):
    
    contents = await file.read()
    image_path = f"/tmp/{file.filename}"

    with open(image_path, 'wb') as f:
        f.write(contents)

    image_result = image_model.predict(image_path)
    severity = scorer.image_severity(image_result)
    return {"image_result": image_result, "severity": severity}

@app.post("/moderate/multimodal")
async def moderate_multimodal(text: str = None, file: UploadFile = None):
    results = {}
    if text:
        text_result = text_model.predict(text)
        severity = scorer.text_severity(text_result)
        results["text_result"] = text_result
        results["text_severity"] = severity
    if file:
        contents = await file.read()
        image_path = f"/tmp/{file.filename}"

        with open(image_path, 'wb') as f:
            f.write(contents)

        image_result = image_model.predict(image_path)
        severity = scorer.image_severity(image_result)
        results["image_results"] = image_result
        results["image_severity"] = severity
    return results