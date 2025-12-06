import asyncio
import os
import edge_tts

from src.core.utility.alias_parser import AliasParser


# Singleton
class TTSEngine:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(TTSEngine, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized') and self._initialized:
            return
        self.keywords = set() # Usate per l'highlight della sintassi
        self.voices = []
        self.voice_keywords = set()
        self.alias_to_voice = {}

        asyncio.run(self._load_voices_async())
        self.reload_keywords()

    # Vengono popolati voices, alias_to_voice e infine keyword
    def reload_keywords(self):
        self.keywords = set()
        self.keywords.update(self.voice_keywords)  # Voci reali (es. it-IT-IsabellaNeural)
        self.reload_alias()  # Aggiorna alias_to_voice
        self.keywords.update(self.alias_to_voice.keys())  # Aggiungi alias come keyword

    # Qui vengono mappati gli alias alle voci effettive
    def reload_alias(self):
        self.alias_to_voice = AliasParser().map_aliases(self.voice_keywords)

    # --- PARTE DEL LOAD DELLE VOCI ---
    # Vengono caricate le voci e aggiunte come keyword (per l'highlight della sintassi)
    async def _load_voices_async(self):
        try:
            voices = await edge_tts.list_voices()
            self.voices = []
            for v in voices:
                friendly_name = self._format_voice_name(v)
                self.voices.append({
                    "id": v['ShortName'],
                    "name": friendly_name
                })

                # Il marker della voce viene salvato come keyword
                self.voice_keywords.add(v['ShortName'])

        except Exception as e:
            print(f"[TTSEngine] Errore caricamento voci: {e}")

    '''
            Trasforma i dati grezzi in un nome leggibile.
            Input: {'ShortName': 'it-IT-DiegoNeural', 'Gender': 'Male'}
            Output: "M - Diego"
    '''
    def _format_voice_name(self, voice_data):
        try:
            # ShortName è tipo "it-IT-DiegoNeural"
            short_name = voice_data['ShortName']
            gender = "M" if voice_data['Gender'] == "Male" else "F"

            # Estraiamo il nome (es. Diego) rimuovendo "Neural" e il prefisso locale
            # Solitamente è l'ultima parte dopo l'ultimo trattino
            raw_name = short_name.split('-')[-1].replace('Neural', '')

            return f"{gender} - {raw_name}"
        except:
            return voice_data['ShortName']
    
    # ------

    # Converte il marker nel valore utilizzabile dall'API
    # Se è un alias viene convertito in voce effettiva, altrimenti viene restituito così com'è
    # Se invece è una roba invalida, viene restituito None
    # TODO: TROVA UN NOME MIGLIORE PER CANON_FORMAT
    def canon_format(self, marker):
        if marker not in self.keywords:
            return None

        if marker in self.alias_to_voice:
            return self.alias_to_voice[marker]
        return marker

    # --- METODI GET ---
    def get_keywords(self):
        return self.keywords
    
    def get_voices(self):
        return self.voices
    # ------

    async def _generate_audio_async(self, text, voice_id, output_path):
        if not voice_id: voice_id = "it-IT-ElsaNeural"
        try:
            communicate = edge_tts.Communicate(text, voice_id)
            await communicate.save(output_path)
            return True
        except Exception as e:
            print(f"[TTSEngine] Errore async: {e}")
            return False

    # Qui viene generato il dialogo, e nessuno lo avrebbe mai detto basandosi sul nome del metodo
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
