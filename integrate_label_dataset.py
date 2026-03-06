import argparse
import os

import pandas as pd


def convert_to_binary_label(class_value: int) -> int:
    return 0 if class_value == 2 else 1


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert label.csv-style dataset to text,label format for training.")
    parser.add_argument(
        "--input",
        default=r"C:\Users\nakka\Downloads\label.csv",
        help="Path to source CSV (default: C:\\Users\\nakka\\Downloads\\label.csv)",
    )
    parser.add_argument(
        "--output",
        default=os.path.join("data", "sample_data.csv"),
        help="Output CSV path in text,label format (default: data/sample_data.csv)",
    )
    parser.add_argument(
        "--keep-offensive-as-hate",
        action="store_true",
        default=True,
        help="Treat class 0 and class 1 as label=1, class 2 as label=0 (default behavior).",
    )
    args = parser.parse_args()

    if not os.path.exists(args.input):
        raise FileNotFoundError(f"Input dataset not found: {args.input}")

    source_df = pd.read_csv(args.input)

    required_columns = {"tweet", "class"}
    missing = required_columns - set(source_df.columns)
    if missing:
        raise ValueError(
            f"Input CSV missing required columns: {sorted(missing)}. "
            f"Found: {list(source_df.columns)}"
        )

    source_df = source_df[["tweet", "class"]].dropna().copy()
    source_df["tweet"] = source_df["tweet"].astype(str).str.strip()
    source_df = source_df[source_df["tweet"] != ""]
    source_df["class"] = pd.to_numeric(source_df["class"], errors="coerce")
    source_df = source_df.dropna(subset=["class"])
    source_df["class"] = source_df["class"].astype(int)

    valid_classes = {0, 1, 2}
    source_df = source_df[source_df["class"].isin(valid_classes)]

    if args.keep_offensive_as_hate:
        source_df["label"] = source_df["class"].apply(convert_to_binary_label)
    else:
        source_df["label"] = source_df["class"].apply(lambda c: 1 if c == 0 else 0)

    output_df = (
        source_df.rename(columns={"tweet": "text"})[["text", "label"]]
        .drop_duplicates()
        .sample(frac=1.0, random_state=42)
        .reset_index(drop=True)
    )

    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
    output_df.to_csv(args.output, index=False)

    print("Dataset integrated successfully.")
    print(f"Input rows (after cleaning): {len(source_df)}")
    print(f"Output rows (deduplicated): {len(output_df)}")
    print(f"Hate/offensive label=1: {int((output_df['label'] == 1).sum())}")
    print(f"Neutral label=0: {int((output_df['label'] == 0).sum())}")
    print(f"Saved to: {args.output}")


if __name__ == "__main__":
    main()