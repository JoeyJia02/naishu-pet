"""Verify packaged bytes and optionally export unchanged atlas cells as APNG."""
import argparse
import hashlib
import json
from pathlib import Path
from PIL import Image
from apng_fullframes import save_full_apng

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--export', action='store_true')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    manifest = json.loads((root/'manifest.json').read_text())
    for item in manifest['files']:
        data = (root/item['path']).read_bytes()
        assert len(data) == item['bytes'], item['path']
        assert hashlib.sha256(data).hexdigest() == item['sha256'], item['path']
    atlas = Image.open(root/'assets/spritesheet.png').convert('RGBA')
    assert atlas.size == (1536, 2288)
    spec = json.loads((root/'assets/animation.json').read_text())
    for row in spec['rows']:
        frames=[]
        for col in range(8):
            cell=atlas.crop((col*192,row['row']*208,(col+1)*192,(row['row']+1)*208))
            occupied=cell.getchannel('A').getbbox() is not None
            assert occupied == (col < row['frames']), (row['state'],col)
            if occupied: frames.append(cell)
        if row['row'] < 9:
            preview=Image.open(root/'previews'/(row['state']+'.apng'))
            assert preview.n_frames == len(frames)
            for i, frame in enumerate(frames):
                preview.seek(i)
                assert preview.convert('RGBA').tobytes() == frame.tobytes(), (row['state'],i)
                assert abs(preview.info['duration']-row['durations_ms'][i]) < .01
        if args.export:
            save_full_apng(frames,row['durations_ms'],root/'exported'/(row['state']+'.apng'))
    print('PASS: file hashes, atlas layout, transparency, and standard preview pixels/timing')

if __name__ == '__main__':
    main()
