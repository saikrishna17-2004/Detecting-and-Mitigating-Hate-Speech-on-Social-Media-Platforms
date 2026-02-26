#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Debug the Telugu false positive issue"""

from backend.models.detector import detector

text = 'నీవు మంచినట్లు ఉన్నావు'  # "You look nice"
result = detector.analyze(text)
print(f'Text: "{text}"')
print(f'Expected: False (benign positive statement)')
print(f'Detected: {result["is_hate_speech"]}, Confidence: {result["confidence"]:.4f}')
print()

# Also test without the specific phrase
test_texts = [
    'మంచిన',  # مंचिन - good/nice
    'నీవు మంచిభూతం',  # You are good
    'ఇది మంచిన రోజు',  # This is a good day
    'నీవు',   # You
    'ఉన్నావు',  # are
]

print('Testing individual terms:')
for test_text in test_texts:
    result = detector.analyze(test_text)
    print(f'  "{test_text}": hate={result["is_hate_speech"]}, conf={result["confidence"]:.4f}')
