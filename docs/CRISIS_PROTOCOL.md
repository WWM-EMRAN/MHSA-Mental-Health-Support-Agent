# Crisis Protocol Documentation

## Overview

This document outlines the crisis detection and response protocol implemented in MHSA (Mental Health Support Agent). The safety of users is our top priority.

## Crisis Detection System

### Detection Levels

MHSA uses a three-tier crisis detection system:

#### 1. Critical Level (Confidence: 1.0)
**Triggers:**
- Direct suicide statements ("kill myself", "end my life", "want to die")
- Specific planning language ("suicide plan", "ending it all")
- Immediate risk indicators

**Keywords:**
- suicide, suicidal
- kill myself
- end my life
- want to die
- better off dead
- no reason to live
- can't go on
- ending it all

#### 2. High Level (Confidence: 0.8)
**Triggers:**
- Self-harm mentions
- Overdose or method references
- High-risk behavior indicators

**Keywords:**
- self harm, self-harm
- cut myself, cutting
- hurt myself, harm myself
- overdose, pills
- die, death

#### 3. Medium Level (Confidence: 0.5)
**Triggers:**
- Multiple distress indicators (2+ keywords required)
- Cumulative concerning patterns

**Keywords:**
- hopeless, helpless
- worthless, burden
- give up
- can't cope
- no point
- empty inside
- numb
- desperate

### Detection Algorithm

```python
def detect_crisis(message: str) -> dict:
    1. Convert message to lowercase
    2. Check for critical keywords (immediate match)
    3. If found: return CRITICAL level
    4. Check for high-risk keywords
    5. If found: return HIGH level
    6. Check for medium-risk keywords
    7. If 2+ found: return MEDIUM level
    8. Otherwise: return NO CRISIS
```

## Crisis Response Protocol

### When Crisis is Detected

#### Immediate Actions

1. **Acknowledge Seriousness**
   - Agent response includes immediate acknowledgment
   - Validates user's feelings
   - Expresses care and concern

2. **Provide Crisis Resources**
   - Display crisis hotline information prominently
   - Show multiple contact options (phone, text, chat)
   - Emphasize 24/7 availability

3. **Modify Agent Response**
   - System prompt includes crisis handling instructions
   - Agent prioritized immediate safety
   - Response is more directive and supportive

4. **Log Incident**
   - Crisis detection logged in database
   - Message flagged with `crisis_keywords_detected = True`
   - Conversation marked with `crisis_detected = True`

#### Crisis Resource Display

```
⚠️  CRISIS ALERT DETECTED ⚠️

CRISIS RESOURCES
================

If you're experiencing a mental health crisis:

• US Crisis Line: 988 (Suicide & Crisis Lifeline)
• US Crisis Text: Text HOME to 741741 (Crisis Text Line)
• International: +1-800-273-8255
• Emergency: 911 (US) or local emergency services
• Online Chat: https://988lifeline.org/chat
• Trevor Project (LGBTQ+ Youth): 1-866-488-7386
• Veterans Crisis: 988 then press 1, or text 838255

You are not alone. Help is available 24/7.
```

### Crisis Response Guidelines

#### DO:
- ✅ Take every crisis indication seriously
- ✅ Provide immediate resources
- ✅ Encourage professional help
- ✅ Express care and support
- ✅ Stay calm and non-judgmental
- ✅ Offer to help user contact crisis services
- ✅ Validate feelings while encouraging action

#### DON'T:
- ❌ Dismiss or minimize concerns
- ❌ Argue about whether feelings are valid
- ❌ Promise everything will be okay
- ❌ Leave user without resources
- ❌ Attempt to diagnose
- ❌ Prescribe treatment
- ❌ Panic or show distress

## Example Crisis Responses

### Critical Level Response

**User:** "I want to kill myself"

**Agent Response:**
```
I'm very concerned about what you're sharing with me. Your safety is the 
most important thing right now.

Please reach out for immediate help:
• Call or text 988 (Suicide & Crisis Lifeline) - Available 24/7
• If you're in immediate danger, call 911 or go to the nearest emergency room

I care about what happens to you, and I want you to stay safe. These crisis 
counselors are trained to help in exactly this situation. Will you reach out 
to them right now?

You are not alone, and there are people who want to help you through this.
```

### High Level Response

**User:** "I've been cutting myself"

**Agent Response:**
```
Thank you for trusting me with this. Self-harm is a sign that you're dealing 
with very difficult feelings, and I want you to get the support you deserve.

Please consider reaching out to:
• 988 Suicide & Crisis Lifeline (call or text)
• Crisis Text Line: Text HOME to 741741

These services can provide immediate support and help you find healthier ways 
to cope with these feelings. Would you be willing to reach out to them?

In the meantime, please ensure any wounds are properly cared for, and if you 
need medical attention, don't hesitate to get it.
```

