# CapCut Simplified Project JSON Format — AI Agent Guide

This document explains the structure and rules of the simplified CapCut project JSON format, designed for AI agents or automated video editors.

## Purpose
This format is used to describe the timeline and media composition for CapCut projects in a clear, editable, and script-friendly way. It is intended for programmatic editing, generation, and synchronization with CapCut projects.

---

## JSON Structure Overview

The root object contains a single key:
- `sequences`: an array of media sequence objects (video or audio).

Example:
```json
{
  "sequences": [
    {
      "path": "C:/absolute/path/to/clip1.mp4",
      "start_time": 0.0,
      "end_time": 10.0,
      "source_in": 0.0,
      "source_out": 10.0,
      "volume": 1.0,
      "type": "video",
      "track_index": 0
    },
    {
      "path": "C:/absolute/path/to/music.mp3",
      "start_time": 0.0,
      "end_time": 10.0,
      "source_in": 0.0,
      "source_out": 10.0,
      "volume": 0.7,
      "type": "audio",
      "track_index": 1
    }
  ]
}
```

---

## Field Descriptions

- `path` (string):
  - **Absolute path** to the media file (video or audio). Must be complete and accessible.
- `start_time` (float):
  - The time (in seconds) when this sequence starts on the global timeline.
- `end_time` (float):
  - The time (in seconds) when this sequence ends on the timeline.
- `source_in` (float):
  - The starting point (in seconds) inside the source media file to use. (Temporal cropping)
- `source_out` (float):
  - The ending point (in seconds) inside the source media file. (Temporal cropping)
- `fade_in_duration` (float):
  - Duration in seconds of the fade-in effect at the start of the sequence. Controls how long the video or audio fades from black/silence.
- `fade_out_duration` (float):
  - Duration in seconds of the fade-out effect at the end of the sequence. Controls how long the video or audio fades to black/silence.
- `volume` (float):
  - Linear volume multiplier (1.0 = 100%, 0.5 = 50%, etc.)
- `type` (string):
  - Either `"video"` or `"audio"`.
- `track_index` (integer):
  - The timeline track number where this sequence will be placed (see rules below).

### Synchronisation parfaite des fades et du volume

- Les fades vidéo sont lus/écrits dans `materials.videos[].audio_fade` dans les fichiers natifs CapCut.
- Les fades audio sont lus/écrits dans `materials.audio_fades[]` (clé liée à l’id du matériel audio).
- Les champs `fade_in_duration` et `fade_out_duration` du JSON simplifié sont synchronisés avec ces objets natifs :
  - **Dans le JSON simplifié** : valeurs en secondes (float).
  - **Dans CapCut natif** : valeurs en microsecondes (int).
- Le volume est toujours synchronisé comme valeur linéaire (1.0 = 100%). Pas de conversion dB : CapCut affiche en dB mais stocke en linéaire.
- Les champs `fade_in`/`fade_out` dans les segments ne sont pas utilisés pour la synchronisation des fades : ils sont ignorés (CapCut ne s’en sert pas pour les vrais fades).

#### Exemple de structure native CapCut pour les fades vidéo :
```json
{
  "materials": {
    "videos": [
      {
        "id": "...",
        "path": "...",
        ...
        "audio_fade": {
          "fade_in_duration": 500000,   // 0.5s
          "fade_out_duration": 1000000, // 1.0s
          "fade_type": 0,
          "id": "...",
          "type": "audio_fade"
        }
      }
    ]
  }
}
```

#### Exemple pour les fades audio :
```json
{
  "materials": {
    "audios": [
      { "id": "AUDIOID1", ... }
    ],
    "audio_fades": [
      {
        "fade_in_duration": 300000,   // 0.3s
        "fade_out_duration": 700000,  // 0.7s
        "fade_type": 0,
        "id": "AUDIOID1",
        "type": "audio_fade"
      }
    ]
  }
}
```

### Fade Duration Empirical Rules

- **Short sequence (< 10 seconds):**
  - Video: max 0.5s (avoid excessive fade)
  - Audio: 0.3–1s depending on desired effect
- **Medium sequence (10–30 seconds):**
  - Video: 0.5–1s
  - Audio: 1–3s
- **Long sequence (> 30 seconds):**
  - Video: 1–2s for a softer effect
  - Audio: 2–5s or more for ambience or long music

> These durations are recommendations. The agent should adapt fade durations to the length and role of the sequence for best montage results.

---

## Empirical Montage Rules (Track Usage)

- **Track 0**: Reserved for all video sequences (clips, visuals).
- **Track 1**: Reserved for background music.
- **Track 2**: Reserved for voices of characters speaking in the trailer.
- **Track 3**: Reserved for the narrator's voice-over.

> **Note:**
> - Do not mix media types on the same track: video must be on track 0, audio on tracks 1, 2, or 3 as per their role.
> - All paths must be absolute and valid on the target system.
> - Sequences can overlap in time if needed (e.g., music and voice).
> - `source_in` and `source_out` allow you to use only a portion of the source file.

---

## Example Use Case

- Place video clips sequentially on track 0.
- Add a background music track on track 1, covering the whole timeline.
- Add character voice lines on track 2, timed to when each character speaks.
- Add narrator voice on track 3, timed as needed.

---

## Compatibility
This format is used by the CapCut Python project for import/export and can be generated or consumed by any AI agent or script.

If you have questions about field meanings or montage rules, see the main README or contact the project maintainer.
