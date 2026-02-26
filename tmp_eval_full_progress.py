import csv
from backend.models.detector import detector

# Fast/offline mode for dataset pass
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

passed = failed = evaluated = total_rows = 0
with open('data/train.csv', 'r', encoding='utf-8-sig', newline='') as f:
    reader = csv.DictReader(f)
    for row in reader:
        total_rows += 1
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

        if evaluated % 5000 == 0:
            acc = (passed / evaluated * 100) if evaluated else 0.0
            print({'progress_evaluated': evaluated, 'accuracy': round(acc, 2)}, flush=True)

acc = (passed / evaluated * 100) if evaluated else 0.0
print({'rows_total': total_rows, 'rows_evaluated': evaluated, 'passed': passed, 'failed': failed, 'accuracy': round(acc, 2)}, flush=True)
