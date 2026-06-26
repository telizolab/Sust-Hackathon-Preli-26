import re

def apply_safety_filters(customer_reply: str, recommended_next_action: str) -> tuple[str, str]:
    """
    Applies strict fintech safety filters to the LLM outputs.
    """
    safe_reply = customer_reply
    safe_action = recommended_next_action

    # Rule 1 (Credential Shield): Override the reply entirely if credentials are asked/mentioned
    cred_keywords = r"\b(pin|otp|password|card number|credentials)\b"
    if re.search(cred_keywords, safe_reply, re.IGNORECASE):
        safe_reply = "We have received your request. For your security, never share your secret credentials with anyone. A support agent will review your case shortly."

    # Rule 2 (Financial Promise Shield): Replace sentences containing specific promises
    # Match a sentence ending with ., !, or ? (or end of string) containing the keywords
    promise_keywords = r"(will refund|have refunded|can refund|process a refund|refund is approved|reversed|unblocked|recovered)"
    
    def promise_replacer(match):
        return "any eligible amount will be returned through official channels"
        
    promise_pattern = re.compile(promise_keywords, re.IGNORECASE)
    safe_reply = promise_pattern.sub(promise_replacer, safe_reply)
    safe_action = promise_pattern.sub(promise_replacer, safe_action)

    # Rule 3 (Third-Party Shield): Replace URLs or phone numbers in customer_reply
    # Simple heuristic for URLs and phones
    url_pattern = r"(https?://\S+|www\.\S+)"
    # Matches simple Bangladeshi phone numbers without capturing tickets
    phone_pattern = r"(?:\+8801|01)[3-9]\d{8}"
    
    third_party_pattern = re.compile(rf"({url_pattern}|{phone_pattern})", re.IGNORECASE)
    
    replacement_text = "Please contact our official in-app support for further assistance."
    
    # The hackathon rule says "If customer_reply contains URLs... replace with"
    # We will replace the whole string if it contains unauthorized contact info, or just the matching part?
    # "replace with" usually implies replacing the whole string or the matched segment.
    # The prompt says "replace with", I'll replace the matched segment to be safe.
    safe_reply = third_party_pattern.sub(replacement_text, safe_reply)

    return safe_reply, safe_action
