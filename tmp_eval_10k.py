import csv
from backend.models.detector import detector

MAX_ROWS = 10000

# Fast/offline evaluation mode
detector.translator = None
detector.translator_mode = None
detector.model_loaded = False

true_labels = {'hate', 'offensive', 'true', 'yes'}
false_labels = {'not hate', 'not offensive', 'clean', 'neutral', 'safe', 'false', 'no'}

def to_bool(label):
    s = str(label).strip().lower()
    if s in true_labels:
        return True
    if s in false_labels:
        return False
    return None

passed = failed = evaluated = 0
with open('data/train.csv', 'r', encoding='utf-8-sig', newline='') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if evaluated >= MAX_ROWS:
            break
        text = (row.get('text') or '').strip()
        label = to_bool(row.get('label'))
        if not text or label is None:
            continue
        pred = detector.analyze(text).get('is_hate_speech', False)
        if pred == label:
            passed += 1
        else:
            failed += 1
        evaluated += 1

acc = (passed / evaluated * 100) if evaluated else 0.0
print({'rows_evaluated': evaluated, 'passed': passed, 'failed': failed, 'accuracy': round(acc, 2)})
