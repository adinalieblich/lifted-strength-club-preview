"""Copies and resizes the site photos the ad landing page mockups use into ./img (run from the repo root)."""
import pathlib
from PIL import Image

OUT = pathlib.Path(__file__).parent / "img"
OUT.mkdir(exist_ok=True)
SRC = {
    "studio": "images/Lifted-Strength-Club-Studio.jpg",
    "sharon": "images/Sharon-Gam-Headshot-7-28a91ab438.jpg",
    "t2": "images/Sharon-Gam-Personal-Training-2-61a5e38837.jpg",
    "t3": "images/Sharon-Gam-Personal-Training-3-1eb3889237.jpg",
    "t5": "images/Sharon-Gam-Personal-Training-5-0c0ea6986f.jpg",
    "t6": "images/Sharon-Gam-Personal-Training-6-e109244809.jpg",
}
for name, path in SRC.items():
    im = Image.open(path).convert("RGB")
    im.thumbnail((1100, 1100))
    im.save(OUT / f"{name}.jpg", quality=80)
Image.open("lifted-logo-white.png").save(OUT / "logo-white.png")
print("images ready in", OUT)
