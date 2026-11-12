# ➶ Vector Quest

A 2D side-scrolling platformer for the desktop, written in Python with pygame, where you move and fight by **drawing vectors with your mouse**. Drag an arrow from your hero and you fly along it. Drag an arrow onto an enemy and it takes damage equal to the arrow's length. Collect four relics across five short stages and place them in the throne room to win.

## Why this project exists

GloryVerse 2.0 was built to explore how a physics idea, **vectors**, can drive real game mechanics instead of just appearing in a textbook. Movement is vector addition (several arrows are summed into one resultant), attack damage is vector magnitude, and your reach grows as you clear enemies. It was also a way to practise building a complete game loop in pygame: event handling, gravity and collisions, simple enemy AI, level transitions and animation.

## Features

- **Mouse-drawn vector mechanics**: one arrow moves you, a sum of arrows moves you faster, and an arrow that lands on an enemy hurts it.
- **Planning mode**: queue up several vectors, then fire them all at once.
- **Five stages**: entrance, enemy-filled field, wave-swept bridge, castle wall and throne room.
- **Enemy AI**: 12 enemies patrol back and forth and home in on you when you get close.
- **Progression**: defeating enemies permanently extends your vector range.
- **Inventory and puzzle ending**: collect a sword, shield, rope and crystal, then place them on four altars.
- Runs at 60 FPS in an 800×400 window. No installer, no config files.

## Built with

