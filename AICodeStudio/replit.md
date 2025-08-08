# Overview

IAnne is a Discord bot designed as a gaming commentator with a unique personality. The bot uses Google's Gemini AI to generate contextual, sarcastic, and entertaining commentary about gaming situations. It features text-to-speech capabilities, multi-language support (Portuguese and English), and a distinctive "tsundere-style" personality that provides witty, slightly arrogant but charming responses to gaming scenarios.

# Recent Changes: Latest modifications with dates

## August 8, 2025 - Major Personality Enhancement
- **Dramatically improved personality prompts** for both Portuguese and English with much more dynamic, expressive, and entertaining responses
- **Enhanced response variation system** with modern slang, Brazilian expressions, and context-aware responses  
- **Advanced context detection** that automatically identifies victory, defeat, epic moments, fails, and other gaming situations
- **Improved TTS quality** with better text processing, emoji handling, and more natural speech patterns
- **Expanded language detection** with comprehensive gaming terminology and modern internet slang
- **Added contextual response categories** including clutch moments, epic fails, and emotional reactions

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Core Bot Framework
- **Discord Integration**: Built using discord.py with message content and voice state intents enabled
- **Event-Driven Architecture**: Responds to Discord events (on_ready, on_message) with mention-based triggers
- **Modular Design**: Separated into distinct managers for different functionalities

## AI Integration
- **Primary AI**: Google Gemini AI for generating contextual responses
- **Prompt Engineering**: Sophisticated personality prompts in both Portuguese and English that define IAnne's sarcastic, witty character
- **Response Generation**: Context-aware commentary tailored to gaming situations

## Personality System
- **Dual Language Support**: Separate personality definitions for Portuguese (Brazilian) and English
- **Character Traits**: Implements "tsundere-style" personality - confident, slightly arrogant, but secretly caring
- **Situational Responses**: Specialized prompts for victories, defeats, epic moments, silly mistakes, and game beginnings

## Language Processing
- **Language Detection**: Uses langdetect library with gaming-specific term dictionaries
- **Contextual Analysis**: Custom indicators for Portuguese and English gaming terminology
- **Fallback Logic**: Defaults to Portuguese when language detection is uncertain

## Text-to-Speech System
- **TTS Engine**: Google Text-to-Speech (gTTS) for voice generation
- **Localization**: Different TTS settings for Brazilian Portuguese (com.br) and US English (com)
- **Audio Management**: Temporary file handling for generated audio clips

## Response Variation System
- **Anti-Repetition**: Tracks recent responses to avoid repetitive commentary
- **Dynamic Variations**: Adds prefixes, suffixes, intensifiers, and transition words
- **Language-Specific Patterns**: Separate variation patterns for Portuguese and English

## Configuration Management
- **Environment Variables**: Secure storage of Discord tokens and API keys via .env files
- **Logging System**: Structured logging for debugging and monitoring
- **Async Operations**: Full asynchronous design for Discord and TTS operations

# External Dependencies

## Core Services
- **Discord API**: Bot hosting and message handling through discord.py
- **Google Gemini AI**: Primary AI model for response generation via google.generativeai
- **Google Text-to-Speech**: Voice synthesis through gTTS library

## Language Processing
- **langdetect**: Language identification for Portuguese/English detection
- **Regular Expressions**: Text cleaning and pattern matching

## Infrastructure
- **Python Environment**: asyncio for asynchronous operations
- **File System**: Temporary file management for audio generation
- **Environment Management**: python-dotenv for configuration loading

## Development Tools
- **Logging**: Python's built-in logging framework for debugging
- **Random Generation**: For response variations and personality quirks