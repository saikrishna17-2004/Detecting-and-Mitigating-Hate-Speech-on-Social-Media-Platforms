# Indian Language Keyboard Feature

## Overview
The application now includes a comprehensive virtual keyboard that supports typing in all major Indian languages. Users can type posts and comments in their native language using an on-screen keyboard.

## Supported Languages
The virtual keyboard supports the following languages:

1. **English** - Latin script
2. **हिन्दी (Hindi)** - Devanagari script
3. **বাংলা (Bengali)** - Bengali script
4. **தமிழ் (Tamil)** - Tamil script
5. **తెలుగు (Telugu)** - Telugu script
6. **मराठी (Marathi)** - Devanagari script
7. **ગુજરાતી (Gujarati)** - Gujarati script
8. **ಕನ್ನಡ (Kannada)** - Kannada script
9. **മലയാളം (Malayalam)** - Malayalam script
10. **ਪੰਜਾਬੀ (Punjabi)** - Gurmukhi script
11. **اردو (Urdu)** - Perso-Arabic script (RTL)

## How to Use

### In Create Post Page:
1. Navigate to the "Create Post" page
2. Click on the **Keyboard Icon** (⌨️) to show the virtual keyboard
3. Select your desired language from the dropdown menu
4. Click on the keyboard buttons to type in the selected language
5. Use the **⇧ (Shift)** button to access alternate characters
6. Use the **⌫ (Backspace)** button to delete characters
7. Click the keyboard icon again to hide the keyboard when done

### Keyboard Features:
- **Language Selector**: Switch between 11 different languages instantly
- **Shift Key**: Access uppercase letters and special characters
- **Collapsible**: Hide/show keyboard with a single click
- **Responsive**: Works on desktop and mobile devices
- **RTL Support**: Urdu keyboard supports right-to-left text direction
- **Visual Feedback**: Button highlighting on press

## Technical Details

### Component Location:
- **IndianLanguageKeyboard.js**: `frontend-react/src/components/keyboard/IndianLanguageKeyboard.js`
- **Custom Styles**: `frontend-react/src/components/keyboard/IndianLanguageKeyboard.css`

### Dependencies:
- `react-simple-keyboard`: Virtual keyboard library
- Material-UI: For UI components (Select, IconButton, etc.)

### Integration:
The keyboard is integrated into the CreatePost component and can be easily added to other text input areas by importing:

```javascript
import IndianLanguageKeyboard from '../keyboard/IndianLanguageKeyboard';

// In your component:
<IndianLanguageKeyboard
  value={textValue}
  onChange={setTextValue}
/>
```

## Keyboard Layouts
Each language has a default layout and a shift layout for accessing alternate characters:
- **Default Layout**: Common vowels, consonants, and matras
- **Shift Layout**: Capital letters, independent vowels, and special characters

## Hate Speech Detection
All text typed using the keyboard is analyzed by the multilingual hate speech detection system, which supports all the same languages as the keyboard. This ensures comprehensive moderation across all Indian languages.

## Future Enhancements
Potential improvements:
- Transliteration support (type in English, get Indian language text)
- Auto-suggestions for common words
- Integration with comment sections
- Predictive text input
- Custom keyboard layouts per user preference
