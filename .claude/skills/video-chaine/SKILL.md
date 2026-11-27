---
name: video-chaine
description: Produire une vidéo pour la chaîne YouTube / page TikTok de l'utilisateur, du sujet à l'export - vulgarisation (cosmos, sciences, ingénierie, histoire, géo, religions, philo, développement personnel) ou podcast IA à deux voix (NotebookLM). Utiliser dès que l'utilisateur demande une vidéo, un script, une idée de sujet, un podcast ou donne un audio ElevenLabs/NotebookLM à monter.
---

# Vidéo de la chaîne (sans visage, voix IA)

Qui fait quoi : Claude propose, vérifie, écrit, dit ce qu'il manque, monte. L'utilisateur choisit, génère l'audio, fournit les ressources, publie.

## 1. Sujet
- Sujet et durée donnés : avancer directement. Plateforme non précisée : moins de 3 min → 9:16, au-delà → 16:9 ; le dire.
- « Propose » : donner 3 sujets tirés de `chaine/idees.md` ou nouveaux, chacun avec titre, promesse en une phrase, durée, format, style ; en recommander un. Vérifier `chaine/journal.md` pour ne pas répéter.
- Créer `projets/<slug>/`.

## 2. Vérification
Chaque chiffre, date ou citation : 2 sources, URL dans `projets/<slug>/sources.md`. Ce qui n'est pas confirmé est retiré ou présenté comme hypothèse. Religions : décrire ce que croient les traditions, sans prosélytisme ni moquerie. Histoire et géopolitique : distinguer faits, thèses, débats.

## 3. Script (`script.md`)
Récit d'enquête : suivre plutôt `video-enquete-storytelling`. Sinon :
1. **0-3 s : accroche** - paradoxe, image forte ou question dont on veut la réponse. Pas de « bonjour », pas de logo. En écrire 3, recommander une.
2. **3-15 s : promesse et enjeu** - ce qu'on va comprendre et pourquoi ça nous concerne.
3. **Développement** - une idée à la fois, relancée par « sauf que », « mais alors », jamais « ensuite ». Une image concrète par notion abstraite (échelle humaine, objet du quotidien). Une question ouverte reste toujours en suspens ; une révélation ou un fait surprenant toutes les 20-30 s.
4. **Pic** - la révélation la plus forte vers 75-85 %.
5. **Fin** - payer la promesse, boucler sur l'accroche (en short, la dernière phrase peut s'enchaîner sur la première).
6. **Engagement** - une question précise qui divise honnêtement (pas « dites-moi en commentaire »), et un abonnement justifié par la suite (« demain : … »). Une seule demande à la fois.

Choisir les mécanismes dans `templates/accroches-retention.md` (une accroche, une ou deux relances, au plus une condition ; varier d'une vidéo à l'autre) et les nommer dans `script.md`.

Écriture : français oral, phrases de moins de 15 mots, tutoiement ou vouvoiement constant, ~150 mots/min (60 s = 150 mots ; 3 min = 450 ; 10 min = 1500). L'accroche ne promet que ce que la vidéo donne.

## 4. Pack livré à l'utilisateur
- `script.md` : voix + intention visuelle par phrase.
- **ElevenLabs** → `voix.txt` : texte seul, nombres et sigles en toutes lettres, prononciations difficiles écrites phonétiquement, ponctuation pour le souffle ; type de voix conseillé.
- **NotebookLM, lecture fidèle (toujours fournie)** → `notebooklm-consigne.txt`, sur le modèle de `projets/machine-a-bonheur/notebooklm-consigne.txt` : lecture mot pour mot de l'unique source `voix.txt`, sans ajout, retrait ni reformulation ; une seule voix ; premier et dernier mots imposés ; jeu précis des passages clés (citer la phrase, ton, pause) ; prononciations. Les consignes de jeu ne vont jamais dans `voix.txt`, elles seraient lues. NotebookLM peut désobéir : comparer la transcription de l'audio à `voix.txt` et signaler chaque écart avant de monter.
- **NotebookLM, podcast à deux hôtes** : même règle de fidélité, avec `voix.txt` écrit en répliques étiquetées `HÔTE A :` / `HÔTE B :` (étiquettes non lues) ; dossier vérifié dans `notebooklm-source.md` seulement si l'utilisateur veut une discussion libre.
- `publication.md` : 3 titres (moins de 60 caractères), texte de miniature (4 mots max) et description visuelle, description YouTube avec sources, légende TikTok, 3-5 hashtags, commentaire à épingler, chapitres si long.

