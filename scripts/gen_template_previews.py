#!/usr/bin/env python3
"""Generate one self-contained preview page per template (Studs Chunky tokens).

Output: docs/previews/<name>-chunky.html (inline CSS, real French content).
Each preview is the gate artefact for templates/<name>.lua: validate the HTML first,
then the Lua builder mirrors it. Tokens are copied from docs/previews/shop-chunky.html.

Usage: python scripts/gen_template_previews.py
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "previews"

ROOT_CSS = """
:root {
  --ink: #0B120F; --gold-top: #FFD23F; --gold-bottom: #E0A800;
  --cream: #FFF6D6; --green-top: #76CC7B; --green-bottom: #4FA95A;
  --coin: #FFC93C; --danger: #E4574C; --backdrop: #2B6E3A;
  --stroke: 4px; --shadow: 5px 5px 0 var(--ink); --radius: 14px;
}
* { box-sizing: border-box; }
html, body { margin: 0; }
body { background: var(--backdrop); color: var(--ink);
  font-family: "Trebuchet MS", Verdana, sans-serif; font-weight: 700;
  min-height: 100vh; padding: 16px; }
.screen { max-width: 1200px; margin: 0 auto; position: relative; }
.surface { background: var(--cream); border: var(--stroke) solid var(--ink);
  border-radius: var(--radius); box-shadow: var(--shadow); padding: 14px; }
.header { background: linear-gradient(180deg, var(--gold-top), var(--gold-bottom));
  display: flex; align-items: center; justify-content: space-between; gap: 12px;
  border: var(--stroke) solid var(--ink); border-radius: var(--radius);
  box-shadow: var(--shadow); padding: 12px 16px; margin-bottom: 18px; }
.header h1 { margin: 0; font-size: clamp(22px, 4.5vw, 36px); text-transform: uppercase; }
.close { flex: 0 0 auto; width: 48px; height: 48px; display: grid; place-items: center;
  background: var(--danger); color: #fff; border: var(--stroke) solid var(--ink);
  border-radius: 10px; box-shadow: 4px 4px 0 var(--ink); font: 900 24px/1 sans-serif; }
.btn { min-height: 48px; padding: 10px 16px; display: inline-flex; align-items: center;
  justify-content: center; gap: 10px; border-radius: 12px; font: 900 18px/1 sans-serif;
  background: linear-gradient(180deg, var(--green-top), var(--green-bottom)); color: var(--cream);
  border: var(--stroke) solid var(--ink); box-shadow: 4px 4px 0 var(--ink); cursor: pointer; }
