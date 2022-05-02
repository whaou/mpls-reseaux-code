# mpls-reseaux-code

## Introduction
Ce dépôt contient le code source de l'application web utilisée lors de 
l'activité *"Internet des objets avec micro:bit"* de la formation 
*"Les secrets des réseaux informatiques"* de la Maison Pour La Science.

Le contenu pédagogique de la formation est disponible sur 
[ce site web](https://whaou.github.io/mpls-reseaux/).


## Architecture
L'application est constituée plusieurs cartes micro:bit *cliente(s)*
(une par stagiaire) qui envoient des messages par radio vers une autre
carte micro:bit dite *serveur*. Cette carte renvoie tous les messages 
qu'elle reçois par la radio vers la liaison série de son port USB.
Des exemples de code (en python) pour ces cartes (cliente et serveur) 
se trouvent dans le répertoire `embedded` de ce dépôt.

Un programme sur le PC interprète ces messages et en publie
le contenu sur un websocket sur le port 8000 du PC. Son code se trouve 
dans le répertoire `server` de ce dépôt.

Une application web se connecte à ce websocket pour récupérer ces 
données et les afficher dans le navigateur web. Son code se trouve dans 
le répertoire `webapp` de ce dépôt.
