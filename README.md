# 🧞 CapGenie: Your CapCut Project Wizard 🪄

**CapGenie** is a Python package that empowers you to programmatically create, load, and modify CapCut project files. It works by giving you direct control over the underlying JSON data that defines your CapCut projects, allowing for powerful automation and manipulation.

Perfect for developers, content creators, and AI agents looking to automate video editing workflows!

## ✨ Features

-   🚀 **Initialize New Projects**: Spin up a complete CapCut project folder structure from scratch.
-   📂 **Load & Edit Existing Projects**: Seamlessly open and make changes to your current CapCut projects.
-   🔧 **Direct JSON Control**: Access and modify all key JSON files within a project (e.g., `draft_content.json`).
-   🔄 **Simplified JSON Sync**:
    -   Export project timelines to a user-friendly, simplified JSON format.
    -   Modify this JSON (manually or programmatically).
    -   Import the changes back into your CapCut project, updating the timeline.
-   📁 **Easy File Management**: List project files and folders with ease.
-   🤖 **AI-Ready**: Designed to be easily integrated into workflows where an AI agent modifies project parameters.

## ⚙️ Installation

You can install CapGenie using pip:

```bash
pip install capgenie
```

*(Note: CapGenie will be available on PyPI once published. For now, you can install it locally as described in the development setup.)*

## 🚀 Quick Start

Here's how to get started with CapGenie:

```python
from capgenie import Project, CapCutFileManager # Assuming CapCutFileManager is also for public use

# --- Option 1: Create a brand new CapCut project ---
# CapGenie will set up the necessary folder structure.
new_project_path = r'C:\\path\\to\\your\\new_capcut_project_folder'
project = Project(project_path=new_project_path, create_new=True)
print(f"🎉 New project created at: {new_project_path}")

# --- Option 2: Load an existing CapCut project ---
# Point to the root folder of your CapCut project (e.g., 'com.lveditor.draft')
existing_project_path = r'C:\\Users\\YourName\\AppData\\Local\\CapCut\\User Data\\Projects\\com.lveditor.draft\\your_project_id_folder'
project = Project(project_path=existing_project_path)
print(f"🎬 Loaded project: {project.project_path}")

# --- Working with the Simplified Project JSON ---

# 1. Export the project's timeline to a simplified JSON
simplified_json_path = r'C:\\path\\to\\your\\project_timeline.json'
project.export_to_simplified_json(simplified_json_path)
print(f"📄 Project timeline exported to: {simplified_json_path}")

# Now, you (or an AI agent!) can open 'project_timeline.json' and modify it.
# See the "Simplified JSON Structure" section below for details.

# 2. Synchronize changes from the simplified JSON back to the CapCut project
project.sync_from_simplified_json(simplified_json_path)
print(f"🔄 Project timeline updated from: {simplified_json_path}")

# --- Direct JSON File Manipulation (Advanced) ---
# You can also directly access and modify specific CapCut JSON files.

# Example: Load, modify, and save 'draft_content.json'
draft_content = project.load_json('draft_content.json')
if draft_content:
    # Make your changes to the draft_content dictionary
    # For example, let's assume we're changing the overall project duration (this is a hypothetical example)
    # draft_content['duration'] = 120000000 # Example: 120 seconds
    print("🔍 Loaded draft_content.json")
    project.save_json('draft_content.json', draft_content)
    print("💾 Saved changes to draft_content.json")
else:
    print("⚠️ Could not load draft_content.json")

# List files and folders within the project
print("\nProject Files:", project.list_files())
print("Project Folders:", project.list_folders())
```

## 📄 Simplified JSON Structure

The `export_to_simplified_json` and `sync_from_simplified_json` methods use a streamlined JSON format to represent the project's timeline. This makes it easier to understand and modify track information.