.btn.alt { background: linear-gradient(180deg, var(--gold-top), var(--gold-bottom)); color: var(--ink); }
.btn.bad { background: var(--danger); color: #fff; }
.coin { width: 22px; height: 22px; border-radius: 50%; background: var(--coin);
  border: 3px solid var(--ink); display: inline-block; flex: 0 0 auto; }
.price { display: inline-flex; align-items: center; gap: 8px; font-weight: 900; font-size: 18px; }
.tag { display: inline-block; background: var(--gold-top); border: 3px solid var(--ink);
  border-radius: 8px; padding: 2px 8px; font-size: 14px; box-shadow: 2px 2px 0 var(--ink); }
.ribbon { position: absolute; top: -14px; right: -10px; transform: rotate(-6deg);
  background: var(--danger); color: #fff; border: 3px solid var(--ink); border-radius: 8px;
  padding: 4px 12px; font-size: 14px; box-shadow: 3px 3px 0 var(--ink); }
.input { background: #fff; border: 3px solid var(--ink); border-radius: 10px; padding: 12px;
  font-size: 17px; font-weight: 600; min-height: 48px; }
.bar { background: #fff; border: 3px solid var(--ink); border-radius: 10px; height: 22px; overflow: hidden; }
.bar > i { display: block; height: 100%; background: linear-gradient(180deg, var(--green-top), var(--green-bottom)); }
.tile { background: #fff; border: 3px solid var(--ink); border-radius: 12px;
  display: grid; place-items: center; box-shadow: 3px 3px 0 var(--ink); min-height: 96px; }
.muted { font-weight: 600; font-size: 16px; }
.grid { display: grid; gap: 16px; grid-template-columns: repeat(3, 1fr); }
.row { display: flex; justify-content: space-between; align-items: center; gap: 12px; font-size: 17px; }
@media (max-width: 760px) { .grid { grid-template-columns: 1fr; } .header h1 { font-size: 22px; } }
"""

PAGE = """<!doctype html>
<html lang="fr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — Studs Chunky (preview)</title>
<style>{css}{extra}</style></head>
<body><main class="screen">
{body}
</main></body></html>
"""


def header(title: str) -> str:
    return f'<header class="header"><h1>{title}</h1><button class="close" aria-label="Fermer">X</button></header>'


def page(name: str, title: str, body: str, extra: str = "") -> str:
    return PAGE.format(title=title, css=ROOT_CSS, extra=extra, body=body)


def login() -> str:
    body = f"""
<section class="surface" style="max-width:460px;margin:24px auto">
  <h1 style="font-size:34px;margin:0 0 6px;text-transform:uppercase">StudGrid</h1>
  <p class="muted" style="margin:0 0 16px">Connecte-toi pour reprendre ta partie.</p>
  <label class="muted">Pseudo</label>
  <div class="input" style="margin:6px 0 14px">Furax_Builder</div>
  <label class="muted">Mot de passe</label>
  <div class="input" style="margin:6px 0 18px">••••••••••</div>
  <button class="btn" style="width:100%">Se connecter</button>
  <div style="height:12px"></div>
  <button class="btn alt" style="width:100%">Créer un compte</button>
  <p class="muted" style="margin:16px 0 0;text-align:center">Mot de passe oublié ?</p>
</section>"""
    return page("login", "Connexion", body)


def main_menu() -> str:
    tiles = ["Jouer", "Boutique", "Quêtes", "Classement", "Paramètres", "Amis"]
    cells = "".join(
        f'<button class="btn{" alt" if i == 0 else ""}" style="min-height:96px;font-size:22px">{t}</button>'
        for i, t in enumerate(tiles)
    )
    body = f"""{header("Menu principal")}
<section class="surface" style="display:grid;grid-template-columns:repeat(3,1fr);gap:16px">{cells}</section>
<p class="muted" style="margin-top:16px;color:var(--cream);text-shadow:2px 2px 0 var(--ink)">Niveau 12 · 340 / 500 XP</p>
<div class="bar" style="margin-top:6px"><i style="width:68%"></i></div>"""
    return page("main-menu", "Menu principal", body, "@media (max-width:760px){.surface{grid-template-columns:1fr!important}}")


def settings() -> str:
    rows = [("Musique", "70 %"), ("Effets sonores", "85 %"), ("Sensibilité caméra", "50 %"), ("Taille du texte", "Moyenne")]
    items = "".join(
        f'<div class="surface" style="margin-bottom:12px"><div class="row"><span>{k}</span><span class="tag">{v}</span></div></div>'
        for k, v in rows
    )
    body = f"""{header("Paramètres")}
<div style="max-width:720px;margin:0 auto">{items}
<button class="btn" style="width:100%">Enregistrer</button></div>"""
    return page("settings", "Paramètres", body)


def inventory_grid() -> str:
    names = ["Casque", "Pelle", "Veste", "Gants", "Lampe", "Sac", "Carte", "Potion", "Clé", "Bottes", "Fusée", "Livre"]
    cells = "".join(f'<div class="tile" style="font-size:15px">{n}</div>' for n in names)
    body = f"""{header("Inventaire")}
<section class="surface" style="display:grid;grid-template-columns:repeat(4,1fr);gap:12px">{cells}</section>
<div class="row" style="margin-top:14px;color:var(--cream);text-shadow:2px 2px 0 var(--ink)"><span>12 / 32 emplacements</span><span>Trier</span></div>"""
    return page("inventory-grid", "Inventaire", body,
                "@media (max-width:760px){section.surface{grid-template-columns:repeat(3,1fr)!important}}")


def quest_log() -> str:
    quests = [("Trouver 5 pièces", 3, 5, "Quotidienne"), ("Construire un abri", 1, 1, "Terminée"), ("Vaincre le gardien", 0, 1, "Hebdo")]
    cards = ""
    for name, cur, total, kind in quests:
        pct = int(cur / total * 100)
        cards += f"""<div class="surface" style="margin-bottom:12px">
  <div class="row"><strong style="font-size:20px">{name}</strong><span class="tag">{kind}</span></div>
  <p class="muted" style="margin:8px 0">{cur} / {total}</p>
  <div class="bar"><i style="width:{pct}%"></i></div></div>"""
    body = f"""{header("Journal de quêtes")}<div style="max-width:720px;margin:0 auto">{cards}</div>"""
    return page("quest-log", "Journal de quêtes", body)


def leaderboard() -> str:
    rows = [("1", "Maxime", "12 480"), ("2", "Léa", "11 210"), ("3", "Furax", "10 905"), ("4", "Tom", "9 340"), ("5", "Nina", "8 712")]
    lines = "".join(
        f'<div class="row" style="padding:10px 0;border-bottom:3px solid var(--ink)"><span>#{r} {n}</span><span class="price"><span class="coin"></span>{s}</span></div>'
        for r, n, s in rows
    )
    body = f"""{header("Classement")}
<section class="surface" style="max-width:720px;margin:0 auto">{lines}</section>
<p class="muted" style="margin-top:14px;color:var(--cream);text-shadow:2px 2px 0 var(--ink)">Mise à jour chaque lundi à 00:00 UTC.</p>"""
    return page("leaderboard", "Classement", body)


def chat() -> str:
    msgs = [("Léa", "Quelqu'un pour la boîte mystère ?"), ("Tom", "Je viens de tirer une légendaire !"), ("Furax", "Les odds sont affichées, 1 % seulement")]
    lines = "".join(f'<div style="margin-bottom:10px"><strong>{a}</strong> <span style="font-weight:600">{t}</span></div>' for a, t in msgs)
    body = f"""{header("Discussion")}
<section class="surface" style="max-width:720px;margin:0 auto;min-height:320px">{lines}
<div class="input" style="margin-top:16px;color:#666">Écris un message…</div></section>"""
    return page("chat", "Discussion", body)


def dialog() -> str:
    body = f"""
<section class="surface" style="max-width:520px;margin:40px auto;position:relative">
  <h2 style="margin:0 0 8px;font-size:26px">Confirmer l'achat</h2>
  <p class="muted" style="margin:0 0 14px">Acheter « Casque de chantier » pour 120 pièces ?</p>
  <p class="price" style="margin:0 0 18px"><span class="coin"></span>120</p>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px">
    <button class="btn alt">Annuler</button><button class="btn">Acheter</button>
  </div>
  <button class="close" style="position:absolute;top:-18px;right:-18px" aria-label="Fermer">X</button>
</section>"""
    return page("dialog", "Dialogue", body)


def hud_overlay() -> str:
    body = """<div style="display:flex;justify-content:space-between;align-items:flex-start;gap:12px">
  <div class="surface" style="min-width:210px"><div class="row"><span>Vie</span><span>80 / 100</span></div><div class="bar" style="margin-top:6px"><i style="width:80%"></i></div></div>
  <div class="surface price"><span class="coin"></span>1 250</div>
</div>
<div style="height:340px"></div>
<div style="display:flex;justify-content:center;gap:10px">
  <div class="tile" style="width:76px;min-height:76px">1</div><div class="tile" style="width:76px;min-height:76px">2</div><div class="tile" style="width:76px;min-height:76px">3</div>
</div>
<p class="muted" style="text-align:center;color:var(--cream);text-shadow:2px 2px 0 var(--ink)">Appuie sur E pour interagir</p>"""
    return page("hud-overlay", "HUD", body)


def loading() -> str:
    body = """<div style="min-height:70vh;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:18px">
  <div class="surface" style="width:min(520px,92%);text-align:center">
    <h1 style="margin:0 0 12px;font-size:30px;text-transform:uppercase">Chargement</h1>
    <div class="bar"><i style="width:45%"></i></div>
    <p class="muted" style="margin:12px 0 0">Chargement des cosmétiques… 45 %</p>
  </div>
  <p class="muted" style="color:var(--cream);text-shadow:2px 2px 0 var(--ink)">Astuce : les boîtes affichent toujours leurs probabilités.</p>
</div>"""
    return page("loading", "Chargement", body)


def error_modal() -> str:
    body = """<section class="surface" style="max-width:480px;margin:40px auto;position:relative">
  <h2 style="margin:0 0 8px;font-size:26px;color:var(--danger)">Connexion perdue</h2>
  <p class="muted" style="margin:0 0 18px">Impossible de joindre le serveur (code 503). Ta progression est sauvegardée localement.</p>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px">
    <button class="btn alt">Quitter</button><button class="btn">Réessayer</button>
  </div>
  <button class="close" style="position:absolute;top:-18px;right:-18px" aria-label="Fermer">X</button>
</section>"""
    return page("error-modal", "Erreur", body)


TEMPLATES = {
    "login": login,
    "main-menu": main_menu,
    "settings": settings,
    "inventory-grid": inventory_grid,
    "quest-log": quest_log,
    "leaderboard": leaderboard,
    "chat": chat,
    "dialog": dialog,
    "hud-overlay": hud_overlay,
    "loading": loading,
    "error-modal": error_modal,
}


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    for name, fn in TEMPLATES.items():
        path = OUT / f"{name}-chunky.html"
        path.write_text(fn(), encoding="utf-8")
        print(f"wrote {path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
