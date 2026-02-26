#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Debug rule_based_detection for Telugu"""

from backend.models.detector import detector

texts = [
    'నీవు మంచినట్లు ఉన్నావు',  # Failing - should be safe
    'ఇది మంచిన రోజు',           # Working - safe
    'మంచినట్లు ఉన్నావు',          # Partial match
    'మంచిన',                       # Single word
]

for text in texts:
    print(f'\nText: "{text}"')
    is_hate, conf = detector.rule_based_detection(text)
    print(f'  Rule-based result: is_hate={is_hate}, conf={conf:.4f}')
    
    # Also check via analyze
    result = detector.analyze(text)
    print(f'  Analyze result: is_hate={result["is_hate_speech"]}, conf={result["confidence"]:.4f}')