### Medium Level Response

**User:** "I feel so hopeless and worthless. There's no point anymore"

**Agent Response:**
```
I hear that you're going through a really difficult time right now, and these 
feelings sound overwhelming. It's important that you know:

1. These feelings, while very real and painful, are not permanent
2. You deserve support and care
3. Help is available

I encourage you to reach out to a crisis counselor who can provide more 
comprehensive support:
• 988 Suicide & Crisis Lifeline
• Crisis Text Line: Text HOME to 741741

Would you also consider talking to a therapist or counselor? They can help 
you work through these feelings in a safe, supportive environment.

What you're feeling matters, and you matter.
```

## Technical Implementation

### Code Flow

```python
# In MentalHealthAgent.generate_response()

# 1. Detect crisis
crisis_info = self.crisis_detector.detect_crisis(user_message)

# 2. Modify messages if crisis detected
if crisis_info['crisis_detected']:
    crisis_instruction = {
        "role": "system",
        "content": f"CRITICAL: Crisis detected ({crisis_info['level']}). "
                  f"Immediately provide crisis resources and support. "
                  f"Keywords detected: {', '.join(crisis_info['keywords_found'])}"
    }
    messages.insert(1, crisis_instruction)

# 3. Generate response with crisis context
response = self.client.chat.completions.create(...)

# 4. Return with crisis metadata
return {
    'response': agent_response,
    'crisis_detected': crisis_info['crisis_detected'],
    'crisis_level': crisis_info['level'],
    'crisis_keywords': crisis_info['keywords_found']
}
```

### Database Logging

Crisis incidents are logged in two places:

1. **Message Table**
   - `crisis_keywords_detected` field set to True
   - Individual message flagged

2. **Conversation Table**
   - `crisis_detected` field set to True
   - Entire conversation marked for review

## Crisis Resources Reference

### United States

| Service | Contact | Description |
|---------|---------|-------------|
| 988 Lifeline | 988 | 24/7 suicide & crisis support |
| Crisis Text Line | Text HOME to 741741 | Free 24/7 text support |
| SAMHSA | 1-800-662-4357 | Substance abuse & mental health |
| Trevor Project | 1-866-488-7386 | LGBTQ+ youth support |
| Veterans Line | 988, press 1 | Veterans crisis support |
| Emergency | 911 | Immediate danger |

### International

| Region | Contact | Description |
|--------|---------|-------------|
| Canada | 1-833-456-4566 | Suicide prevention |
| UK | 116 123 | Samaritans |
| Australia | 13 11 14 | Lifeline |
| EU | 112 | Emergency services |
| International | [IASP](https://www.iasp.info/resources/Crisis_Centres/) | Global directory |

## Continuous Improvement

### Monitoring

- Review flagged conversations regularly
- Analyze false positive/negative rates
- Update keyword lists based on patterns
- Gather feedback from crisis counselors

### Updates

Crisis detection system should be reviewed and updated:
- Quarterly keyword review
- Annual protocol assessment
- After any incident
- Based on new research

## Training and Guidelines

### For Developers

- Understand crisis detection logic
- Test crisis scenarios thoroughly
- Never disable crisis detection
- Prioritize safety over features

### For Users

- MHSA is not a replacement for crisis services
- Always have crisis resources available
- Know how to contact emergency services
- Encourage others to seek professional help

## Legal and Ethical Considerations

### Limitations

1. MHSA cannot:
   - Contact emergency services on user's behalf
   - Physically intervene
   - Provide 24/7 human monitoring
   - Guarantee detection of all crises

2. Users must understand:
   - This is an AI tool, not a human therapist
   - Crisis services provide human support
   - In emergency, call 911 or local emergency services

### Data Handling

- Crisis flags stored securely
- User privacy maintained
- No data shared without consent
- Logs used only for safety improvement

## Testing Crisis Detection

### Test Cases

```python
# Critical level tests
assert detect_crisis("I want to kill myself")['level'] == 'critical'
assert detect_crisis("planning my suicide")['level'] == 'critical'

# High level tests
assert detect_crisis("I'm cutting myself")['level'] == 'high'
assert detect_crisis("thinking about overdose")['level'] == 'high'

# Medium level tests
assert detect_crisis("I feel hopeless and worthless")['level'] == 'medium'
assert detect_crisis("I'm desperate and can't cope")['level'] == 'medium'

# No crisis tests
assert detect_crisis("I'm feeling a bit sad")['crisis_detected'] == False
assert detect_crisis("Having a bad day")['crisis_detected'] == False
```

## Contact for Concerns

If you have concerns about the crisis detection system:
1. Open an issue on GitHub
2. Contact project maintainers
3. Report any false negatives immediately

---

**Remember:** The goal is to connect users with professional help as quickly as possible. When in doubt, err on the side of caution and provide crisis resources.
