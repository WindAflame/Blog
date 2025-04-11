+++
title = "Réduisez votre empreinte numérique : solutions Low-Tech à portée de main"
# description = "Réduisez votre empreinte numérique : solutions Low-Tech à portée de main"
date = 2023-10-14
# updated = 2024-10-24
draft = true
[extra]
[extra.cover]
image_url = ""
alt = "A Markdown logo"
width = 1920
height = 620
[taxonomies]
tags = ["Low-Tech", "Raspberry Pi", "Numérique Responsable"]
authors = ["endyw"]
+++

**De nos jours, nous utilisons quotidiennement des services en ligne pour écouter de la musique, stocker des photos, ou visionner des vidéos. Mais connaissez-vous l’impact réel de ces services ? Et saviez-vous que des solutions logicielles sont à votre disposition pour faire la même chose chez vous ?**

Dans cet article, nous allons vous proposer une alternative à ces services en ligne pour que vous puissiez les héberger

L’empreinte carbone du numérique lors de l’utilisation de service en ligne est évidemment une thématique incontournable que nous aborderons, ainsi que la gestion de vos données personnelles.

Enfin, place aux solutions : nous vous présenterons un mode d’utilisation alternatif permettant de maitriser votre consommation, le tout en adoptant un système Low-Tech.

## Pollution des data centers

En 2022, une étude de l’ADEME a révélé l’impact significatif du numérique sur l’environnement. En France, le secteur numérique contribuait à 2,5% de l’empreinte carbone nationale et à 3 à 4% des émissions de gaz à effet de serre mondiales. Nous savons que ces chiffres sont déjà largement dépassés aujourd’hui.

Les data centers, infrastructures essentielles pour le stockage et la gestion des données numériques, jouent un rôle clé dans cette empreinte carbone. Nos activités en ligne, telles que les plateformes de streaming comme Netflix et Spotify, requièrent une quantité colossale de ressources énergétiques.

Malgré les avancées vers une transition écologique, le développement des technologies pose des défis majeurs en termes d’empreinte environnementale. Des entreprises telles que Netflix et Spotify se sont engagées à atteindre la neutralité carbone d’ici 2030, une démarche visant à compenser leurs émissions de CO2, qui s’élèvent à 353 054 tonnes de CO2 pour Spotify en 2021. Cette compensation est une première prise de conscience, mais le principe même est très discutable et ne favorise pas vraiment un changement de comportement.

