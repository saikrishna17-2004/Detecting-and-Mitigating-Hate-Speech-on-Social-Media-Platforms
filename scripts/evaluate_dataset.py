import argparse
import csv
import json
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.models.detector import detector

TRUE_LABELS = {
    'hate', 'hateful', 'yes', 'true', '1', 'toxic', 'abusive', 'offensive'
}
FALSE_LABELS = {
    'not hate', 'non hate', 'non-hate', 'no', 'false', '0', 'clean', 'neutral', 'safe'
}

TEXT_COLUMN_CANDIDATES = [
    'Translated Post Description',
    'Post description',
    'text',
    'content',
    'message'
]


def normalize_label(raw):
    if raw is None:
        return None
    value = str(raw).strip().lower()
    if value in TRUE_LABELS:
        return 1
    if value in FALSE_LABELS:
        return 0
    return None


def pick_text_column(fieldnames):
    if not fieldnames:
        return None
    lookup = {name.lower(): name for name in fieldnames}
    for candidate in TEXT_COLUMN_CANDIDATES:
        if candidate.lower() in lookup:
            return lookup[candidate.lower()]
    return None


def safe_div(num, den):
    return (num / den) if den else 0.0


def main():
    parser = argparse.ArgumentParser(description='Evaluate hate/non-hate detection on a CSV dataset.')
    parser.add_argument('--source', default='data/Dataset.csv', help='Path to source CSV dataset')
    parser.add_argument('--label-column', default='Hate', help='Column containing hate labels')
    parser.add_argument('--text-column', default='', help='Column containing text to analyze (auto-detected if omitted)')
    parser.add_argument('--max-rows', type=int, default=0, help='Max rows to process (0 means all rows)')
    parser.add_argument('--predictions-out', default='reports/dataset_predictions.csv', help='CSV file to write per-row predictions')
    parser.add_argument('--summary-out', default='reports/dataset_eval_summary.json', help='JSON file to write aggregate metrics')
    args = parser.parse_args()

    source_path = Path(args.source)
    if not source_path.exists():
        raise FileNotFoundError(f'Dataset not found: {source_path}')

    predictions_path = Path(args.predictions_out)
    summary_path = Path(args.summary_out)
    predictions_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.parent.mkdir(parents=True, exist_ok=True)

    total_rows = 0
    processed_rows = 0
    labeled_rows = 0

    tp = fp = tn = fn = 0
    predicted_hate = 0
    predicted_non_hate = 0

    with source_path.open('r', encoding='utf-8-sig', newline='') as dataset_file, \
         predictions_path.open('w', encoding='utf-8', newline='') as predictions_file:
        reader = csv.DictReader(dataset_file)

        text_column = args.text_column.strip() or pick_text_column(reader.fieldnames)
        if not text_column:
            raise ValueError(
                'Could not detect a text column. Pass --text-column explicitly. '
                f'Available columns: {reader.fieldnames}'
            )

        output_fields = [
            'row_index', 'text_column', 'label_column', 'actual_label',
            'predicted_label', 'is_hate_speech', 'confidence', 'category', 'language', 'text_preview'
        ]
        writer = csv.DictWriter(predictions_file, fieldnames=output_fields)
        writer.writeheader()

        for row_index, row in enumerate(reader, start=1):
            total_rows += 1
            if args.max_rows > 0 and processed_rows >= args.max_rows:
                break

            text = (row.get(text_column) or '').strip()
            if not text:
                continue

            result = detector.analyze(text)
            is_hate = bool(result.get('is_hate_speech', False))
            predicted_label = 1 if is_hate else 0
            confidence = float(result.get('confidence', 0.0) or 0.0)
            category = result.get('category', '')
            language = result.get('language', '')

            if is_hate:
                predicted_hate += 1
            else:
                predicted_non_hate += 1

            actual_label = normalize_label(row.get(args.label_column))
            if actual_label is not None:
                labeled_rows += 1
                if actual_label == 1 and predicted_label == 1:
                    tp += 1
                elif actual_label == 0 and predicted_label == 1:
                    fp += 1
                elif actual_label == 0 and predicted_label == 0:
                    tn += 1
                elif actual_label == 1 and predicted_label == 0:
                    fn += 1

            writer.writerow({
                'row_index': row_index,
                'text_column': text_column,
                'label_column': args.label_column,
                'actual_label': '' if actual_label is None else ('hate' if actual_label == 1 else 'not_hate'),
                'predicted_label': 'hate' if predicted_label == 1 else 'not_hate',
                'is_hate_speech': is_hate,
                'confidence': round(confidence, 4),
                'category': category,
                'language': language,
                'text_preview': text[:200].replace('\n', ' ')
            })

            processed_rows += 1
            if processed_rows % 1000 == 0:
                print(f'Processed {processed_rows} rows...')

    precision = safe_div(tp, tp + fp)
    recall = safe_div(tp, tp + fn)
    f1 = safe_div(2 * precision * recall, precision + recall)
    accuracy = safe_div(tp + tn, labeled_rows)

    summary = {
        'source': str(source_path),
        'rows_seen': total_rows,
        'rows_processed': processed_rows,
        'rows_with_labels': labeled_rows,
        'text_column_used': text_column,
        'label_column_used': args.label_column,
        'predicted_hate': predicted_hate,
        'predicted_non_hate': predicted_non_hate,
        'confusion_matrix': {
            'tp': tp,
            'fp': fp,
            'tn': tn,
            'fn': fn
        },
        'metrics': {
            'accuracy': round(accuracy, 4),
            'precision': round(precision, 4),
            'recall': round(recall, 4),
            'f1': round(f1, 4)
        },
        'predictions_file': str(predictions_path),
        'generated_summary_file': str(summary_path)
    }

    with summary_path.open('w', encoding='utf-8') as summary_file:
        json.dump(summary, summary_file, indent=2)

    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
