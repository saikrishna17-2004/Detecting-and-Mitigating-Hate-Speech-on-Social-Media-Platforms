#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test detector confidence levels on known hate speech"""

import sys
sys.path.insert(0, '/c/Users/nakka/Desktop/pp1')

from backend.models.detector import detector

# Test with various hate speech texts
test_cases = [
    ('Direct slur', 'This person is a terrorist'),
    ('Direct slur 2', 'You are subhuman vermin'),
    ('Violence advocacy', 'All infiltrators must be killed'),
    ('Group hate', 'Those people are animals'),
    ('Mild', 'I don\'t like that person'),
    ('Benign', 'This is a good day'),
]

print('Testing detector confidence levels:\n')
print(f'{"Text":<40} {"Detected":<10} {"Confidence":<12} {"Action (0.9 threshold)"}')
print('-' * 75)

for label, text in test_cases:
    result = detector.analyze(text)
    is_hate = result['is_hate_speech']
    conf = result['confidence']
    action = 'BLOCK' if (is_hate and conf >= 0.9) else 'ALLOW' if not is_hate else 'WARN'
    
    print(f'{label:<40} {str(is_hate):<10} {conf:<12.4f} {action}')

print(f'\nBLOCK_CONFIDENCE threshold: 0.9')
print(f'All results with confidence >= 0.92 should be blocked')
