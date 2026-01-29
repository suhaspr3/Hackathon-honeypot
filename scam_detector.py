import sys
import json

# 1. THE "BRAIN" - Your Lists of suspicious words
# You can add more words here later!
keywords = {
    "high_risk": ["otp", "cvv", "password", "bank account", "lottery", "winner", "urgent"],
    "medium_risk": ["click here", "verify", "update", "expired", "blocked", "refund"]
}

def analyze_message(message):
    score = 0
    evidence = []
    
    # Lowercase the message to make matching easier
    message_lower = message.lower()

    # 2. CHECK FOR KEYWORDS
    # Check High Risk (+20 points)
    for word in keywords["high_risk"]:
        if word in message_lower:
            score += 20
            evidence.append(f"High risk word found: '{word}'")

    # Check Medium Risk (+10 points)
    for word in keywords["medium_risk"]:
        if word in message_lower:
            score += 10
            evidence.append(f"Medium risk word found: '{word}'")

    # 3. DECIDE ACTION
    # If score is 50 or more, we hand off to the Agent (Shreya's part)
    action = "passive"
    if score >= 30: # Low threshold for testing
        action = "agent_handoff"

    # 4. PREPARE THE OUTPUT
    result = {
        "score": score,
        "action": action,
        "evidence": evidence,
        "original_message": message
    }
    
    # Print as JSON so Nikhil's server can read it
    print(json.dumps(result))

if __name__ == "__main__":
    # This line grabs the message Nikhil sends from the command line
    try:
        incoming_message = sys.argv[1]
        analyze_message(incoming_message)
    except IndexError:
        print(json.dumps({"error": "No message provided"}))