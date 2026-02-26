#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify English lexicon is loaded"""

from backend.models.detector import detector

print(f'English keywords loaded: {len(detector.offensive_keywords)}')
print(f'English phrases loaded: {len(detector.offensive_phrases)}')
print(f'\nFirst 20 keywords:')
for kw in sorted(list(detector.offensive_keywords))[:20]:
    print(f'  - {kw}')

print(f'\nFirst 5 phrases:')
for phrase in sorted(list(detector.offensive_phrases))[:5]:
    print(f'  - {phrase}')

print(f'\nKey checks:')
print(f'  "infiltrator" in keywords? {"infiltrator" in detector.offensive_keywords}')
print(f'  "must be killed" in phrases? {"must be killed" in detector.offensive_phrases}')
print(f'  "terrorist" in keywords? {"terrorist" in detector.offensive_keywords}')
