import sys
import json
import re

# --- CONFIGURATION ---
# 1. KEYWORDS: Simple word matching
keywords = {
    "high_risk": ["otp", "cvv", "password", "bank account", "lottery", "winner", "urgent", "pay tm", "gpay", "phonepe"],
    "medium_risk": ["click here", "verify", "update", "expired", "blocked", "refund", "sir", "madam", "kyc"]
}
THRESHOLD = 50

def analyze_message(message, current_total_score):
    score_increment = 0
    evidence = []
    message_lower = message.lower()

    # 2. KEYWORD CHECK
    for word in keywords["high_risk"]:
        if word in message_lower:
            score_increment += 20
            evidence.append(f"High risk keyword: '{word}'")

    for word in keywords["medium_risk"]:
        if word in message_lower:
            score_increment += 10
            evidence.append(f"Medium risk keyword: '{word}'")

    # 3. REGEX PATTERNS (The "Smart" Detection)
    # Detects any 10-digit number (Phone/Mobile)
    if re.search(r'\b\d{10}\b', message):
        score_increment += 15
        evidence.append("Pattern match: 10-digit number detected")
    
    # Detects UPI IDs (e.g., name@okicici)
    if re.search(r'[\w\.-]+@[\w\.-]+', message):
        score_increment += 25
        evidence.append("Pattern match: UPI ID detected")

    # 4. ACCUMULATE SCORE (Memory)
    new_total_score = current_total_score + score_increment

    # 5. DECIDE STATE
    state = "passive"
    if new_total_score >= THRESHOLD:
        state = "agent_handoff"

    # 6. OUTPUT
    result = {
        "score_added": score_increment,
        "total_score": new_total_score,
        "state": state,
        "evidence": evidence
    }
    
    print(json.dumps(result))

if __name__ == "__main__":
    try:
        # Argument 1: The Message
        incoming_message = sys.argv[1]
        
        # Argument 2: The Previous Score (Nikhil sends this!)
        try:
            previous_score = int(sys.argv[2])
        except (IndexError, ValueError):
            previous_score = 0
            
        analyze_message(incoming_message, previous_score)
        
    except Exception as e:
        # Failsafe JSON so server doesn't crash
        print(json.dumps({"error": str(e), "score_added": 0, "total_score": 0, "state": "passive"}))
