import os
from pathlib import Path
from .file_manager import FileManager

class Project:
    """
    Represents a CapCut project. Can create a new project structure or load from an existing one.
    """
    DEFAULT_FOLDERS = [
        'common_attachment', 'matting', 'qr_upload', 'Resources', 'smart_crop', 'subdraft', 'adjust_mask'
    ]
    DEFAULT_FILES = [
        'attachment_editing.json', 'attachment_pc_common.json', 'draft.extra', 'draft_agency_config.json',
        'draft_biz_config.json', 'draft_content.json', 'draft_content.json.bak', 'draft_cover.jpg',
        'draft_meta_info.json', 'draft_settings', 'draft_virtual_store.json', 'draftMainWindowLayoutConfig.json',
        'key_value.json', 'performance_opt_info.json', 'template.tmp', 'template-2.tmp'
    ]

    def __init__(self, project_path: str, json_path: str, create: bool = False, overwrite: bool = False):
        """
        Initialize a CapCut project by specifying both the CapCut project folder and the associated simplified JSON file.
        :param project_path: Path to the CapCut project folder
        :param json_path: Path to the associated simplified JSON file
        :param create: Whether to create a new project structure if not present
        :param overwrite: Whether to overwrite existing project structure
        """
        self.path = Path(project_path)
        self.json_path = Path(json_path)
        if create:
            if overwrite or not self.path.exists():
                self._create_project_structure()
        elif not self.path.exists():
            raise FileNotFoundError(f"Project folder {self.path} does not exist.")

    def _create_project_structure(self):
        import shutil
        import uuid
        import json
        from datetime import datetime

        TEMPLATE_PATH = Path(__file__).parent.parent / "template_capcut_project"
        shutil.copytree(TEMPLATE_PATH, self.path, dirs_exist_ok=True)

        # Adaptation dynamique des fichiers JSON principaux
        # 1. draft_meta_info.json
        meta_path = self.path / "draft_meta_info.json"
        if meta_path.exists():
            with open(meta_path, "r", encoding="utf-8") as f:
                meta = json.load(f)
            # Générer des valeurs uniques
            draft_id = str(uuid.uuid4()).upper()
            draft_name = self.path.name
            now = int(datetime.now().timestamp() * 1e6)
            draft_fold_path = str(self.path)
            draft_root_path = str(self.path.parent)
            # Adapter les champs
            meta["draft_id"] = draft_id
            meta["draft_name"] = draft_name
            meta["draft_fold_path"] = draft_fold_path
            meta["draft_root_path"] = draft_root_path
            meta["tm_draft_create"] = now
            meta["tm_draft_modified"] = now
            with open(meta_path, "w", encoding="utf-8") as f:
                json.dump(meta, f, indent=2)

        # 2. draft_content.json, draft_content.json.bak, template.tmp, template-2.tmp
        for fname in ["draft_content.json", "draft_content.json.bak", "template.tmp", "template-2.tmp"]:
            fpath = self.path / fname
            if fpath.exists():
                with open(fpath, "r", encoding="utf-8") as f:
                    try:
                        data = json.load(f)
                        # Pour les .tmp, certains sont du json
                    except Exception:
                        continue
                # Adapter les champs si existants
                if "name" in data:
                    data["name"] = self.path.name
                if "id" in data:
                    data["id"] = draft_id
                if "path" in data:
                    data["path"] = str(self.path)
                with open(fpath, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2)
            elif file == "draft_meta_info.json":
                FileManager.ensure_file(
                    str(self.path / file),
                    default_content={
                        "cloud_package_completed_time": "",
                        "draft_cloud_capcut_purchase_info": "",
                        "draft_cloud_last_action_download": False,
                        "draft_cloud_package_type": "",
                        "draft_cloud_purchase_info": "",
                        "draft_cloud_template_id": "",
                        "draft_cloud_tutorial_info": "",
                        "draft_cloud_videocut_purchase_info": "",
                        "draft_cover": "draft_cover.jpg",
                        "draft_deeplink_url": "",
                        "draft_enterprise_info": {
                            "draft_enterprise_extra": "",
                            "draft_enterprise_id": "",
                            "draft_enterprise_name": "",
                            "enterprise_material": []
                        },
                        "draft_fold_path": "C:/Users/Yanis/AppData/Local/CapCut/User Data/Projects/com.lveditor.draft/0527",
                        "draft_id": "E9B7A696-C9D1-4d8f-B444-972AE202972B",
                        "draft_is_ae_produce": False,
                        "draft_is_ai_packaging_used": False,
                        "draft_is_ai_shorts": False,
                        "draft_is_ai_translate": False,
                        "draft_is_article_video_draft": False,
                        "draft_is_from_deeplink": "false",
                        "draft_is_invisible": False,
                        "draft_materials": [
                            {"type": 0, "value": []},
                            {"type": 1, "value": []},
                            {"type": 2, "value": []},
                            {"type": 3, "value": []},
                            {"type": 6, "value": []},
                            {"type": 7, "value": []},
                            {"type": 8, "value": []}
                        ],
                        "draft_materials_copied_info": [],
                        "draft_name": "0527",
                        "draft_need_rename_folder": False,
                        "draft_new_version": "",
                        "draft_removable_storage_device": "",
                        "draft_root_path": "C:\\Users\\Yanis\\AppData\\Local\\CapCut\\User Data\\Projects\\com.lveditor.draft",
                        "draft_segment_extra_info": [],
                        "draft_timeline_materials_size_": 8080,
                        "draft_type": "",
                        "tm_draft_cloud_completed": "",
                        "tm_draft_cloud_modified": 0,
                        "tm_draft_cloud_space_id": -1,
                        "tm_draft_create": 1748373258615818,
                        "tm_draft_modified": 1748373274514938,
                        "tm_draft_removed": 0,
                        "tm_duration": 0
                    }
                )
            elif file == "draft_settings":
                FileManager.ensure_file(
                    str(self.path / file),
                    default_content="""[General]
cloud_last_modify_platform=windows
draft_create_time=1748373258
layoutType=0
draft_last_edit_time=1748373274
real_edit_seconds=12
real_edit_keys=1
"""
                )
            elif file == "performance_opt_info.json":
                FileManager.ensure_file(
                    str(self.path / file),
                    default_content={"manual_cancle_precombine_segs": None}
                )
            elif file == "template.tmp":
                FileManager.ensure_file(
                    str(self.path / file),
                    default_content={
                        "canvas_config": {"background": None, "height": 0, "ratio": "original", "width": 0},
                        "color_space": -1,
                        "config": {
                            "adjust_max_index": 1,
                            "attachment_info": [],
                            "combination_max_index": 1,
                            "export_range": None,
                            "extract_audio_last_index": 1,
                            "lyrics_recognition_id": "",
                            "lyrics_sync": True,
                            "lyrics_taskinfo": [],
                            "maintrack_adsorb": True,
                            "material_save_mode": 0,
                            "multi_language_current": "none",
                            "multi_language_list": [],
                            "multi_language_main": "none",
                            "multi_language_mode": "none",
                            "original_sound_last_index": 1,
                            "record_audio_last_index": 1,
                            "sticker_max_index": 1,
                            "subtitle_keywords_config": None,
                            "subtitle_recognition_id": "",
                            "subtitle_sync": True,
                            "subtitle_taskinfo": [],
                            "system_font_list": [],
                            "use_float_render": False,
                            "video_mute": False,
                            "zoom_info_params": None
                        },
                        "cover": None,
                        "create_time": 0,
                        "duration": 0,
                        "extra_info": None,
                        "fps": 30.0,
                        "free_render_index_mode_on": False,
                        "group_container": None,
                        "id": "E92C6FA4-39AA-4476-A2C6-B6F0E22F5954",
                        "is_drop_frame_timecode": False,
                        "keyframe_graph_list": [],
                        "keyframes": {
                            "adjusts": [],
                            "audios": [],
                            "effects": [],
                            "filters": [],
                            "handwrites": [],
                            "stickers": [],
                            "texts": [],
                            "videos": []
                        },
                        "last_modified_platform": {
                            "app_id": 0,
                            "app_source": "",
                            "app_version": "",
                            "device_id": "",
                            "hard_disk_id": "",
                            "mac_address": "",
                            "os": "",
                            "os_version": ""
                        },
                        "lyrics_effects": [],
                        "materials": {
                            "ai_translates": [],
                            "audio_balances": [],
                            "audio_effects": [],
                            "audio_fades": [],
                            "audio_track_indexes": [],
                            "audios": [],
                            "beats": [],
                            "canvases": [],
                            "chromas": [],
                            "color_curves": [],
                            "common_mask": [],
                            "digital_humans": [],
                            "drafts": [],
                            "effects": [],
                            "flowers": [],
                            "green_screens": [],
                            "handwrites": [],
                            "hsl": [],
                            "images": [],
                            "log_color_wheels": [],
                            "loudnesses": [],
                            "manual_beautys": [],
                            "manual_deformations": [],
                            "material_animations": [],
                            "material_colors": [],
                            "multi_language_refs": [],
                            "placeholder_infos": [],
                            "placeholders": [],
                            "plugin_effects": [],
                            "primary_color_wheels": [],
                            "realtime_denoises": [],
                            "shapes": [],
                            "smart_crops": [],
                            "smart_relights": [],
                            "sound_channel_mappings": [],
                            "speeds": [],
                            "stickers": [],
                            "tail_leaders": [],
                            "text_templates": [],
                            "texts": [],
                            "time_marks": [],
                            "transitions": [],
                            "video_effects": [],
                            "video_trackings": [],
                            "videos": [],
                            "vocal_beautifys": [],
                            "vocal_separations": []
                        },
                        "mutable_config": None,
                        "name": "",
                        "new_version": "75.0.0",
                        "path": "",
                        "platform": {
                            "app_id": 0,
                            "app_source": "",
                            "app_version": "",
                            "device_id": "",
                            "hard_disk_id": "",
                            "mac_address": "",
                            "os": "",
                            "os_version": ""
                        },
                        "relationships": [],
                        "render_index_track_mode_on": False,
                        "retouch_cover": None,
                        "source": "default",
                        "static_cover_image_path": "",
                        "time_marks": None,
                        "tracks": [],
                        "uneven_animation_template_info": {
                            "composition": "",
                            "content": "",
                            "order": "",
                            "sub_template_info_list": []
                        },
                        "update_time": 0,
                        "version": 360000
                    }
                )
            elif file == "template-2.tmp":
                FileManager.ensure_file(
                    str(self.path / file),
                    default_content={
                        "canvas_config": {"background": None, "height": 1080, "ratio": "original", "width": 1920},
                        "color_space": -1,
                        "config": {
                            "adjust_max_index": 1,
                            "attachment_info": [],
                            "combination_max_index": 1,
                            "export_range": None,
                            "extract_audio_last_index": 1,
                            "lyrics_recognition_id": "",
                            "lyrics_sync": True,
                            "lyrics_taskinfo": [],
                            "maintrack_adsorb": True,
                            "material_save_mode": 0,
                            "multi_language_current": "none",
                            "multi_language_list": [],
                            "multi_language_main": "none",
                            "multi_language_mode": "none",
                            "original_sound_last_index": 1,
                            "record_audio_last_index": 1,
                            "sticker_max_index": 1,
                            "subtitle_keywords_config": None,
                            "subtitle_recognition_id": "",
                            "subtitle_sync": True,
                            "subtitle_taskinfo": [],
                            "system_font_list": [],
                            "use_float_render": False,
                            "video_mute": False,
                            "zoom_info_params": None
                        },
                        "cover": None,
                        "create_time": 0,
                        "duration": 0,
                        "extra_info": None,
                        "fps": 30.0,
                        "free_render_index_mode_on": False,
                        "group_container": None,
                        "id": "8902C01E-5B61-4a19-A1C0-28EACF11C513",
                        "is_drop_frame_timecode": False,
                        "keyframe_graph_list": [],
                        "keyframes": {
                            "adjusts": [],
                            "audios": [],
                            "effects": [],
                            "filters": [],
                            "handwrites": [],
                            "stickers": [],
                            "texts": [],
                            "videos": []
                        },
                        "last_modified_platform": {
                            "app_id": 359289,
                            "app_source": "cc",
                            "app_version": "6.2.8",
                            "device_id": "fa71b85f68d3d9a0261399379c11fe36",
                            "hard_disk_id": "",
                            "mac_address": "0001a0e5b616d6fec770edbeb78d9bd9",
                            "os": "windows",
                            "os_version": "10.0.26100"
                        },
                        "lyrics_effects": [],
                        "materials": {
                            "ai_translates": [],
                            "audio_balances": [],
                            "audio_effects": [],
                            "audio_fades": [],
                            "audio_track_indexes": [],
                            "audios": [],
                            "beats": [],
                            "canvases": [],
                            "chromas": [],
                            "color_curves": [],
                            "common_mask": [],
                            "digital_humans": [],
                            "drafts": [],
                            "effects": [],
                            "flowers": [],
                            "green_screens": [],
                            "handwrites": [],
                            "hsl": [],
                            "images": [],
                            "log_color_wheels": [],
                            "loudnesses": [],
                            "manual_beautys": [],
                            "manual_deformations": [],
                            "material_animations": [],
                            "material_colors": [],
                            "multi_language_refs": [],
                            "placeholder_infos": [],
                            "placeholders": [],
                            "plugin_effects": [],
                            "primary_color_wheels": [],
                            "realtime_denoises": [],
                            "shapes": [],
                            "smart_crops": [],
                            "smart_relights": [],
                            "sound_channel_mappings": [],
                            "speeds": [],
                            "stickers": [],
                            "tail_leaders": [],
                            "text_templates": [],
                            "texts": [],
                            "time_marks": [],
                            "transitions": [],
                            "video_effects": [],
                            "video_trackings": [],
                            "videos": [],
                            "vocal_beautifys": [],
                            "vocal_separations": []
                        },
                        "mutable_config": None,
                        "name": "",
                        "new_version": "135.0.0",
                        "path": "",
                        "platform": {
                            "app_id": 359289,
                            "app_source": "cc",
                            "app_version": "6.2.8",
                            "device_id": "fa71b85f68d3d9a0261399379c11fe36",
                            "hard_disk_id": "",
                            "mac_address": "0001a0e5b616d6fec770edbeb78d9bd9",
                            "os": "windows",
                            "os_version": "10.0.26100"
                        },
                        "relationships": [],
                        "render_index_track_mode_on": True,
                        "retouch_cover": None,
                        "source": "default",
                        "static_cover_image_path": "",
                        "time_marks": None,
                        "tracks": [],
                        "uneven_animation_template_info": {
                            "composition": "",
                            "content": "",
                            "order": "",
                            "sub_template_info_list": []
                        },
                        "update_time": 0,
                        "version": 360000
                    }
                )
            else:
                FileManager.ensure_file(str(self.path / file), default_content={})

    def load_json(self, filename: str):
        return FileManager.load_json(str(self.path / filename))

    def save_json(self, filename: str, data):
        FileManager.save_json(str(self.path / filename), data)

    def list_files(self):
        return [f.name for f in self.path.iterdir() if f.is_file()]

    def list_folders(self):
        return [f.name for f in self.path.iterdir() if f.is_dir()]

    def sync_from_json(self, json_path: str = None):
        """
        Écrase le projet CapCut courant à partir d'un fichier JSON simplifié (voir export_to_json pour le format).
        Prend en compte cropping temporel (source_in/source_out), position sur la timeline (start_time), volume, type, piste.
        """
        import json, uuid, os
        if json_path is None:
            json_path = self.json_path
        with open(json_path, 'r', encoding='utf-8') as f:
            project_data = json.load(f)
        # Réinitialiser les tracks et materials
        for fname in ["draft_content.json", "draft_content.json.bak"]:
            fpath = self.path / fname
            if not fpath.exists():
                continue
            with open(fpath, 'r', encoding='utf-8') as f2:
                data = json.load(f2)
            data['tracks'] = []
            data.setdefault('materials', {})
            data['materials']['videos'] = []
            data['materials']['audios'] = []
            # --- Fix: Always reset audio_fades to avoid duplicates and ensure correct references ---
            data['materials']['audio_fades'] = []
            # Création des tracks
            tracks = {}
            for seq in project_data.get('sequences', []):
                idx = seq.get('track_index', 0 if seq.get('type','video')=='video' else 1)
                if idx not in tracks:
                    tracks[idx] = {
                        "attribute": 0,
                        "flag": 0,
                        "id": f"TRACK-{idx}" if seq['type']=="video" else f"AUDIO-TRACK-{idx}",
                        "is_default_name": True,
                        "name": f"Track {idx}" if seq['type']=="video" else f"Audio Track {idx}",
                        "segments": [],
                        "type": seq['type']
                    }
                # Ajout dans materials
                mat_id = str(uuid.uuid4()).upper()
                source_in = seq.get('source_in', 0.0)
                source_out = seq.get('source_out', None)
                seg_duration = seq['end_time']-seq['start_time']
                if source_out is None:
                    source_out = source_in + seg_duration
                source_in_us = int(source_in * 1_000_000)
                source_out_us = int(source_out * 1_000_000)
                source_duration = source_out_us - source_in_us
                fade_in_us = int(seq.get('fade_in_duration', 0.0) * 1_000_000)
                fade_out_us = int(seq.get('fade_out_duration', 0.0) * 1_000_000)
                # --- Fix: For each video, create a single audio_fade object if needed, and reference it in both video and global list ---
                if seq['type'] == 'video':
                    video_obj = {
                        "id": mat_id,
                        "path": seq['path'],
                        "duration": source_duration,
                        "material_name": os.path.basename(seq['path']),
                        "volume": seq.get('volume', 1.0),
                        "width": 1280,
                        "height": 720,
                        "type": "video"
                    }
                    if fade_in_us == 0 and fade_out_us == 0:
                        # No fade: CapCut expects audio_fade to be null
                        video_obj["audio_fade"] = None
                    else:
                        # Fade present: create a unique audio_fade object, add to global list, and reference in video
                        audio_fade_id = str(uuid.uuid4()).upper()
                        audio_fade_obj = {
                            "fade_in_duration": fade_in_us,
                            "fade_out_duration": fade_out_us,
                            "fade_type": 0,
                            "id": audio_fade_id,
                            "type": "audio_fade"
                        }
                        video_obj["audio_fade"] = audio_fade_obj
                        data['materials']['audio_fades'].append(audio_fade_obj)
                    data['materials']['videos'].append(video_obj)
                elif seq['type'] == 'audio':
                    audio_obj = {
                        "id": mat_id,
                        "path": seq['path'],
                        "duration": source_duration,
                        "material_name": os.path.basename(seq['path']),
                        "volume": seq.get('volume', 1.0),
                        "type": "audio"
                    }
                    data['materials']['audios'].append(audio_obj)
                    # For audio, only add to global audio_fades if fade is present
                    if fade_in_us > 0 or fade_out_us > 0:
                        audio_fade_obj = {
                            "fade_in_duration": fade_in_us,
                            "fade_out_duration": fade_out_us,
                            "fade_type": 0,
                            "id": mat_id,  # For audio, use material id as fade id
                            "type": "audio_fade"
                        }
                        data['materials']['audio_fades'].append(audio_fade_obj)
                # Ajout du segment dans la piste
                # --- Génération des ressources associées pour CapCut ---
                extra_refs = []
                # 1. Canvas : un par vidéo, réutilisé si déjà créé
                if 'canvases' not in data['materials']:
                    data['materials']['canvases'] = []
                canvas_id = None
                for c in data['materials']['canvases']:
                    if c.get('material_name', None) == seq['path']:
                        canvas_id = c['id']
                        break
                if not canvas_id:
                    canvas_id = str(uuid.uuid4()).upper()
                    data['materials']['canvases'].append({
                        "id": canvas_id,
                        "type": "canvas_color",
                        "color": "",
                        "blur": 0.0,
                        "album_image": "",
                        "image": "",
                        "image_id": "",
                        "image_name": "",
                        "source_platform": 0,
                        "team_id": "",
                        "material_name": seq['path']
                    })
                extra_refs.append(canvas_id)

                # 2. Speed : un par vidéo, réutilisé si déjà créé
                if 'speeds' not in data['materials']:
                    data['materials']['speeds'] = []
                speed_id = None
                for s in data['materials']['speeds']:
                    if s.get('material_name', None) == seq['path']:
                        speed_id = s['id']
                        break
                if not speed_id:
                    speed_id = str(uuid.uuid4()).upper()
                    data['materials']['speeds'].append({
                        "id": speed_id,
                        "type": "speed",
                        "mode": 0,
                        "speed": 1.0,
                        "curve_speed": None,
                        "material_name": seq['path']
                    })
                extra_refs.append(speed_id)

                # 3. Placeholder : un par vidéo, réutilisé si déjà créé
                if 'placeholder_infos' not in data['materials']:
                    data['materials']['placeholder_infos'] = []
                placeholder_id = None
                for p in data['materials']['placeholder_infos']:
                    if p.get('material_name', None) == seq['path']:
                        placeholder_id = p['id']
                        break
                if not placeholder_id:
                    placeholder_id = str(uuid.uuid4()).upper()
                    data['materials']['placeholder_infos'].append({
                        "id": placeholder_id,
                        "type": "placeholder_info",
                        "meta_type": "none",
                        "res_path": "",
                        "res_text": "",
                        "error_path": "",
                        "error_text": "",
                        "material_name": seq['path']
                    })
                extra_refs.append(placeholder_id)

                # 4. Audio Fade : only if fade is present and for video, add the fade id to extra_refs
                if seq['type'] == 'video' and fade_in_us > 0 or fade_out_us > 0:
                    if fade_in_us > 0 or fade_out_us > 0 and video_obj.get('audio_fade'):
                        extra_refs.append(video_obj['audio_fade']['id'])
                elif seq['type'] == 'audio' and fade_in_us > 0 or fade_out_us > 0:
                    extra_refs.append(mat_id)  # For audio, fade id is mat_id

                # --- Création du segment vidéo avec toutes les références ---
                segment = {
                    "id": str(uuid.uuid4()).upper(),
                    "material_id": mat_id,
                    "target_timerange": {
                        "start": int(seq['start_time']*1_000_000),
                        "duration": int(seg_duration*1_000_000)
                    },
                    "source_timerange": {
                        "start": source_in_us,
                        "duration": source_duration
                    },
                    "volume": seq.get('volume', 1.0),
                    "fade_in": {"duration": int(seq.get('fade_in_duration', 0.0) * 1_000_000)},
                    "fade_out": {"duration": int(seq.get('fade_out_duration', 0.0) * 1_000_000)},
                    # CapCut references (canvas, speed, placeholder, fade...)
                    "extra_material_refs": extra_refs
                }
                tracks[idx]['segments'].append(segment)

            # Injection des tracks dans le projet
            data['tracks'] = [tracks[k] for k in sorted(tracks.keys())]
            # Correction de la durée du projet
            max_end = 0
            for t in data['tracks']:
                for s in t['segments']:
                    end = s['target_timerange']['start'] + s['target_timerange']['duration']
                    if end > max_end:
                        max_end = end
            if 'duration' in data:
                data['duration'] = max_end
            # Patch: force la présence du champ audio_fade dans chaque vidéo
            if 'materials' in data and 'videos' in data['materials']:
                for v in data['materials']['videos']:
                    if 'audio_fade' not in v:
                        v['audio_fade'] = None
            with open(fpath, 'w', encoding='utf-8') as f2:
                json.dump(data, f2, indent=2)

    def export_to_json(self, export_path: str):
        """
        Exporte le projet CapCut courant dans un fichier JSON simplifié (voir doc).
        Inclut cropping temporel (source_in/source_out), position sur la timeline (start_time), volume, type, piste.
        """
        import json
        for fname in ["draft_content.json"]:
            fpath = self.path / fname
            if not fpath.exists():
                continue
            with open(fpath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            sequences = []
            for idx, track in enumerate(data.get('tracks', [])):
                ttype = track.get('type', 'video')
                for seg in track.get('segments', []):
                    mat_id = seg.get('material_id')
                    # Chercher dans materials
                    mat = None
                    if ttype == 'video':
                        for v in data.get('materials', {}).get('videos', []):
                            if v.get('id') == mat_id:
                                mat = v
                                break
                    elif ttype == 'audio':
                        for a in data.get('materials', {}).get('audios', []):
                            if a.get('id') == mat_id:
                                mat = a
                                break
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump({"sequences": sequences}, f, indent=2)

        """
        Exporte le projet CapCut courant dans un fichier JSON simplifié (voir doc).
        """
        import json
        for fname in ["draft_content.json"]:
            fpath = self.path / fname
            if not fpath.exists():
                continue
            with open(fpath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            sequences = []
            track_types = []
            for idx, track in enumerate(data.get('tracks', [])):
                ttype = track.get('type', 'video')
                track_types.append(ttype)
                for seg in track.get('segments', []):
                    mat_id = seg.get('material_id')
                    # Chercher dans materials
                    mat = None
                    if ttype == 'video':
                        for v in data.get('materials', {}).get('videos', []):
                            if v.get('id') == mat_id:
                                mat = v
                                break
                    elif ttype == 'audio':
                        for a in data.get('materials', {}).get('audios', []):
                            if a.get('id') == mat_id:
                                mat = a
                                break
                    if mat:
                        start = seg['target_timerange']['start']/1_000_000
                        end = (seg['target_timerange']['start']+seg['target_timerange']['duration'])/1_000_000
                        source_in = seg.get('source_timerange', {}).get('start', 0)/1_000_000
                        source_out = (seg.get('source_timerange', {}).get('start', 0) + seg.get('source_timerange', {}).get('duration', seg['target_timerange']['duration']))/1_000_000
                        # Pour la vidéo : fade dans mat['audio_fade'] si présent
                        fade_in = 0.0
                        fade_out = 0.0
                        if ttype == 'video' and mat:
                            audio_fade = mat.get('audio_fade')
                            if audio_fade:
                                fade_in = audio_fade.get('fade_in_duration', 0) / 1_000_000
                                fade_out = audio_fade.get('fade_out_duration', 0) / 1_000_000
                        # Pour l'audio : chercher dans materials.audio_fades
                        elif ttype == 'audio' and mat:
                            audio_fade = None
                            for af in data.get('materials', {}).get('audio_fades', []):
                                if af.get('id') == mat.get('id'):
                                    audio_fade = af
                                    break
                            if audio_fade:
                                fade_in = audio_fade.get('fade_in_duration', 0) / 1_000_000
                                fade_out = audio_fade.get('fade_out_duration', 0) / 1_000_000
                        sequences.append({
                            "path": mat.get('path'),
                            "start_time": start,
                            "end_time": end,
                            "source_in": float(source_in),
                            "source_out": float(source_out),
                            "fade_in_duration": float(fade_in),
                            "fade_out_duration": float(fade_out),
                            "volume": seg.get('volume', mat.get('volume', 1.0)),
                            "type": ttype,
                            "track_index": idx
                        })
            # Sauvegarde du json simplifié
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump({"sequences": sequences}, f, indent=2)

    def add_video_sequence(self, video_path: str, start_time: float, end_time: float, source_in: float = 0.0, source_out: float = None, volume: float = 1.0, track_index: int = 0, fade_in_duration: float = 0.0, fade_out_duration: float = 0.0):
        """
        Ajoute une séquence vidéo au projet CapCut, avec cropping temporel optionnel.
        - video_path: chemin du fichier vidéo
        - start_time: position sur la timeline (en secondes)
        - end_time: fin sur la timeline (en secondes)
        - source_in: début du tronçon dans la vidéo source (en secondes)
        - source_out: fin du tronçon dans la vidéo source (en secondes, défaut=fin du fichier)
        - volume: volume de la séquence
        - track_index: numéro de la piste vidéo (défaut 0)
        """
        import uuid, json
        from pathlib import Path
        start_us = int(start_time * 1_000_000)
        end_us = int(end_time * 1_000_000)
        duration = end_us - start_us
        if source_out is None:
            # On suppose que la longueur du tronçon est end_time-start_time si non précisé
            source_out = source_in + (end_time - start_time)
        source_in_us = int(source_in * 1_000_000)
        source_out_us = int(source_out * 1_000_000)
        source_duration = source_out_us - source_in_us
        for fname in ["draft_content.json", "draft_content.json.bak"]:
            fpath = self.path / fname
            if not fpath.exists():
                continue
            with open(fpath, "r", encoding="utf-8") as f:
                data = json.load(f)
            video_id = str(uuid.uuid4()).upper()
            segment_id = str(uuid.uuid4()).upper()
            data.setdefault("materials", {})
            data["materials"].setdefault("videos", [])
            data["materials"]["videos"].append({
                "id": video_id,
                "path": video_path,
                "duration": source_duration,
                "material_name": Path(video_path).name,
                "volume": volume,
                "width": 1280,
                "height": 720,
                "type": "video"
            })
            data.setdefault("tracks", [])
            # Chercher la piste vidéo voulue
            video_track = None
            for t in data["tracks"]:
                if t.get("type") == "video" and data["tracks"].index(t) == track_index:
                    video_track = t
                    break
            if not video_track:
                video_track = {
                    "attribute": 0,
                    "flag": 0,
                    "id": f"TRACK-{track_index}",
                    "is_default_name": True,
                    "name": f"Track {track_index}",
                    "segments": [],
                    "type": "video"
                }
                # Ajoute à la bonne position
                while len(data["tracks"]) <= track_index:
                    data["tracks"].append({"type": "video", "segments": []})
                data["tracks"][track_index] = video_track
            segments = video_track["segments"]
            segment_entry = {
                "id": segment_id,
                "material_id": video_id,
                "target_timerange": {"start": start_us, "duration": duration},
                "source_timerange": {"start": source_in_us, "duration": source_duration},
                "volume": volume,
                "fade_in": {"duration": int(fade_in_duration * 1_000_000)},
                "fade_out": {"duration": int(fade_out_duration * 1_000_000)}
            }
            segments.append(segment_entry)
            # Sauvegarder le fichier
            with open(fpath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)

    def add_audio_sequence(self, audio_path: str, start_time: float, end_time: float, source_in: float = 0.0, source_out: float = None, volume: float = 1.0, track_index: int = 1, fade_in_duration: float = 0.0, fade_out_duration: float = 0.0):
        """
        Ajoute une séquence audio au projet CapCut, avec cropping temporel optionnel.
        - audio_path: chemin du fichier audio
        - start_time: position sur la timeline (en secondes)
        - end_time: fin sur la timeline (en secondes)
        - source_in: début du tronçon dans l'audio source (en secondes)
        - source_out: fin du tronçon dans l'audio source (en secondes, défaut=fin du fichier)
        - volume: volume de la séquence
        - track_index: numéro de la piste audio (défaut 1)
        """
        import uuid, json
        from pathlib import Path
        start_us = int(start_time * 1_000_000)
        end_us = int(end_time * 1_000_000)
        duration = end_us - start_us
        if source_out is None:
            source_out = source_in + (end_time - start_time)
        source_in_us = int(source_in * 1_000_000)
        source_out_us = int(source_out * 1_000_000)
        source_duration = source_out_us - source_in_us
        for fname in ["draft_content.json", "draft_content.json.bak"]:
            fpath = self.path / fname
            if not fpath.exists():
                continue
            with open(fpath, "r", encoding="utf-8") as f:
                data = json.load(f)
            audio_id = str(uuid.uuid4()).upper()
            segment_id = str(uuid.uuid4()).upper()
            data.setdefault("materials", {})
            data["materials"].setdefault("audios", [])
            data["materials"]["audios"].append({
                "id": audio_id,
                "path": audio_path,
                "duration": source_duration,
                "material_name": Path(audio_path).name,
                "volume": volume,
                "type": "audio"
            })
            data.setdefault("tracks", [])
            # Chercher la piste audio voulue
            audio_track = None
            for t in data["tracks"]:
                if t.get("type") == "audio" and data["tracks"].index(t) == track_index:
                    audio_track = t
                    break
            if not audio_track:
                audio_track = {
                    "attribute": 0,
                    "flag": 0,
                    "id": f"AUDIO-TRACK-{track_index}",
                    "is_default_name": True,
                    "name": f"Audio Track {track_index}",
                    "segments": [],
                    "type": "audio"
                }
                while len(data["tracks"]) <= track_index:
                    data["tracks"].append({"type": "audio", "segments": []})
                data["tracks"][track_index] = audio_track
            segments = audio_track["segments"]
            segment_entry = {
                "id": segment_id,
                "material_id": audio_id,
                "target_timerange": {"start": start_us, "duration": duration},
                "source_timerange": {"start": source_in_us, "duration": source_duration},
                "volume": volume,
                "fade_in": {"duration": int(fade_in_duration * 1_000_000)},
                "fade_out": {"duration": int(fade_out_duration * 1_000_000)}
            }
            segments.append(segment_entry)
            # Sauvegarder le fichier
            with open(fpath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)

        """
        Ajoute une séquence vidéo au projet CapCut.
        video_path: chemin absolu de la vidéo
        start_time: début de la séquence (en SECONDES)
        end_time: fin de la séquence (en SECONDES)
        crop: dict optionnel avec les clés (lower_left_x, lower_left_y, lower_right_x, lower_right_y, upper_left_x, upper_left_y, upper_right_x, upper_right_y)
        """
        import uuid
        import json
        from pathlib import Path
        # Conversion secondes -> microsecondes
        start_us = int(start_time * 1_000_000)
        end_us = int(end_time * 1_000_000)
        duration = end_us - start_us
        for fname in ["draft_content.json", "draft_content.json.bak"]:
            fpath = self.path / fname
            if not fpath.exists():
                continue
            with open(fpath, "r", encoding="utf-8") as f:
                data = json.load(f)
            # Générer les IDs uniques
            video_id = str(uuid.uuid4()).upper()
            segment_id = str(uuid.uuid4()).upper()
            # Ajout dans materials["videos"]
            data.setdefault("materials", {})
            data["materials"].setdefault("videos", [])
            data["materials"]["videos"].append({
                "aigc_history_id": "",
                "aigc_item_id": "",
                "aigc_type": "none",
                "audio_fade": None,
                "beauty_body_preset_id": "",
                "beauty_face_auto_preset": {"name": "", "preset_id": "", "rate_map": ""},
                "beauty_face_auto_preset_infos": [],
                "beauty_face_preset_infos": [],
                "cartoon_path": "",
                "category_id": "",
                "category_name": "local",
                "check_flag": 62978047,
                "crop": crop if crop else {"lower_left_x":0.0,"lower_left_y":1.0,"lower_right_x":1.0,"lower_right_y":1.0,"upper_left_x":0.0,"upper_left_y":0.0,"upper_right_x":1.0,"upper_right_y":0.0},
                "crop_ratio": "free",
                "crop_scale": 1.0,
                "duration": duration,
                "extra_type_option": 0,
                "formula_id": "",
                "freeze": None,
                "has_audio": True,
                "has_sound_separated": False,
                "height": 720,
                "id": video_id,
                "intensifies_audio_path": "",
                "intensifies_path": "",
                "is_ai_generate_content": False,
                "is_copyright": False,
                "is_text_edit_overdub": False,
                "is_unified_beauty_mode": False,
                "live_photo_cover_path": "",
                "live_photo_timestamp": -1,
                "local_id": "",
                "local_material_from": "",
                "local_material_id": str(uuid.uuid4()),
                "material_id": "",
                "material_name": Path(video_path).name,
                "material_url": "",
                "matting": {"custom_matting_id": "","enable_matting_stroke": False,"expansion": 0,"feather": 0,"flag": 0,"has_use_quick_brush": False,"has_use_quick_eraser": False,"interactiveTime":[],"path": "","reverse": False,"strokes": []},
                "media_path": "",
                "multi_camera_info": None,
                "object_locked": None,
                "origin_material_id": "",
                "path": video_path,
                "picture_from": "none",
                "picture_set_category_id": "",
                "picture_set_category_name": "",
                "request_id": "",
                "reverse_intensifies_path": "",
                "reverse_path": "",
                "smart_match_info": None,
                "smart_motion": None,
                "source": 0,
                "source_platform": 0,
                "stable": {"matrix_path": "","stable_level": 0,"time_range": {"duration": 0,"start": 0}},
                "team_id": "",
                "type": "video",
                "video_algorithm": {"ai_background_configs":[],"ai_expression_driven":None,"ai_motion_driven":None,"aigc_generate":None,"algorithms":[],"complement_frame_config":None,"deflicker":None,"gameplay_configs":[],"image_interpretation":None,"motion_blur_config":None,"mouth_shape_driver":None,"noise_reduction":None,"path": "","quality_enhance":None,"smart_complement_frame":None,"super_resolution":None,"time_range":None},
                "width": 1280
            })
            # Gestion du track unique vidéo principal
            data.setdefault("tracks", [])
            # Chercher un track vidéo principal (type=="video")
            video_track = None
            for t in data["tracks"]:
                if t.get("type") == "video":
                    video_track = t
                    break
            if not video_track:
                # Créer un nouveau track vidéo principal
                import uuid
                video_track = {
                    "attribute": 0,
                    "flag": 0,
                    "id": str(uuid.uuid4()).upper(),
                    "is_default_name": True,
                    "name": "",
                    "segments": [],
                    "type": "video"
                }
                data["tracks"].append(video_track)
            # Calcul du start réel (fin du dernier segment ou 0)
            segments = video_track["segments"]
            if segments:
                last = segments[-1]
                prev_end = last["target_timerange"]["start"] + last["target_timerange"]["duration"]
                real_start = prev_end
            else:
                real_start = 0
            # Correction de la durée projet si besoin
            if "duration" in data:
                data["duration"] = max(data.get("duration", 0), real_start + duration)
            # Ajout du segment à la suite
            segment_entry = {
                "caption_info": None,
                "cartoon": False,
                "clip": {
                    "alpha": 1.0,
                    "flip": {"horizontal": False, "vertical": False},
                    "rotation": 0.0,
                    "scale": {"x": 1.0, "y": 1.0},
                    "transform": {"x": 0.0, "y": 0.0}
                },
                "color_correct_alg_result": "",
                "common_keyframes": [],
                "desc": "",
                "digital_human_template_group_id": "",
                "enable_adjust": True,
                "enable_adjust_mask": False,
                "enable_color_correct_adjust": False,
                "enable_color_curves": True,
                "enable_color_match_adjust": False,
                "enable_color_wheels": True,
                "enable_hsl": False,
                "enable_lut": True,
                "enable_smart_color_adjust": False,
                "enable_video_mask": True,
                "extra_material_refs": [],
                "group_id": "",
                "hdr_settings": {"intensity": 1.0, "mode": 1, "nits": 1000},
                "id": segment_id,
                "intensifies_audio": False,
                "is_loop": False,
                "is_placeholder": False,
                "is_tone_modify": False,
                "keyframe_refs": [],
                "last_nonzero_volume": 1.0,
                "lyric_keyframes": None,
                "material_id": video_id,
                "raw_segment_id": "",
                "render_index": 0,
                "render_timerange": {"duration": 0, "start": 0},
                "responsive_layout": {"enable": False, "horizontal_pos_layout": 0, "size_layout": 0, "target_follow": "", "vertical_pos_layout": 0},
                "reverse": False,
                "source_timerange": {"duration": duration, "start": start_us},
                "speed": 1.0,
                "state": 0,
                "target_timerange": {"duration": duration, "start": real_start},
                "template_id": "",
                "template_scene": "default",
                "track_attribute": 0,
                "track_render_index": 0,
                "uniform_scale": {"on": True, "value": 1.0},
                "visible": True,
                "volume": 1.0
            }
            segments.append(segment_entry)
            # Sauvegarder le fichier
            with open(fpath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
