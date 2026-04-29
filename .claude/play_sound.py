import sys
import os

if sys.platform == 'win32':
    import winsound
    winsound.MessageBeep(winsound.MB_OK)
elif sys.platform == 'darwin':
    os.system('afplay /System/Library/Sounds/Ping.aiff')
else:
    os.system('paplay /usr/share/sounds/freedesktop/stereo/complete.oga 2>/dev/null || beep 2>/dev/null || true')
