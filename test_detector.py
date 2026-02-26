#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Quick test of hate speech detector"""

from backend.models.detector import detector

# Test with known hate speech
test_cases = [
    'This person is a terrorist and must die',
    'All terrorists must be eliminated',
    'You are a subhuman vermin',
    'Kill all infiltrators',
    'good day',  # Should NOT be detected
]

print('Testing detector with known hate speech:\n')
for text in test_cases:
    result = detector.analyze(text)
    status = '✓ DETECTED' if result['is_hate_speech'] else '✗ NOT DETECTED'
    print(f'{status}: "{text}"')
    print(f'  Confidence: {result["confidence"]:.4f}, Language: {result["language"]}\n')
    
print(f'\nLexicon terms loaded:')
for lang, (keywords, phrases) in detector.language_lexicons.items():
    print(f'  {lang}: {len(keywords)} keywords, {len(phrases)} phrases')

print(f'\nEnglish offensive keywords count: {len(detector.offensive_keywords)}')
print(f'English offensive phrases count: {len(detector.offensive_phrases)}')
print(f'Sample English keywords: {list(detector.offensive_keywords)[:10]}')
