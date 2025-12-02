import asyncio
import os
import edge_tts


class TTSEngine:
    def __init__(self):
        self.voices = []
        # Carica le voci all'avvio
        asyncio.run(self._load_voices_async())

    def _format_voice_name(self, voice_data):
        """
        Trasforma i dati grezzi in un nome leggibile.
        Input: {'ShortName': 'it-IT-DiegoNeural', 'Gender': 'Male', 'Locale': 'it-IT'}
        Output: "Diego (Italiano) - M"
        """
        try:
            # ShortName è tipo "it-IT-DiegoNeural"
            short_name = voice_data['ShortName']
            locale = voice_data['Locale']
            gender = "M" if voice_data['Gender'] == "Male" else "F"

            # Estraiamo il nome (es. Diego) rimuovendo "Neural" e il prefisso locale
            # Solitamente è l'ultima parte dopo l'ultimo trattino
            raw_name = short_name.split('-')[-1].replace('Neural', '')

            # Mappiamo il locale in una lingua leggibile (base)
            lang_map = {
                'it-IT': 'Italiano', 'en-US': 'Inglese USA', 'en-GB': 'Inglese UK',
                'fr-FR': 'Francese', 'de-DE': 'Tedesco', 'es-ES': 'Spagnolo'
            }
            lang_readable = lang_map.get(locale, locale)  # Fallback al codice se non trovato

            return f"{raw_name} ({lang_readable}) - {gender}"
        except:
            return voice_data['ShortName']

    async def _load_voices_async(self):
        try:
            voices = await edge_tts.list_voices()
            self.voices = []
            for v in voices:
                friendly_name = self._format_voice_name(v)
                self.voices.append({
                    "id": v['ShortName'],
                    "name": friendly_name,
                    "locale": v['Locale']  # Utile per ordinare
                })

            # Ordiniamo: Prima le italiane, poi le altre
            self.voices.sort(key=lambda x: (x['locale'] != 'it-IT', x['name']))

        except Exception as e:
            print(f"[TTSEngine] Errore caricamento voci: {e}")

    def get_voices(self):
        return self.voices

    async def _generate_audio_async(self, text, voice_id, output_path):
        if not voice_id: voice_id = "it-IT-ElsaNeural"
        try:
            communicate = edge_tts.Communicate(text, voice_id)
            await communicate.save(output_path)
            return True
        except Exception as e:
            print(f"[TTSEngine] Errore async: {e}")
            return False

    def generate_dialogue(self, segments, final_output_path):
        """
        Genera il dialogo salvandolo esattamente in final_output_path.
        """
        output_dir = os.path.dirname(final_output_path)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)

        temp_files = []
        print(f"Inizio generazione -> {final_output_path}")

        for idx, seg in enumerate(segments):
            # Creiamo i file temp nella stessa cartella dell'output finale
            # per evitare errori di permessi tra dischi diversi
            filename = f"temp_seg_{idx}.mp3"
            full_path = os.path.join(output_dir, filename)

            voice_id = seg.get('voice', '')
            text = seg.get('text', '')

            print(f"[TTS] Processo segmento {idx}...")

            try:
                success = asyncio.run(self._generate_audio_async(text, voice_id, full_path))
                if success and os.path.exists(full_path):
                    temp_files.append(full_path)
            except Exception as e:
                print(f"Errore generazione segmento: {e}")

        if not temp_files:
            return False

        # Merge finale
        success_merge = self._merge_mp3_files(temp_files, final_output_path)

        # Pulizia
        for f in temp_files:
            try:
                os.remove(f)
            except:
                pass

        return success_merge

    def _merge_mp3_files(self, file_list, output_path):
        try:
            with open(output_path, 'wb') as outfile:
                for fname in file_list:
                    with open(fname, 'rb') as infile:
                        outfile.write(infile.read())
            return True
        except Exception as e:
            print(f"[MERGE] Errore: {e}")
            return False