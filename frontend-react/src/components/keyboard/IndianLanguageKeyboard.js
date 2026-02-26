import React, { useState, useRef } from 'react';
import Keyboard from 'react-simple-keyboard';
import 'react-simple-keyboard/build/css/index.css';
import './IndianLanguageKeyboard.css';
import { 
  Box, 
  FormControl, 
  Select, 
  MenuItem, 
  InputLabel,
  Paper,
  IconButton,
  Collapse
} from '@mui/material';
import KeyboardIcon from '@mui/icons-material/Keyboard';
import KeyboardHideIcon from '@mui/icons-material/KeyboardHide';

// Keyboard layouts for major Indian languages
const keyboardLayouts = {
  hindi: {
    name: 'हिन्दी (Hindi)',
    default: [
      'ौ ै ा ी ू ब ह ग द ज ड ़',
      'ो े ् ि ु प र क त च ट',
      'ॉ म न व ल स य {bksp}',
      '{shift} ष ण भ ङ घ ध झ ञ {shift}',
      '{space}'
    ],
    shift: [
      'औ ऐ आ ई ऊ भ ङ घ ध झ ढ ञ',
      'ओ ए अ इ उ फ ऋ ख थ छ ठ',
      'ऑ ं ॅ ँ ः ष ऱ {bksp}',
      '{shift} क्ष त्र ज्ञ श्र {shift}',
      '{space}'
    ]
  },
  bengali: {
    name: 'বাংলা (Bengali)',
    default: [
      'ৌ ৈ া ী ূ ব হ গ দ জ ড ়',
      'ো ে ্ ি ু প র ক ত চ ট',
      'ং ম ন ব ল স য {bksp}',
      '{shift} ষ ণ ভ ঙ ঘ ধ ঝ ঞ {shift}',
      '{space}'
    ],
    shift: [
      'ঔ ঐ আ ঈ ঊ ভ ঙ ঘ ধ ঝ ঢ ঞ',
      'ও এ অ ই উ ফ ঋ খ থ ছ ঠ',
      'ঁ ः ৎ শ ষ স ঃ {bksp}',
      '{shift} ক্ষ জ্ঞ শ্র {shift}',
      '{space}'
    ]
  },
  tamil: {
    name: 'தமிழ் (Tamil)',
    default: [
      'ௌ ை ா ீ ூ ப ஹ க த ச ட',
      'ோ ே ் ி ு ப ர க த ச ட',
      'ம ன வ ல ஸ ய ற {bksp}',
      '{shift} ஷ ண ங ஞ {shift}',
      '{space}'
    ],
    shift: [
      'ஔ ஐ ஆ ஈ ஊ ங ஞ ண ந ம',
      'ஓ ஏ அ இ உ எ ஒ க ற ன',
      'ஃ ஶ ஜ ஷ ஸ ஹ {bksp}',
      '{shift} க்ஷ ஶ்ரீ {shift}',
      '{space}'
    ]
  },
  telugu: {
    name: 'తెలుగు (Telugu)',
    default: [
      'ౌ ై ా ీ ూ బ హ గ ద జ డ',
      'ో ే ్ ి ు ప ర క త చ ట',
      'ం మ న వ ల స య {bksp}',
      '{shift} ష ణ భ ఙ ఘ ధ ఝ ఞ {shift}',
      '{space}'
    ],
    shift: [
      'ఔ ఐ ఆ ఈ ఊ భ ఙ ఘ ధ ఝ ఢ ఞ',
      'ఓ ఏ అ ఇ ఉ ఫ ఋ ఖ థ ఛ ఠ',
      'ః ఁ ఀ శ ష స ఱ {bksp}',
      '{shift} క్ష త్ర జ్ఞ శ్ర {shift}',
      '{space}'
    ]
  },
  marathi: {
    name: 'मराठी (Marathi)',
    default: [
      'ौ ै ा ी ू ब ह ग द ज ड ़',
      'ो े ् ि ु प र क त च ट',
      'ॉ म न व ल स य {bksp}',
      '{shift} ष ण भ ङ घ ध झ ञ {shift}',
      '{space}'
    ],
    shift: [
      'औ ऐ आ ई ऊ भ ङ घ ध झ ढ ञ',
      'ओ ए अ इ उ फ ऋ ख थ छ ठ',
      'ऑ ं ॅ ँ ः ष ळ {bksp}',
      '{shift} क्ष त्र ज्ञ श्र {shift}',
      '{space}'
    ]
  },
  gujarati: {
    name: 'ગુજરાતી (Gujarati)',
    default: [
      'ૌ ૈ ા ી ૂ બ હ ગ દ જ ડ',
      'ો ે ્ િ ુ પ ર ક ત ચ ટ',
      'ં મ ન વ લ સ ય {bksp}',
      '{shift} ષ ણ ભ ઙ ઘ ધ ઝ ઞ {shift}',
      '{space}'
    ],
    shift: [
      'ઔ ઐ આ ઈ ઊ ભ ઙ ઘ ધ ઝ ઢ ઞ',
      'ઓ એ અ ઇ ઉ ફ ઋ ખ થ છ ઠ',
      'ઃ ૐ ઁ ં ઍ ષ ળ {bksp}',
      '{shift} ક્ષ ત્ર જ્ઞ શ્ર {shift}',
      '{space}'
    ]
  },
  kannada: {
    name: 'ಕನ್ನಡ (Kannada)',
    default: [
      'ೌ ೈ ಾ ೀ ೂ ಬ ಹ ಗ ದ ಜ ಡ',
      'ೋ ೇ ್ ಿ ು ಪ ರ ಕ ತ ಚ ಟ',
      'ಂ ಮ ನ ವ ಲ ಸ ಯ {bksp}',
      '{shift} ಷ ಣ ಭ ಙ ಘ ಧ ಝ ಞ {shift}',
      '{space}'
    ],
    shift: [
      'ಔ ಐ ಆ ಈ ಊ ಭ ಙ ಘ ಧ ಝ ಢ ಞ',
      'ಓ ಏ ಅ ಇ ಉ ಫ ಋ ಖ ಥ ಛ ಠ',
      'ಃ ಁ ಀ ಶ ಷ ಸ ಱ {bksp}',
      '{shift} ಕ್ಷ ತ್ರ ಜ್ಞ ಶ್ರ {shift}',
      '{space}'
    ]
  },
  malayalam: {
    name: 'മലയാളം (Malayalam)',
    default: [
      'ൌ ൈ ാ ീ ൂ ബ ഹ ഗ ദ ജ ഡ',
      'ോ േ ് ി ു പ ര ക ത ച ട',
      'ം മ ന വ ല സ യ {bksp}',
      '{shift} ഷ ണ ഭ ങ ഘ ധ ഝ ഞ {shift}',
      '{space}'
    ],
    shift: [
      'ഔ ഐ ആ ഈ ഊ ഭ ങ ഘ ധ ഝ ഢ ഞ',
      'ഓ ഏ അ ഇ ഉ ഫ ഋ ഖ ഥ ഛ ഠ',
      'ഃ ഁ ഀ ശ ഷ സ ള {bksp}',
      '{shift} ക്ഷ ത്ര ജ്ഞ ശ്ര {shift}',
      '{space}'
    ]
  },
  punjabi: {
    name: 'ਪੰਜਾਬੀ (Punjabi)',
    default: [
      'ੌ ੈ ਾ ੀ ੂ ਬ ਹ ਗ ਦ ਜ ਡ',
      'ੋ ੇ ੍ ਿ ੁ ਪ ਰ ਕ ਤ ਚ ਟ',
      'ਂ ਮ ਨ ਵ ਲ ਸ ਯ {bksp}',
      '{shift} ਸ਼ ਣ ਭ ਙ ਘ ਧ ਝ ਞ {shift}',
      '{space}'
    ],
    shift: [
      'ਔ ਐ ਆ ਈ ਊ ਭ ਙ ਘ ਧ ਝ ਢ ਞ',
      'ਓ ਏ ਅ ਇ ਉ ਫ ੳ ਖ ਥ ਛ ਠ',
      'ਃ ੱ ੰ ਖ਼ ਗ਼ ਜ਼ ਫ਼ {bksp}',
      '{shift} ਸ਼੍ਰ ਤ੍ਰ ਗ੍ਯ {shift}',
      '{space}'
    ]
  },
  urdu: {
    name: 'اردو (Urdu)',
    default: [
      'ط ظ ع غ ف ق ک گ ل م ن',
      'و ہ ھ ء ی ے پ ت ٹ ث ج',
      'چ ح خ د ڈ ذ ر ڑ ز {bksp}',
      '{shift} ژ س ش ص ض ا ب {shift}',
      '{space}'
    ],
    shift: [
      'ً ٌ ٍ َ ُ ِ ّ ْ ؀ ؁ ؂',
      '۱ ۲ ۳ ۴ ۵ ۶ ۷ ۸ ۹ ۰',
      'آ أ ؤ إ ئ ة ۃ {bksp}',
      '{shift} ﷲ {shift}',
      '{space}'
    ]
  },
  english: {
    name: 'English',
    default: [
      'q w e r t y u i o p',
      'a s d f g h j k l',
      'z x c v b n m {bksp}',
      '{shift} , . @ {shift}',
      '{space}'
    ],
    shift: [
      'Q W E R T Y U I O P',
      'A S D F G H J K L',
      'Z X C V B N M {bksp}',
      '{shift} ! ? @ {shift}',
      '{space}'
    ]
  }
};

