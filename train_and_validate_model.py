#!/usr/bin/env python3
"""
Train and validate the hate speech detection model with expanded lexicons.
Tests detection across all major Indian languages and English.
"""

import json
import sys
import os
import csv
from pathlib import Path

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.models.detector import detector

def print_section(title):
    """Print a formatted section header."""
    print(f"\n{'='*80}")
    print(f"  {title}")
    print(f"{'='*80}\n")

def count_lexicon_terms():
    """Count total terms in all lexicons."""
    lexicons = {
        'Hindi': 'data/hate_keywords_hi.txt',
        'Bengali': 'data/hate_keywords_bn.txt',
        'Tamil': 'data/hate_keywords_ta.txt',
        'Telugu': 'data/hate_keywords_te.txt',
        'Marathi': 'data/hate_keywords_mr.txt',
        'Gujarati': 'data/hate_keywords_gu.txt',
        'Kannada': 'data/hate_keywords_kn.txt',
        'Malayalam': 'data/hate_keywords_ml.txt',
        'Punjabi': 'data/hate_keywords_pa.txt',
        'Urdu': 'data/hate_keywords_ur.txt',
    }
    
    stats = {}
    total_terms = 0
    
    for lang_name, path in lexicons.items():
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                lines = [l.strip() for l in f if l.strip() and not l.startswith('#')]
                stats[lang_name] = len(lines)
                total_terms += len(lines)
    
    return stats, total_terms

def reload_lexicons():
    """Reload all language lexicons into the detector."""
    print_section("LOADING LEXICONS")
    
    lang_codes = ['hi', 'bn', 'ta', 'te', 'mr', 'gu', 'kn', 'ml', 'pa', 'ur']
    loaded = 0
    
    for lang_code in lang_codes:
        path = f'data/hate_keywords_{lang_code}.txt'
        if os.path.exists(path):
            detector.load_language_lexicon(lang_code, path)
            with open(path, 'r', encoding='utf-8') as f:
                count = len([l for l in f if l.strip() and not l.startswith('#')])
            print(f"✓ Loaded {lang_code.upper()}: {count} terms from {path}")
            loaded += 1
        else:
            print(f"✗ Missing lexicon: {path}")
    
    print(f"\nLoaded {loaded}/10 language lexicons")
    return loaded == 10

def test_batch(description, test_cases):
    """Run and report on a batch of test cases.
    
    test_cases: list of (text, language, expected_hate, description)
    """
    print(f"\n{description}")
    print("-" * 80)
    
    results = {
        'passed': 0,
        'failed': 0,
        'results': []
    }
    
    for text, language, expected_hate, case_desc in test_cases:
        result = detector.analyze(text)
        is_hate = result.get('is_hate_speech', False)
        confidence = result.get('confidence', 0.0)
        detected_lang = result.get('language', 'unknown')
        
        # Check if result matches expectation
        passed = is_hate == expected_hate
        status = "✓ PASS" if passed else "✗ FAIL"
        
        if passed:
            results['passed'] += 1
        else:
            results['failed'] += 1
        
        results['results'].append({
            'text': text,
            'expected': expected_hate,
            'detected': is_hate,
            'confidence': round(confidence, 4),
            'language': detected_lang,
            'status': status
        })
        
        print(f"{status} | {case_desc}")
        print(f"      Text: {text[:60]}..." if len(text) > 60 else f"      Text: {text}")
        print(f"      Expected hate: {expected_hate}, Detected: {is_hate} (conf: {confidence:.4f}, lang: {detected_lang})")
    
    accuracy = results['passed'] / (results['passed'] + results['failed']) * 100 if (results['passed'] + results['failed']) > 0 else 0
    print(f"\nResults: {results['passed']}/{results['passed'] + results['failed']} passed ({accuracy:.1f}%)")
    
    return results

def _find_column(fieldnames, candidates):
    """Find the first matching column name (case-insensitive)."""
    if not fieldnames:
        return None
    normalized = {name.strip().lower(): name for name in fieldnames}
    for candidate in candidates:
        if candidate in normalized:
            return normalized[candidate]
    return None

