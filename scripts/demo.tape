# Regenerate docs/demo.gif from the repo root:
#
#     vhs scripts/demo.tape
#
# Requires vhs (which pulls in ttyd + ffmpeg):  brew install vhs
# The demo runs the *local* build via the project venv, so the fix for the
# emoji-width box alignment is what you see.

Output docs/demo.gif

Set Shell "zsh"
Set FontSize 18
Set Width 1080
Set Height 820
Set Padding 20
Set Theme "Dracula"
Set TypingSpeed 55ms

# Activate the local build so `weather-tty` is on PATH (hidden from the recording).
Hide
Type "source .venv/bin/activate && clear"
Enter
Sleep 1s
Show

Type "weather-tty --city Dubai"
Sleep 700ms
Enter
Sleep 2.5s

Type "weather-tty --city Dubai --verbose"
Sleep 700ms
Enter
Sleep 2.5s

Type "weather-tty --city Dubai --forecast"
Sleep 700ms
Enter
Sleep 3s
