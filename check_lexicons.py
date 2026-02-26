#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Check if newly added terms are in lexicon files"""

import os

# Check Telugu lexicon
te_file = 'data/hate_keywords_te.txt'
with open(te_file, 'r', encoding='utf-8') as f:
    te_terms = [line.strip() for line in f if line.strip() and not line.startswith('#')]
print(f'Telugu terms ({len(te_terms)}):')
if 'గాండూ' in te_terms:
    print('  ✓ గాండూ found in Telugu lexicon')
else:
    print('  ✗ గాండూ NOT in Telugu lexicon')
    print(f'  Last 5 terms: {te_terms[-5:]}')

# Check Tamil lexicon  
ta_file = 'data/hate_keywords_ta.txt'
with open(ta_file, 'r', encoding='utf-8') as f:
    ta_terms = [line.strip() for line in f if line.strip() and not line.startswith('#')]
print(f'\nTamil terms ({len(ta_terms)}):')
if 'மூட்டாள்' in ta_terms:
    print('  ✓ மூட்டாள் found in Tamil lexicon')
else:
    print('  ✗ மூட்டாள் NOT in Tamil lexicon')
    print(f'  Last 5 terms: {ta_terms[-5:]}')

# Check Marathi lexicon
mr_file = 'data/hate_keywords_mr.txt'
with open(mr_file, 'r', encoding='utf-8') as f:
    mr_terms = [line.strip() for line in f if line.strip() and not line.startswith('#')]
print(f'\nMarathi terms ({len(mr_terms)}):')
if 'कुत्रा' in mr_terms:
    print('  ✓ कुत्रा found in Marathi lexicon')
if 'कुत्रे' in mr_terms:
    print('  ✓ कुत्रे found in Marathi lexicon')
has_kuthr = any('कुत्र' in t for t in mr_terms)
print(f'  Contains kuthr: {has_kuthr}')
print(f'  Last 5 terms: {mr_terms[-5:]}')