| Item | Details |
|---|---|
| Language | Python 3.8 or newer |
| Game library | [pygame](https://www.pygame.org/) (windowing, input, image loading, drawing, rect collisions) |
| Standard library | `random`, `datetime`, `sys`, `time` |
| Art | PNG/JPG sprites, backgrounds and a 12-frame wave animation (see [Required asset files](#required-asset-files)) |

## Screenshots

> Replace these with your own captures (see [Adding screenshots](#adding-screenshots)).

| Title screen | Drawing vectors | Enemies in the field |
|---|---|---|
| ![Title screen](docs/screenshots/title.png) | ![Drawing vectors](docs/screenshots/vectors.png) | ![Field level](docs/screenshots/field.png) |
| **Bridge and wave** | **Castle wall** | **Throne room / win** |
| ![Bridge](docs/screenshots/bridge.jpg) | ![Castle wall](docs/screenshots/castle-walls.jpg) | ![Throne room](docs/screenshots/throne.png) |

## Getting started

### 1. Prerequisites

- Python 3.8 or newer (`python --version` to check)
- `pip`, which comes with Python

### 2. Get the code

```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>
```

### 3. (Recommended) create a virtual environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### 4. Install the dependency

```bash
pip install pygame
```

Check it worked:

```bash
python -c "import pygame; print(pygame.version.ver)"
```

### 5. Run the game

Run it **from the project folder**, because every image is loaded by a relative path:

```bash
python main.py
```

(Use whatever your script is called; `main.py` is used here as an example.)

There are no environment variables and no build step. A terminal window stays open alongside the game and prints hints and status messages such as `LEVEL 1 COMPLETED!`, so it's worth keeping visible.

## Required asset files

The game loads all of its art from the folder you run it in (and one subfolder for the wave animation). If the game crashes on start with a "No file ... found" error, one of these is missing.

| Used for | Files |
|---|---|
| Player (40×50 px) | `player-0.png` (standing), `player-1.png` (jumping), `player--1.png` (falling) |
| Vector arrow tip | `arrowhead.png` |
| Inventory / altar icons | `sword-frame-filled.png`, `shield-frame-filled.png`, `rope-frame-filled.png`, `crystal-frame-filled.png` |
| Enemy | `enemy_red_100_by_100.png` |
| Platform and ground tiles | `tile_map-layer1.jpg`, `tile_map-layer2.jpg` |
| Level backgrounds (800×400) | `entrance.png` (stage 0), `2d-background.jpg` (stage 1), `crystal-level1.png` (stage 1 after all enemies are defeated), `bridge-in-forest.jpg` (stage 2), `castle-gates.jpg` (stage 3), `throne-room.png` (stage 4) |
| Full-screen overlays | `start-menu.png`, `death-screen.png`, `win_screen.png` |
| Wave animation (12 frames) | `anim/waves/wave0.png` … `anim/waves/wave11.png` |

## How to play

**Goal:** get through all five stages, collecting a sword, shield, rope and crystal, then place all four on the altars in the throne room and walk to the centre to win.

### Controls

| Input | Action |
|---|---|
| **Enter** | Start the game from the title screen |
| **A / D** | Move left / right (hold) |
| **W** | Jump (only while on the ground) |
| **Mouse: press, drag, release** | Draw a vector (see below) |
| **Q** | Toggle *planning mode* (see below) |
| **C** | Pick up an item when standing at a pickup spot (stages 0 and 1) |
| **K** | Place a relic on an altar (stage 4) |
| **R** | Restart from stage 1 after a game over |
| Close the window | Quit |

### The vector system

Press the mouse button where the arrow should **start**, drag, and release where it should **end**. The arrow is drawn as a thick brown line with an arrowhead.

- **Range limit.** Both ends of a vector must be within your current *range* of the player (100 px at the start). Vectors that go out of range are discarded, and only in-range vectors are drawn. The range is not drawn on screen.
- **Move vector.** If the arrow *starts on your character*, you are carried by the arrow's displacement (how far it goes in x and y). Draw several move vectors and they are **added together** into one resultant, and each extra vector also multiplies your speed. This is how you cross gaps and climb walls that a normal jump can't.
- **Attack vector.** If the arrow starts *anywhere else* and its tip lands on an enemy, the enemy takes damage equal to the arrow's **length in pixels**. Enemies have 100 HP.
- **Planning mode (Q).** Normally each vector fires the moment you release the mouse. Press **Q** to enter planning mode, draw as many vectors as you like, then press **Q** again to fire them all together. There is no on-screen indicator; the terminal prints `PREPARING: True/False`.

### Range upgrades

Your range grows permanently as you clear the 12 enemies in stage 1:

| Enemies remaining | Bonus | Total range |
|---|---|---|
| 12 to 10 | none | 100 px |
| 9 or fewer | +50 | 150 px |
| 7 or fewer | +100 | 250 px |
| 4 or fewer | +200 | 450 px |

### Enemies

Twelve red enemies float at random heights in stage 1 and patrol back and forth. If one gets within about 100 px of you it homes in on you, and **touching one is instant game over**. Kill them from a distance with attack vectors.

<details>
<summary><strong>Stage-by-stage walkthrough (spoilers)</strong></summary>

| Stage | What to do |
|---|---|
| **0 · Entrance** | Press **Enter** on the title screen. Stand in the middle of the screen (x ≈ 375–500) and press **C** to take the **sword** and **shield**. Walk off the right edge. (You already start with the **rope**.) |
| **1 · Field** | Defeat the enemies with attack vectors. Once all are gone, the background changes to reveal the crystal. Stand at x ≈ 584–652 and press **C** to take the **crystal**, then walk off the right edge. |
| **2 · Bridge** | Walk across. A wave animation starts as you advance, and you can't pass x = 300 until it has been beaten. You survive it only if you have the **sword**; without it you get a game over. |
| **3 · Castle wall** | Climb the wall using move vectors, because jumping alone isn't high enough. The wall is lower at x ≈ 81–139, 261–499 and 651–699, so those are the easiest places to climb. |
| **4 · Throne room** | Stand at each altar and press **K**: sword (x ≈ 0–50), shield (x ≈ 150–220), rope (x ≈ 550–620), crystal (x ≈ 720–750). When all four are placed, steps rise toward the centre. Walk to x ≈ 362–434 to win. |

</details>

## How the code is organised

Everything is in one script, in roughly this order:

1. **Setup**: window (800×400), world constants (ground level, screen limits) and the shared lists for vectors, enemies and tiles.
2. **Classes**
   - `Player`: sprites (standing, jumping, falling), rect, inventory, current destination and step speed.
   - `Enemy`: 100 HP, patrol direction and speed, collision flag.
   - `vectorAttack`: base range, range bonuses, `eff_range` (the total) and the arrowhead sprite.
   - `Coords`: a small helper for adding and subtracting coordinate pairs.
   - `BackGround` and `Obj`: lazy-loaded background holder, and an inventory item (name plus icon).
3. **Helper functions**
   - `move_toward`: steps an object toward a target along the straight line between them.
   - `distance`: Euclidean distance between two points.
   - `check_vector_movements`: sums every move vector into a resultant and sets the player's destination.
   - `check_vector_attack`: applies damage to enemies hit by attack vectors and removes dead ones.
   - `reward_player`: grants the range bonuses.
   - `enemy_movement`, `tiles_collision`, `load_bg`, `draw_ground`.
4. **Main loop** (60 times a second):
   1. Load and draw the current stage's background and ground.
   2. Run stage-specific logic (edge-of-screen transitions, the wave check, the wall climb check, the altars).
   3. Handle events (mouse vectors and keyboard).
   4. Apply movement: A/D, vector destination, jump, gravity, clamp to the screen.
   5. Move and draw enemies (stage 1) and resolve tile collisions.
   6. Draw vectors, tiles, the player and any overlay (title, death or win screen).
   7. `pygame.display.update()` and `clock.tick(60)`.

## Project structure

```
.
├── main.py                  # the whole game (use your script's real name)
├── README.md
├── *.png / *.jpg            # sprites, backgrounds, overlays (see Required asset files)
├── anim/
│   └── waves/
│       └── wave0.png … wave11.png
└── docs/
    └── screenshots/         # images used in this README
```

## Adding screenshots

1. Run the game and play to each of the moments listed in the [Screenshots](#screenshots) table. Planning mode (**Q**) with a few vectors drawn makes a good "Drawing vectors" shot.
2. Capture the game window (Windows: `Win + Shift + S`; macOS: `Cmd + Shift + 4`; Linux: your screenshot tool).
3. Save the images in `docs/screenshots/` using the file names used above (`gameplay.png`, `title.png`, `vectors.png`, `field.png`, `bridge.png`, `castle.png`, `throne.png`).
4. Commit them so they render on GitHub.

## Troubleshooting

| Problem | Fix |
|---|---|
| `ModuleNotFoundError: No module named 'pygame'` | Install it into the same Python you run the game with: `python -m pip install pygame`. |
| `pip install pygame` fails on a very new Python version | Use [pygame-ce](https://pypi.org/project/pygame-ce/), a community fork with the same API (`pip install pygame-ce`), or a slightly older Python such as 3.12 or 3.13. |
| `FileNotFoundError` / "No file ... found" on startup | Run the script from the project folder and check every file in [Required asset files](#required-asset-files) is present. |
| Crash when the wave appears on stage 2 (macOS / Linux) | That line loads `anim\waves\waveN.png` with Windows backslashes. Change it to `f"anim/waves/wave{int(frame)}.png"`; forward slashes work on every OS, including Windows. |
| Keys do nothing | Click the game window so it has focus. |
| Vectors don't appear | One end of the arrow is outside your range. Start closer to the character, or clear more enemies to extend the range. |
| Lots of text in the terminal | Normal: the game prints debug and status messages while you play. |

## Known limitations and ideas

- Pressing **R** after a game over returns you to stage 1 but doesn't respawn defeated enemies or reset your inventory.
- A few images (title, death screen, wave frames, the cleared-field background) are re-loaded from disk every frame they're shown. Pre-loading them once would be faster.
- Levels, altars and pickup spots are hard-coded x-ranges inside one long script. Moving them into data structures, and splitting the code into modules, would make adding stages easier.
- Ideas: an on-screen HUD (range circle, planning-mode indicator, HP bars), sound, a score or timer, and gamepad support.

## Credits

Add attribution for any third-party art here (sprites, backgrounds, tile sets), with links and licenses, for example:

- Sprites: *name / source / license*
- Backgrounds: *name / source / license*

## License

Add a license of your choice (for example MIT) as a `LICENSE` file, and mention it here.