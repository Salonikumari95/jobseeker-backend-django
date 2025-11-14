import requests

def classify_comment(text):
    
    try:
        response = requests.post(
            "https://comment-classifier-0ep9.onrender.com/check-comment",
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