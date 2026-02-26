#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Debug script to test failing detection cases"""

from backend.models.detector import detector

# Test cases that are failing
test_cases = [
    ('Tamil', 'ta', 'அவன் மூட்டாள்'),  # Tamil: Direct insult - should fail
    ('Telugu', 'te', 'అతను గాండూ'),     # Telugu: Direct slur - should fail
    ('Hindi', 'hi', 'वह आदमी हरामी है'),  # Hindi: Direct slur - should pass
    ('Marathi', 'mr', 'सर्व कुत्रे अयोग्य आहेत'),  # Marathi: Dehumanization - should fail
]

print("Testing detection on failing cases:\n")
for lang_name, lang_code, text in test_cases:
    result = detector.analyze(text)
    status = "✓ PASS" if result['is_hate_speech'] else "✗ FAIL"
    print(f"{status} | {lang_name}: \"{text}\"")
    print(f"  Detected: {result['is_hate_speech']}, Confidence: {result['confidence']:.4f}")
    print()
