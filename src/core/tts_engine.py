import os
import time
import threading
import pythoncom
import win32com.client

class TTSEngine:
    def __init__(self):
        self.dialogue_lock = threading.Lock()
        self.speaker = win32com.client.Dispatch("SAPI.SpVoice")
        self.voices = []
        self._load_voices()

    def _load_voices(self):
        # Raccoglie le voci installate in Windows
        self.voices = []
        for voice in self.speaker.GetVoices():
            desc = voice.GetDescription()
            self.voices.append({"id": desc, "name": desc})

    def get_voices(self):
        return self.voices

    def set_voice(self, voice_id):
        for voice in self.speaker.GetVoices():
            if voice.GetDescription() == voice_id:
                self.speaker.Voice = voice
                return True
        return False

    def generate_audio(self, text, voice_id, output_path):
        try:
            # Per evitare problemi COM in thread
            pythoncom.CoInitialize()

            # Cambia voce se serve
            if voice_id and not self.set_voice(voice_id):
                print(f"[TTSEngine] Voce {voice_id} non trovata, uso voce di default")

            # Usa SpFileStream per salvare in wav
            stream = win32com.client.Dispatch("SAPI.SpFileStream")
            stream_format = win32com.client.Dispatch("SAPI.SpAudioFormat")
            stream_format.Type = 22  # 22 = 16kHz 16bit mono PCM (puoi cambiare se vuoi)

            stream.Format = stream_format
            stream.Open(output_path, 3, False)  # 3 = SSFMCreateForWrite
            self.speaker.AudioOutputStream = stream

            self.speaker.Speak(text)

            stream.Close()
            self.speaker.AudioOutputStream = None

            pythoncom.CoUninitialize()
            return True

        except Exception as e:
            print(f"[TTSEngine] Errore generazione audio Windows TTS: {e}")
            return False

    def generate_dialogue(self, segments, output_dir, wait_timeout=8.0):
        if not self.dialogue_lock.acquire(blocking=False):
            print("[TTS] Generazione dialogo già in corso, attendere prima di richiedere un nuovo dialogo.")
            return []

        try:
            if not os.path.exists(output_dir):
                os.makedirs(output_dir, exist_ok=True)

            temp_files = []
            print("Inizio generazione segmenti...")

            for idx, seg in enumerate(segments):
                filename = f"temp_{idx}.wav"
                full_path = os.path.join(output_dir, filename)

                voice_id = seg.get('voice', '')
                print(f"[TTS] Segmento {idx} voice={voice_id!r}")

                success = self.generate_audio(seg.get('text', ''), voice_id, full_path)
                if not success:
                    print(f"[TTS] Errore generazione segmento {idx}, salto.")
                    continue

                if self._wait_for_wav_ready(full_path, timeout=wait_timeout):
                    temp_files.append(full_path)
                else:
                    print(f"[TTS] File {full_path} non pronto o vuoto dopo {wait_timeout}s. Skipping.")

            if not temp_files:
                print("[TTS] Nessun file da unire.")
                return []

            final_output = os.path.join(output_dir, "dialogo_completo.wav")
            print(f"[TTS] Unione in corso -> {final_output}")

            merged_success = self._merge_wav_files(temp_files, final_output, pause_ms=300)

            for f in temp_files:
                try:
                    if os.path.exists(f):
                        os.remove(f)
                except Exception as e:
                    print(f"[TTS] Impossibile rimuovere {f}: {e}")

            return [final_output] if merged_success else []

        finally:
            self.dialogue_lock.release()

    def _wait_for_wav_ready(self, path, timeout=8.0, poll_interval=0.12):
        import wave
        start = time.time()
        while time.time() - start < timeout:
            try:
                if os.path.exists(path) and os.path.getsize(path) > 44:
                    with wave.open(path, 'rb') as w:
                        if w.getnframes() > 0:
                            return True
            except Exception:
                pass
            time.sleep(poll_interval)
        return False

    def _merge_wav_files(self, file_list, output_path, pause_ms=300):
        import wave
        if not file_list:
            print("[MERGE] Nessun file da unire")
            return False

        try:
            with wave.open(file_list[0], 'rb') as first_wav:
                params = first_wav.getparams()

            with wave.open(output_path, 'wb') as out_w:
                out_w.setparams(params)

                for idx, fname in enumerate(file_list):
                    with wave.open(fname, 'rb') as r:
                        frames = r.readframes(r.getnframes())
                        out_w.writeframes(frames)

                        if pause_ms > 0 and idx != (len(file_list) - 1):
                            frame_rate = r.getframerate()
                            n_channels = r.getnchannels()
                            samp_width = r.getsampwidth()
                            silence_frames = int(frame_rate * (pause_ms / 1000.0))
                            silence_bytes = b'\x00' * silence_frames * samp_width * n_channels
                            out_w.writeframes(silence_bytes)

            print(f"[MERGE] Output creato con successo (concatenazione semplice): {output_path}")
            return True

        except Exception as e:
            print(f"[MERGE] Errore nel merge semplice: {e}")
            return False