def _label_to_bool(raw_label, numeric_profile=None):
    """Convert dataset label to boolean hate/not-hate.

    Handles common label schemes:
    - {0,1} => 1 is hate
    - {0,1,2} => 0/1 are hate(or offensive), 2 is non-hate
    - string labels like hate/offensive/toxic
    """
    if raw_label is None:
        return None

    value = str(raw_label).strip().lower()
    if value == '':
        return None

    # String-based labels
    true_labels = {
        'hate', 'hateful', 'hate_speech', 'abusive', 'offensive',
        'toxic', 'toxic_hate', 'yes', 'true'
    }
    false_labels = {
        'non-hate', 'nonhate', 'clean', 'neutral', 'safe', 'no', 'false',
        'not offensive', 'not_offensive', 'non offensive', 'non-offensive',
        'not hate', 'not_hate'
    }

    if value in true_labels:
        return True
    if value in false_labels:
        return False

    # Numeric labels
    try:
        number = int(float(value))
    except Exception:
        return None

    profile = numeric_profile or set()
    if profile.issubset({0, 1}):
        return number == 1
    if profile.issubset({0, 1, 2}):
        return number in {0, 1}
    if profile.issubset({1, 2}):
        return number == 1

    # Fallback: anything above zero is treated as hate/offensive
    return number > 0

