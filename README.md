# FOSSGlaze

### Why just use Linux when you can rub it in everyone's face on Discord?

All of your Discord friends need to know that you are currently on a Linux system instead of Windows. FOSSGlaze solves this existential crisis by plastering your distro of choice all over your Discord profile.

#### Features:

- Smart Distro Detection: Automatically figures out what you're running by reading /etc/os-release.

- The Most Important Feature: Sets your status to "i use arch btw" if it detects an Arch-based system. Let's sort Linux users and Arch users.

- Fallback Support: A respectful "i use linux just in case" for... everyone else (Debian, Fedora, etc.).

- Gaslight Your Friends: Use fossglaze `--distro` gentoo to pretend you've spent 3 days wasting your life - other XXXtoo forks aren't supported yet. Go find a life purpose and stop building these distros.

- Safe, Sudo-Free Autostart: A handy fossglaze --setup systemd command that installs a user service (no sudo needed) and just works.

- Tiling WM Support: fossglaze --setup tiling will print the exact exec-once lines for your "saucy" Hyprland or i3 config.

### Installation
This is on the ***AUR*** yet, because of course it is. 

Guide (you should know this y'know?):
`yay -S fossglaze`

If you're not on an Arch-based distro, I don't know what to tell you. Clone the repo, install python-pypresence (`pip3 install pypresence`), and run python3 fossglaze.py.

### Usage (After Installing)

After you install it from the AUR, you have two choices:
1. *Peasant Mode* (Run it manually)
Just run fossglaze in your terminal. It will stay running. Close the terminal, it dies. Simple.

2. ***King Mode*** (Make it start automatically)
You want this to run every time you log in, right? Right.
Run this one command. It does not need sudo and is 100% safe: `fossglaze --setup systemd`
This will ask you for permission, then automatically create a user service file at *~/.config/systemd/user/fossglaze.service* and enable it. It will now launch when you log in and restart if it ever crashes.

#### For Tiling WM Chads
If you don't use a DE and laugh at systemd user services, just run:

`fossglaze --setup tiling`


It will print the exact exec-once line you need to paste into your hyprland.conf or i3/config.

#### IF IT DOESN'T WORK (IT DEFINETELY SHOULD):
You're going to run this and see *FOSSGlaze Error: Could not connect to Discord.*

You will say, "but my Discord is open??? duhhhhhh"
I know. The stable Discord client on Linux is... special. Its RPC socket is notoriously broken.
**The Fix**: Use **Discord Canary**! This is the fix. 99% of the time, this is the entire problem. Stable is for horses, Canary is for users.
And then:
- Run Discord Canary.
- Run fossglaze.

It will now work. Also, make sure "Activity Status" is enabled in your Discord User Settings -> Activity Privacy, but you already checked that, right?

### Forking & Adding Your Own Distro

Want to add your special distro that only you and 3 other people use? Fork this repo and create your own Discord application. Just kidding, I can implement all of the ***good*** distros but I ain't gonna implement infinite count of niche shi. Open an issue if you have one (probably skill issue).

### License
GPL-3.0. Go nuts. Do whatever you want I guess.
