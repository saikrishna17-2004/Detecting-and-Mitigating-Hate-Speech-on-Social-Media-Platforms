from backend.models.detector import detector

samples = [
    "bhen ke lode",
    "bh3n k3 l0d3",
    "madarchod saale",
    "m@drch0d harami",
    "chut!ye aadmi",
    "thank you so much bhai",
]

for text in samples:
    result = detector.analyze(text)
    print(text, '=>', result.get('is_hate_speech'), result.get('confidence'))
