import requests
import os
def classify_comment(text):
    
    try:
        response = requests.post(
            os.getenv("COMMENT_CLASSIFICATION_API_URL") ,
            json={"text": text},
            headers={"Content-Type": "application/json"}
        )
        if response.status_code == 200:
            data = response.json()
            return {
                "is_spam": data.get("spam_check", {}).get("is_spam", False),
                "spam_confidence": data.get("spam_check", {}).get("confidence"),
                "is_profane": data.get("profanity_check", {}).get("is_profane", False),
                "profanity_confidence": data.get("profanity_check", {}).get("confidence"),
            }
    except Exception:
        pass
    
    return {
        "is_spam": False,
        "spam_confidence": None,
        "is_profane": False,
        "profanity_confidence": None,
    }