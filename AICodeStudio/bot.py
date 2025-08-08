import discord
import os
from dotenv import load_dotenv
import asyncio
from google import genai
from google.genai import types
import logging

from personality import PersonalityManager
from language_detector import LanguageDetector
from tts_manager import TTSManager
from response_variations import ResponseVariations

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini AI
client = genai.Client(api_key=GEMINI_API_KEY)

# Initialize managers
personality_manager = PersonalityManager()
language_detector = LanguageDetector()
tts_manager = TTSManager()
response_variations = ResponseVariations()

# Configure Discord intents
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

discord_client = discord.Client(intents=intents)


async def send_long_message(channel, message, max_length=1900):
    """Send a message, splitting it into chunks if it's too long for Discord"""
    if len(message) <= max_length:
        await channel.send(message)
        return
    
    # Split message into chunks while preserving word boundaries
    chunks = []
    current_chunk = ""
    
    # Split by sentences first, then by words if needed
    sentences = message.split('. ')
    
    for sentence in sentences:
        # Check if adding this sentence would exceed the limit
        test_chunk = current_chunk + ('. ' if current_chunk else '') + sentence
        
        if len(test_chunk) <= max_length:
            current_chunk = test_chunk
        else:
            # If current chunk has content, save it
            if current_chunk:
                chunks.append(current_chunk + ('.' if not current_chunk.endswith('.') else ''))
                current_chunk = sentence
            else:
                # If single sentence is too long, split by words
                words = sentence.split(' ')
                for word in words:
                    test_chunk = current_chunk + (' ' if current_chunk else '') + word
                    if len(test_chunk) <= max_length:
                        current_chunk = test_chunk
                    else:
                        if current_chunk:
                            chunks.append(current_chunk)
                            current_chunk = word
                        else:
                            # Single word too long, force split
                            chunks.append(word[:max_length])
                            current_chunk = word[max_length:]
    
    # Add remaining chunk
    if current_chunk:
        chunks.append(current_chunk + ('.' if not current_chunk.endswith('.') else ''))
    
    # Send all chunks
    for i, chunk in enumerate(chunks):
        if i > 0:
            chunk = "..." + chunk  # Add continuation indicator
        await channel.send(chunk)


@discord_client.event
async def on_ready():
    logger.info(f'IAnne bot logged in as {discord_client.user}')
    print(f'IAnne está online como {discord_client.user}!')


