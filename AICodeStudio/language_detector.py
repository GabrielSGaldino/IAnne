from langdetect import detect, DetectorFactory
from langdetect.lang_detect_exception import LangDetectException
import re

# Set seed for consistent results
DetectorFactory.seed = 0

class LanguageDetector:
    def __init__(self):
        # Common Portuguese gaming terms and phrases
        self.portuguese_indicators = [
            # Gaming terms
            'jogo', 'jogos', 'jogador', 'vitória', 'derrota', 'morreu', 'morri',
            'consegui', 'perdi', 'ganhei', 'fase', 'nível', 'boss', 'chefe',
            'vida', 'saúde', 'energia', 'arma', 'ataque', 'defesa', 'item',
            'missão', 'quest', 'objetivo', 'pontos', 'score', 'ranking',
            'derrotei', 'matei', 'kill', 'morte', 'respawn', 'checkpoint',
            'save', 'load', 'continuar', 'pausar', 'restart', 'recomeçar',
            
            # Brazilian expressions
            'mano', 'cara', 'véi', 'irmão', 'brother', 'bro', 'parceiro',
            'caramba', 'nossa', 'eita', 'orra', 'caralho', 'porra', 'merda',
            'putz', 'droga', 'oxe', 'uai', 'né', 'pô', 'po', 'aí', 'rapaz',
            'mermão', 'mlk', 'menino', 'garoto', 'guri', 'piá', 'molecada',
            
            # Common words
            'que', 'não', 'sim', 'muito', 'pouco', 'mais', 'menos', 'tá', 'está',
            'agora', 'depois', 'antes', 'aqui', 'ali', 'lá', 'onde', 'como',
            'quando', 'por', 'para', 'de', 'em', 'com', 'sem', 'sobre',
            
            # Emotional expressions
            'legal', 'maneiro', 'massa', 'show', 'top', 'dahora', 'foda',
            'difícil', 'fácil', 'impossível', 'complicado', 'tranquilo',
            'suave', 'beleza', 'joia', 'valeu', 'obrigado', 'obrigada'
        ]
        
        # Common English gaming terms and phrases
        self.english_indicators = [
            # Gaming terms
            'game', 'games', 'player', 'victory', 'defeat', 'died', 'dead', 'kill',
            'won', 'lost', 'level', 'stage', 'boss', 'health', 'energy', 'hp', 'mp',
            'weapon', 'attack', 'defense', 'item', 'mission', 'quest', 'campaign',
            'objective', 'points', 'score', 'ranking', 'leaderboard', 'achievement',
            'unlock', 'upgrade', 'powerup', 'respawn', 'checkpoint', 'save', 'load',
            'restart', 'continue', 'pause', 'settings', 'options', 'inventory',
            
            # Internet slang & gaming culture
            'noob', 'pro', 'skilled', 'clutch', 'epic', 'fail', 'rekt', 'pwned',
            'gg', 'ez', 'op', 'nerf', 'buff', 'meta', 'speedrun', 'grinding',
            'farming', 'camping', 'rushing', 'flanking', 'headshot', 'combo',
            
            # Modern slang
            'bruh', 'bro', 'dude', 'man', 'guy', 'bestie', 'sis', 'queen', 'king',
            'slay', 'periodt', 'cap', 'bet', 'mood', 'vibe', 'sus', 'cringe',
            'based', 'cursed', 'blessed', 'fire', 'slaps', 'hits', 'different',
            
            # Expressions
            'cool', 'awesome', 'great', 'amazing', 'incredible', 'insane', 'crazy',
            'damn', 'shit', 'fuck', 'hell', 'omg', 'wtf', 'lol', 'lmao', 'rofl',
            'wow', 'whoa', 'yikes', 'oof', 'rip', 'nice', 'sweet', 'sick',
            
            # Common words
            'yes', 'no', 'very', 'much', 'more', 'less', 'now', 'later',
            'before', 'after', 'here', 'there', 'where', 'how', 'when',
            'difficult', 'easy', 'impossible', 'hard', 'simple', 'complicated'
        ]

    def detect_language(self, text):
        """
        Detect if the text is in Portuguese (pt) or English (en)
        Returns 'pt' for Portuguese, 'en' for English
        """
        if not text or len(text.strip()) < 3:
            return 'pt'  # Default to Portuguese
        
        # Clean the text
        cleaned_text = re.sub(r'[^\w\s]', ' ', text.lower())
        words = cleaned_text.split()
        
        # Count language indicators
        pt_count = sum(1 for word in words if word in self.portuguese_indicators)
        en_count = sum(1 for word in words if word in self.english_indicators)
        
        # If we have clear indicators, use them
        if pt_count > en_count and pt_count > 0:
            return 'pt'
        elif en_count > pt_count and en_count > 0:
            return 'en'
        
        # Fallback to langdetect library
        try:
            detected = detect(text)
            
            # Map detected languages
            if detected in ['pt', 'es']:  # Portuguese or Spanish (close enough)
                return 'pt'
            elif detected in ['en']:
                return 'en'
            else:
                # For other languages, try to determine based on text characteristics
                return self._determine_by_characteristics(text)
                
        except LangDetectException:
            # If detection fails, analyze text characteristics
            return self._determine_by_characteristics(text)

    def _determine_by_characteristics(self, text):
        """
        Determine language based on text characteristics when automatic detection fails
        """
        text_lower = text.lower()
        
        # Portuguese specific patterns
        pt_patterns = [
            r'\bção\b', r'\bções\b', r'\bão\b', r'\bões\b', r'\bção\b',
            r'\bãe\b', r'\bãs\b', r'\bnh\b', r'\blh\b', r'\bção\b'
        ]
        
        # English specific patterns
        en_patterns = [
            r'\bthe\b', r'\band\b', r'\bor\b', r'\bof\b', r'\bin\b',
            r'\bto\b', r'\bis\b', r'\bit\b', r'\bthat\b', r'\bwith\b'
        ]
        
        pt_score = sum(1 for pattern in pt_patterns if re.search(pattern, text_lower))
        en_score = sum(1 for pattern in en_patterns if re.search(pattern, text_lower))
        
        if pt_score > en_score:
            return 'pt'
        elif en_score > pt_score:
            return 'en'
        else:
            # Default to Portuguese if uncertain
            return 'pt'

    def get_confidence(self, text, detected_lang):
        """
        Get confidence score for the detected language
        """
        try:
            # Use langdetect to get confidence
            from langdetect import detect_langs
            langs = detect_langs(text)
            
            for lang in langs:
                if (detected_lang == 'pt' and lang.lang in ['pt', 'es']) or \
                   (detected_lang == 'en' and lang.lang == 'en'):
                    return lang.prob
            
            return 0.5  # Medium confidence if not found
            
        except:
            return 0.5  # Default medium confidence
