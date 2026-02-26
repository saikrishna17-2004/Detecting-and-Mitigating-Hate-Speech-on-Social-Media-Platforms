#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Detailed debug of why a specific phrase isn't detected"""

import sys
sys.path.insert(0, '/c/Users/nakka/Desktop/pp1')

from backend.models.detector import detector

text = 'All infiltrators must be killed'

print(f'Analyzing: "{text}"\n')

# Check what's in the detector
print(f'1. Is "infiltrator" in offensive_keywords? {"infiltrator" in detector.offensive_keywords}')
print(f'2. Is "kill them" in offensive_phrases? {"kill them" in detector.offensive_phrases}')
print(f'3. Is "must be killed" in offensive_phrases? {"must be killed" in detector.offensive_phrases}')

# Check lexicon matching
lex_conf = detector._match_offensive_lexicon(text, 'en')
print(f'\n4. Lexicon confidence: {lex_conf}')

# Check pattern matching
pattern_conf = detector._match_indian_language_patterns(text)
print(f'5. Indian language pattern confidence: {pattern_conf}')

# Check rule-based
rule_is_hate, rule_conf = detector.rule_based_detection(text)
print(f'6. Rule-based result: is_hate={rule_is_hate}, conf={rule_conf}')

# Full analysis
result = detector.analyze(text)
print(f'\n7. Final result:')
print(f'   is_hate_speech: {result["is_hate_speech"]}')
print(f'   confidence: {result["confidence"]}')

# Test similar phrases
print(f'\n8. Testing similar phrases:')
phrases = [
    'Kill infiltrators',
    'infiltrators must die',
    'All infiltrators',
    'must be killed',
]

for phrase in phrases:
    result = detector.analyze(phrase)
    print(f'   "{phrase}": {result["is_hate_speech"]} (conf: {result["confidence"]:.4f})')
