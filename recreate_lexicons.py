# -*- coding: utf-8 -*-
"""Recreate language lexicons with proper UTF-8 encoding"""
import os

os.chdir('data')

# Telugu lexicon - properly encoded
TELUGU_TERMS = [
    'కుక్క', 'పంది', 'దుష్టుడు', 'జంతువు', 'నీచుడు', 
    'ఉగ్రవాది', 'దేశద్రోహి', 'నేరస్తుల సమూహం', 'కొడుకు', 'వేశ్య',
    'రాక్షసుడు', 'దయ్యం', 'అసురుడు', 'కసాయి', 'అడవి జంతువు',
    'చంపేయండి', 'కాల్చేయండి', 'తరిమేయండి', 'చట్టవిరుద్ధ చొరబాటుదారులు', 
    'దేశ శత్రువులు', 'ద్రోహులు', 'హంతకుడు', 'రక్తపిపాసి', 'అసభ్యమైన జంతువు',
    'నాశనం చేయండి', 'అంతం చేయండి', 'వధించండి', 'గాండూ'
]

# Tamil lexicon - properly encoded  
TAMIL_TERMS = [
    'பயங்கரவาதி', 'புண்ணையன்', 'கணவாதி', 'விலங்கு', 'விலங்குகள்',
    'மூட்டாள்', 'கரடு', 'பாவம்', 'தீய', 'கொடிய', 'கொடியவன்',
    'சீரழிப்பு', 'தாழ்ந்த', 'மனிதம் இல்லாதவர்', 'அபர்ணவாத',
    'ஆணவம்', 'கொலை', 'எதிரி', 'சாவ', 'குற்றம்', 
    'மண்டை', 'பாவம்', 'தீயவர்', 'தாழ்', 'குற்றவாளி'
]

# Marathi lexicon - properly encoded
MARATHI_TERMS = [
    'कतर', 'डककर', 'हलकट', 'जनवर', 'नच', 'दहशतवद',
    'दशदरह', 'गनगर समदय', 'रड', 'कत', 'भडव', 'गड',
    'हजड', 'रखश', 'असर', 'घणसपद जव', 'कशपपकर', 'दहशत',
    'चप', 'कलच', 'तरमय', 'चटटवरदध', 'दश शतर', 'दरह',
    'हतक', 'रकत पपस', 'असभय जव', 'नशन', 'कुत्रे', 'कुत्रा'
]

# Write Telugu lexicon
with open('hate_keywords_te.txt', 'w', encoding='utf-8') as f:
    f.write('# Telugu hate speech keywords/phrases\n')
    f.write('# One term per line; lines starting with # are comments\n')
    f.write('# Only most severe, universally offensive terms\n\n')
    for term in TELUGU_TERMS:
        f.write(term + '\n')
print(f'✓ Created Telugu lexicon with {len(TELUGU_TERMS)} terms')

# Write Tamil lexicon
with open('hate_keywords_ta.txt', 'w', encoding='utf-8') as f:
    f.write('# Tamil hate speech keywords/phrases\n')
    f.write('# One term per line; lines starting with # are comments\n\n')
    for term in TAMIL_TERMS:
        f.write(term + '\n')
print(f'✓ Created Tamil lexicon with {len(TAMIL_TERMS)} terms')

# Write Marathi lexicon
with open('hate_keywords_mr.txt', 'w', encoding='utf-8') as f:
    f.write('# Marathi hate speech keywords/phrases\n')
    f.write('# One term per line; lines starting with # are comments\n\n')
    for term in MARATHI_TERMS:
        f.write(term + '\n')
print(f'✓ Created Marathi lexicon with {len(MARATHI_TERMS)} terms')
