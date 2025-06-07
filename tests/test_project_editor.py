
from capcut_project import Project
# To create a new project:
project = Project(
    r'C:\Users\Yanis\AppData\Local\CapCut\User Data\Projects\com.lveditor.draft\test_4',
    r'projects/test_4.json',
    create=True
)


project.sync_from_json(r'projects/test_4.json')
#project.export_to_json(r'projects/test_4.json')


# project.add_video_sequence(
#     video_path=r'C:\Users\Yanis\Documents\code\retro_engineered_capcut\test_video\test_vid_1.mp4',
#     start_time=2.5,    # 2,5 secondes
#     end_time=7.0,      # 7,0 secondes

#     crop=None          # ou dictionnaire crop si besoin
# )

# project.add_video_sequence(
#     video_path=r'C:\Users\Yanis\Documents\code\retro_engineered_capcut\test_video\test_vid_2.mp4',
#     start_time=7.0,    # 2,5 secondes
#     end_time=9.0,      # 7,0 secondes
#     crop=None          # ou dictionnaire crop si besoin
# )