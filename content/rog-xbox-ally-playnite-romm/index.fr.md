+++
title = "ROG Xbox Ally : Playnite, RomM et des sauvegardes partout"
description = "Ma configuration de la ROG Xbox Ally avec Playnite et RomM, et comment passer RetroArch par Steam pour garder mes sauvegardes en triple et jouer à plusieurs."
date = 2026-09-29
path = "fr/rog-xbox-ally-playnite-romm"
draft = true
[taxonomies]
tags = ["setup", "ROG Xbox Ally", "Playnite", "RomM", "RetroArch", "Steam"]
authors = ["endyw"]
+++

Une console portable sous Windows, c'est génial jusqu'au moment où il faut retrouver
ses jeux. Entre Steam, les autres launchers et les émulateurs, tout est éparpillé. Et
les sauvegardes restent souvent coincées sur une seule machine.

Voici comment j'ai configuré ma ROG Xbox Ally pour avoir **une seule bibliothèque**, avec
**mes ROMs servies par mon propre serveur**. Au passage, mes **sauvegardes existent en
trois exemplaires** et me suivent d'une machine à l'autre.

## Vue d'ensemble

| Brique                                                                             | Rôle                                                                            |
| ---------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| [Playnite](https://playnite.link/)                                                 | Le launcher unique, en mode plein écran, pilotable à la manette.                |
| [RomM](https://github.com/rommapp/romm)                                            | Mon serveur auto-hébergé qui range mes ROMs et garde une copie des sauvegardes. |
| [Extension RomM pour Playnite](https://github.com/rommapp/playnite-plugin)         | Importe la bibliothèque RomM dans Playnite et synchronise les sauvegardes.      |
| [RetroArch (version Steam)](https://store.steampowered.com/app/1118310/RetroArch/) | L'émulateur, lancé *via* Steam pour profiter de Steam Cloud et de Steam Input.  |
| [Plugin RetroArch (Steam)](https://github.com/WindAflame/playnite-plugins)         | Mon plugin : il fait passer Playnite par la version Steam de RetroArch.         |

L'idée : Playnite affiche tout, RomM fournit les jeux, et RetroArch passe par Steam au
lieu d'être lancé directement.

## Étape 1 : Playnite comme interface principale

Sur la ROG Xbox Ally, j'utilise Playnite en **mode plein écran** (*Fullscreen mode*). Il
est pensé pour la manette et affiche dans une seule interface les jeux Steam, ceux des
autres launchers et ceux de RomM.

Deux réglages à faire dans Playnite :

- lancer Playnite au démarrage de Windows ;
- l'ouvrir directement en mode plein écran.

La console démarre alors directement sur ma bibliothèque.

## Étape 2 : brancher RomM

RomM est un gestionnaire de ROMs auto-hébergé : il range la collection, récupère les
métadonnées et les jaquettes, et sert les fichiers aux clients.

L'[extension officielle RomM](https://github.com/rommapp/playnite-plugin) fait le lien avec
Playnite :

1. Installer l'extension depuis Playnite (menu **Add-ons**).
2. Renseigner l'adresse du serveur RomM et s'authentifier (identifiants, jeton d'API ou
   QR code).
3. Associer chaque plateforme RomM à un émulateur et à un profil (le *core* RetroArch).
4. Lancer l'import : les jeux apparaissent dans Playnite et se téléchargent à la demande.

> [!NOTE]
> L'extension a besoin d'une instance RomM configurée avec des identifiants d'API IGDB.
> Voir la [documentation de RomM](https://docs.romm.app/).

Gros avantage de RomM : une ROM porte **le même nom de fichier sur tous mes appareils**.
Or c'est justement ce nom que RetroArch utilise pour nommer la sauvegarde. C'est ce qui
rend les sauvegardes portables d'une machine à l'autre.

## Étape 3 : faire passer RetroArch par Steam

Par défaut, Playnite lance `retroarch.exe` directement. Sur une console portable, on perd
alors tout ce que Steam apporte :

- **Steam Input** et ses profils de manette ;
- l'**overlay** Steam ;
- le **temps de jeu** compté sur Steam ;
- **Steam Cloud**, qui synchronise les sauvegardes de RetroArch ;
- **Remote Play Together**.

Mon [plugin RetroArch (Steam)](https://github.com/WindAflame/playnite-plugins) crée dans
Playnite un émulateur « RetroArch (Steam) », avec un profil par *core*. Chaque profil
passe par `steam.exe -applaunch 1118310 ...` au lieu de lancer l'exécutable. Le plugin
télécharge aussi automatiquement les *cores* manquants au lancement d'un jeu.

Pour l'installer : récupérer le `.pext` sur la [page des
releases](https://github.com/WindAflame/playnite-plugins/releases) et l'ouvrir avec
Playnite. Il suffit ensuite de choisir **RetroArch (Steam)** comme émulateur dans les
associations de plateformes de l'extension RomM.

<!-- TODO: vérifier que la synchro RomM reconnaît bien l'émulateur Custom « RetroArch (Steam) » (profil + retroarch.cfg) avant de publier. -->

## Étape 4 : régler RetroArch pour des sauvegardes portables

Pour qu'une sauvegarde faite sur la ROG Xbox Ally soit reprise ailleurs, RetroArch doit
l'écrire **au même endroit, avec le même nom, sur chaque machine**. Dans les réglages
**Paramètres > Répertoires** et **Paramètres > Sauvegarde** de RetroArch :

- garder les dossiers de sauvegarde **par défaut**, à l'intérieur du dossier de
  RetroArch : c'est là que Steam Cloud les récupère ;
- ne **pas** écrire les sauvegardes dans le dossier du contenu ;
- utiliser les **mêmes options de tri** (par *core*, par dossier de contenu) sur tous les
  appareils ;
- utiliser le **même *core*** pour un système donné partout.

Côté `retroarch.cfg`, ça donne :

```ini
savefiles_in_content_dir = "false"
sort_savefiles_enable = "false"
sort_savefiles_by_content_enable = "false"
```

Les valeurs de tri comptent moins que leur cohérence : il faut simplement les mêmes sur
chaque machine.

## Étape 5 : activer la synchro RomM

Depuis sa version 0.9.0, l'extension RomM sait synchroniser les sauvegardes avec le
serveur. Il suffit de cocher **Enable save sync** dans ses réglages. Ensuite :

- **avant le lancement** d'un jeu, elle récupère la dernière sauvegarde du serveur ;
- **à la fermeture**, elle y envoie la sauvegarde locale ;
- l'action **Sync saves with RomM**, dans le menu d'un jeu, force une synchro à la main ;
- en cas de conflit, **la version la plus récente gagne**.

Pour trouver les sauvegardes, l'extension lit directement `retroarch.cfg`. Les réglages de
l'étape 4 lui servent donc aussi.

## Le résultat : trois copies de chaque sauvegarde

| Copie       | Où                                  | Quand                                            | Contenu                       |
| ----------- | ----------------------------------- | ------------------------------------------------ | ----------------------------- |
| Locale      | Dossier de RetroArch sur la console | En continu, pendant la partie                    | Sauvegardes et *save states*  |
| Steam Cloud | Serveurs de Valve                   | À la fermeture et au lancement de RetroArch      | Les dossiers suivis par Steam |
| RomM        | Mon serveur                         | Avant et après chaque partie lancée par Playnite | Sauvegardes internes (`.srm`) |

Concrètement :

- **si la console tombe en panne**, les sauvegardes sont à la fois sur Steam et sur mon
  serveur ;
- **si mon serveur est coupé**, Steam Cloud prend le relais, et inversement ;
- **sur une autre machine** (PC fixe, Steam Deck…), il suffit d'installer RetroArch depuis
  Steam : Steam Cloud rapatrie les sauvegardes, que la machine soit sous Windows ou Linux ;
- **avec un autre client RomM**, la synchro passe par le serveur.

## Bonus : Remote Play Together

Comme RetroArch est lancé *via* Steam, Steam le voit comme un jeu comme les autres. Pour
un jeu multijoueur en local (écran partagé, jeux de combat, *party games*…), je peux
inviter un ami avec **Remote Play Together** depuis l'overlay Steam. Il joue chez lui,
sans posséder RetroArch ni la ROM.

## Les limites à connaître

- **Les *save states* ne sont pas portables** : ils dépendent du *core* et parfois de sa
  version. La synchro RomM ne gère que les sauvegardes internes (`.srm`). Pour
  continuer une partie sur une autre machine, mieux vaut s'appuyer sur la sauvegarde du
  jeu que sur un *save state*.
- **Deux synchros tournent en parallèle** : Steam Cloud et RomM ont chacun leur logique de
  conflit. En pratique, jouer sur une machine à la fois suffit à éviter les surprises.
- **Les systèmes à sauvegardes en dossier** (PS2, PSP, GameCube, Switch…) ne sont pas
  encore gérés par la synchro RomM.

## Liens utiles

- [Playnite](https://playnite.link/)
- [RomM](https://github.com/rommapp/romm) et sa [documentation](https://docs.romm.app/)
- [Extension RomM pour Playnite](https://github.com/rommapp/playnite-plugin)
- [RetroArch sur Steam](https://store.steampowered.com/app/1118310/RetroArch/)
- [Mon plugin RetroArch (Steam) pour Playnite](https://github.com/WindAflame/playnite-plugins)
