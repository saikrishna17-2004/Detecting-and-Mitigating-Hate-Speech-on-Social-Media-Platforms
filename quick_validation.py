#!/usr/bin/env python3
"""Quick model validation and status."""

import sys
import os
sys.path.insert(0, 'backend')

from backend.models.detector import detector

# Quick test cases
tests = [
    ("वह हरामी है", "hi", True),
    ("यह अच्छा दिन है", "hi", False),
    ("সে হারামজাদা", "bn", True),
    ("এটি ভালো দিন", "bn", False),
    ("All terrorists must be eliminated", "en", True),
    ("This is a beautiful day", "en", False),
]

print("\n" + "="*70)
print("  HATE SPEECH DETECTION MODEL - QUICK VALIDATION")
print("="*70 + "\n")

passed = 0
failed = 0

for text, lang, expected in tests:
    result = detector.analyze(text)
    is_hate = result.get('is_hate_speech', False)
    conf = result.get('confidence', 0.0)
    
    if is_hate == expected:
        status = "✓ PASS"
        passed += 1
    else:
        status = "✗ FAIL"
        failed += 1
    
    print(f"{status} | {text[:50]:<50} (conf: {conf:.3f})")

accuracy = (passed / (passed +  failed) * 100) if (passed + failed) > 0 else 0
print(f"\n{'─'*70}")
print(f"Results: {passed}/{passed+failed} passed ({accuracy:.1f}%)")

print("\n" + "="*70)
if accuracy >= 80:
    print("✓ MODEL TRAINED - Ready for deployment")
    print(f"  Accuracy: {accuracy:.1f}%")
    print(f"  Lexicon terms: Check loading status above")
    sys.exit(0)
else:
    print("⚠ MODEL NEEDS REFINEMENT")
    print(f"  Current accuracy: {accuracy:.1f}%")
    sys.exit(1)
