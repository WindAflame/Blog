+++
title = "ROG Xbox Ally: Playnite, RomM and saves everywhere"
description = "My ROG Xbox Ally setup with Playnite and RomM, and how routing RetroArch through Steam keeps my saves in three places and lets me play with friends."
date = 2026-10-08
path = "rog-xbox-ally-playnite-romm"
[taxonomies]
tags = ["ROG Xbox Ally", "Playnite", "RomM", "RetroArch", "Steam"]
authors = ["endyw"]
+++

A handheld running Windows sounds great, until you have to find your games and your saves.
Between the various launchers and the various apps you play with, everything ends up
scattered.

Here is how I set up my ROG Xbox Ally to get **a single retro library**, with **my ROMs
served by my own server**. Along the way, my **saves exist in three copies** and follow me
from one device to another.

## Overview

| Component                                                                          | Role                                                                                         |
| ---------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| [Playnite](https://playnite.link/)                                                 | The launcher, with a desktop mode and a fullscreen mode, the latter controllable by gamepad. |
| [RomM](https://github.com/rommapp/romm)                                            | My self-hosted server that organizes my ROMs and keeps a copy of my saves.                   |
| [RomM extension for Playnite](https://github.com/rommapp/playnite-plugin)          | Imports the RomM library into Playnite and syncs saves.                                      |
| [RetroArch (Steam version)](https://store.steampowered.com/app/1118310/RetroArch/) | The emulator, launched *via* Steam to get Steam Cloud, Steam Input and Remote Play Together. |
| [RetroArch (Steam) plugin](https://github.com/WindAflame/playnite-plugins)         | My plugin: it makes Playnite go through the Steam version of RetroArch.                      |

The idea: Playnite is the interface where you pick a game. It lists the games provided by
RomM, then launches them *via* the Steam version of RetroArch.

## Step 1: install Playnite

On the ROG Xbox Ally, I use Playnite in **fullscreen mode**. It is designed for gamepads
and shows Steam games, games from other launchers and RomM games in a single interface.

Playnite can be downloaded from [its official website](https://playnite.link/):

1. Switch the ROG Xbox Ally to Desktop mode.
2. Download and install Playnite.
3. In Armoury Crate, add a shortcut to `Playnite Fullscreen` to launch it straight from
   the console interface.

## Step 2: set up the RetroArch emulator

First, install [RetroArch from Steam](https://store.steampowered.com/app/1118310/RetroArch/)
(it's free), then enable Steam Cloud in its properties if it isn't already.

By default, Playnite launches `retroarch.exe` directly. On a handheld, you then lose
everything Steam brings:

- **Steam Input** and its controller profiles;
- the Steam **overlay**;
- **playtime** tracked on Steam;
- **Steam Cloud**, which syncs RetroArch saves;
- **Remote Play Together**.

My [RetroArch (Steam) plugin](https://github.com/WindAflame/playnite-plugins) creates a
"RetroArch (Steam)" emulator in Playnite, with one profile per *core*. Each profile goes
through `steam.exe -applaunch 1118310 ...` instead of launching the executable. The plugin
also automatically downloads missing *cores* when a game is launched.

To install it: grab the `.pext` from the [releases
page](https://github.com/WindAflame/playnite-plugins/releases) and open it with Playnite.

## Step 3: connect Playnite to RomM

RomM is a self-hosted ROM manager: it organizes the collection, fetches metadata and cover
art, and serves the files to clients.

The [official RomM extension](https://github.com/rommapp/playnite-plugin) bridges it with
Playnite:

1. Install the extension from Playnite (**Add-ons** menu).
2. Enter the RomM server address and authenticate (credentials, API token or QR code).
3. Map each RomM platform to an emulator and a profile (the "RetroArch (Steam)" *core*).
4. Run the import: games show up in Playnite and are downloaded on demand.

> [!NOTE]
> The extension needs a RomM instance configured with IGDB API credentials.
> See the [RomM documentation](https://docs.romm.app/).

A big advantage of RomM: a ROM has **the same file name on all my devices**. And that is
exactly the name RetroArch uses to name the save file. This is what makes saves portable
from one device to another.

## Step 4: enable RomM sync

Since version 0.9.0, the RomM extension can sync saves with the server. Just tick
**Enable save sync** in its settings. Then:

- **before launching** a game, it fetches the latest save from the server;
- **on exit**, it uploads the local save;
- the **Sync saves with RomM** action, in a game's menu, forces a manual sync;
- in case of conflict, **the most recent version wins**.

To find the saves, the extension reads RetroArch's configuration directly: nothing to set
up there either.

Pleasant surprise: the RomM extension's save sync works perfectly with our
"RetroArch (Steam)" emulator, even though it goes through Steam. There is nothing more to
configure.

## The result: three copies of every save

| Copy        | Where                           | When                                            | Content                  |
| ----------- | ------------------------------- | ----------------------------------------------- | ------------------------ |
| Local       | RetroArch folder on the console | Continuously, while playing                     | Saves and *save states*  |
| Steam Cloud | Valve's servers                 | When RetroArch starts and exits                 | Folders tracked by Steam |
| RomM        | My server                       | Before and after each game launched by Playnite | In-game saves (`.srm`)   |

In practice:

- **if the console breaks**, the saves are both on Steam and on my server;
- **if my server is down**, Steam Cloud takes over, and vice versa;
- **on another device** (desktop PC, Steam Deck…), just install RetroArch from Steam:
  Steam Cloud brings the saves back, whether the machine runs Windows or Linux;
- **with another RomM client**, sync goes through the server.

## One save, many screens

Since RomM centralizes saves, I get my progress back whichever app I play with:

- the **RomM web interface**, which lets you play right in the browser;
- [Argosy](https://github.com/rommapp/argosy-launcher), the official RomM Android client;
- [RetroArch (Steam)](https://store.steampowered.com/app/1118310/RetroArch/), through
  Playnite on Windows.

So I can start a game on the ROG Xbox Ally, continue it on my phone on the train, then
finish it in the browser.

## Bonus: Remote Play Together

Since RetroArch is launched *via* Steam, Steam sees it like any other game. For a local
multiplayer game (split screen, fighting games, *party games*…), I can invite a friend with
**Remote Play Together** from the Steam overlay. They play from home, without owning
RetroArch or the ROM.

## Limitations to keep in mind

- **Save states are not portable**: they depend on the *core* and sometimes on its
  version. To continue a game on another device, rely on the in-game save rather than a
  *save state*.
- **Two syncs run in parallel**: Steam Cloud and RomM each have their own conflict logic.
  In practice, playing on one device at a time is enough to avoid surprises.
- **Systems with folder-based saves** (PS2, PSP, GameCube, Switch…) are not yet supported
  by RomM sync.
- **You need a server**: RomM is self-hosted, so you need a machine running (NAS, mini PC,
  VPS…) to benefit from it, especially away from home.

## Conclusion

With Playnite as the interface, RomM as the library and RetroArch routed through Steam, the
ROG Xbox Ally becomes a true retro console: one place to launch your games, saves in three
copies and remote multiplayer as a bonus. Once it's set up, everything happens
automatically: all that's left is to play.

## Useful links

- [Playnite](https://playnite.link/)
- [RomM](https://github.com/rommapp/romm) and its [documentation](https://docs.romm.app/)
- [RomM extension for Playnite](https://github.com/rommapp/playnite-plugin)
- [Argosy, the RomM Android client](https://github.com/rommapp/argosy-launcher)
- [RetroArch on Steam](https://store.steampowered.com/app/1118310/RetroArch/)
- [My RetroArch (Steam) plugin for Playnite](https://github.com/WindAflame/playnite-plugins)
