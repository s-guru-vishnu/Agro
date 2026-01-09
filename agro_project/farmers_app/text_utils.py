import re
from django.conf import settings
import requests


def paraphrase_text(text):
    if not text or not text.strip():
        return text

    try:

        paraphrase_api_url = getattr(settings, 'PARAPHRASE_API_URL', None)
        paraphrase_api_key = getattr(settings, 'PARAPHRASE_API_KEY', None)

        if paraphrase_api_url and paraphrase_api_key:

            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {paraphrase_api_key}'
            }
            payload = {
                'text': text,
                'language': 'en'
            }

            response = requests.post(
                paraphrase_api_url,
                json=payload,
                headers=headers,
                timeout=10
            )

            if response.status_code == 200:
                result = response.json()
                paraphrased = result.get('paraphrased_text') or result.get('text') or result.get('output')
                if paraphrased:
                    print(f"✅ Text paraphrased using API")
                    return paraphrased



        paraphrased = simple_paraphrase(text)
        print(f"✅ Text paraphrased using simple transformation")
        return paraphrased

    except Exception as e:
        print(f"⚠️ Error paraphrasing text: {e}")

        return text


def simple_paraphrase(text):
    if not text:
        return text


    replacements = {
        r'\bcan\b': 'could',
        r'\bshould\b': 'ought to',
        r'\bneed to\b': 'must',
        r'\bimportant\b': 'crucial',
        r'\bhelp\b': 'assist',
        r'\buse\b': 'utilize',
        r'\bget\b': 'obtain',
        r'\bmake sure\b': 'ensure',
        r'\bvery\b': 'extremely',
        r'\bgood\b': 'excellent',
        r'\bbad\b': 'poor',
        r'\bproblem\b': 'issue',
        r'\bsolution\b': 'approach',
    }

    paraphrased = text


    for pattern, replacement in replacements.items():
        paraphrased = re.sub(pattern, replacement, paraphrased, flags=re.IGNORECASE)


    if paraphrased == text:

        sentences = re.split(r'[.!?]+', text)
        paraphrased_sentences = []

        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue



            if re.search(r'^you should', sentence, re.IGNORECASE):
                sentence = re.sub(r'^you should\s+', 'It is recommended to ', sentence, flags=re.IGNORECASE)
            elif re.search(r'^you can', sentence, re.IGNORECASE):
                sentence = re.sub(r'^you can\s+', 'You have the option to ', sentence, flags=re.IGNORECASE)
            elif re.search(r'^you need to', sentence, re.IGNORECASE):
                sentence = re.sub(r'^you need to\s+', 'It is necessary to ', sentence, flags=re.IGNORECASE)

            paraphrased_sentences.append(sentence)

        if paraphrased_sentences:
            paraphrased = '. '.join(paraphrased_sentences)
            if not paraphrased.endswith(('.', '!', '?')):
                paraphrased += '.'


    if paraphrased == text and len(text) > 20:


        pass

    return paraphrased if paraphrased != text else text


def format_response_with_line_breaks(text):
    if not text or not text.strip():
        return text

    import re


    if re.search(r'\d+\.\s+', text):

        parts = re.split(r'(\d+\.\s+)', text)
        if len(parts) > 1:
            formatted_parts = []
            current_item = ""
            for i, part in enumerate(parts):
                if re.match(r'^\d+\.\s+$', part):

                    if current_item.strip():
                        formatted_parts.append(current_item.strip())
                    current_item = part
                else:

                    current_item += part
            if current_item.strip():
                formatted_parts.append(current_item.strip())

            if len(formatted_parts) > 1:

                return '\n\n'.join([p.strip() for p in formatted_parts if p.strip()])


    transition_patterns = [
        (r'(For example[,\s:])', re.IGNORECASE),
        (r'(Additionally[,\s:])', re.IGNORECASE),
        (r'(Furthermore[,\s:])', re.IGNORECASE),
        (r'(Moreover[,\s:])', re.IGNORECASE),
        (r'(However[,\s:])', re.IGNORECASE),
        (r'(Therefore[,\s:])', re.IGNORECASE),
        (r'(In addition[,\s:])', re.IGNORECASE),
        (r'(This means[,\s:])', re.IGNORECASE),
        (r'(Ensure to[,\s:])', re.IGNORECASE),
        (r'(If you have[,\s:])', re.IGNORECASE),
    ]

    for pattern, flags in transition_patterns:
        if re.search(pattern, text, flags):
            parts = re.split(pattern, text, flags=flags)
            if len(parts) > 2:
                formatted_parts = []
                for i in range(0, len(parts), 2):
                    if i < len(parts):
                        if i + 1 < len(parts):
                            combined = (parts[i] + parts[i + 1]).strip()
                            if combined:
                                formatted_parts.append(combined)
                        else:
                            if parts[i].strip():
                                formatted_parts.append(parts[i].strip())
                if len(formatted_parts) > 1:
                    return '\n\n'.join([p for p in formatted_parts if p])



    if len(text) > 150:

        parts = re.split(r'(\.\s+)([A-Z])', text)
        if len(parts) > 3:
            formatted_parts = []
            i = 0
            while i < len(parts):
                if i + 2 < len(parts):

                    sentence = parts[i] + parts[i + 1] + parts[i + 2]
                    formatted_parts.append(sentence.strip())
                    i += 3
                else:
                    if parts[i].strip():
                        formatted_parts.append(parts[i].strip())
                    i += 1

            if len(formatted_parts) > 1:

                return '\n'.join([p for p in formatted_parts if p.strip()])


    if len(text) > 300:
        sentences = re.split(r'(\.\s+)', text)
        if len(sentences) > 2:
            formatted_sentences = []
            i = 0
            while i < len(sentences):
                if i + 1 < len(sentences) and re.match(r'^\.\s+$', sentences[i + 1]):
                    formatted_sentences.append(sentences[i] + sentences[i + 1])
                    i += 2
                else:
                    if sentences[i].strip():
                        formatted_sentences.append(sentences[i].strip())
                    i += 1

            if len(formatted_sentences) > 1:
                return '\n'.join([s for s in formatted_sentences if s.strip()])


    return text


def save_audio_to_wav_file(audio_data, input_format='webm', filename=None):
    try:
        from django.conf import settings
        import os
        from datetime import datetime


        media_root = getattr(settings, 'MEDIA_ROOT', None)
        if not media_root:
            return None


        audio_dir = os.path.join(media_root, 'audio')
        os.makedirs(audio_dir, exist_ok=True)


        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'recording_{timestamp}.{input_format}'


        file_path = os.path.join(audio_dir, filename)
        with open(file_path, 'wb') as f:
            f.write(audio_data)


        return os.path.join('audio', filename)

    except Exception as e:
        print(f"⚠️ Error saving audio file: {e}")
        return None