# Mosaic

Watch up to four games or videos on one screen. Mosaic arranges Chrome windows into a grid and can expand each video player to fill its tile. Pick games from a terminal menu or bring your own links.

Built for **macOS and Google Chrome**.

## Features

- Watch one to four videos with layouts chosen automatically.
- Browse games by sport, combine leagues, or search by team name.
- See scores and game status in the picker when matching data is available.
- Use a connected external display automatically, or choose your primary display.
- Open YouTube links in one local grid, or other sources in separate Chrome app windows.
- Expand supported players with the bundled Chrome extension or Apple Events script.

## Start here: first-time setup

You need a **Mac**, **Google Chrome**, and an internet connection. Windows and Linux are not supported. You do not need to know how to code or have a GitHub account to download Mosaic.

### 1. Open Terminal

Press **Command + Space**, type **Terminal**, and press **Return**. Terminal is the Mac app where you paste the commands below.

Copy only the text inside each command box, paste it into Terminal, and press **Return**. Run the boxes in order. When a box contains several lines, you can paste them together. Wait for a command to finish before continuing. You do not need to copy the gray formatting or the words around the boxes.

### 2. Check the tools Mosaic needs

**Google Chrome:** if you do not have it, download it from [Google's Chrome website](https://www.google.com/chrome/), open the downloaded file, and drag Chrome into **Applications**. Open Chrome once to finish its setup.

**Git** downloads Mosaic. Check whether it is installed:

```sh
git --version
```

If you see a version number, continue. If macOS offers to install command line developer tools, accept the installation and wait for it to finish. If it does not offer, run this command and follow the installer:

```sh
xcode-select --install
```

Then run `git --version` again. This installation method is documented on [Git's macOS installation page](https://git-scm.com/install/mac).

**Python** runs the game picker. Check whether it is installed:

```sh
python3 --version
```

If you see `Python 3` followed by a version number, continue. Otherwise, download a Python 3 **macOS installer** from [Python's official download page](https://www.python.org/downloads/macos/), open it, and follow the installer. Close and reopen Terminal, then run `python3 --version` again.

Mosaic does not require Homebrew, Node.js, or any extra Python packages.

### 3. Download Mosaic and start it

Copy and run this box **once**. It downloads Mosaic into a folder called `mosaic` inside your Mac's home folder, then opens the NHL game picker:

```sh
git clone https://github.com/rithvikm/mosaic.git "$HOME/mosaic"
cd "$HOME/mosaic"
export PATH="$PWD:$PATH"
mosaic nhl
```

If Terminal says the folder already exists because you downloaded Mosaic before, skip the `git clone` line and run the remaining three lines. If no NHL games are listed today, try:

```sh
mosaic all
```

The `export PATH` line tells this Terminal window where to find the `mosaic` command. It lasts until you close that window. You can also run `./mosaic nhl` from inside the Mosaic folder without that line.

On the first launch, macOS may ask whether Terminal can control Google Chrome. Choose **Allow** so Mosaic can arrange the windows.

### 4. Choose your games

Here is an example of the picker. These scores are made up to illustrate the screen:

```text
Mosaic | 3 games | 2/4 selected
Up/Down: move  Space: select  Enter: launch  q: quit
a: select all (up to 4)  c: clear  PgUp/PgDn: scroll  Home/End: first/last
[x]   1  Buffalo Sabres vs Chicago Blackhawks    3-2  8:42 - 3rd
[x]   2  Edmonton Oilers vs Seattle Kraken       1-1  12:06 - 2nd
[ ]   3  Toronto Maple Leafs vs Ottawa Senators  —    7:00 PM ET
```

- **Up / Down arrows:** move through the games. The list scrolls as you move.
- **Space:** select the highlighted game. `[x]` means selected. Press Space again to deselect it.
- **Return / Enter:** open exactly the games you selected. Choose at least one and at most four.
- **a:** select every game when the list has four or fewer. If eight games are shown, use Space to choose any four of those eight.
- **c:** clear your selections.
- **q** or **Esc:** leave without opening games.
- **Page Up / Page Down**, or **Home / End:** jump through a longer list. You can also move one row at a time with the arrow keys.

Scores follow the order of the teams in each matchup. The text beside a score shows the game clock, scheduled start, or status. Scores are fetched when you run the command; they do not refresh continuously in the menu. Missing scores appear as `—`.

Chrome opens and arranges the games you checked. You may need to sign in to a provider or press **Play** in each player. Mute the players you do not want to hear using their volume controls. If the webpage surrounds the video, follow [Make the video fill its window](#make-the-video-fill-its-window).

### 5. Start Mosaic again later

Whenever you open a new Terminal window, paste this box. **You do not need to download Mosaic again.**

```sh
cd "$HOME/mosaic"
export PATH="$PWD:$PATH"
mosaic all
```

Replace `all` with `nhl`, `nba`, `nfl`, or another sport to narrow the list. Close the game windows using their red close buttons when you finish watching. Closing Terminal alone does not close Chrome.

## Examples to try

The commands below assume you have completed step 3 or step 5 in the current Terminal window.

### Pick games

```sh
mosaic all                # Browse all games in the listing
mosaic nhl                # Browse one sport
mosaic nfl nba            # Combine sports in one menu
mosaic soccer             # Browse soccer leagues together
mosaic cricket            # Browse cricket matches
mosaic nhl sabres         # Search within a sport
mosaic sabres             # Search across sports
```

Sport filters show the scrollable picker. Team keywords launch matching games directly when there are four or fewer matches; larger result sets show the picker. Multiple keywords narrow the results. Available sport keys depend on that day's listings; when nothing matches, the error lists available sports and aliases.

The interactive picker uses Python's standard-library `curses` module and needs no additional packages. Piped input, terminals without interactive support, or `MOSAIC_PICKER=plain` use the numbered menu instead. In that mode, type up to four game numbers separated by spaces:

```sh
MOSAIC_PICKER=plain mosaic nhl
```

The picker fetches listings from the configured main source and cricket source. It also looks up scores and game status through ESPN scoreboard data and ESPNcricinfo. These are a snapshot taken when the command runs, not a continuously updating scoreboard. Matching is based on team names, so coverage and accuracy vary; unavailable scores or status may be blank.

### Open your own links

Pass one to four URLs, quoting each URL to protect query parameters from the shell:

```sh
mosaic 'https://www.youtube.com/watch?v=VIDEO_ID_1' \
          'https://www.youtube.com/watch?v=VIDEO_ID_2'
```

Replace the example video IDs with real ones. You can also run `mosaic` without arguments and paste one URL per line. Submit an empty line to finish, or enter four links.

| Links | Viewing mode |
| --- | --- |
| All YouTube | One Chrome window containing a local embed grid; videos request muted autoplay |
| Other sources, including mixed YouTube and other links | Separate Chrome app windows arranged on the target display |
| Recognized watch pages | Attempts to open the embedded player directly; otherwise opens the original page |

Provider login, playback restrictions, and subscription stream limits still apply. Some videos cannot be embedded or expanded successfully.

## Make the video fill its window

If a video opens with menus, ads, or other page content around it, use one of the two options below. You only need to set this up once. The YouTube grid and pages containing only a player may already fill the window.

### Chrome extension

1. Open `chrome://extensions` in Chrome.
2. Enable **Developer mode**.
3. Click **Load unpacked**.
4. In the folder chooser, press **Command + Shift + G**, paste `~/mosaic/extension`, and press **Return**. Click **Select** or **Open** to load that folder.
5. The extension should appear as **Mosaic Fill**. Close and reopen your game windows if necessary.

The extension appears as **Mosaic Fill**. It runs on HTTP and HTTPS pages, including their frames, and attempts to expand the largest video or player iframe in windows no wider than roughly 60% of the screen. This size check also applies to ordinary narrow Chrome windows; it does not identify Mosaic windows specifically.

### Apple Events

In Chrome's menu bar, enable **View → Developer → Allow JavaScript from Apple Events**. Mosaic can then inject `mosaic-fill.js` into the active tab when placing a window. To retry later:

```sh
mosaic pin
```

The injected script looks for a video in the active page; the extension additionally supports player iframes. Both retry periodically while the page is open. Videos keep their aspect ratio, so letterboxing can remain.

### Optional: hide window title bars

In **System Settings → Privacy & Security → Accessibility**, enable the terminal application you use to run Mosaic. This allows Mosaic to tuck title bars behind neighboring windows or the menu bar. Without it, window tiling still works with visible title bars.

## Displays and layouts

Mosaic uses the first external display it finds, falling back to the primary display. To force the primary display:

```sh
MOSAIC_MAIN=1 mosaic nhl
```

| Videos | Separate windows | YouTube grid |
| --- | --- | --- |
| 1 | Fills the display's work area | One video |
| 2 | Top and bottom | Side by side |
| 3 | Two above, one wide below | Two above, one wide below |
| 4 | 2 × 2 | 2 × 2 |

The launcher positions newly opened windows and leaves existing windows in place. The separate `pin` command can act on existing small Chrome windows.

For a TV or projector, connect it as an extended display or configure mirroring in macOS. Mosaic handles window placement; display mirroring is managed by the operating system.

## Advanced settings (optional)

| Variable | Default | Purpose |
| --- | --- | --- |
| `BUFF_DOMAIN` | `https://mybuffstreams.plus` | Base URL for the main game-listing source |
| `CRIC_DOMAIN` | `https://cricwatch.io` | Base URL for cricket listings |
| `MOSAIC_MAIN` | Unset | Any nonempty value forces the primary display |
| `MOSAIC_PICKER` | Unset | Set to `plain` to use numbered input instead of the scrollable picker |

If a listing source changes domains, set its base URL without a trailing slash:

```sh
BUFF_DOMAIN='https://replacement.example' mosaic nhl
```

The YouTube grid and certain player redirects use a local Python HTTP server bound to `127.0.0.1:8787`. The launcher starts it when needed, and it can remain running after the video windows close. To find it:

```sh
lsof -nP -iTCP:8787 -sTCP:LISTEN
```

To stop it, run `kill PID` using the process ID after confirming it is Mosaic's Python server.

## Get updates

To download newer versions after installing Mosaic, run:

```sh
cd "$HOME/mosaic"
git pull --ff-only
```

If Git says you have local changes, it is protecting files you edited. Keep those files and ask for help before retrying. If you use the Chrome extension, open `chrome://extensions` and click its reload button after an update.

## Troubleshooting

| Problem | What to check |
| --- | --- |
| `mosaic: command not found` | Run all three lines in step 5, or use `./mosaic` from inside the Mosaic folder. |
| `cd: no such file or directory` | Complete the download in step 3 first. If you downloaded to another folder, open that folder in Terminal instead. |
| `python3: command not found` | Install Python 3 and confirm `python3 --version` works in your terminal. |
| Chrome windows do not move | Check your terminal's Chrome permission under **Privacy & Security → Automation**. |
| The webpage surrounds the video | Configure Mosaic Fill or Apple Events, wait for the player to load, and check the window-size limitation above. |
| Title bars remain visible | Enable Accessibility for your terminal application. |
| No games found or listing fetch fails | Check available sport names, your connection, and the configured source domains. Direct URLs can be used independently of the picker. |
| Scores or clocks are missing | Score data or team-name matching may be unavailable. Run the command again to request a new snapshot. |
| A YouTube embed will not play | The video may disallow embedding or require playback on YouTube. |
| The local grid does not load | Check whether another application is using port 8787. |
| A paid stream stops or asks for sign-in | Check the provider's account, playback, and concurrent-stream requirements. |

## For contributors

```text
mosaic                  Bash launcher, game picker, score lookup, and window placement
picker.py               Scrollable terminal selection interface
mosaic-fill.js          Video expansion script for Apple Events
extension/
  manifest.json         Chrome extension configuration
  content.js            Video and iframe expansion script
web/
  mosaic.html           Local YouTube grid
  go.html               Local redirect page for certain player URLs
```

There is no build step or package installation. A basic launcher syntax check is:

```sh
bash -n mosaic
python3 -m unittest discover -s tests -v
```

Playback and window placement need manual verification on macOS with Chrome. Listing parsers and score lookups depend on external page formats and APIs and may need updates when those sources change.

## Credits

Mosaic was copied from **Hardhi’s [quadbox](https://github.com/hshringeri/quadbox)** and builds on his original work. This version adds score and game-status lookup to the game picker.

Mosaic opens video sources in your browser; it does not host, proxy, or decrypt video streams. Use sources you are authorized to access and follow the applicable providers' terms.
