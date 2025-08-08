from gtts import gTTS
import asyncio
import os
import tempfile
import logging

logger = logging.getLogger(__name__)

class TTSManager:
    def __init__(self):
        self.portuguese_tld = 'com.br'  # Brazilian Portuguese
        self.english_tld = 'com'       # US English
        
    async def generate_tts(self, text, language='pt'):
        """
        Generate TTS audio file for the given text and language
        Returns the path to the generated audio file
        """
        try:
            # Determine TTS language and settings
            if language == 'en':
                lang_code = 'en'
                tld = self.english_tld
                # Adjust speech for English - slightly faster and more natural
                slow = False
            else:
                lang_code = 'pt'
                tld = self.portuguese_tld
                # Brazilian Portuguese settings
                slow = False
            
            # Clean text for TTS
            clean_text = self._clean_text_for_tts(text)
            
            if not clean_text:
                logger.warning("Empty text after cleaning, skipping TTS")
                return None
            
            # Create temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_file:
                temp_filename = temp_file.name
            
            # Generate TTS
            tts = gTTS(
                text=clean_text,
                lang=lang_code,
                tld=tld,
                slow=slow
            )
            
            # Save to file
            tts.save(temp_filename)
            
            logger.info(f"TTS generated successfully: {temp_filename} (lang: {language})")
            return temp_filename
            
        except Exception as e:
            logger.error(f"Error generating TTS: {e}")
            return None
    
    def _clean_text_for_tts(self, text):
        """
        Clean text to make it more suitable for TTS while preserving personality
        """
        if not text:
            return ""
        
        import re
        
        # Remove markdown formatting
        text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
        text = re.sub(r'\*(.*?)\*', r'\1', text)
        
        # Convert some expressions to more TTS-friendly versions
        text = re.sub(r'OMG|omg', 'oh my god', text)
        text = re.sub(r'WTF|wtf', 'what the hell', text)
        text = re.sub(r'LOL|lol', 'haha', text)
        text = re.sub(r'LMAO|lmao', 'haha', text)
        
        # Handle caps for emphasis (convert to repeated words for TTS emphasis)
        def emphasize_caps(match):
            word = match.group(0).lower()
            if len(word) > 3:  # Only emphasize longer words
                return f"{word}... {word}"
            return word
        
        text = re.sub(r'\b[A-Z]{3,}\b', emphasize_caps, text)
        
        # Remove most emojis but keep some emotional indicators
        emoji_replacements = {
            '🤔': ' hmm ',
            '😂': ' haha ',
            '😭': ' oh no ',
            '🔥': ' that\'s fire ',
            '💀': ' I\'m dead ',
            '🎯': ' exactly ',
            '✨': ' amazing ',
            '👑': ' queen ',
            '💯': ' one hundred percent '
        }
        
        for emoji, replacement in emoji_replacements.items():
            text = text.replace(emoji, replacement)
        
        # Remove remaining emojis
        text = re.sub(r'[^\w\s\.,!?\-\'"();:]', ' ', text)
        
        # Clean up multiple spaces
        text = re.sub(r'\s+', ' ', text)
        
        # Add pauses for dramatic effect with commas
        text = re.sub(r'([.!?])\s*([A-Z])', r'\1, \2', text)
        
        # Remove excessive punctuation but keep some for emotion
        text = re.sub(r'[.]{3,}', '...', text)  # Keep ellipsis for pauses
        text = re.sub(r'[!]{3,}', '!!', text)   # Keep some exclamation for emphasis
        text = re.sub(r'[?]{3,}', '??', text)   # Keep some question marks
        
        return text.strip()
    
    def get_voice_settings(self, language='pt'):
        """
        Get optimal voice settings for each language
        """
        if language == 'en':
            return {
                'lang': 'en',
                'tld': self.english_tld,
                'slow': False,
                'description': 'US English voice'
            }
        else:
            return {
                'lang': 'pt',
                'tld': self.portuguese_tld,
                'slow': False,
                'description': 'Brazilian Portuguese voice'
            }
    
    async def test_tts(self, language='pt'):
        """
        Test TTS functionality for a given language
        """
        if language == 'en':
            test_text = "Hello! This is a test of my English voice. How do I sound?"
        else:
            test_text = "Olá! Este é um teste da minha voz em português. Como estou soando?"
        
        try:
            audio_file = await self.generate_tts(test_text, language)
            if audio_file:
                logger.info(f"TTS test successful for {language}: {audio_file}")
                return audio_file
            else:
                logger.error(f"TTS test failed for {language}")
                return None
        except Exception as e:
            logger.error(f"TTS test error for {language}: {e}")
            return None
