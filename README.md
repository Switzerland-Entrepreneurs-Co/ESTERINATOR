# ESTERINATOR
naele è stupido

## Struttura del progetto
L'ha fatta ChatGPT quindi qualsiasi errore non è colpa mia

audio_editor_project/
├── README.md
├── requirements.txt
├── main.py
├── setup.py
├── src/
│   ├── app.py
│   ├── config.py
│   ├── constants.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── audio_helpers.py
│   │   ├── file_io.py
│   │   └── tts_helpers.py
│   ├── audio/
│   │   ├── __init__.py
│   │   ├── audio_track.py
│   │   ├── audio_mixer.py
│   │   ├── waveform_view.py
│   │   └── effects.py
│   ├── tts/
│   │   ├── __init__.py
│   │   ├── tts_engine.py
│   │   ├── tts_manager.py
│   │   └── voice_parser.py
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── main_window.py
│   │   ├── editor_view.py
│   │   ├── tts_view.py
│   │   └── settings_view.py
│   └── data/
│       └── voices.json
├── tests/
│   ├── test_audio_mixer.py
│   ├── test_tts_engine.py
│   └── test_voice_parser.py
└── docs/
    ├── architecture.md
    ├── roadmap.md
    └── usage_guide.md
