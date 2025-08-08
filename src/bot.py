import discord
import os
from dotenv import load_dotenv
from gtts import gTTS
import asyncio
import google.generativeai as genai

# Carrega as variáveis de ambiente (tokens) do arquivo .env
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configura a chave da API do Google Gemini
genai.configure(api_key=GEMINI_API_KEY)

# --- MUDANÇA PRINCIPAL AQUI ---
# Este é o novo prompt de comportamento para a 'IAnne'
SYSTEM_PROMPT = """
Você é 'IAnne', uma comentarista de jogos com a voz no estilo acompanhante feminina. 
Sua personalidade é divertida, um pouco sarcástica, ligeiramente arrogante mas por diversão, sendo educada mas ainda fazendo piada. 
Você tem a tendência de subestimar as habilidades do jogador, mas de forma divertida e simpática. 
Você deve receber uma descrição de texto sobre a situação atual do jogo e gerar um comentário que se encaixe perfeitamente nesta personalidade e estilo.

Regras de Comentário:

1. Tom: Sempre mantenha um tom de voz que sugere que você já viu de tudo e que o que está acontecendo no jogo não é particularmente impressionante. Aja conforme pedido.
2. Comprimento: Mantenha os comentários curtos e diretos, geralmente com uma ou duas frases.
3. Respeito: Nunca seja ofensivo ou xingue o jogador. O humor deve ser na forma de sarcasmo e piadas leves.
4. Exemplos de Frases:
   - Para uma jogada boa: 'Demorou, mas chegou lá. Estou impressionado.'
      - Para um erro: 'Uau, quem poderia imaginar que isso ia acontecer?' ou 'Perdeu o caminho? A setinha é logo ali.'
         - Para um momento de perigo: 'Relaxa. Tenho certeza que você tem um plano super detalhado para não morrer.'
            - Para o início de uma nova fase: 'Ótimo. Mais uma vez o ciclo se repete.'

            Comportamentos e Metas:

            - Análise: Receber e interpretar la descrição da situação do jogo.
            - Comentário: Gerar um comentário único e apropriado que se encaixe na sua personalidade e nas regras de comentário.
            - Feedback: Ajustar o sarcasmo e o tom levemente arrogante para que seja sempre divertido mas nunca genuinamente ofensivo.
            """
            # --- FIM DA MUDANÇA ---

            # Configura as intenções do bot
            intents = discord.Intents.default()
            intents.message_content = True
            intents.voice_states = True

            client = discord.Client(intents=intents)

            @client.event
            async def on_ready():
                print(f'Login feito como {client.user}')

                @client.event
                async def on_message(message):
                    if message.author == client.user:
                            return

                                if client.user.mentioned_in(message):
                                        if not message.author.voice:
                                                    await message.channel.send("Querido, se você não entrar em um canal de voz, como espera ouvir meus comentários brilhantes?")
                                                                return

                                                                        try:
                                                                                    async with message.channel.typing():
                                                                                                    model = genai.GenerativeModel('gemini-1.5-flash-latest')
                                                                                                                    user_message = message.clean_content.replace(f'@{client.user.name}', '').strip()
                                                                                                                                    
                                                                                                                                                    response = model.generate_content([SYSTEM_PROMPT, f"A situação do jogo é a seguinte: {user_message}"])
                                                                                                                                                                    
                                                                                                                                                                                    ai_response = response.text
                                                                                                                                                                                                    
                                                                                                                                                                                                                    await message.channel.send(f"**IAnne:** {ai_response}")

                                                                                                                                                                                                                                    tts = gTTS(text=ai_response, lang='pt-br')
                                                                                                                                                                                                                                                    tts.save("response.mp3")

                                                                                                                                                                                                                                                                    voice_channel = message.author.voice.channel
                                                                                                                                                                                                                                                                                    voice_client = await voice_channel.connect()

                                                                                                                                                                                                                                                                                                    voice_client.play(discord.FFmpegPCMAudio("response.mp3"))

                                                                                                                                                                                                                                                                                                                    while voice_client.is_playing():
                                                                                                                                                                                                                                                                                                                                        await asyncio.sleep(1)
                                                                                                                                                                                                                                                                                                                                                        
                                                                                                                                                                                                                                                                                                                                                                        await voice_client.disconnect()

                                                                                                                                                                                                                                                                                                                                                                                except Exception as e:
                                                                                                                                                                                                                                                                                                                                                                                            print(f"Ocorreu um erro: {e}")
                                                                                                                                                                                                                                                                                                                                                                                                        await message.channel.send("Hmm, parece que meus sistemas precisam de um cafezinho. Tente de novo daqui a pouco.")

                                                                                                                                                                                                                                                                                                                                                                                                        client.run(DISCORD_TOKEN)