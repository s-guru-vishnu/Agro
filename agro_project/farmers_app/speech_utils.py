import warnings
import whisper
import os
import tempfile
import numpy as np
import librosa
import soundfile as sf
from datetime import datetime
from django.conf import settings


warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")


LANGUAGE_CODES = {
    'en': 'en',
    'ta': 'ta',
    'hi': 'hi',
    'te': 'te',
    'kn': 'kn',
    'ml': 'ml',
    'mr': 'mr',
    'gu': 'gu',
    'bn': 'bn',
    'pa': 'pa',
    'ur': 'ur',
    'es': 'es',
    'fr': 'fr',
    'de': 'de',
    'it': 'it',
    'pt': 'pt',
    'ru': 'ru',
    'ja': 'ja',
    'ko': 'ko',
    'zh': 'zh',
    'ar': 'ar',
}


LANGUAGE_NAMES = {
    'en': 'English',
    'ta': 'Tamil',
    'hi': 'Hindi',
    'te': 'Telugu',
    'kn': 'Kannada',
    'ml': 'Malayalam',
    'mr': 'Marathi',
    'gu': 'Gujarati',
    'bn': 'Bengali',
    'pa': 'Punjabi',
    'ur': 'Urdu',
    'es': 'Spanish',
    'fr': 'French',
    'de': 'German',
    'it': 'Italian',
    'pt': 'Portuguese',
    'ru': 'Russian',
    'ja': 'Japanese',
    'ko': 'Korean',
    'zh': 'Chinese',
    'ar': 'Arabic',
}


_whisper_model = None


def get_whisper_model():
    global _whisper_model
    if _whisper_model is None:
        print("🔄 Loading Whisper model (this may take a moment on first use)...")

        model_size = getattr(settings, 'WHISPER_MODEL_SIZE', 'base')
        _whisper_model = whisper.load_model(model_size)
        print(f"✅ Whisper model '{model_size}' loaded successfully")
    return _whisper_model







def transcribe_audio_with_whisper(audio_data, language=None, input_format='webm'):
    try:

        model = get_whisper_model()


        with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{input_format}') as temp_file:
            temp_file.write(audio_data)
            temp_file_path = temp_file.name

        try:
            print(f"📡 Transcribing with Whisper...")
            print(f"   Audio format: {input_format}")


            audio_array = None
            sample_rate = 16000


            if input_format.lower() == 'wav':
                try:
                    print(f"🔄 Loading WAV with soundfile...")
                    audio_array, sample_rate = sf.read(temp_file_path)

                    if len(audio_array.shape) > 1:
                        audio_array = np.mean(audio_array, axis=1)

                    if sample_rate != 16000:
                        audio_array = librosa.resample(audio_array, orig_sr=sample_rate, target_sr=16000)
                        sample_rate = 16000

                    audio_array = audio_array.astype(np.float32)
                    print(f"✅ Audio loaded with soundfile: {len(audio_array)} samples at {sample_rate}Hz, dtype: {audio_array.dtype}")
                except Exception as sf_error:
                    print(f"⚠️ soundfile failed: {sf_error}")
                    audio_array = None


            if audio_array is None:
                try:
                    print(f"🔄 Loading audio with librosa...")
                    audio_array, sample_rate = librosa.load(
                        temp_file_path,
                        sr=16000,
                        mono=True
                    )

                    audio_array = audio_array.astype(np.float32)
                    print(f"✅ Audio loaded with librosa: {len(audio_array)} samples at {sample_rate}Hz, dtype: {audio_array.dtype}")
                except Exception as librosa_error:
                    print(f"⚠️ librosa failed (may need ffmpeg for {input_format}): {librosa_error}")

                    audio_array = None




            transcription_options = {
                "task": "transcribe",
                "temperature": 0.0,
                "beam_size": 5,
                "best_of": 5,
                "condition_on_previous_text": True,
                "compression_ratio_threshold": 2.4,
                "logprob_threshold": -1.0,
                "no_speech_threshold": 0.6,
            }


            if language == 'ta':
                transcription_options["initial_prompt"] = "விவசாயம், பயிர், உரம், நீர்ப்பாசனம், விவசாய கருவிகள், பண்ணை, விவசாயி"
                print(f"   Using Tamil-specific prompt for better accuracy")

            if language:
                print(f"   Language: {language} (forced)")
                transcription_options["language"] = language

                if audio_array is not None:

                    result = model.transcribe(audio_array, **transcription_options)
                else:

                    result = model.transcribe(temp_file_path, **transcription_options)
            else:
                print(f"   Language: Auto-detect")

                if audio_array is not None:

                    result = model.transcribe(audio_array, **transcription_options)
                else:

                    result = model.transcribe(temp_file_path, **transcription_options)

            transcribed_text = result["text"].strip()
            detected_language = result.get("language", language)

            print(f"✅ Transcription successful!")
            print(f"   Text: \"{transcribed_text}\"")
            print(f"   Detected Language: {detected_language}")

            return {
                'success': True,
                'text': transcribed_text,
                'language': detected_language,
                'language_used': detected_language or language or 'auto',
                'error': None
            }

        finally:

            try:
                os.unlink(temp_file_path)
            except:
                pass

    except Exception as e:
        error_msg = f"Error processing audio with Whisper: {str(e)}"
        print(f"❌ {error_msg}")
        import traceback
        traceback.print_exc()
        return {
            'success': False,
            'text': None,
            'language': None,
            'language_used': language or 'auto',
            'error': error_msg
        }


def get_language_code(language_key):
    return LANGUAGE_CODES.get(language_key, 'en')


def get_available_languages():
    return LANGUAGE_NAMES