@discord_client.event
async def on_message(message):
    # Ignora mensagens do próprio bot
    if message.author == discord_client.user:
        return

    # Responde quando mencionado em servidores, ou qualquer mensagem em DMs
    is_dm = isinstance(message.channel, discord.DMChannel)
    should_respond = is_dm or discord_client.user.mentioned_in(message)

    if should_respond:
        # Em servidores, verifica se o usuário está em canal de voz para TTS
        needs_voice_channel = not is_dm
        has_voice_access = hasattr(message.author, 'voice') and message.author.voice

        if needs_voice_channel and not has_voice_access:
            lang = language_detector.detect_language(message.content)
            if lang == 'pt':
                await message.channel.send("Querido, se você não entrar em um canal de voz, como espera ouvir meus comentários brilhantes? 🎤")
            else:
                await message.channel.send("Sweetie, if you don't join a voice channel, how do you expect to hear my brilliant commentary? 🎤")
            return

        try:
            async with message.channel.typing():
                logger.info("Recebida mensagem, iniciando processamento...")
                
                # Limpar a mensagem e detectar idioma
                if is_dm:
                    user_message = message.clean_content.strip()
                else:
                    user_message = message.clean_content.replace(f'@{discord_client.user.name}', '').strip()
                
                detected_lang = language_detector.detect_language(user_message)
                context_type = response_variations.detect_context_from_message(user_message, detected_lang)

                system_prompt = personality_manager.get_system_prompt(detected_lang)
                
                logger.info(f"Gerando resposta do Gemini para: '{user_message[:50]}...'")
                
                # Usar a nova API do Gemini 2.5
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=[
                        types.Content(
                            role="user",
                            parts=[
                                types.Part(text=f"{system_prompt}\n\nA situação do jogo é a seguinte: {user_message}")
                            ])
                    ])
                
                ai_response = response.text.strip()
                
                ai_response = response_variations.get_context_aware_response(ai_response, context_type, detected_lang)
                ai_response = response_variations.add_variation(ai_response, detected_lang)

                # Enviar resposta de texto
                if is_dm:
                    # Em DMs, abordagem mais casual
                    dm_indicator = "💬" if detected_lang == 'pt' else "💬"
                    await send_long_message(message.channel, f"**IAnne** {dm_indicator}: {ai_response}")
                    
                    # Avisar sobre TTS só estar disponível em servidores
                    if detected_lang == 'pt':
                        await message.channel.send("*Psiu: Para ouvir minha voz incrível, me chame em um servidor! 🎤*")
                    else:
                        await message.channel.send("*Psst: To hear my amazing voice, call me in a server! 🎤*")
                else:
                    # Em servidores, experiência completa com TTS
                    await send_long_message(message.channel, f"**IAnne** 🎮: {ai_response}")
                    
                    # Gerar e tocar TTS apenas em servidores
                    if has_voice_access:
                        logger.info("Gerando áudio TTS...")
                        audio_file = await tts_manager.generate_tts(ai_response, detected_lang)
                        
                        if audio_file:
                            voice_channel = message.author.voice.channel
                            voice_client = discord.utils.get(discord_client.voice_clients, guild=message.guild)
                            
                            if voice_client and voice_client.is_connected():
                                logger.info(f"Movendo para o canal de voz: {voice_channel.name}")
                                await voice_client.move_to(voice_channel)
                            else:
                                logger.info(f"Conectando ao canal de voz: {voice_channel.name}")
                                voice_client = await voice_channel.connect()

                            logger.info("Conexão bem-sucedida. Tocando áudio...")
                            voice_client.play(discord.FFmpegPCMAudio(audio_file), after=lambda e: logger.error(f'Erro no player: {e}') if e else None)

                            while voice_client.is_playing():
                                await asyncio.sleep(1)
                            
                            logger.info("Áudio finalizado. Desconectando...")
                            await voice_client.disconnect()
                            logger.info("Desconectado com sucesso.")
                        else:
                            logger.error("Falha ao gerar arquivo TTS.")

        except discord.errors.ClientException as e:
            logger.error(f"Erro de cliente Discord (provavelmente permissões): {e}")
            if detected_lang == 'pt':
                await message.channel.send("Não consegui entrar no seu canal de voz. Você tem certeza que eu tenho permissão para 'Conectar' e 'Falar' aí?")
            else:
                await message.channel.send("I couldn't join your voice channel. Are you sure I have 'Connect' and 'Speak' permissions?")
        except Exception as e:
            logger.error(f"Erro geral no processamento da mensagem: {e}", exc_info=True)
            try:
                lang = language_detector.detect_language(message.content)
            except:
                lang = 'pt'
            
            if is_dm:
                if lang == 'pt':
                    await message.channel.send("Eita! Deu bug aqui... Mesmo sendo perfeita, às vezes acontece. Tenta de novo? 😅")
                else:
                    await message.channel.send("Oops! Got a bug here... Even though I'm perfect, sometimes it happens. Try again? 😅")
            else:
                if lang == 'pt':
                    await message.channel.send("Eita! Deu um bug geral aqui... Tenta de novo? Se não der, avisa meu criador.")
                else:
                    await message.channel.send("Oops! Something went wrong... Try again? If it doesn't work, let my creator know.")
        finally:
            if 'audio_file' in locals() and os.path.exists(audio_file):
                os.remove(audio_file)
                logger.info(f"Arquivo de áudio temporário {audio_file} removido.")


# Run the bot
if __name__ == "__main__":
    if not DISCORD_TOKEN:
        logger.error("DISCORD_TOKEN not found in environment variables")
        exit(1)
    if not GEMINI_API_KEY:
        logger.error("GEMINI_API_KEY not found in environment variables")
        exit(1)

    discord_client.run(DISCORD_TOKEN)
