import numpy as np
from matplotlib.colors import ListedColormap

flow_colors_hex = [
    "#000000",  # 0  empty square
    "#FF0000",  # 1  Bright Red
    "#FFFF00",  # 2  Yellow
    "#0000FF",  # 3  Blue
    "#008000",  # 4  Green
    "#FF8C00",  # 5  Orange
    "#00FFFF",  # 6 Cyan (Light Blue)
    "#800080",  # 7  Purple
    "#FF1493",  # 8  Pink (Magenta)
    "#8B0000",  # 9  Dark Red (Maroon)
    "#FFFFFF",  # 10 White
]
flow_colors = ["Black", "Red", "Yellow", "Blue", "Green", "Orange", "Cyan", "Purple", "Pink", "Dark Red", "White"]
boards_sizes = ("6x6", "8x8", "10x10")

game_boards_examples = {
    "6x6": np.array([
        [0, 0, 0, 3, 0, 0],
        [0, 4, 0, 5, 1, 3],
        [0, 0, 0, 4, 0, 2],
        [0, 2, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 5],
    ]),
    "8x8": np.array([
        [0, 0, 0, 0, 0, 0, 0, 9],
        [0, 3, 0, 4, 0, 0, 5, 2],
        [0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 7, 0, 0, 0],
        [0, 0, 4, 0, 5, 9, 0, 0],
        [0, 0, 3, 0, 0, 0, 0, 0],
        [0, 0, 1, 7, 8, 0, 8, 0],
        [6, 0, 0, 6, 2, 0, 0, 0]
    ]),
    "10x10": np.array([
        [0, 9, 0, 0, 0, 0, 0, 0, 0, 1],
        [0, 4, 0, 5, 0, 0, 0, 0, 0, 3],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 9],
        [0, 0, 1, 7, 8, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 8, 0, 0, 0, 0],
        [0, 5, 0, 0, 0, 4, 7, 0, 3, 0],
        [0, 6, 2, 0, 0, 0, 0, 0, 6, 0],
        [0, 0, 0, 0, 0, 0, 0, 2, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ])
}

setting = {
    "6x6": {
        "colors_num": 5,
        "w": 6, "h": 6, "cmap": ListedColormap(flow_colors_hex[:6]),
        "options": [*range(6)],
        "ex_positions": {v: np.argwhere(game_boards_examples["6x6"] == v) for v in range(1, 6)}
    },
    "8x8": {
        "colors_num": 9,
        "w": 8, "h": 8, "cmap": ListedColormap(flow_colors_hex[:10]),
        "options": [*range(8)],
        "ex_positions": {v: np.argwhere(game_boards_examples["8x8"] == v) for v in range(1, 10)}
    },
    "10x10": {
        "colors_num": 9,
        "w": 10, "h": 10, "cmap": ListedColormap(flow_colors_hex[:10]),
        "options": [*range(10)],
        "ex_positions": {v: np.argwhere(game_boards_examples["10x10"] == v) for v in range(1, 10)}
    },
}
