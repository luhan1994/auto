import os
import shutil
from PIL import Image
from pathlib import Path

IMAGE_PATH = "luhan1994.github.io/assets/"

if __name__ == "__main__":
    p = Path(IMAGE_PATH)
    file_names = [x.name for x in p.iterdir()]
    for infile in file_names:
        f, e = os.path.splitext(infile)
        outfile = f + ".jpg"
        if infile != outfile:
            try:
                with Image.open(IMAGE_PATH + infile) as im:
                    im.save(IMAGE_PATH + outfile)
                os.remove(IMAGE_PATH + infile)
            except OSError:
                print("cannot convert", infile)