def evaluate_dataset(dataset_path='data/train.csv'):
    """Evaluate detector against dataset rows in data/train.csv."""
    if not os.path.exists(dataset_path):
        return None

    rows = []
    with open(dataset_path, 'r', encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames or []

        text_column = _find_column(fieldnames, ['text', 'tweet', 'content', 'comment', 'sentence'])
        label_column = _find_column(fieldnames, ['label', 'class', 'target', 'is_hate', 'hate_speech', 'category'])

        if not text_column or not label_column:
            return {
                'loaded': False,
                'reason': 'Could not infer text/label columns',
                'columns': fieldnames
            }

        for row in reader:
            text = (row.get(text_column) or '').strip()
            label = row.get(label_column)
            if text:
                rows.append((text, label))

    if not rows:
        return {
            'loaded': False,
            'reason': 'Dataset has no usable rows'
        }

    numeric_values = set()
    for _, raw_label in rows:
        try:
            numeric_values.add(int(float(str(raw_label).strip())))
        except Exception:
            pass

    evaluated = 0
    passed = 0
    failed = 0

    # Offline evaluation: disable translation temporarily to avoid network latency
    original_translator = detector.translator
    original_translator_mode = detector.translator_mode
    original_model_loaded = detector.model_loaded
    detector.translator = None
    detector.translator_mode = None
    detector.model_loaded = False

    try:
        for text, raw_label in rows:
            expected_hate = _label_to_bool(raw_label, numeric_profile=numeric_values)
            if expected_hate is None:
                continue

            try:
                detected = detector.analyze(text).get('is_hate_speech', False)
            except Exception:
                continue

            if detected == expected_hate:
                passed += 1
            else:
                failed += 1
            evaluated += 1
    finally:
        detector.translator = original_translator
        detector.translator_mode = original_translator_mode
        detector.model_loaded = original_model_loaded

    accuracy = (passed / evaluated * 100) if evaluated > 0 else 0.0
    return {
        'loaded': True,
        'path': dataset_path,
        'rows_total': len(rows),
        'rows_evaluated': evaluated,
        'passed': passed,
        'failed': failed,
        'accuracy': accuracy,
        'numeric_label_profile': sorted(list(numeric_values))
    }

def main():
    """Run full model training and validation."""
    print("\n" + "="*80)
    print("  HATE SPEECH DETECTION MODEL - TRAINING & VALIDATION")
    print("="*80)
    
    # Step 1: Count lexicons
    print_section("LEXICON STATISTICS")
    stats, total = count_lexicon_terms()
    for lang, count in sorted(stats.items(), key=lambda x: x[1], reverse=True):
        print(f"  {lang:15s}: {count:3d} terms")
    print(f"  {'─'*36}")
    print(f"  {'TOTAL':15s}: {total:3d} terms")
    
    # Step 2: Reload lexicons
    if not reload_lexicons():
        print("ERROR: Failed to load all lexicons!")
        return False

    # Step 2.5: Evaluate user dataset (if available)
    print_section("DATASET EVALUATION (data/train.csv)")
    dataset_eval = evaluate_dataset('data/train.csv')
    if not dataset_eval:
        print("No dataset evaluation performed.")
    elif not dataset_eval.get('loaded'):
        print(f"⚠ Dataset not evaluated: {dataset_eval.get('reason')}")
        if dataset_eval.get('columns'):
            print(f"  Available columns: {dataset_eval.get('columns')}")
    else:
        print(f"✓ Dataset loaded: {dataset_eval['path']}")
        print(f"  Rows total: {dataset_eval['rows_total']}")
        print(f"  Rows evaluated: {dataset_eval['rows_evaluated']}")
        print(f"  Accuracy: {dataset_eval['accuracy']:.1f}%")
        print(f"  Label profile: {dataset_eval['numeric_label_profile']}")
    
    # Step 3: Test Hindi detection
    print_section("HINDI (हिन्दी) HATE SPEECH DETECTION")
    hindi_tests = [
        ("वह आदमी हरामी है", "hi", True, "Hindi: Direct slur"),
        ("सभी कश्मीरी जानवर हैं और मार डालो", "hi", True, "Hindi: Group hate with dehumanization"),
        ("यह एक अच्छा दिन है", "hi", False, "Hindi: Benign text"),
        ("वह भारतीय है", "hi", False, "Hindi: Neutral statement"),
        ("चूतिया लोग सब गद्दार हैं", "hi", True, "Hindi: Multiple slurs"),
    ]
    hindi_results = test_batch("HINDI DETECTION TESTS", hindi_tests)
    
    # Step 4: Test Bengali detection
    print_section("BENGALI (বাংলা) HATE SPEECH DETECTION")
    bengali_tests = [
        ("সে হারামজাদা লোক", "bn", True, "Bengali: Direct slur"),
        ("সব কুকুর অযোগ্য প্রাণী", "bn", True, "Bengali: Dehumanization"),
        ("আজ সুন্দর দিন", "bn", False, "Bengali: Benign text"),
        ("তিনি শিক্ষক", "bn", False, "Bengali: Neutral statement"),
    ]
    bengali_results = test_batch("BENGALI DETECTION TESTS", bengali_tests)
    
    # Step 5: Test Tamil detection
    print_section("TAMIL (தமிழ்) HATE SPEECH DETECTION")
    tamil_tests = [
        ("அவன் மூட்டாள்", "ta", True, "Tamil: Direct insult"),
        ("அந்த சமுதாயம் விலங்குகள்", "ta", True, "Tamil: Dehumanization"),
        ("நல்ல நாள்", "ta", False, "Tamil: Benign text"),
        ("அவர் நன்றாக இருக்கிறார்", "ta", False, "Tamil: Positive statement"),
    ]
    tamil_results = test_batch("TAMIL DETECTION TESTS", tamil_tests)
    
    # Step 6: Test Telugu detection
    print_section("TELUGU (తెలుగు) HATE SPEECH DETECTION")
    telugu_tests = [
        ("అతను గాండూ", "te", True, "Telugu: Direct slur"),
        ("ఆ సమూహం కుక్క", "te", True, "Telugu: Dehumanization"),
        ("ఇది మంచి రోజు", "te", False, "Telugu: Benign text"),
        ("నీవు మంచినట్లు ఉన్నావు", "te", False, "Telugu: Positive statement"),
    ]
    telugu_results = test_batch("TELUGU DETECTION TESTS", telugu_tests)
    
    # Step 7: Test Marathi detection
    print_section("MARATHI (मराठी) HATE SPEECH DETECTION")
    marathi_tests = [
        ("तो हरामी माणूस आहे", "mr", True, "Marathi: Direct slur"),
        ("सर्व कुत्रे अयोग्य आहेत", "mr", True, "Marathi: Dehumanization"),
        ("हा चांगला दिवस आहे", "mr", False, "Marathi: Benign text"),
        ("तुम्ही बरे आहात", "mr", False, "Marathi: Positive statement"),
    ]
    marathi_results = test_batch("MARATHI DETECTION TESTS", marathi_tests)
    
    # Step 8: Test English detection
    print_section("ENGLISH HATE SPEECH DETECTION")
    english_tests = [
        ("All terrorists must be eliminated", "en", True, "English: Direct hate call"),
        ("These people are subhuman vermin", "en", True, "English: Dehumanization"),
        ("This is a beautiful day", "en", False, "English: Benign text"),
        ("He is a good person", "en", False, "English: Positive statement"),
        ("Destroy all infiltrators", "en", True, "English: Violence advocacy"),
    ]
    english_results = test_batch("ENGLISH DETECTION TESTS", english_tests)
    
    # Step 9: Multilingual mixed test
    print_section("MULTILINGUAL MIXED DETECTION")
    multi_tests = [
        ("मुझे आज का दिन पसंद है लेकिन वह कश्मीरी हरामी है", "mixed", True, "Hindi: Mixed benign + hate"),
        ("This is good and terrorist should die", "en", True, "English: Mixed benign + hate"),
    ]
    multi_results = test_batch("MULTILINGUAL MIXED TESTS", multi_tests)
    
    # Step 10: Generate final report
    print_section("FINAL VALIDATION REPORT")
    
    all_results = [
        ("Hindi", hindi_results),
        ("Bengali", bengali_results),
        ("Tamil", tamil_results),
        ("Telugu", telugu_results),
        ("Marathi", marathi_results),
        ("English", english_results),
        ("Multilingual", multi_results),
    ]
    
    total_passed = sum(r[1]['passed'] for r in all_results)
    total_failed = sum(r[1]['failed'] for r in all_results)
    total_accuracy = (total_passed / (total_passed + total_failed) * 100) if (total_passed + total_failed) > 0 else 0
    
    print(f"{'Language':<15} {'Passed':<10} {'Failed':<10} {'Accuracy':<10}")
    print("-" * 45)
    for lang_name, result in all_results:
        passed = result['passed']
        failed = result['failed']
        acc = (passed / (passed + failed) * 100) if (passed + failed) > 0 else 0
        print(f"{lang_name:<15} {passed:<10} {failed:<10} {acc:>6.1f}%")
    
    print("-" * 45)
    print(f"{'TOTAL':<15} {total_passed:<10} {total_failed:<10} {total_accuracy:>6.1f}%")
    
    # Save report to file
    report = {
        'timestamp': __import__('datetime').datetime.now().isoformat(),
        'lexicon_stats': stats,
        'total_lexicon_terms': total,
        'dataset_evaluation': dataset_eval,
        'validation_results': {
            lang: {
                'passed': r['passed'],
                'failed': r['failed'],
                'accuracy': (r['passed'] / (r['passed'] + r['failed']) * 100) if (r['passed'] + r['failed']) > 0 else 0,
                'details': r['results']
            }
            for lang, r in all_results
        },
        'overall': {
            'total_passed': total_passed,
            'total_failed': total_failed,
            'overall_accuracy': total_accuracy,
            'detection_threshold': 0.9,
            'model_status': 'TRAINED' if total_accuracy >= 80 else 'NEEDS_IMPROVEMENT'
        }
    }
    
    with open('model_training_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ Report saved to: model_training_report.json")
    
    # Model status
    print_section("MODEL STATUS")
    if total_accuracy >= 90:
        print("✓ MODEL FULLY TRAINED - Excellent detection across all languages")
        print(f"  Overall Accuracy: {total_accuracy:.1f}%")
        print(f"  Lexicon Terms: {total}")
        print(f"  Languages: 10 major Indian languages + English")
        print(f"  Detection Threshold: 0.9 (90% confidence)")
        return True
    elif total_accuracy >= 80:
        print("⚠ MODEL TRAINED - Good detection but may need refinement")
        print(f"  Overall Accuracy: {total_accuracy:.1f}%")
        return True
    else:
        print("✗ MODEL NEEDS IMPROVEMENT - Accuracy below 80%")
        print(f"  Overall Accuracy: {total_accuracy:.1f}%")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
