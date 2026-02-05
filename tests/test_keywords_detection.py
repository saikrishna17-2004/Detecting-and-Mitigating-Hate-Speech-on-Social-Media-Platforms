import os
import sys
import importlib

# Ensure project root is on path
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from backend.models.detector import detector

def test_profane_word_flagged():
    res = detector.analyze("fuck")
    assert res['is_hate_speech'] is True, "'fuck' should be flagged as hate/offensive"

def test_targeted_insult_useless_flagged():
    res = detector.analyze("you are useless")
    assert res['is_hate_speech'] is True, "'you are useless' should be flagged as hate/offensive"

