import xml.etree.ElementTree as ET
from moviepy.editor import VideoFileClip, concatenate_videoclips, CompositeVideoClip, TextClip


def read_fcpxml(fcpxml_file):
    tree = ET.parse(fcpxml_file)
    root = tree.getroot()
    
    video_assets = {}
    clips_data = []

    for asset in root.findall('.//asset'):
        asset_id = asset.get('id')
        video_src = asset.get('src').replace('file://', '')
        video_assets[asset_id] = video_src
    
    for clip in root.findall('.//spine/clip'):
        clip_data = {
            'name': clip.get('name'),
            'offset': clip.get('offset', '0s'),
            'duration': clip.get('duration', '10s'),
            'ref': clip.find('video').get('ref')
        }
        clips_data.append(clip_data)

    return video_assets, clips_data

def render_video_from_fcpxml(fcpxml_file, output_file):

    video_assets, clips_data = read_fcpxml(fcpxml_file)
    
    clips = []

    for clip_data in clips_data:
        video_file = video_assets[clip_data['ref']]
        clip_duration = float(clip_data['duration'].replace('s', '')) 
        
        video_clip = VideoFileClip(video_file).subclip(0, clip_duration)
        
        clips.append(video_clip)

    final_video = concatenate_videoclips(clips, method="compose")

    final_video.write_videofile(output_file, codec='libx264', audio_codec='aac')
    print(f"Video rendered and saved to {output_file}")

fcpxml_file = 'output_timeline.fcpxml'
output_file = 'final_video.mp4'

render_video_from_fcpxml(fcpxml_file, output_file)
