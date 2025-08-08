import random
import time
from collections import defaultdict, deque

class ResponseVariations:
    def __init__(self):
        # Track recent responses to avoid repetition
        self.recent_responses = deque(maxlen=10)  # Keep last 10 responses
        self.response_count = defaultdict(int)   # Count how many times each response was used
        
        # Variation patterns for Portuguese
        self.pt_variations = {
            'prefixes': [
                "", "Ó meu filho,", "Eita,", "Nossa senhora,", "Caramba,", "Orra,", "Mano,", 
                "Tipo assim ó,", "Olha só que coisa,", "Bom,", "Enfim,", "Ai ai ai,", "Ó,", "E aí,", 
                "Pera aí,", "Oi? Como assim?", "Gente,", "Sério agora,", "Puts,", "Oxe,", "Rapaz,"
            ],
            'suffixes': [
                "", "né meu bem?", "então né.", "viu aí.", "cara.", "mesmo viu.", "tá vendo?", 
                "entendeu?", "sacou?", "né não?", "vai vendo.", "ué né.", "po.", "aí ó.", "mermão.",
                "né possível.", "tá loco.", "que isso meu.", "vai entender.", "é fogo.", "é osso."
            ],
            'intensifiers': [
                "muito", "super", "mega", "ultra", "bem", "bastante", "demais da conta",
                "realmente", "pra caramba", "demais", "total", "completamente", "absurdamente",
                "extremamente", "ridiculamente", "inacreditavelmente", "surrealmente"
            ],
            'transition_words': [
                "aliás", "inclusive", "além disso", "enfim", "anyway", "tipo",
                "ou seja", "quer dizer", "resumindo", "basicamente", "né isso", "real",
                "sem zoeira", "na moral", "de verdade", "falando sério", "não é meme"
            ],
            'expressions': [
                "nossa que loucura!", "mano do céu!", "que isso cara!", "eita porra!",
                "caramba meu!", "misericórdia!", "que coisa hein!", "ta doido!", "afe!",
                "que bagulho é esse!", "como assim véi!", "não pode ser!", "é muita coisa!"
            ]
        }
        
        # Variation patterns for English
        self.en_variations = {
            'prefixes': [
                "", "Oh honey,", "Listen sweetie,", "Oh my GOD,", "Bestie,", "Babe,", "Girl,", 
                "Okay but like,", "Hold up,", "Wait what?", "Excuse me?", "Umm,", "Sis,", "Yo,",
                "Nah but seriously,", "Real talk,", "Not gonna lie,", "Okay so like,", "Bruh,"
            ],
            'suffixes': [
                "", "no cap!", "for real!", "periodt.", "and that's on that.", "fr fr.", "deadass.", 
                "you feel me?", "ya know?", "lowkey.", "highkey.", "it's giving...", "idk man.",
                "respectfully.", "just saying.", "that's kinda sus.", "no offense.", "bestie."
            ],
            'intensifiers': [
                "absolutely", "totally", "completely", "literally", "genuinely", "seriously",
                "ridiculously", "incredibly", "insanely", "wildly", "outrageously", "stupidly",
                "criminally", "disgustingly", "aggressively", "violently", "astronomically"
            ],
            'transition_words': [
                "anyway", "besides", "also", "well", "so", "like", "but also",
                "I mean", "basically", "honestly", "frankly", "real talk", "not gonna lie",
                "to be fair", "lowkey", "highkey", "deadass", "no cap", "for real"
            ],
            'expressions': [
                "what the actual hell!", "I can't even!", "this hits different!", "that's a whole mood!",
                "I'm deceased!", "that slaps!", "it's giving main character!", "we love to see it!",
                "that's so valid!", "the audacity!", "I'm weak!", "not this!", "the drama!"
            ]
        }
    
    def add_variation(self, response, language='pt'):
        """
        Add natural variations to avoid repetitive responses
        """
        # Check if this exact response was used recently
        if response in self.recent_responses:
            response = self._modify_for_variety(response, language)
        
        # Add the response to tracking
        self.recent_responses.append(response)
        self.response_count[response] += 1
        
        # Apply random variations
        if random.random() < 0.3:  # 30% chance to add variations
            response = self._add_natural_variations(response, language)
        
        return response
    
    def _modify_for_variety(self, response, language):
        """
        Modify a repeated response to add variety
        """
        variations = self.pt_variations if language == 'pt' else self.en_variations
        
        # Add a transition word at the beginning
        if random.random() < 0.5:
            transition = random.choice(variations['transition_words'])
            if language == 'pt':
                response = f"{transition}, {response.lower()}"
            else:
                response = f"{transition}, {response.lower()}"
        
        # Or modify with intensifiers
        else:
            intensifier = random.choice(variations['intensifiers'])
            # Simple word replacement for common words
            if language == 'pt':
                response = response.replace('muito', intensifier)
                response = response.replace('bem', intensifier)
            else:
                response = response.replace('very', intensifier)
                response = response.replace('really', intensifier)
        
        return response
    
    def _add_natural_variations(self, response, language):
        """
        Add natural language variations to make responses feel more dynamic
        """
        variations = self.pt_variations if language == 'pt' else self.en_variations
        
        # Sometimes add a prefix
        if random.random() < 0.4:
            prefix = random.choice(variations['prefixes'])
            if prefix:
                response = f"{prefix} {response.lower()}"
        
        # Sometimes add a suffix
        if random.random() < 0.3:
            suffix = random.choice(variations['suffixes'])
            if suffix and not response.endswith(('.', '!', '?')):
                response = f"{response} {suffix}"
            elif suffix and response.endswith('.'):
                response = response[:-1] + f" {suffix}"
        
        return response
    
    def get_context_aware_response(self, base_response, context_type, language='pt'):
        """
        Modify response based on context (victory, defeat, epic moment, etc.)
        """
        if language == 'pt':
            context_modifiers = {
                'victory': [
                    'FINALMENTE! 🎉', 'AEEE! CONSEGUIU!', 'NOSSA! IMPRESSIONANTE!', 'CARAMBA! FOI ISSO AÍ!',
                    'EITA! QUE JOGADA!', 'MANO DO CÉU! FOI LINDO!', 'SIM! ISSO É QUE É TALENTO!', 'UHUUL!',
                    'QUE COISA LINDA!', 'AGORA SIM HEIN!', 'ÓTIMO! GOSTEI!', 'BOAAAA!'
                ],
                'defeat': [
                    'Ai ai ai...', 'Eita porra...', 'Nossa... que pena.', 'Oof... doeu aqui.',
                    'Coitadinho...', 'F no chat.', 'Que tristeza...', 'Oxe... como assim?',
                    'Poxa vida...', 'É fogo...', 'Que azar...', 'Puts... que bad.'
                ],
                'epic': [
                    'MANO DO CÉU! 🔥', 'QUE PORRA É ESSA?!', 'NOSSA SENHORA! QUE ISSO!',
                    'CARAMBA! TÔ CHOCADA!', 'MEU DEUS! QUE LOUCURA!', 'EITA! SURREAL!',
                    'CARALHO! (desculpa) MAS QUE COISA!', 'AI MEU DEUS! NÃO ACREDITO!',
                    'QUE BAGULHO LOUCO!', 'MISERICÓRDIA! QUE JOGADA!'
                ],
                'mistake': [
                    'Opa... que foi isso?', 'Eita... escorregou?', 'Ai ai ai... acontece.',
                    'Afe... que mico.', 'Oxe... como assim?', 'Puts... que fail.',
                    'Ih... deu ruim.', 'Nossa... que bad.', 'Opa... bug?', 'Eita... é isso mesmo?'
                ],
                'beginning': [
                    'Bora lá! Vamos ver...', 'Lá vamos nós de novo...', 'Aqui começa a mágica!',
                    'E aí? Preparado?', 'Vamo que vamo!', 'Agora vai!', 'Bora pro jogo!',
                    'Começou! Vamos ver o que rola...', 'Aí sim! Partiu!'
                ],
                'clutch': [
                    'CLUTCH! QUE ISSO!', 'PRESSAO! MAS CONSEGUIU!', 'NO SUFOCO! MAS DEU CERTO!',
                    'QUE NERVO! QUE SANGUE FRIO!', 'CARALHO! QUE CLASSE!', 'PRESSAO GIGANTE! MAS AGUENTOU!'
                ],
                'fail_epic': [
                    'COMO VOCÊ CONSEGUE FALHAR ISSO?!', 'MEU DEUS... FOI TÃO FÁCIL!',
                    'CARA... ERA SÓ APERTAR UM BOTÃO!', 'QUE TALENTO PRA ERRAR!',
                    'IMPRESSIONANTE! EM 1000 CHANCES, VOCÊ ERROU!'
                ]
            }
        else:
            context_modifiers = {
                'victory': [
                    'YESSS! 🎉', 'SLAY QUEEN!', 'THAT WAS FIRE! 🔥', 'PERIODT!',
                    'NOT YOU ACTUALLY WINNING!', 'WE LOVE TO SEE IT!', 'MAIN CHARACTER ENERGY!',
                    'THAT HITS DIFFERENT!', 'YOU DID THAT!', 'BESTIE POPPED OFF!'
                ],
                'defeat': [
                    'Oh honey... no.', 'Bestie... what was that?', 'Oop... that\'s rough.',
                    'RIP... it was nice knowing you.', 'F in the chat.', 'Not this...',
                    'Sis... we don\'t talk about that.', 'Yikes... that hurt to watch.',
                    'Baby girl... what happened?', 'The secondhand embarrassment...'
                ],
                'epic': [
                    'WHAT THE ACTUAL HELL?! 🤯', 'I\'M LITERALLY DECEASED!', 'THAT WAS INSANE!',
                    'HOLY SHIT! (sorry not sorry)', 'I CAN\'T EVEN!', 'BESTIE SNAPPED!',
                    'THAT WAS ABSOLUTELY CRIMINAL!', 'THE AUDACITY! THE TALENT!',
                    'I\'M SHOOK! WIGLESS! DECEASED!', 'THAT SLAPPED DIFFERENT!'
                ],
                'mistake': [
                    'Oop... what was that?', 'Bestie... no.', 'Girl... that ain\'t it.',
                    'Sis... we\'ve talked about this.', 'Baby... what happened?',
                    'Honey... that was a choice.', 'Sweetie... bless your heart.',
                    'Oh dear... that was something.', 'Girlie... we need to practice.'
                ],
                'beginning': [
                    'Alright bestie, let\'s see...', 'Here we go again...', 'Show me what you got!',
                    'Time to slay or get slayed!', 'Let\'s see this energy!', 'Periodt, let\'s go!',
                    'Main character moment incoming!', 'Time to serve looks!'
                ],
                'clutch': [
                    'CLUTCH GODDESS!', 'PRESSURE MAKES DIAMONDS!', 'ICE IN THE VEINS!',
                    'THAT\'S HOW YOU DO IT!', 'NERVES OF STEEL!', 'UNDER PRESSURE AND DELIVERED!'
                ],
                'fail_epic': [
                    'HOW DO YOU MESS THAT UP?!', 'BESTIE... IT WAS RIGHT THERE!',
                    'SIS... THAT WAS IMPOSSIBLE TO MISS!', 'THE TALENT FOR FAILING!',
                    'IMPRESSIVE! OUT OF 1000 CHANCES, YOU MISSED!'
                ]
            }
        
        if context_type in context_modifiers and random.random() < 0.6:
            modifier = random.choice(context_modifiers[context_type])
            if random.random() < 0.3:  # Sometimes combine with base response
                base_response = f"{modifier} {base_response}"
            else:  # Sometimes replace entirely for more dynamic feel
                base_response = modifier
        
        return base_response
    
    def reset_tracking(self):
        """
        Reset response tracking (useful for new sessions)
        """
        self.recent_responses.clear()
        self.response_count.clear()
    
    def detect_context_from_message(self, message, language='pt'):
        """
        Try to detect the context type from the user's message
        """
        message_lower = message.lower()
        
        if language == 'pt':
            context_keywords = {
                'victory': ['ganhei', 'venci', 'consegui', 'vitória', 'win', 'sucesso', 'conseguir', 'derrotei'],
                'defeat': ['morri', 'perdi', 'derrota', 'game over', 'fail', 'fracasso', 'lose', 'died'],
                'epic': ['incrível', 'épico', 'amazing', 'wow', 'caramba', 'nossa', 'impressionante', 'lindo'],
                'mistake': ['errei', 'erro', 'fail', 'burrada', 'besteira', 'vacilo', 'mancada'],
                'beginning': ['começando', 'iniciando', 'começar', 'start', 'novo jogo', 'primeira fase'],
                'clutch': ['quase', 'por pouco', 'sufoco', 'tensão', 'clutch', 'pressão'],
                'fail_epic': ['como assim', 'impossível', 'era fácil', 'óbvio', 'simples']
            }
        else:
            context_keywords = {
                'victory': ['won', 'victory', 'success', 'beat', 'defeated', 'killed', 'completed'],
                'defeat': ['died', 'lost', 'defeat', 'game over', 'fail', 'dead', 'killed'],
                'epic': ['amazing', 'incredible', 'epic', 'wow', 'insane', 'crazy', 'unbelievable'],
                'mistake': ['mistake', 'error', 'fail', 'messed up', 'screwed up', 'wrong'],
                'beginning': ['starting', 'beginning', 'new game', 'first level', 'tutorial'],
                'clutch': ['close', 'barely', 'clutch', 'pressure', 'tight', 'intense'],
                'fail_epic': ['how did', 'impossible', 'easy', 'obvious', 'simple']
            }
        
        for context, keywords in context_keywords.items():
            for keyword in keywords:
                if keyword in message_lower:
                    return context
        
        return 'general'  # Default context
    
    def get_personality_mood(self, language='pt'):
        """
        Get a random personality mood for more varied responses
        """
        if language == 'pt':
            moods = {
                'sarcastic': {'probability': 0.4, 'modifier': 'Com muito sarcasmo: '},
                'excited': {'probability': 0.3, 'modifier': 'Super empolgada: '},
                'caring': {'probability': 0.2, 'modifier': 'Meio carinhosa: '},
                'sassy': {'probability': 0.1, 'modifier': 'Sendo meio arrogante: '}
            }
        else:
            moods = {
                'sarcastic': {'probability': 0.4, 'modifier': 'With maximum sarcasm: '},
                'excited': {'probability': 0.3, 'modifier': 'Super excited: '},
                'caring': {'probability': 0.2, 'modifier': 'Actually caring: '},
                'sassy': {'probability': 0.1, 'modifier': 'Being extra sassy: '}
            }
        
        mood_choice = random.random()
        cumulative = 0
        
        for mood, data in moods.items():
            cumulative += data['probability']
            if mood_choice <= cumulative:
                return mood, data['modifier']
        
        return 'general', ''
    
    def get_response_stats(self):
        """
        Get statistics about response patterns
        """
        return {
            'total_responses': len(self.recent_responses),
            'unique_responses': len(set(self.recent_responses)),
            'most_common': max(self.response_count.items(), key=lambda x: x[1]) if self.response_count else None
        }
