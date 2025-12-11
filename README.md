# Content Moderation System

## Overview
A multi-modal AI system for content moderation that detects toxic text and NSFW images. Returns severity scores (0–100) and supports batch processing.

---

## Features
- **Text Moderation:** Hate speech, toxicity, threats, insults  
- **Image Moderation:** NSFW detection  
- **Severity Scoring:** Unified score 0–100  
- **Multi-Language Support:** English + others  
- **Batch Processing API**  
- **Admin Dashboard:** Streamlit UI to review flagged content  

---

## Tech Stack
- **Text:** Transformers (BERT, DistilBERT, RuBERT)  
- **Images:** Vision Transformer (ViT)  
- **Backend:** FastAPI  
- **Frontend:** Streamlit  
- **Other:** PyTorch, Pillow, Torchvision  