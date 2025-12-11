from fastapi import Body, FastAPI, File, UploadFile
from src.text_moderator import TextModerator
from src.image_moderator import ImageModerator
from src.scorer import SeverityScorer
from PIL import Image
from typing import List
import io

app = FastAPI()

text_model = TextModerator()
image_model = ImageModerator()
scorer = SeverityScorer()

@app.post("/moderate/text")
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

@app.post("/moderate/batch")
async def moderate_batch(
    texts: list[str] = Body(default=[]),
    files: list[UploadFile] = None
):
    results = []

    # Process texts
    for text in texts:
        text_result = text_model.predict(text)
        text_sev = scorer.text_severity(text_result)
        results.append({"type": "text", "input": text, "result": text_result, "severity": text_sev})

    # Process images
    if files:
        for file in files:
            img = Image.open(io.BytesIO(await file.read())).convert("RGB")
            image_result = image_model.predict(img)
            image_sev = scorer.image_severity(image_result)
            results.append({"type": "image", "input": file.filename, "result": image_result, "severity": image_sev})

    return results