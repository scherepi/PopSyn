import numpy as np


emotion_colors = {
    "fear":        (128, 0, 128),   # purple
    "anger":       (255, 0, 0),     # red
    "anticipation":(255, 165, 0),   # orange
    "trust":       (0, 128, 0),     # green
    "surprise":    (0, 255, 255),   # cyan
    "positive":    (255, 255, 255), # white
    "negative":    (0, 0, 0),       # black
    "sadness":     (0, 0, 255),     # blue
    "disgust":     (0, 100, 0),     # dark green
    "joy":         (255, 255, 0)    # yellow
}

def emotions_to_color(emotions):
    for e in emotion_colors:
        emotions.setdefault(e, 0)
    total = sum(emotions.values())
    if total == 0:
        return (128, 128, 128)  # neutral gray
    
    normalized = {k: v / total for k, v in emotions.items()}

    r, g, b = 0, 0, 0
    for emotion, weight in normalized.items():
        cr, cg, cb = emotion_colors[emotion]
        r += cr * weight
        g += cg * weight
        b += cb * weight

    return int(r), int(g), int(b)

def rgb_to_hex(rgb: tuple[int, int, int]) -> str:
    return "#{:02x}{:02x}{:02x}".format(*rgb)