S'arrêter ici : l'utilisateur dépose l'audio dans `projets/<slug>/audio/`.

## 5. Ressources
Au vu du script, donner un verdict clair : **« Lemo-Opuscar suffit »** ou liste des éléments manquants (image IA avec prompt prêt à coller, photo/archive avec source libre, musique), chacun avec la phrase concernée, le format et le nom de fichier attendu dans `projets/<slug>/ressources/`. Demander le minimum.

Styles à envisager (lire son `STYLE.md` avant de promettre ; éviter ceux marqués ✦) :
| Thème | Styles |
|---|---|
| Cosmos, univers | flat-space-explainer, dark-documentary, firefly-pointillism, hologram-hud |
| Sciences | colored-pencil, whiteboard, microscope, oscilloscope-math, chalkboard |
| Ingénierie | blueprint, teardown, precise-mechanism, hardcore-info, briefing-board |
| Histoire | visual-investigation, archive-lighttable, engraving, vintage-collage, newsreel |
| Géographie, géopolitique | map-explainer, satellite-briefing, transit-map, lidar-survey |
| Religions, mythes | stained-glass, gilded-illumination, shadow-puppet, woodcut |
| Philosophie | one-line, ink-wash, double-exposure, marker-paper |
| Développement personnel | stick-explainer, pip-simulation, swiss-motion, sketchnote |
| Podcast (deux voix) | one-line, swiss-motion, neon-tubes ; ou HyperFrames avec sous-titres par locuteur |
Deux ou trois styles récurrents par thème, pour que la chaîne soit reconnaissable.

## 6. Montage
- **L'audio est le maître** : transcrire avec minutage, corriger avec le script, caler chaque plan sur les mots.
- Film animé : skill `lemo-opuscar`, PATH ffmpeg 7 (voir CLAUDE.md), voix = fichier fourni. Rendu long coûteux : pour plus de 3 min, montrer 20-30 s et annoncer l'ordre de grandeur avant de continuer ; mélanger scènes réutilisées, images et typographie.
- Podcast long : NotebookLM livre un seul fichier ; séparer les locuteurs, vérifier, habillage léger réutilisable, chapitres.
- Sous-titres incrustés en 9:16 ; texte hors des zones d'interface (haut, bas, droite).
- Contrôle : ffprobe, images clés, son -14 LUFS, relecture des sous-titres. Export `exports/<slug>.mp4`.

## 7. Décliner et apprendre
- Vidéo longue ou podcast : proposer 3-5 extraits autonomes de 30-90 s, chacun avec sa propre accroche, renvoyant vers la version longue.
- Ajouter une ligne à `chaine/journal.md`. Quand l'utilisateur donne ses statistiques (rétention, vues, abonnés gagnés), les noter et en tirer la prochaine décision.

## Garde-fous
- Ne jamais promettre un nombre de vues ou d'abonnés.
- Rappeler d'étiqueter le contenu IA quand la plateforme l'exige (images/voix réalistes). Pas de voix clonée d'une personne réelle sans son accord.
- Droits : musiques et images libres ou fournies, crédits notés. Règles des plateformes et des outils (monétisation, licences) : vérifier en ligne avant d'affirmer.
- Éviter la production en série interchangeable : chaque vidéo apporte un angle et une recherche propres.
- Rien n'est publié sans accord explicite.
