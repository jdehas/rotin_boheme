# Rotin Bohème · Univers 1 · Les petits bonheurs d'occasion

Maquette de page d'accueil, prête à devenir un thème Shopify (Online Store 2.0).
Ouvrir `index.html` dans un navigateur. Aucun JavaScript.

## Correspondance avec le thème Shopify

| Bloc de la maquette | Fichier Shopify | Réglages à prévoir |
| --- | --- | --- |
| Barre d'annonce | `sections/announcement-bar.liquid` | texte |
| En-tête et macaron | `sections/header.liquid` | logo SVG, menu |
| Héro et bande photomaton | `sections/hero.liquid` | titre, texte, bouton, 4 images |
| Rayures de bistrot | `snippets/rayures.liquid` | aucun (CSS seul) |
| Les pièces qui attendent | `sections/featured-collection.liquid` | collection, 4 produits |
| Le photomaton des objets | `sections/image-with-text.liquid` (variante) | texte, 2 bandes de 4 images |
| Les quatre pièces | `sections/collection-list.liquid` | 4 collections |
| Citation | `sections/rich-text.liquid` | citation |
| Le petit bonheur* | `sections/multicolumn.liquid` (variante) | étiquette, texte |
| L'atelier | `sections/image-with-text.liquid` | image, texte |
| Lettre | `sections/newsletter.liquid` | formulaire Shopify |
| Pied de page | `sections/footer.liquid` | menus |

`assets/rotin-boheme.css` va dans `assets/`. Les variables `:root` se branchent sur `config/settings_schema.json` (couleurs et polices).

## Tokens

Crème brûlée #F0D9AC · Rouge confiture #A92F28 · Vert bouteille #31573C · Jaune miel #D6A53B · Clémentine #E77D2D · Brun chocolat #38271F · Papier de page #F7EFDE.
Titres Fraunces · texte Karla (16 px minimum) · écriture à la main Caveat (macaron, légendes).

## Photomaton

Une bande = 4 vues de ratio 4:3 (portrait, profil, détail, personnalité). Chaque produit Shopify reçoit 4 images dans cet ordre. Le fond de bande (vert bouteille, rouge confiture ou crème brûlée) peut devenir une métadonnée produit.

## À remplacer avant mise en ligne

- Illustrations (lampes, fauteuils) par les photos Pavo.
- Textes marqués provisoires par ceux de Léa.
- Prix, noms de lampes, photo de l'atelier.
- Macaron : texte SVG à vectoriser en tracé une fois la police manuscrite choisie.
- Retirer la ligne « Maquette » en haut de page.
