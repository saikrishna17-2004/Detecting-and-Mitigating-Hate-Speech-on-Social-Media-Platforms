#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Debug the detection process for మంచిన"""

from backend.models.detector import detector

text = 'మంచిన'
print(f'Analyzing: "{text}"\n')

# Check language detection
lang = detector.detect_language(text)
print(f'1. Detected language: {lang}')

# Check translation
if lang != 'en':
    translated, was_translated = detector.translate_to_english(text, lang)
    print(f'2. Translation: "{translated}" (was_translated: {was_translated})')
else:
    print(f'2. No translation needed (English)')

# Check individual detection layers
if lang in detector.language_lexicons:
    lex_conf = detector._match_offensive_lexicon(text, lang)
    print(f'3. Lexicon match: {lex_conf}')

pattern_conf = detector._match_indian_language_patterns(text)
print(f'4. Pattern match: {pattern_conf}')

rule_conf, rule_hate = detector.rule_based_detection(text)
print(f'5. Rule-based: {rule_hate}, {rule_conf}')

# Check ML model if available
if hasattr(detector, 'model') and detector.model:
    print(f'6. ML model available: Yes')
else:
    print(f'6. ML model available: No')
