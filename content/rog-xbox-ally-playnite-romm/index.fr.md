+++
title = "ROG Xbox Ally : Playnite, RomM et des sauvegardes partout"
description = "Ma configuration de la ROG Xbox Ally avec Playnite et RomM, et comment passer RetroArch par Steam pour garder mes sauvegardes en triple et jouer à plusieurs."
date = 2026-10-08
path = "fr/rog-xbox-ally-playnite-romm"
[taxonomies]
tags = ["ROG Xbox Ally", "Playnite", "RomM", "RetroArch", "Steam"]
authors = ["endyw"]
+++

Une console portable sous Windows, l'idée semble géniale, jusqu'au moment où il faut retrouver
ses jeux et ses sauvegardes. Entre les différents launchers et les différentes applications qui
permettent de jouer, tout est éparpillé.

Voici comment j'ai configuré ma ROG Xbox Ally pour avoir **une seule bibliothèque rétro**, avec
**mes ROMs servies par mon propre serveur**. Au passage, mes **sauvegardes existent en
trois exemplaires** et me suivent d'une machine à l'autre.

## Vue d'ensemble

| Brique                                                                             | Rôle                                                                                                     |
| ---------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| [Playnite](https://playnite.link/)                                                 | Le launcher, avec un mode bureau et un mode plein écran, ce dernier étant pilotable à la manette.        |
| [RomM](https://github.com/rommapp/romm)                                            | Mon serveur auto-hébergé qui range mes ROMs et garde une copie des sauvegardes.                          |
| [Extension RomM pour Playnite](https://github.com/rommapp/playnite-plugin)         | Importe la bibliothèque RomM dans Playnite et synchronise les sauvegardes.                               |
| [RetroArch (version Steam)](https://store.steampowered.com/app/1118310/RetroArch/) | L'émulateur, lancé *via* Steam pour profiter de Steam Cloud, de Steam Input et de Remote Play Together.  |
| [Plugin RetroArch (Steam)](https://github.com/WindAflame/playnite-plugins)         | Mon plugin : il fait passer Playnite par la version Steam de RetroArch.                                  |

L'idée : Playnite sert d'interface pour choisir son jeu. Il liste les jeux fournis par RomM,
puis les lance *via* la version Steam de RetroArch.

## Étape 1 : installer Playnite

Sur la ROG Xbox Ally, j'utilise Playnite en **mode plein écran** (*Fullscreen mode*). Il
est pensé pour la manette et affiche dans une seule interface les jeux Steam, ceux des
autres launchers et ceux de RomM.

Playnite se télécharge sur [son site officiel](https://playnite.link/) :

1. Passer la ROG Xbox Ally en mode Bureau.
2. Télécharger et installer Playnite.
3. Dans Armoury Crate, ajouter un raccourci vers `Playnite Fullscreen` pour le lancer
   directement depuis l'interface de la console.

## Étape 2 : configurer l'émulateur RetroArch

Installer d'abord [RetroArch depuis Steam](https://store.steampowered.com/app/1118310/RetroArch/)
(il est gratuit), puis activer Steam Cloud dans ses propriétés si ce n'est pas déjà le cas.

Par défaut, Playnite lance `retroarch.exe` directement. Sur une console portable, on perd
alors tout ce que Steam apporte :

- **Steam Input** et ses profils de manette ;
- l'**overlay** Steam ;
- le **temps de jeu** comptabilisé sur Steam ;
- **Steam Cloud**, qui synchronise les sauvegardes de RetroArch ;
- **Remote Play Together**.

Mon [plugin RetroArch (Steam)](https://github.com/WindAflame/playnite-plugins) crée dans
Playnite un émulateur « RetroArch (Steam) », avec un profil par *core*. Chaque profil
passe par `steam.exe -applaunch 1118310 ...` au lieu de lancer l'exécutable. Le plugin
télécharge aussi automatiquement les *cores* manquants au lancement d'un jeu.

Pour l'installer : récupérer le `.pext` sur la [page des
releases](https://github.com/WindAflame/playnite-plugins/releases) et l'ouvrir avec
Playnite.

## Étape 3 : raccorder Playnite à RomM

RomM est un gestionnaire de ROMs auto-hébergé : il range la collection, récupère les
métadonnées et les jaquettes, et sert les fichiers aux clients.

L'[extension officielle RomM](https://github.com/rommapp/playnite-plugin) fait le lien avec
Playnite :

1. Installer l'extension depuis Playnite (menu **Add-ons**).
2. Renseigner l'adresse du serveur RomM et s'authentifier (identifiants, jeton d'API ou
   QR code).
3. Associer chaque plateforme RomM à un émulateur et à un profil (le *core* de « RetroArch (Steam) »).
4. Lancer l'import : les jeux apparaissent dans Playnite et se téléchargent à la demande.

> [!NOTE]
> L'extension a besoin d'une instance RomM configurée avec des identifiants d'API IGDB.
> Voir la [documentation de RomM](https://docs.romm.app/).

Gros avantage de RomM : une ROM porte **le même nom de fichier sur tous mes appareils**.
Or c'est justement ce nom que RetroArch utilise pour nommer la sauvegarde. C'est ce qui
rend les sauvegardes portables d'une machine à l'autre.

## Étape 4 : activer la synchro RomM

Depuis sa version 0.9.0, l'extension RomM sait synchroniser les sauvegardes avec le
serveur. Il suffit de cocher **Enable save sync** dans ses réglages. Ensuite :

- **avant le lancement** d'un jeu, elle récupère la dernière sauvegarde du serveur ;
- **à la fermeture**, elle y envoie la sauvegarde locale ;
- l'action **Sync saves with RomM**, dans le menu d'un jeu, force une synchro à la main ;
- en cas de conflit, **la version la plus récente gagne**.

Pour trouver les sauvegardes, l'extension lit directement la configuration de RetroArch :
là non plus, rien à régler.

Bonne surprise : la synchro des sauvegardes de l'extension RomM reconnaît parfaitement notre
émulateur « RetroArch (Steam) », alors qu'il passe par Steam. Il n'y a rien de plus à configurer.

## Le résultat : trois copies de chaque sauvegarde

| Copie       | Où                                  | Quand                                            | Contenu                       |
| ----------- | ----------------------------------- | ------------------------------------------------ | ----------------------------- |
| Locale      | Dossier de RetroArch sur la console | En continu, pendant la partie                    | Sauvegardes et *save states*  |
| Steam Cloud | Serveurs de Valve                   | Au lancement et à la fermeture de RetroArch      | Les dossiers suivis par Steam |
| RomM        | Mon serveur                         | Avant et après chaque partie lancée par Playnite | Sauvegardes internes (`.srm`) |

Concrètement :

- **si la console tombe en panne**, les sauvegardes sont à la fois sur Steam et sur mon
  serveur ;
- **si mon serveur est coupé**, Steam Cloud prend le relais, et inversement ;
- **sur une autre machine** (PC fixe, Steam Deck…), il suffit d'installer RetroArch depuis
  Steam : Steam Cloud rapatrie les sauvegardes, que la machine soit sous Windows ou Linux ;
- **avec un autre client RomM**, la synchro passe par le serveur.

## Une sauvegarde, plusieurs écrans

Comme RomM centralise les sauvegardes, je retrouve ma progression quelle que soit
l'application avec laquelle je joue :

- l'**interface web de RomM**, qui permet de jouer directement dans le navigateur ;
- [Argosy](https://github.com/rommapp/argosy-launcher), le client Android officiel de RomM ;
- [RetroArch (Steam)](https://store.steampowered.com/app/1118310/RetroArch/), au travers de
  Playnite sur Windows.

Je peux donc commencer une partie sur la ROG Xbox Ally, la continuer sur mon téléphone dans
le train, puis la terminer depuis le navigateur.

## Bonus : Remote Play Together

Comme RetroArch est lancé *via* Steam, Steam le voit comme un jeu comme les autres. Pour
un jeu multijoueur en local (écran partagé, jeux de combat, *party games*…), je peux
inviter un ami avec **Remote Play Together** depuis l'overlay Steam. Il joue chez lui,
sans posséder RetroArch ni la ROM.

## Les limites à connaître

- **Les *save states* ne sont pas portables** : ils dépendent du *core* et parfois de sa
  version. Pour continuer une partie sur une autre machine, mieux vaut s'appuyer sur la
  sauvegarde du jeu que sur un *save state*.
- **Deux synchros tournent en parallèle** : Steam Cloud et RomM ont chacun leur logique de
  conflit. En pratique, jouer sur une machine à la fois suffit à éviter les surprises.
- **Les systèmes à sauvegardes en dossier** (PS2, PSP, GameCube, Switch…) ne sont pas
  encore gérés par la synchro RomM.
- **Il faut un serveur** : RomM est auto-hébergé, il faut donc une machine allumée
  (NAS, mini-PC, VPS…) pour en profiter, surtout en dehors de chez soi.

## Conclusion

Avec Playnite comme interface, RomM comme bibliothèque et RetroArch passé par Steam, la
ROG Xbox Ally devient une vraie console rétro : un seul endroit pour lancer ses jeux, des
sauvegardes en triple et le multijoueur à distance en prime. Une fois en place, tout se fait
automatiquement : il n'y a plus qu'à jouer.

## Liens utiles

- [Playnite](https://playnite.link/)
- [RomM](https://github.com/rommapp/romm) et sa [documentation](https://docs.romm.app/)
- [Extension RomM pour Playnite](https://github.com/rommapp/playnite-plugin)
- [Argosy, le client Android de RomM](https://github.com/rommapp/argosy-launcher)
- [RetroArch sur Steam](https://store.steampowered.com/app/1118310/RetroArch/)
- [Mon plugin RetroArch (Steam) pour Playnite](https://github.com/WindAflame/playnite-plugins)