const IndianLanguageKeyboard = ({ value, onChange, onKeyPress }) => {
  const [selectedLanguage, setSelectedLanguage] = useState('english');
  const [layoutName, setLayoutName] = useState('default');
  const [isVisible, setIsVisible] = useState(false);
  const keyboard = useRef();

  const handleLanguageChange = (event) => {
    setSelectedLanguage(event.target.value);
    setLayoutName('default');
  };

  const onKeyboardChange = (input) => {
    onChange(input);
  };

  const handleShift = () => {
    const newLayoutName = layoutName === 'default' ? 'shift' : 'default';
    setLayoutName(newLayoutName);
  };

  const onKeyPressHandler = (button) => {
    if (button === '{shift}') {
      handleShift();
    } else if (button === '{bksp}') {
      // Handle backspace
      const newValue = value.slice(0, -1);
      onChange(newValue);
    } else if (button === '{space}') {
      onChange(value + ' ');
    } else {
      // Regular character
      onChange(value + button);
    }
    
    if (onKeyPress) {
      onKeyPress(button);
    }
  };

  const currentLayout = keyboardLayouts[selectedLanguage];

  return (
    <Box sx={{ width: '100%', mt: 2 }}>
      <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 1 }}>
        <FormControl size="small" sx={{ minWidth: 200 }}>
          <InputLabel>Keyboard Language</InputLabel>
          <Select
            value={selectedLanguage}
            label="Keyboard Language"
            onChange={handleLanguageChange}
          >
            <MenuItem value="english">{keyboardLayouts.english.name}</MenuItem>
            <MenuItem value="hindi">{keyboardLayouts.hindi.name}</MenuItem>
            <MenuItem value="bengali">{keyboardLayouts.bengali.name}</MenuItem>
            <MenuItem value="tamil">{keyboardLayouts.tamil.name}</MenuItem>
            <MenuItem value="telugu">{keyboardLayouts.telugu.name}</MenuItem>
            <MenuItem value="marathi">{keyboardLayouts.marathi.name}</MenuItem>
            <MenuItem value="gujarati">{keyboardLayouts.gujarati.name}</MenuItem>
            <MenuItem value="kannada">{keyboardLayouts.kannada.name}</MenuItem>
            <MenuItem value="malayalam">{keyboardLayouts.malayalam.name}</MenuItem>
            <MenuItem value="punjabi">{keyboardLayouts.punjabi.name}</MenuItem>
            <MenuItem value="urdu">{keyboardLayouts.urdu.name}</MenuItem>
          </Select>
        </FormControl>
        
        <IconButton 
          onClick={() => setIsVisible(!isVisible)}
          color="primary"
          size="small"
        >
          {isVisible ? <KeyboardHideIcon /> : <KeyboardIcon />}
        </IconButton>
      </Box>

      <Collapse in={isVisible}>
        <Paper elevation={3} sx={{ p: 2, bgcolor: '#f5f5f5' }}>
          <Keyboard
            keyboardRef={r => (keyboard.current = r)}
            layoutName={layoutName}
            layout={currentLayout}
            onChange={onKeyboardChange}
            onKeyPress={onKeyPressHandler}
            theme="hg-theme-default"
            baseClass="simple-keyboard"
            display={{
              '{bksp}': '⌫',
              '{shift}': '⇧',
              '{space}': 'Space'
            }}
            buttonTheme={[
              {
                class: 'hg-shift',
                buttons: '{shift}'
              },
              {
                class: 'hg-space',
                buttons: '{space}'
              },
              {
                class: 'hg-bksp',
                buttons: '{bksp}'
              }
            ]}
            buttonAttributes={[
              {
                attribute: 'data-lang',
                value: selectedLanguage,
                buttons: '{all}'
              }
            ]}
          />
        </Paper>
      </Collapse>
    </Box>
  );
};

export default IndianLanguageKeyboard;
