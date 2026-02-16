## record_timestamps_and_create_compilations.py

Custom script that takes a beachvolley video as input, and gives different videos as output:
1. The whole video, but dead time between points trimmed away.
2. Highlights.
3. ((Compilations for each player (receive/attack))).

## How to use:
1. Start script and immediately start the video, and never pause it. (The script relies on a circa ~1-4 sec difference between starting the script and then the video).

2. Wait at least 5 seconds? Some bug?

3. Watch the video and press keys when certain events happen:

For trimming:
- **j** - points is about to start
- **k** - point ended

For highlights:
- **h** - 10 sec highlight, e.g. a nice spike
- **g** - 16 sec highlight, e.g. nice defence action followed by a nice spike
- **f** - 22 sec highlight (rare, long rallies)
- **d** - 30 sec highlight (rare, long rallies)

Note to self - would be better (in almost all cases) to just have 1 highlight hotkey, then reuse values for start/end.

### Secondary features:

For player mistakes focus:
- **1** - player 1 mistake
- **2** - player 2 mistake
- **3** - player 3 mistake
- **4** - player 4 mistake

For player sideout focus:
- **5** - player 1 received a serve (and will attack if beach)
- **6** - player 2 received a serve (and will attack if beach)
- **7** - player 3 received a serve (and will attack if beach)
- **8** - player 4 received a serve (and will attack if beach)
