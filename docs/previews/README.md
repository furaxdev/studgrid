# Prévisualisations

## Templates (validation par Furax)

Les 11 templates non boutique sont **modélisés par type d'écran** (login, menu, paramètres, etc.),
pas sur une capture de jeu. Accepté par Furax. Le brief demande une capture citée par écran :
ce point reste ouvert et devra être comblé avec le catalogue DevForum (`docs/refs/catalog.json`)
ou des captures de jeux.

Les mesures (padding 14 px, rayon 14 px, contour 4 px, ombre 5 px, bouton 48 px) viennent de
`shop-chunky.html`, pas d'une capture.

## Fichiers

- `gallery.html` : galerie de validation (1440 px et 390 px).
- `<nom>-chunky.html` : sources générées par `scripts/gen_template_previews.py`.
- `renders/` : rendus PNG générés par `scripts/render_preview.js`.
