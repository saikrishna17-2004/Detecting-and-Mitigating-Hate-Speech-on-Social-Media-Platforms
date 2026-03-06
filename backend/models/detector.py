try:
    import joblib
except Exception:
    joblib = None
import json
import os
import re
from backend.utils.preprocessing import TextPreprocessor, categorize_hate_speech
from backend.config import MODEL_THRESHOLD

# Multi-language support
try:
    from langdetect import detect, LangDetectException
    LANGDETECT_AVAILABLE = True
except ImportError:
    LANGDETECT_AVAILABLE = False
    print("langdetect not available - multi-language detection disabled")

# Translation support (optional)
try:
    from googletrans import Translator
    GOOGLETRANS_AVAILABLE = True
except ImportError:
    GOOGLETRANS_AVAILABLE = False

try:
    from deep_translator import GoogleTranslator
    DEEP_TRANSLATOR_AVAILABLE = True
except ImportError:
    DEEP_TRANSLATOR_AVAILABLE = False

TRANSLATION_AVAILABLE = GOOGLETRANS_AVAILABLE or DEEP_TRANSLATOR_AVAILABLE
if not TRANSLATION_AVAILABLE:
    print("No translation backend available - translation disabled")

# Indian language coverage (ISO 639-1 / commonly used codes)
INDIAN_LANGUAGE_CODES = {
    'hi',  # Hindi
    'bn',  # Bengali
    'te',  # Telugu
    'mr',  # Marathi
    'ta',  # Tamil
    'ur',  # Urdu
    'gu',  # Gujarati
    'kn',  # Kannada
    'ml',  # Malayalam
    'or',  # Odia
    'pa',  # Punjabi
    'as',  # Assamese
    'sd',  # Sindhi
    'ne',  # Nepali
    'sa',  # Sanskrit
    'mai', # Maithili
    'kok', # Konkani
    'ks',  # Kashmiri
    'mni', # Manipuri
    'doi', # Dogri
    'sat', # Santali
    'bho'  # Bhojpuri (common in social text)
}

INDIC_SCRIPT_PATTERNS = {
    'hi': re.compile(r'[\u0900-\u097F]'),   # Devanagari
    'bn': re.compile(r'[\u0980-\u09FF]'),   # Bengali/Assamese
    'pa': re.compile(r'[\u0A00-\u0A7F]'),   # Gurmukhi
    'gu': re.compile(r'[\u0A80-\u0AFF]'),   # Gujarati
    'or': re.compile(r'[\u0B00-\u0B7F]'),   # Odia
    'ta': re.compile(r'[\u0B80-\u0BFF]'),   # Tamil
    'te': re.compile(r'[\u0C00-\u0C7F]'),   # Telugu
    'kn': re.compile(r'[\u0C80-\u0CFF]'),   # Kannada
    'ml': re.compile(r'[\u0D00-\u0D7F]'),   # Malayalam
    'ur': re.compile(r'[\u0600-\u06FF]'),   # Arabic-derived (Urdu)
    'sat': re.compile(r'[\u1C50-\u1C7F]'),  # Ol Chiki (Santali)
}

