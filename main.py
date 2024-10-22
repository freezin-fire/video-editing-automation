import xml.etree.ElementTree as ET
from xml.dom import minidom

def prettify(elem):
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def create_fcpxml(video_paths, output_file):
    fcpxml = ET.Element('fcpxml', version="1.8")

    resources = ET.SubElement(fcpxml, 'resources')

    for i, video_path in enumerate(video_paths):
        asset = ET.SubElement(resources, 'asset', {
            'id': f'r{i+1}',
            'name': video_path,
            'src': f'file://{video_path}'
        })

    library = ET.SubElement(fcpxml, 'library')
    event = ET.SubElement(library, 'event', {'name': 'Video Event'})
    project = ET.SubElement(event, 'project', {'name': 'Stitched Videos'})
    sequence = ET.SubElement(project, 'sequence', {'duration': '60s'})
    spine = ET.SubElement(sequence, 'spine')

    for i, video_path in enumerate(video_paths):
        clip = ET.SubElement(spine, 'clip', {
            'name': video_path,
            'offset': f'{i * 20}s',
            'duration': '20s'
        })

        video = ET.SubElement(clip, 'video', {'ref': f'r{i+1}'})
        
        if i < len(video_paths) - 1:
            transition = ET.SubElement(spine, 'transition', {
                'name': 'Cross Dissolve',
                'offset': f'{(i+1) * 20}s',
                'duration': '2s'
            })

    xml_str = prettify(fcpxml)

    with open(output_file, 'w') as f:
        f.write(xml_str)

    print(f"FCPXML saved successfully at {output_file}")

video_paths = [
    "videos/one.mp4",
    "videos/two.mp4",
    "videos/three.mp4"
]

output_file = "output_timeline.fcpxml"

create_fcpxml(video_paths, output_file)