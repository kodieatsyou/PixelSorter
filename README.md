# PixelSorter

A small desktop app for making glitchy **pixel-sorted images** using Python, Tkinter, NumPy, and Pillow.

Pixel sorting is a visual effect where contiguous runs of pixels are reordered by brightness. This tool lets you experiment with that effect interactively: load an image, tweak thresholds, sort vertically or horizontally, and export the result.

---

## Features

- Load `.png` and `.jpg` images  
- Sort pixels:
  - **Vertically** (down each column)
  - **Horizontally** (across each row)
- Control how aggressive the effect is using light/dark thresholds  
- Export the final image to disk

---

## Requirements

- Python 3.10+ (newer versions are fine as long as Tkinter works)
- Packages:
  - `numpy`
  - `pillow`

---

## Setup

From the project directory:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install numpy pillow
```

## Running the app
```bash
python pixelsorter.py
```
A window should open with the UI.

## How to use it
- Click Select Image and choose a PNG or JPG.
-(Optional) Adjust:
 - Lightness threshold
 - Darkness threshold
- Click Vertical Sort or Horizontal Sort to apply the effect.
- Click Export Sorted Image to save the output.

## Thresholds explained

The app doesn’t sort every pixel — only pixels whose brightness falls inside a range:

dark_threshold <= brightness <= light_threshold

What this means visually:
- Thresholds close together → subtle, broken-up glitch effect
- Thresholds far apart → heavy smearing and strong pixel stretching
If you accidentally swap the values, the app automatically fixes the order internally.

## Example results

### Before:
![Input](input/Test.png)

### After (Horizontal Sort):
![Output](output/export.png)