![ademe](https://www.norsys.fr/sites/default/files/logo_ademe.svg_.png)

Pour réduire l’impact environnemental des data centers, il est crucial de sensibiliser sur l’importance de la consommation responsable. Suivre les recommandations de l’ADEME, telles que privilégier la consommation de médias à domicile, peut contribuer à une diminution des émissions de CO2 liées au numérique.

C’est dans cette volonté que nous nous sommes questionnés sur ces enjeux et que nous avons souhaité expérimenter la mise en place d’un système d’hébergement à domicile.

En installant une infrastructure de stockage de données à domicile, il pourrait être possible de mieux contrôler l’utilisation des données, réduisant ainsi la consommation de bande passante et les émissions de CO2 associées aux transferts de données en ligne.

## Gérer vos données personnelles en ligne : conseils pour une meilleure confidentialité

L’utilisation répandue de services en ligne tels que Google Drive, OneDrive ou Digiposte pour le stockage de données personnelles est devenue incontournable. Ces plateformes offrent une facilité d’accès et s’intègrent sans complexité dans nos systèmes.

Cependant, il est crucial d’aborder une approche réfléchie et de considérer les implications de cette dépendance croissante aux services en ligne. En effet, cette pratique peut nous priver de l’accès à nos données dans des situations imprévues, mettant en péril notre confidentialité et notre contrôle sur nos informations personnelles.

![confidentialite](https://www.haenchen.fr/media/fr-23/logos-pictos/datenschutz-fr-new.png?m=1680197567)

Avant de céder à la commodité de ces services, il est essentiel de se familiariser avec leurs politiques de confidentialité. Comprendre comment ces plateformes collectent, utilisent et stockent nos données est essentiel pour prendre des décisions informées pour protéger notre vie privée en ligne.

Nous vous invitons à lire cet article de blog, « Google vend-il vos données ? » sur ce lien <https://www.simpleanalytics.com/fr/blog/google-vend-il-vos-donnees>, qui vous explique que vos données sont confidentielles, mais elles peuvent être utilisées à des fins discutables.

En prenant en considération ces éléments, la première possibilité est de se tourner vers des services plus éthiques. C’est le parti pris de Framasoft : <https://degooglisons-internet.org/fr/>.

Nous vous proposons d’aller plus loin et d’envisager la mise en place d’un système d’hébergement autonome.

Vous pourrez maintenir un contrôle absolu sur vos données et sur les partages, renforçant ainsi votre confidentialité et limitant votre dépendance à l’égard de ces services en ligne.

## Une alternative à nos usages quotidiens portée par un système Low-Tech

Mais alors, pour minimiser au maximum la consommation énergétique des data center, tout en gardant le contrôle sur la confidentialité de vos données, quelle solution adopter ?

Le scénario idéal est le suivant : dans un environnement non connecté à Internet, offrir des services de stockage de fichiers similaires à Google Drive ou OneDrive, ainsi que la possibilité de profiter de contenus multimédias pour se passer de Netflix et Spotify.

Comme vous pouvez l’imaginer, nous ne traiterons pas d’un scénario où notre système est connecté à internet. Ce sujet sera examiné dans un article ultérieur. Cependant, nous partagerons notre retour d’expérience à la fin, en intégrant cet aspect.

Notre solution nécessite deux appareils : un routeur et un serveur avec un espace de stockage adéquat.

![schema](schema.png)

Dans notre schéma, le rôle du routeur est de rendre nos ressources accessibles dans le réseau local (et éventuellement sur Internet), tandis que le serveur agit comme un emplacement physique pour exécuter nos services et stocker nos données.

Le choix du serveur dépend de nos besoins. Pour ce scénario, nous avons fait le choix d’utiliser une solution Low-Tech. C’est-à-dire que cette solution doit être durable, accessible, économe en énergie, modulaire et fonctionnelle, tout en minimisant l’impact environnemental. 

> C’est pour ces raisons que nous nous sommes portés vers un Raspberry Pi. Ce micro-ordinateur est à la fois abordable financièrement et possède une faible consommation de 15W. Il est modulaire pour faire de multiples projets et peu encombrant.

![rpi](https://toppng.com/uploads/preview/i-raspberry-pi-logo-1156358478346otp1xmac.png)

Pour la suite de l’article, nous vous présenterons des alternatives possibles par rapport à 3 cas d’usages, tout s’inscrivant dans une démarche Low-Tech.

### Stockage de fichiers numériques

Comment nous l’avons déjà abordé dans une précédente section, intitulée “Gérer vos données personnelles en ligne : Conseils pour une meilleure confidentialité”, les services en lignes, tel que Google Drive et OneDrive, offrent de nombreux avantages qui facilitent notre quotidien.

L’un des principaux avantages de Google Drive est la possibilité de synchroniser et stocker

Quant à OneDrive, il nous permet de stocker toutes nos données importantes sur notre ordinateur. Cela garantit que nos fichiers soient sauvegardés et accessibles en cas de problème avec notre appareil ou en cas d’une perte de données. De plus, grâce à l’intégration de OneDrive avec les autres services Microsoft, tels que Word et Excel, nous pouvons travailler de manière transparente sur nos documents, en les sauvegardant automatiquement et en y accédant facilement.

Ces outils offrent également une facilité de transition lors d’un changement d’appareil. Il est simple de récupérer toutes nos données et de reprendre nos habitudes d’utilisation sans effort supplémentaire.

Cependant, il est important de noter qu’il existe des alternatives auto-hébergées à ces outils. L’utilisation d’une solution auto-hébergée vous offrira plus de contrôle sur vos données, car elles ne sont pas stockées sur des serveurs tiers.

> Dans ce contexte, nous vous recommandons d’utiliser NextCloud, qui propose une solution alternative avec des fonctionnalités similaires et une intégration poussée dans nos appareils, presque aussi avancée que les offres gratuites de Google Drive et OneDrive.

![NextCloud](https://p7.hiclipart.com/preview/627/658/483/logo-nextcloud-transparency-clip-art-scalable-vector-graphics-cloud-security-logo.jpg)

### Lecture de musiques et vidéos

De nos jours, notre consommation de films, de musiques et de séries se fait au travers des services comme Amazon Musique ou Amazon Vidéos. Ces plateformes offrent un excellent compromis en termes de qualité, de quantité et de prix. Cependant, elles nous obligent à suivre leurs évolutions dans la consommation des médias, car nous ne possédons pas les contenus.

De plus, si vous souhaitez utiliser des films, de la musique ou des séries que vous possédez et qui ne sont pas liés à ces plateformes, vous devez les acquérir à nouveau ou souscrire à un abonnement supplémentaire.

> Pour se dissocier de ces services et de leurs serveurs tiers, nous vous recommandons d’utiliser une solution alternative telle que Plex. Avec > Plex, vous pouvez héberger votre propre serveur et avoir le contrôle total sur votre contenu.

Cela vous permet de centraliser vos médias et de les diffuser facilement sur différents appareils. De plus, en utilisant Plex, vous pouvez organiser votre bibliothèque multimédia selon vos préférences et accéder à vos contenus de manière pratique, que ce soit chez vous ou en déplacement.

![Plex](https://w7.pngwing.com/pngs/111/900/png-transparent-plex-brand-logo-subscription-gratis-gym-outdoor-poster-angle-text-logo.png)

### Service web d’hébergement et de gestion de développement de logiciels

Cette fois-ci, nous parlerons d’outils à destination des développeurs ou bricoleurs numériques. Il est courant d’utiliser l’un des deux services suivants, en public ou dans un réseau privé, Github ou GitLab.

Ces solutions permettent d’héberger notre code source, de gérer un projet ou encore de gérer un déploiement.

En termes de solution alternative décentralisée, GitLab Community Edition est un excellent choix, toutefois, elle reste trop volumineuse pour un micro-ordinateur de type “Raspberry Pi”.

> Nous recommandons l’utilisation d’une application nommée Gitea, qui sert à l’hébergement de code source. Malheureusement, les outils de gestion de projet ou de déploiement ne sont pas accessibles via cet outil à ce jour.

![Gitea](https://seekvectors.com/files/download/4e405313fbc2cf36f461bd3bc9fd4ff2.png)

Si vous souhaitez continuer à utiliser les services gratuits et stocker vos sources. Vous pouvez configurer des synchronisations de dépôts avec votre service Gitea (ou autre). Pour Gitea, il faut suivre les indications de cette page : <https://docs.gitea.com/usage/repo-mirror#pulling-from-a-remote-repository>

## L’équipement à posséder pour le déploiement de son micro-datacenter

Pour se munir d’un micro-datacenter à domicile, il vous faut au moins le matériel suivant :

* Raspberry Pi (Exemple : Raspberry Pi 5 – Modèle B – 8 Go)
* Alimentation (Exemple : [Alimentation USB-C 27W](https://www.kubii.com/fr/alimentations/4107-1890-alimentation-raspberry-pi-27w-usb-c-3272496315761.html#/couleur-noir/embout_d_alimentation-europeenne_ue))
* Carte SD (Exemple : [Carte µSD 16GB](https://www.kubii.com/fr/support-de-stockage/1630-carte-micro-sd-noobs-16go-classe-10-avec-adaptateur-sd-kubii-640522710904.html))
* Boitier (Exemple : [Boitier officiel – Raspberry Pi 5](https://www.kubii.com/fr/boitiers-ventiles-intelligents/4108-boitier-officiel-pour-raspberry-pi-5-avec-ventilateur-3272496316638.html))

Si vous ne les possédez pas, vous pouvez les acquérir sur ce [lien](https://www.kubii.com/fr/kits-nano-ordinateurs/4122-1866-kit-starter-raspberry-pi-5-3272496315907.html?mot_tcid=65f2f436-4443-4f2e-8084-699386c96f96#/ram-8_gb) dans la boutique Kubii.

Ensuite, vous aurez besoin d’un espace de stockage adéquat en fonction de vos besoins.

Vous pouvez opter pour une de ces solutions :

* Une clé USB, peu encombrante. (Exemple : [Sandisk UltraFit 128GB](https://www.amazon.fr/SanDisk-Ultra-128Go-allant-jusqu%C3%A0/dp/B07855LJ99))
* Disque dur externe. (Exemple : [Toshiba 2TB Canvio Basics](https://www.amazon.fr/Toshiba-HDTB420EK3AA-Disque-Externe-Portable/dp/B07994QL95/ref=sr_1_3?__mk_fr_FR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=N375XQDMDYHR&keywords=toshiba+externe+2to&qid=1701866099&s=computers&sprefix=toshiba+externe+2to%2Ccomputers%2C75&sr=1-3))
* Un boîtier externe. (Exemple : [ICY BOX IB-256WP](https://www.amazon.fr/ICY-BOX-commutateur-construction-IB-256WP/dp/B074J1LGZP/ref=sr_1_3?__mk_fr_FR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=ZF7JKA85395S&keywords=icy+box+boitier+externe&qid=1701866272&s=computers&sprefix=icy+box+boitier+externe%2Ccomputers%2C67&sr=1-3))
* Un boîtier externe multiple baie avec connectique USB 3 (Exemple : [ICY BOX IB-RD3620SU3](https://www.amazon.fr/Icy-Box-IB-RD3620SU3-Bo%C3%AEtier-Disque/dp/B00I3M72HG/ref=sr_1_4?__mk_fr_FR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=1XKYR16PJVXIJ&keywords=JBOD&qid=1701866167&s=computers&sprefix=jbod%2Ccomputers%2C72&sr=1-4))
* Un NAS, bien que très coûteux. (Exemple : [WD My Cloud EX2 Ultra](https://www.amazon.fr/WD-Cloud-Ultra-S%C3%A9rie-Expert/dp/B01BIGST2U/ref=sr_1_4?__mk_fr_FR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=OEG9U1VE61RY&keywords=WD%2BMy%2BCloud%2BEX2%2BUltra&qid=1701867321&sprefix=wd%2Bmy%2Bcloud%2Bex2%2Bultra%2Caps%2C136&sr=8-4&th=1))
* Une carte d’extension pour Raspberry Pi pour étendre les capacités du micro-ordinateur. Attention, pour utilisateur avancé (Exemple : [PENTA SATA Hat](https://radxa.com/products/accessories/penta-sata-hat/#buy), Tuto : [Pi NAS](https://www.the-diy-life.com/i-built-a-4-bay-raspberry-pi-5-based-nas/))

Dans un prochain article, nous vous expliquerons comment mettre en place ce système, afin de rendre votre micro-datacenter accessible dans votre domicile. Nous aborderons également la configuration requise pour connecter le système à internet ainsi que les aspects liés à la redondance des données.

## Retour d’expérience

Après avoir exploré cette solution, nous sommes ravis de partager notre expérience avec vous.

**Mise en place du micro-datacenter :**

* Utilisation des clés USB pour le stockage, offrant un compromis idéal entre coût et compacité.
* Choix du système OpenMediaVault 7 basé sur Debian, facilitant la gestion grâce à son interface réseau et son application web intuitive.

**Applications installées :**

* Docker pour héberger des services essentiels comme le Reverse Proxy.
* Plex pour la gestion des médias, configuré pour une utilisation optimale.
* NextCloud offrant une expérience similaire à Google Drive, personnalisée pour répondre à nos besoins.
* Gitea, un outil de gestion de code source efficace doté d’une interface conviviale.

**Gestion des utilisateurs :**

* Processus manuel d’ajout des utilisateurs, avec la possibilité d’implémenter une identification LDAP pour simplifier la configuration.

**Expérience utilisateur :**

* Limitation du streaming sur Plex à 2 utilisateurs simultanés en dehors du domicile.
* Aucun problème rencontré avec les autres outils, offrant une expérience aussi fluide que sur les plateformes cloud traditionnelles.

**Configuration supplémentaire :**

* Mise en place d’une réplication de stockage pour une redondance efficace.
* Intégration de Portainer et NGINX Proxy Manager dans le docker pour une gestion simplifiée et un déploiement homogène des services.

Il est important de noter que l’utilisation d’applications au sein d’environnements virtualisés, comme Docker, peut entraîner une consommation de ressources plus élevée par rapport à une installation directe sur le système. Bien que cette méthode puisse sembler moins optimale en termes d’efficacité, elle a été choisie pour sa commodité. En effet, la virtualisation offre plusieurs avantages, tels que la flexibilité et la facilité de gestion, qui justifient notre choix.

En conclusion, bien que la configuration initiale demande du temps, cette solution s’avère prometteuse. La combinaison d’outils soigneusement sélectionnés et d’une gestion proactive ouvre de nouvelles perspectives. Malgré quelques limitations, notre démarche nous a permis de reprendre le contrôle et d’explorer une alternative locale pertinente dans un écosystème numérique dominé par les géants de la tech. Une petite victoire pour une approche plus responsable et autonome.

## Comment résoudre ce problème à plus grande échelle ?

Nous souhaiterions pouvoir fournir des données chiffrées, mais malheureusement, il est impossible de répondre à cette question.

Les grands fournisseurs de services cloud tels que Google, Netflix, etc., ont probablement peu d’intérêt à être totalement transparents sur leurs chiffres. Les rares bilans carbone partagés par ces entreprises ne permettent pas d’obtenir de détails sur l’utilisation et sont souvent remis en question par les experts. C’est frustrant, mais nous devons nous contenter d’intuitions.

Tout d’abord, le mix énergétique en France est principalement bas carbone et peu consommateur d’eau (principalement nucléaire). Rapatrier le service à domicile permet de contrôler la localisation du service et l’origine de l’énergie.

De plus, la consommation en local sur le réseau permet d’économiser des requêtes sur internet qui mobiliseraient plusieurs équipements réseau. Du point de vue de la consommation d’énergie et de ses impacts environnementaux, nous croyons que la solution proposée présente des avantages.

Le point le plus important est probablement que l’utilisateur reprend le contrôle de l’infrastructure matérielle. Le serveur local (Raspberry Pi) a une faible consommation énergétique. Il peut être éteint pendant les heures creuses (pendant la journée de travail, la nuit), permettant à l’utilisateur de gérer sa consommation.

En ce qui concerne les zones d’ombre, il est essentiel de considérer tout le cycle de vie du matériel personnel pour compenser le coût environnemental de sa fabrication sur un nombre d’années suffisant.

La mutualisation a ses avantages. Il est probable que les grands fournisseurs optimisent au maximum le matériel (ne serait-ce que pour des raisons de coût). Une solution idéale pourrait être de déployer le système à l’échelle d’un immeuble ou d’un quartier.

> Il est possible que les serveurs aient une meilleure efficacité que notre modeste Raspberry Pi (en termes de calculs par watt dépensé). Malheureusement, ces questions soulèvent les limites de cette expérimentation.
>
> Cette expérimentation menée sur un Raspberry pourrait tout à fait être transposée sur un vieux PC de récupération. Les sites de matériel d’occasion foisonnent de matériel supposément obsolète à tout petit prix.
>
> Notre intuition est que la solution testée est plus respectueuse de l’environnement en termes de consommation énergétique par rapport à l’utilisation des gros services cloud. Cependant, si l’on considère l’ensemble du cycle de vie et les impacts de la fabrication, la réponse reste incertaine.
>
> Il est important de rester modestes, car nous ne sommes pas en mesure de le confirmer. Est-ce une bonne idée ou une fausse bonne idée ? Nous vous laissons en juger.
>
> D’un point de vue plus idéologique, cette approche a le mérite de proposer une alternative locale à notre dépendance envers les GAFAM, ce qui en soi représente une petite victoire.

## Sources

* Pollution des data centers : Comment réduire leur empreinte carbone ? | Big média | S’inspirer, S’informer, S’engager (bpifrance.fr)
<https://infos.ademe.fr/magazine-fevrier-2023/faits-et-chiffres/support-physique-vs-numerique-limpact-environnemental-des-services-culturels/>
* <https://presse.ademe.fr/2022/11/streaming-vs-cd-ou-dvd-liseuse-vs-livre-papier-quels-sont-les-impacts-environnementaux-de-la-digitalisation-des-services-culturels.html>
* <https://www.ionos.fr/digitalguide/serveur/configuration/raspberry-pi-nextcloud/>
* <https://www.ionos.fr/digitalguide/serveur/configuration/raspberry-pi-et-plex-creez-votre-propre-serveur-media/>
* <https://www.ionos.fr/digitalguide/serveur/configuration/raspberry-pi-nas/>
* <https://www.simpleanalytics.com/fr/blog/google-vend-il-vos-donnee>,
* <https://fr.wikipedia.org/wiki/WebDAV>
* <https://fr.wikipedia.org/wiki/Digital_Living_Network_Alliance>

## Liens utiles

* Plex : <https://www.plex.tv/fr/>
* NextCloud <https://nextcloud.com/fr/>
* OpenMediaVault : <https://www.openmediavault.org>
* Gitea : <https://about.gitea.com/>
* NGINX Proxy Manager : <https://nginxproxymanager.com/>
* Kit Mini-PC Switcher (Raspberry Pi 4 – 8 GB) : <https://www.kubii.com/fr/kits-nano-ordinateurs/4177-1901-kit-mini-pc-switcher-3272496316331.html#/ram-8_gb/capacite_de_stockage-128_gb>
* Starter Kit Raspberry Pi 5 Officiel (8 GB) : <https://www.kubii.com/fr/kits-nano-ordinateurs/4122-1866-kit-starter-raspberry-pi-5-3272496315907.html?mot_tcid=65f2f436-4443-4f2e-8084-699386c96f96#/ram-8_gb>