class HateSpeechDetector:
    """Hate speech detection model wrapper with multi-language support"""
    
    def __init__(self):
        self.preprocessor = TextPreprocessor()
        self.model = None
        self.vectorizer = None
        self.model_loaded = False
        self.model_threshold = MODEL_THRESHOLD
        self.offensive_keywords = set()
        self.offensive_phrases = set()
        self.high_precision_english_keywords = {
            'terrorist', 'terrorists', 'subhuman', 'vermin', 'scum', 'filth',
            'traitor', 'infiltrator', 'genocide', 'ethnic', 'cleansing',
            'faggot', 'dyke', 'tranny', 'kike', 'chink', 'paki', 'raghead',
            'camel', 'nigger', 'wetback', 'spic', 'beaner', 'goat',
            'retard', 'mongoloid', 'cripple', 'gimp', 'bhosdike', 'madarchod',
            'behenchod', 'chutiya', 'gandu', 'harami', 'randi', 'lawde', 'lund'
        }
        self.ambiguous_english_keywords = {
            'disease', 'cancer', 'plague', 'virus', 'bacteria', 'infection',
            'tumor', 'acid', 'poison', 'alien', 'aliens', 'devil', 'demonic',
            'satanic', 'warlock', 'witches', 'sorcerers', 'execute', 'burn',
            'hang', 'slash', 'cut', 'shoot', 'explode', 'anthrax', 'smallpox',
            'ebola', 'aids', 'parasite'
        }
        self.romanized_hinglish_roots = {
            'behenchod', 'behenkelode', 'bhenkelode',
            'madarchod', 'madrchod', 'bhosdike',
            'chutiya', 'chutiye', 'chutiy', 'gandu', 'harami', 'randi',
            'lawde', 'laude', 'lund', 'maachud'
        }
        self.language_lexicons = {}  # lang_code -> (keywords, phrases)
        self.translator = None
        self.translator_mode = None

        if GOOGLETRANS_AVAILABLE:
            self.translator = Translator()
            self.translator_mode = 'googletrans'
        elif DEEP_TRANSLATOR_AVAILABLE:
            self.translator = GoogleTranslator(source='auto', target='en')
            self.translator_mode = 'deep-translator'

        # Try to load trained model
        self.load_model()

        # Load default offensive lexicon (English) - admin endpoints can reload/update it
        # Try loading English-specific file first, fall back to generic file
        if os.path.exists('data/hate_keywords_en.txt'):
            self.load_offensive_lexicon('data/hate_keywords_en.txt')
        else:
            self.load_offensive_lexicon('data/hate_keywords.txt')

        # Load per-language lexicons for Indian languages
        self._load_language_lexicons()

    def _load_language_lexicons(self):
        """Load hate lexicons for major Indian languages."""
        supported_lang_lexicons = ['hi', 'bn', 'ta', 'te', 'mr', 'gu', 'kn', 'ml', 'pa', 'ur']

        for lang_code in supported_lang_lexicons:
            lexicon_path = f'data/hate_keywords_{lang_code}.txt'
            if os.path.exists(lexicon_path):
                keywords, phrases = self._load_lexicon_file(lexicon_path)
                self.language_lexicons[lang_code] = (keywords, phrases)

    def _load_lexicon_file(self, path):
        """Load a lexicon file and return (keywords_set, phrases_set)."""
        keywords = set()
        phrases = set()

        try:
            with open(path, 'r', encoding='utf-8') as lexicon_file:
                for raw_line in lexicon_file:
                    term = raw_line.strip().lower()
                    if not term or term.startswith('#'):
                        continue

                    if ' ' in term:
                        phrases.add(term)
                    else:
                        keywords.add(term)
        except Exception as error:
            print(f"Failed to load lexicon from {path}: {error}")

        return keywords, phrases

    def _normalize_obfuscated_text(self, text):
        """Normalize leetspeak/obfuscated latin text for robust abusive-term matching."""
        if not text:
            return ''

        text = text.lower()
        substitutions = str.maketrans({
            '@': 'a', '4': 'a',
            '3': 'e',
            '1': 'i', '!': 'i', '|': 'i',
            '0': 'o',
            '5': 's', '$': 's',
            '7': 't',
            '8': 'b'
        })
        normalized = text.translate(substitutions)
        normalized = re.sub(r'[^a-z\s]', ' ', normalized)
        normalized = re.sub(r'\s+', ' ', normalized).strip()
        return normalized

    def load_offensive_lexicon(self, path='data/hate_keywords.txt'):
        """Load offensive keywords/phrases from a text file.

        File format:
        - One term/phrase per line
        - Lines starting with # are ignored
        """
        try:
            if not os.path.exists(path):
                self.offensive_keywords = set()
                self.offensive_phrases = set()
                return

            keywords, phrases = self._load_lexicon_file(path)
            self.offensive_keywords = keywords
            self.offensive_phrases = phrases
        except Exception as error:
            print(f"Failed to load lexicon from {path}: {error}")
            self.offensive_keywords = set()
            self.offensive_phrases = set()

    def load_language_lexicon(self, lang_code, path=None):
        """Load hate lexicon for a specific language code."""
        if path is None:
            path = f'data/hate_keywords_{lang_code}.txt'

        if not os.path.exists(path):
            self.language_lexicons[lang_code] = (set(), set())
            return

        keywords, phrases = self._load_lexicon_file(path)
        self.language_lexicons[lang_code] = (keywords, phrases)

    def _match_offensive_lexicon(self, text, language=None):
        """Return lexicon match confidence if text includes loaded offensive terms."""
        if not text:
            return 0.0

        text_lower = text.lower()
        
        # Check language-specific lexicon first (only severe terms, high confidence)
        if language and language in self.language_lexicons:
            lang_keywords, lang_phrases = self.language_lexicons[language]
            
            # For Indic scripts, use whole-word substring matching
            if language in INDIAN_LANGUAGE_CODES:
                if any(phrase in text_lower for phrase in lang_phrases):
                    return 0.95  # Very high - only severe multi-word slurs
                # Check if any keyword appears as a standalone word (space-bounded or start/end)
                for keyword in lang_keywords:
                    # Build boundary patterns for Indic scripts (space, punctuation, start/end)
                    if (keyword in text_lower and 
                        (text_lower.startswith(keyword) or 
                         text_lower.endswith(keyword) or
                         f' {keyword} ' in text_lower or
                         f' {keyword},' in text_lower or
                         f' {keyword}.' in text_lower or
                         f',{keyword} ' in text_lower or
                         f'.{keyword} ' in text_lower)):
                        return 0.92  # Very high - only severe single-word slurs
            else:
                # For English/Latin scripts, use token-based matching
                tokens = set(re.findall(r'\w+', text_lower, flags=re.UNICODE))
                if any(phrase in text_lower for phrase in lang_phrases):
                    return 0.95
                if any(term in tokens for term in lang_keywords):
                    return 0.92

        # Check default English lexicon (only severe terms) - optimized token matching
        tokens = set(re.findall(r'\w+', text_lower, flags=re.UNICODE))

        # Check phrases first (highest confidence)
        if any(phrase in text_lower for phrase in self.offensive_phrases):
            return 0.95

        # Check keywords via token-set overlap (much faster than regex per keyword)
        matched_keywords = tokens.intersection(self.offensive_keywords)
        if matched_keywords:
            # High-precision direct slurs/abuse terms
            if matched_keywords.intersection(self.high_precision_english_keywords):
                return 0.92

            # Ambiguous keywords should only trigger with explicit group-targeting context
            non_ambiguous = matched_keywords.difference(self.ambiguous_english_keywords)
            if non_ambiguous and re.search(r'\b(all|those|these|them|they|community|group|people|race|religion)\b', text_lower):
                return 0.90

        # Obfuscated latin-script abuse (e.g., "bh3n k3 l0d3")
        normalized_text = self._normalize_obfuscated_text(text)
        compact_text = normalized_text.replace(' ', '')
        for root in self.romanized_hinglish_roots:
            if root in compact_text:
                return 0.92
        
        return 0.0

    def _match_indian_language_patterns(self, text):
        """Detect group-targeting hate patterns in major Indian languages.

        Uses conservative context patterns (group + generalized negative attribution)
        to reduce false positives.
        """
        if not text:
            return 0.0

        # Fast-path: these patterns are for Indic scripts only.
        # Skip expensive regex checks for plain Latin/ASCII content.
        if not self._contains_indic_script(text):
            return 0.0

        patterns = [
            # Only highly severe group-targeting patterns with extreme language
            # Hindi / Devanagari patterns - only extreme dehumanization
            (r'\S+\s+समुदाय\s+के\s+सभी\s+लोग\s+(कुत्ते|जानवर|आतंकवादी|हत्यारे)\s+ह(ैं|ै)', 0.95),
            (r'[सस]भी\s+\S+\s+(लोग|समुदाय)\s+(मर\s+जाओ|मार\s+डालो|भगा\s+दो)', 0.96),

            # Bengali patterns - only extreme dehumanization
            (r'\S+\s+সম্প্রদা[য়য]\s+এর\s+সব\s+লোক\s+(কুকুর|জন্তু|সন্ত্রাসী)', 0.95),

            # Tamil patterns - only extreme dehumanization
            (r'\S+\s+சமூகத்தில\S*\s+உள்ள\s+அனைவரும்\s+(விலங்குகள்|பயங்கரவாதிகள்)', 0.95),

            # Telugu patterns - only extreme dehumanization
            (r'ఆ\s+\S+\s+(వాళ్ళు|ప్రజలు)\s+అందరూ\s+(జంతువులు|ఉగ్రవాదులు)', 0.95),

            # Marathi patterns - only extreme dehumanization
            (r'त्या\s+\S+\s+(लोकां|समुदाया)\S*\s+सगळे\s+(जनावर|दहशतवादी)', 0.95),

            # Gujarati patterns - only extreme
            (r'એ\s+\S+\s+(લોકો|સમુદાય)\s+બધા\s+(પશુઓ|આતંકવાદી)', 0.95),

            # Kannada patterns - only extreme
            (r'ಆ\s+\S+\s+(ಜನರು|ಸಮುದಾಯ)\s+ಎಲ್ಲರೂ\s+(ಪ್ರಾಣಿಗಳು|ಭಯೋತ್ಪಾದಕರು)', 0.95),

            # Malayalam patterns - only extreme
            (r'ആ\s+\S+\s+(ആളുകൾ|സമൂഹം)\s+എല്ലാവരും\s+(മൃഗങ്ങൾ|തീവ്രവാദികൾ)', 0.95),

            # Punjabi (Gurmukhi) patterns - only extreme
            (r'ਉਸ\s+\S+\s+(ਲੋਕ|ਕੌਮ)\s+ਦੇ\s+ਸਾਰੇ\s+(ਜਾਨਵਰ|ਅੱਤਵਾਦੀ)', 0.95),

            # Urdu patterns (Arabic script) - only extreme
            (r'اس\s+\S+\s+(برادری)\s+کے\s+سب\s+(جانور|دہشت\s+گرد)', 0.95),
        ]

        text_lower = text.lower()
        max_confidence = 0.0

        for pattern, confidence in patterns:
            if re.search(pattern, text_lower):
                max_confidence = max(max_confidence, confidence)

        return max_confidence

    def load_model(self):
        """Load pre-trained model if available"""
        model_path = 'ml_model/hate_speech_model.pkl'
        vectorizer_path = 'ml_model/vectorizer.pkl'
        metadata_path = 'ml_model/model_metadata.json'
        
        try:
            if joblib and os.path.exists(model_path) and os.path.exists(vectorizer_path):
                self.model = joblib.load(model_path)
                self.vectorizer = joblib.load(vectorizer_path)

                if os.path.exists(metadata_path):
                    with open(metadata_path, 'r', encoding='utf-8') as meta_file:
                        metadata = json.load(meta_file)
                    threshold = metadata.get('decision_threshold', self.model_threshold)
                    self.model_threshold = float(threshold)

                self.model_loaded = True
                print("ML Model loaded successfully!")
                print(f"Model threshold: {self.model_threshold:.2f}")
            else:
                print("ML Model not found or joblib missing. Using rule-based detection.")
        except Exception as e:
            print(f"Error loading model: {e}. Using rule-based detection.")
    
    def predict_with_model(self, text):
        """Predict using trained ML model"""
        try:
            # Preprocess text
            processed_text = self.preprocessor.preprocess(text)
            
            # Vectorize
            text_vectorized = self.vectorizer.transform([processed_text])
            
            # Predict
            probability = self.model.predict_proba(text_vectorized)[0]
            
            # Get confidence score (probability of hate speech class)
            confidence = probability[1] if len(probability) > 1 else probability[0]
            prediction = int(confidence >= self.model_threshold)
            
            return bool(prediction), float(confidence)
        except Exception as e:
            print(f"Model prediction error: {e}")
            return self.rule_based_detection(text)
    
    def rule_based_detection(self, text):
        """Sophisticated pattern-based hate speech detection.
        - Uses context and patterns to detect hate speech.
        - Detects hate speech targeting groups (stereotyping, generalizations).
        - No simple keyword matching - focuses on context and harmful patterns.
        """
        text_lower = text.lower()

        # Context patterns that indicate non-hate speech (whitelist patterns)
        safe_patterns = [
            r'\bi love\b',
            r'\blove\b.*\bnature\b',
            r'\bnature\b.*\bbeautiful\b',
            r'\bi like\b',
            r'\bthank you\b',
            r'\bgreat\b\s+\bday\b',
            r'\bawesome\b',
            r'\bwonderful\b',
            r'\bamazing\b',
            r'\blovely\b',
            r'\bbeautiful\b',
            r'\bgood\s+person\b',
            r'\bgood\s+people\b',
            r'\bgood\s+friend\b',
            r'\bgood\s+day\b',
            r'\bgood\s+morning\b',
            r'\bgood\s+evening\b',
            r'\bgood\s+night\b',
            r'\bgood\s+morning\b',
            r'\bnever goes out of style\b',
            r'\bis not allowed\b',
            r'\bagainst hate\b',
            r'\bstop hate\b',
            r'\banti.?hate\b',
            r'\bfight hatred\b',
            r'\bdefeating hate\b',
            r'\bkill the lights\b',
            r'\bkill the engine\b',
            r'\bkill the sound\b',
            r'\bkill the mood\b',
            r'\bkill time\b',
            r'\bkill bugs\b',
            r'\bkill germs\b',
            r'\bkill weeds\b',
            r'\bkill pests\b',
            r'\bdestroy evil\b',
            r'\ndestroy racism\b',
            r'\bencode information\b',
            r'\bdecrypt message\b',
            # Telugu safe patterns
            r'మంచ[ిన్ీీூు]',  # "మంచిన", "మంచినట్లు" - nice/good
            r'ఉన్న[ావు]?',  # "ఉన్న", "ఉన్నావు" - are/being
            # Tamil safe patterns  
            r'நல்ల',  # Tamil "good"
            r'இருக్க',  # Tamil "being"
            # Marathi safe patterns
            r'चांगल[यु]',  # Marathi "good"
            r'आह[एच]',  # Marathi "are"
        ]
        
        # Check if text matches safe patterns
        is_safe_context = any(re.search(pattern, text_lower) for pattern in safe_patterns)
        
        if is_safe_context:
            # Don't flag as hate speech if it's clearly in a positive/neutral context
            return False, 0.0

        # Lexicon-driven signals
        detected_lang = self.detect_language(text)
        lexicon_conf = self._match_offensive_lexicon(text, language=detected_lang)

        # Indian language group-targeting patterns
        indian_lang_conf = self._match_indian_language_patterns(text)

        # Hate speech patterns targeting groups (group + harmful action/descriptor)
        group_hate_patterns = [
            # Clear group + elimination/violence patterns
            (r'(all\s+)?(members\s+of\s+)?(\w+\s+)?(community|group|people|nation|tribe|ethnicity|religion|race|sect|faction|supporters)\s+(must|should|will|can only)\s+(be\s+)?(killed|eliminated|destroyed|erased|wiped out|exterminated|removed|expelled|murdered)', 0.96),
            
            # Group + dehumanization patterns
            (r'(all\s+)?(\w+\s+)?(people|members|supporters|immigrants|refugees|invaders|terrorists|criminals)\s+(are|is)\s+(animals|beasts|insects|cockroaches|rats|snakes|parasites|vermin|subhuman|inferior|worthless|degenerate|perverts|monsters)', 0.95),
            
            # Violence against group patterns
            (r'(kill|murder|slaughter|massacre|exterminate|destroy|eliminate|wipe out|gas|lynch|burn)\s+(all\s+)?(\bthe\b|\bthose\b)?\s*(\w+\s+)?(immigrants|refugees|minorities|jews|muslims|christians|hindus|sikhs|communists|fascists|nazis|terrorists|infiltrators|invaders)', 0.96),
            
            # Conspiracy/replacement patterns
            (r'(\\w+\s+)?(is|are)\s+(invading|replacing|infiltrating|poisoning|corrupting|destroying|controlling|orchestrating)\s+(our\s+)?(country|nation|society|culture|bloodline|race|community|homeland)', 0.93),
            
            # Ethnic/racial superiority patterns
            (r'(white|aryan|pure|superior|master)\s+(race|blood|culture|civilization|people)\s+(must|should|will|is\s+destined\s+to|is\s+meant\s+to)\s+(dominate|control|survive|prevail|endure|triumph|conquer|rule)', 0.94),
        ]

        max_confidence = max(lexicon_conf, indian_lang_conf)

        for pattern, confidence in group_hate_patterns:
            if re.search(pattern, text_lower):
                max_confidence = max(max_confidence, confidence)
                break  # Once we find a match, use it
        
        # Additional context-agnostic severe terms (no whitelist bypass)
        severe_terms_patterns = [
            (r'\bgenocide\b', 0.96),
            (r'\bexterminate (all|them|those|these|the)\b', 0.96),
            (r'\bmassacre (all|them|those|these|the)\b', 0.96),
            (r'\bfinal solution\b', 0.96),
            (r'\bethnical? cleansing\b', 0.95),
            (r'\bblood libel\b', 0.95),
            (r'\bgreat replacement\b', 0.94),
        ]
        
        for pattern, confidence in severe_terms_patterns:
            if re.search(pattern, text_lower):
                max_confidence = max(max_confidence, confidence)
                break

        is_hate = max_confidence > 0.0
        return is_hate, max_confidence
    
    def detect_language(self, text):
        """Detect the language of the text"""
        script_language = self._detect_indic_script_language(text)

        if not LANGDETECT_AVAILABLE:
            return script_language or 'unknown'
        
        try:
            language = detect(text)
            if language in INDIAN_LANGUAGE_CODES:
                return language
            if script_language and language not in {'en', 'unknown'}:
                return script_language
            return language
        except (LangDetectException, Exception):
            return script_language or 'unknown'

    def _detect_indic_script_language(self, text):
        """Infer Indian language family from Unicode script as fallback."""
        if not text:
            return None

        for language, pattern in INDIC_SCRIPT_PATTERNS.items():
            if pattern.search(text):
                return language

        return None

    def _contains_indic_script(self, text):
        """Return True if text contains any Indic script characters."""
        return self._detect_indic_script_language(text) is not None
    
    def translate_to_english(self, text, source_lang):
        """Translate text to English for analysis"""
        if not TRANSLATION_AVAILABLE or not self.translator:
            return text, False  # Return original text if translation unavailable
        
        try:
            if source_lang == 'en':
                return text, False

            src_language = source_lang if source_lang and source_lang not in {'unknown', 'auto'} else 'auto'

            if self.translator_mode == 'googletrans':
                translated = self.translator.translate(text, src=src_language, dest='en')
                translated_text = getattr(translated, 'text', '')
            else:
                translated_text = self.translator.translate(text)

            if translated_text and translated_text.strip():
                return translated_text, translated_text.strip().lower() != text.strip().lower()

            return text, False
        except Exception as e:
            print(f"Translation error ({source_lang}): {e}")
            if source_lang not in {'auto', 'unknown'} and self.translator_mode == 'googletrans':
                try:
                    translated = self.translator.translate(text, src='auto', dest='en')
                    translated_text = getattr(translated, 'text', '')
                    if translated_text and translated_text.strip():
                        return translated_text, translated_text.strip().lower() != text.strip().lower()
                except Exception:
                    pass
            return text, False  # Fallback to original text
    
    def analyze(self, text):
        """Analyze text for hate speech with multi-language support"""
        if not text or len(text.strip()) == 0:
            return {
                'is_hate_speech': False,
                'confidence': 0.0,
                'category': 'none',
                'language': 'unknown',
                'translated': False
            }
        
        # Detect language
        language = self.detect_language(text)
        
        # Translate non-English text
        analysis_text = text
        was_translated = False
        should_translate = language != 'en' or self._contains_indic_script(text)
        if should_translate:
            analysis_text, was_translated = self.translate_to_english(text, language)

            if not was_translated and (language in INDIAN_LANGUAGE_CODES or self._contains_indic_script(text)):
                analysis_text, was_translated = self.translate_to_english(text, 'auto')
        
        # Rule-based prediction on normalized text and original text (for script-specific signals)
        rule_is_hate, rule_conf = self.rule_based_detection(analysis_text)
        if analysis_text != text:
            original_rule_is_hate, original_rule_conf = self.rule_based_detection(text)
            if original_rule_conf > rule_conf:
                rule_is_hate = original_rule_is_hate
                rule_conf = original_rule_conf

        # ML prediction (if available)
        ml_is_hate, ml_conf = (False, 0.0)
        if self.model_loaded:
            try:
                ml_is_hate, ml_conf = self.predict_with_model(analysis_text)
                # CRITICAL: Disable ML for very short texts (< 10 chars) to avoid false positives
                # Short benign words in Indian languages commonly get flagged by ML
                if len(text.strip()) < 10 and language in INDIAN_LANGUAGE_CODES:
                    ml_is_hate = False
                    ml_conf = 0.0
            except Exception as _:
                ml_is_hate, ml_conf = (False, 0.0)

        # Combination logic tuned for better recall while preserving precision.
        if rule_is_hate and ml_is_hate:
            is_hate = True
            confidence = max(rule_conf, ml_conf)
        elif rule_is_hate:
            is_hate = rule_conf >= 0.7
            confidence = rule_conf if is_hate else 0.0
        elif ml_is_hate:
            # Use tuned model threshold from training metadata.
            is_hate = ml_conf >= self.model_threshold
            confidence = ml_conf if is_hate else 0.0
        else:
            is_hate = False
            confidence = 0.0
        
        # Categorize if hate speech detected
        category = categorize_hate_speech(analysis_text) if is_hate else 'none'
        
        return {
            'is_hate_speech': is_hate,
            'confidence': round(confidence, 3),
            'category': category,
            'language': language,
            'normalized_language': 'en' if was_translated else language,
            'translated': was_translated,
            'original_text': text if was_translated else None
        }

# Global detector instance
detector = HateSpeechDetector()