```json
{
  "project_name": "My Awesome Video", // Optional: A name for your project
  "aspect_ratio": "16:9",             // Optional: e.g., "16:9", "9:16", "1:1"
  "duration_ms": 10000,               // Optional: Total duration in milliseconds
  "materials": {                      // Contains all media used in tracks
    "videos": [
      {
        "id": "video_001",
        "path": "C:/path/to/your/video1.mp4",
        "duration_ms": 5000 // Original duration of the media file
      }
    ],
    "audios": [
      {
        "id": "audio_001",
        "path": "C:/path/to/your/audio1.mp3",
        "duration_ms": 3000
      }
    ],
    "images": [], // Placeholder for future image support
    "texts": [    // For text overlays
      {
        "id": "text_001",
        "content": "Hello World!",
        "font_size": 72,
        "color": "#FFFFFF"
        // ... other text properties
      }
    ]
  },
  "tracks": [
    { // Video Track 0
      "type": "video", // "video", "audio"
      "segments": [
        {
          "material_id": "video_001", // Links to an ID in `materials.videos`
          "name": "Clip 1",
          "start_time_ms": 0,         // Position on the track timeline (ms)
          "duration_ms": 2500,        // How long this segment plays on the track (ms)
          "media_start_time_ms": 0,   // From where in the original media file to start (ms)
          "volume": 1.0,              // 0.0 to 1.0
          "speed": 1.0,               // Playback speed
          "transition_outgoing": {    // Optional: Transition to the next segment
            "name": "fade",
            "duration_ms": 500
          }
        },
        {
          "material_id": "video_001",
          "name": "Clip 2",
          "start_time_ms": 2500,
          "duration_ms": 2500,
          "media_start_time_ms": 2500, // Start from 2.5s into the original video
          "volume": 1.0,
          "speed": 1.0
        }
      ]
    },
    { // Audio Track 0 (often linked to video) or separate Audio Track 1
      "type": "audio",
      "segments": [
        {
          "material_id": "audio_001",
          "name": "Background Music",
          "start_time_ms": 0,
          "duration_ms": 3000,
          "media_start_time_ms": 0,
          "volume": 0.5
        }
      ]
    },
    { // Text Track 0
      "type": "text",
      "segments": [
        {
          "material_id": "text_001", // Links to an ID in `materials.texts`
          "name": "Intro Text",
          "start_time_ms": 500,
          "duration_ms": 2000
        }
      ]
    }
  ]
}
```

**Key points about the simplified JSON:**

-   **Human-Readable**: Designed to be easily understood and modified.
-   **AI-Friendly**: Structured for programmatic manipulation by AI agents or scripts.
-   **Synchronization**:
    -   `export_to_simplified_json`: Reads your CapCut project and generates this JSON.
    -   `sync_from_simplified_json`: Takes a modified version of this JSON and updates your CapCut project's timeline accordingly.
-   **Caution**: `sync_from_simplified_json` will typically overwrite the existing timeline based on the JSON content. Always back up important projects.

*(The exact structure of this simplified JSON will depend on how your `Project.export_to_simplified_json` and `Project.sync_from_simplified_json` methods are implemented. The example above is a comprehensive suggestion.)*

## 🏛️ CapCut Project Structure (Brief Overview)

A CapCut project folder (often found in `...AppData\\Local\\CapCut\\User Data\\Projects\\com.lveditor.draft\\[PROJECT_ID_FOLDER]`) typically contains:

```
[PROJECT_ID_FOLDER]/
├── draft_content.json       # Core timeline, media, effects data (VERY IMPORTANT)
├── draft_meta_info.json     # Project metadata
├── draft_cover.jpg          # Project thumbnail
├── Resources/               # Sometimes stores imported media copies
├── common_attachment/
├── matting/
├── ... (other folders and JSON files for specific features)
```

CapGenie helps you manage and interact with these files, especially the critical `draft_content.json`.

## 🛠️ How CapGenie Works

1.  **Project Initialization/Loading**: CapGenie either sets up a new valid CapCut folder structure or loads an existing one by identifying key files like `draft_content.json`.
2.  **JSON Parsing**: It reads and parses the CapCut JSON files (which are complex) into Python dictionaries.
3.  **Simplified Abstraction (Optional but Recommended)**:
    *   The `export_to_simplified_json` method translates the complex `draft_content.json` (and potentially other files) into a more manageable, high-level JSON structure (as shown above). This is the "agent-editable" JSON.
    *   The `sync_from_simplified_json` method takes this simplified JSON, translates it back into the detailed format CapCut expects, and updates the `draft_content.json` (and other necessary files).
4.  **Direct Manipulation**: You can also opt to directly load, modify, and save the raw CapCut JSON files if you understand their intricate structure.
5.  **File System Operations**: CapGenie uses the `CapCutFileManager` (or similar utility) to handle the correct creation, copying, and organization of files and folders to ensure CapCut can recognize the project.

**The Goal**: To allow an agent (or a script) to define video edits (like adding clips, text, changing timings) by modifying a relatively simple JSON, and then have CapGenie translate those instructions into a fully functional CapCut project.

## 🤝 Contributing

Contributions are welcome! If you'd like to improve CapGenie or add new features:

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/your-feature-name`).
3.  Make your changes.
4.  Write tests for your changes.
5.  Ensure all tests pass (`pytest`).
6.  Submit a pull request.

Please read our (to-be-created) `CONTRIBUTING.md` for more detailed guidelines.

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Made with ❤️ and 🐍 by Yanis Djeroro (and Cascade!)
