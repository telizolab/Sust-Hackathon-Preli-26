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
        safe_reply = "We have received your request. For your security, never share your PIN or OTP with anyone. A support agent will review your case shortly."
        return safe_reply, safe_action # Exit early since we override the entire string

    # Rule 2 (Financial Promise Shield): Replace sentences containing specific promises
    # Match a sentence ending with ., !, or ? (or end of string) containing the keywords
    promise_keywords = r"(will refund|have refunded|reversed|unblocked|recovered)"
    
    def promise_replacer(match):
        return "We are investigating your case. Any eligible amount will be returned through official channels."
        
    # Find sentences: start of string or after punctuation + spaces, then any chars except sentence endings, the keyword, more chars, then ending punctuation
    promise_pattern = re.compile(r'[^.!?]*\b' + promise_keywords + r'\b[^.!?]*[.!?]?', re.IGNORECASE)
    safe_reply = promise_pattern.sub(promise_replacer, safe_reply)
    safe_action = promise_pattern.sub(promise_replacer, safe_action)

    # Rule 3 (Third-Party Shield): Replace URLs or phone numbers in customer_reply
    # Simple heuristic for URLs and phones
    url_pattern = r"(https?://\S+|www\.\S+)"
    # Matches simple phone numbers e.g. +1-800-123-4567, 1234567890
    phone_pattern = r"(\+?\d{1,3}[-.\s]?\(?\d{2,3}\)?[-.\s]?\d{3}[-.\s]?\d{4}|\b\d{10}\b)"
    
    third_party_pattern = re.compile(rf"({url_pattern}|{phone_pattern})", re.IGNORECASE)
    
    replacement_text = "Please contact our official in-app support for further assistance."
    
    # The hackathon rule says "If customer_reply contains URLs... replace with"
    # We will replace the whole string if it contains unauthorized contact info, or just the matching part?
    # "replace with" usually implies replacing the whole string or the matched segment.
    # The prompt says "replace with", I'll replace the matched segment to be safe.
    safe_reply = third_party_pattern.sub(replacement_text, safe_reply)

    return safe_reply, safe_action
