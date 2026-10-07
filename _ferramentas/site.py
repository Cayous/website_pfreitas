#!/usr/bin/env python3
"""Ferramentas do site rfreitas.adv.br.

O site continua estático e sem build: o que está no repositório é o que vai ao
ar. Este script só reescreve, dentro dos .html, os trechos que se repetem em
várias páginas, para que não divirjam.

    python3 _ferramentas/site.py sincronizar        menu e rodapé em todas as páginas
    python3 _ferramentas/site.py artigos [PASTA]    artigos, índice, sumário da home, sitemap e feed
    python3 _ferramentas/site.py tudo [PASTA]       os dois

PASTA é onde moram os .md dos artigos (padrão: a pasta de marketing do
repositório do escritório). O repositório do site é público e o do escritório
não; por isso o .md fica lá e só o HTML vem para cá, e do cabeçalho do .md só
se leem os campos de LER_DO_ARTIGO. Campos internos (caso-fonte, pendências)
nunca chegam ao site.

Um artigo vai ao site quando o cabeçalho diz `publicar: sim`.

Os trechos compartilhados ficam entre marcadores:

    <!-- menu --> ... <!-- /menu -->                     itens do menu
    <!-- rodape --> ... <!-- /rodape -->                 rodapé das páginas comuns
    <!-- artigos-recentes --> ... <!-- /artigos-recentes -->   sumário por área na home

A Retaguarda tem rodapé próprio e só recebe o menu.
"""

import datetime as dt
import html
import json
import re
import shutil
import sys
from email.utils import format_datetime
from pathlib import Path

import yaml
from markdown_it import MarkdownIt

RAIZ = Path(__file__).resolve().parent.parent
SITE = "https://rfreitas.adv.br"
PASTA_ARTIGOS = Path.home() / "Documentos/Advocacia/4-escritorio/marketing/artigos"
LER_DO_ARTIGO = ("titulo", "descricao", "data", "atualizado", "area", "slug", "publicar")

# Ordem das áreas no sumário. Área que não estiver aqui entra depois, em ordem alfabética.
AREAS_ORDEM = ["Tribunais superiores", "Saúde suplementar", "Direito bancário",
               "Responsabilidade civil médica"]

# Na página inicial o sumário tem tamanho fixo, por mais que o blog cresça:
# no máximo HOME_AREAS áreas, com os HOME_POR_AREA artigos mais recentes de cada.
HOME_AREAS = 6
HOME_POR_AREA = 2

# No índice /artigos/, os INDICE_POR_AREA mais recentes de cada área. A página
# de cada área (/artigos/<área>/) lista todos, POR_PAGINA por página.
INDICE_POR_AREA = 8
POR_PAGINA = 25

AUTOR = "Ricardo Pacheco Mesquita de Freitas"
WHATSAPP = "5561996798902"
EMAIL = "contato@rfreitas.adv.br"

MESES = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho",
         "agosto", "setembro", "outubro", "novembro", "dezembro"]

# Páginas fixas que entram no sitemap, na ordem.
PAGINAS = ["/", "/tribunais-superiores.html", "/causas-complexas.html",
           "/retaguarda.html", "/artigos/", "/sobre.html", "/contato.html",
           "/privacidade.html"]

# Endereços antigos que continuam respondendo e levam ao conteúdo novo.
REDIRECIONAMENTOS = {
    "escritorio.html": "/sobre.html",
    "equipe.html": "/sobre.html",
    "empresarial.html": "/",
    "plano-de-saude.html": "/artigos/plano-de-saude-negativa-de-cobertura.html",
    "medico.html": "/artigos/responsabilidade-civil-medica-medico-e-hospital.html",
    "golpe-falso-funcionario-banco.html": "/artigos/golpe-do-falso-funcionario-responsabilidade-do-banco.html",
}

MENU = """<ul class="navbar-menu" id="navbar-menu">
      <li><a href="/tribunais-superiores.html">Tribunais Superiores</a></li>
      <li><a href="/causas-complexas.html">Causas Complexas</a></li>
      <li><a href="/retaguarda.html">Retaguarda</a></li>
      <li><a href="/artigos/">Artigos</a></li>
      <li class="navbar-secondary"><a href="/sobre.html">Sobre</a></li>
      <li class="navbar-menu-contato"><a href="/contato.html">Contato</a></li>
    </ul>"""

RODAPE = """<footer class="footer">
  <div class="container">
    <div class="footer-grid">

      <div class="brand-block">
        <img src="/assets/logo.png" alt="Pacheco Freitas Advocacia" class="footer-logo" width="240" height="141" loading="lazy">
        <p>Advocacia em Brasília para a fase recursal nos tribunais superiores e para causas complexas e urgentes, em parceria com advogados de todo o país.</p>
      </div>

      <div>
        <h4>Atuação</h4>
        <ul>
          <li><a href="/tribunais-superiores.html">Tribunais Superiores</a></li>
          <li><a href="/causas-complexas.html">Causas complexas e urgentes</a></li>
          <li><a href="/retaguarda.html">Retaguarda para escritórios</a></li>
          <li><a href="/artigos/">Artigos</a></li>
        </ul>
      </div>

      <div>
        <h4>Escritório</h4>
        <ul>
          <li><a href="/sobre.html">Sobre</a></li>
          <li><a href="/contato.html">Contato</a></li>
          <li><a href="/privacidade.html">Política de privacidade</a></li>
          <li><a href="/feed.xml">Feed dos artigos (RSS)</a></li>
        </ul>
      </div>

      <div>
        <h4>Contato</h4>
        <p class="contact-line"><a href="https://wa.me/5561996798902" target="_blank" rel="noopener noreferrer">WhatsApp (61) 99679-8902</a></p>
        <p class="contact-line"><a href="mailto:contato@rfreitas.adv.br">contato@rfreitas.adv.br</a></p>
        <p class="contact-line" style="margin-top: 14px;">Guará II · QI 33 · Lote 2<br>Brasília · DF · 71065-330</p>
      </div>

    </div>

    <div class="footer-bottom">
      <div class="copyright">© 2026 Pacheco Freitas Advocacia</div>
      <div class="credentials">OAB/DF 44.412 · OAB/MG 145.814</div>
    </div>
  </div>
</footer>"""

CABECA_COMUM = """<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
<link rel="alternate" type="application/rss+xml" title="Artigos · Pacheco Freitas Advocacia" href="/feed.xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;0,600;0,700;1,300;1,400;1,500&family=Lora:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Montserrat:wght@300;400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/styles.css">
<link rel="stylesheet" href="/assets/navbar.css">"""

NAV_ABRE = """<nav class="navbar" aria-label="Navegação principal">
  <div class="navbar-inner">
    <a href="/" class="navbar-brand" aria-label="Pacheco Freitas Advocacia">
      <img src="/assets/logo-mark.png" alt="" class="brand-mark" width="52" height="52" aria-hidden="true">
      <div class="name">Pacheco Freitas<span>Advocacia</span></div>
    </a>
    <!-- menu -->
    """

NAV_FECHA = """
    <!-- /menu -->
    <a href="/contato.html" class="navbar-cta">Fale Conosco</a>
    <button class="navbar-toggle" id="navbar-toggle" type="button" aria-label="Abrir menu" aria-controls="navbar-menu" aria-expanded="false">
      <span></span><span></span><span></span>
    </button>
  </div>
</nav>"""


def link_whatsapp(texto):
    from urllib.parse import quote
    return f"https://wa.me/{WHATSAPP}?text={quote(texto)}"


def trocar_marcado(texto, nome, conteudo):
    """Troca o que estiver entre <!-- nome --> e <!-- /nome -->."""
    padrao = re.compile(rf"(<!-- {nome} -->)(.*?)(<!-- /{nome} -->)", re.S)
    if not padrao.search(texto):
        return texto, False
    novo = padrao.sub(lambda m: f"{m.group(1)}\n{conteudo}\n{m.group(3)}", texto, count=1)
    return novo, novo != texto


def paginas_html():
    yield from sorted(RAIZ.glob("*.html"))
    yield from sorted((RAIZ / "artigos").rglob("*.html"))


def sincronizar():
    alteradas = []
    for pagina in paginas_html():
        texto = pagina.read_text(encoding="utf-8")
        novo, _ = trocar_marcado(texto, "menu", "    " + MENU)
        novo, _ = trocar_marcado(novo, "rodape", RODAPE)
        if novo != texto:
            pagina.write_text(novo, encoding="utf-8")
            alteradas.append(pagina.relative_to(RAIZ))
    for nome, destino in REDIRECIONAMENTOS.items():
        conteudo = pagina_redirecionamento(destino)
        caminho = RAIZ / nome
        if not caminho.exists() or caminho.read_text(encoding="utf-8") != conteudo:
            caminho.write_text(conteudo, encoding="utf-8")
            alteradas.append(caminho.relative_to(RAIZ))
    return alteradas


def pagina_redirecionamento(destino):
    url = SITE + destino
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Conteúdo movido | Pacheco Freitas Advocacia</title>
  <link rel="canonical" href="{url}">
  <meta http-equiv="refresh" content="0; url={destino}">
</head>
<body>
  <p>Este conteúdo mudou de endereço: <a href="{destino}">{url}</a>.</p>
  <script>
    window.location.replace("{destino}" + window.location.search + window.location.hash);
  </script>
</body>
</html>
"""


# --------------------------------------------------------------------- artigos

def ler_artigo(caminho):
    texto = caminho.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", texto, re.S)
    if not m:
        return None
    cabecalho = yaml.safe_load(m.group(1)) or {}
    publicar = cabecalho.get("publicar")
    if publicar not in (True, "sim"):
        return None
    meta = {k: cabecalho.get(k) for k in LER_DO_ARTIGO}
    faltando = [k for k in ("titulo", "descricao", "data", "area", "slug") if not meta.get(k)]
    if faltando:
        sys.exit(f"{caminho.name}: falta {', '.join(faltando)} no cabeçalho")
    corpo = m.group(2).strip()
    # O título já vai no topo da página; um "# título" no começo do corpo sairia duplicado.
    corpo = re.sub(r"\A# [^\n]*\n+", "", corpo)
    meta["data"] = para_data(meta["data"])
    meta["atualizado"] = para_data(meta["atualizado"]) if meta.get("atualizado") else meta["data"]
    meta["corpo_md"] = corpo
    meta["palavras"] = len(re.findall(r"\w+", corpo))
    meta["minutos"] = max(1, round(meta["palavras"] / 200))
    meta["url"] = f"/artigos/{meta['slug']}.html"
    meta["origem"] = caminho.name
    return meta


def para_data(valor):
    if isinstance(valor, dt.date):
        return valor
    return dt.date.fromisoformat(str(valor))


def data_extenso(data):
    return f"{data.day} de {MESES[data.month - 1]} de {data.year}"


def md_para_html(texto):
    md = MarkdownIt("commonmark", {"typographer": False}).enable("table")
    return md.render(texto)


def ancora(area):
    sem_acento = area.lower().translate(str.maketrans("áàâãéêíóôõúüç", "aaaaeeiooouuc"))
    return re.sub(r"[^a-z0-9]+", "-", sem_acento).strip("-")


def por_area(artigos):
    """Agrupa por área, na ordem de AREAS_ORDEM e depois alfabética; dentro, do mais novo ao mais antigo."""
    grupos = {}
    for a in artigos:
        grupos.setdefault(a["area"], []).append(a)
    ordem = [x for x in AREAS_ORDEM if x in grupos] + sorted(x for x in grupos if x not in AREAS_ORDEM)
    return [(area, grupos[area]) for area in ordem]


def url_area(area, pagina=1):
    """Página da área: /artigos/<área>/ e, a partir da segunda, /artigos/<área>/<n>/."""
    return f"/artigos/{ancora(area)}/" + (f"{pagina}/" if pagina > 1 else "")


def itens_lista(lista):
    return "\n".join(
        f'          <li><a href="{a["url"]}">{html.escape(a["titulo"])}</a>'
        f'<span class="quando">{MESES[a["data"].month - 1][:3]} {a["data"].year}</span></li>'
        for a in lista)


def bloco_area(area, lista, limite, nivel="h2"):
    """Bloco de uma área com os `limite` mais recentes e o link para a página da área."""
    mais = ""
    if len(lista) > limite:
        mais = (f'\n        <a class="mais" href="{url_area(area)}">'
                f'Todos os {len(lista)} artigos de {html.escape(area.lower())} →</a>')
    return f"""<section class="sumario-area" id="{ancora(area)}">
        <{nivel}><a href="{url_area(area)}">{html.escape(area)}</a></{nivel}>
        <ul>
{itens_lista(lista[:limite])}
        </ul>{mais}
      </section>"""


def paginacao(area, atual, total):
    if total == 1:
        return ""
    # Primeira, última e duas vizinhas da atual; o resto vira "…".
    mostrar = sorted({1, total} | {n for n in range(atual - 2, atual + 3) if 1 <= n <= total})
    partes, anterior_n = [], 0
    for n in mostrar:
        if n - anterior_n > 1:
            partes.append('<span class="reticencias">…</span>')
        partes.append(f'<span aria-current="page">{n}</span>' if n == atual
                      else f'<a href="{url_area(area, n)}">{n}</a>')
        anterior_n = n
    numeros = " ".join(partes)
    anterior = (f'<a class="ant" href="{url_area(area, atual - 1)}" rel="prev">← Mais recentes</a>'
                if atual > 1 else '<span class="ant"></span>')
    proxima = (f'<a class="prox" href="{url_area(area, atual + 1)}" rel="next">Mais antigos →</a>'
               if atual < total else '<span class="prox"></span>')
    return f"""
    <nav class="paginacao" aria-label="Páginas de {html.escape(area.lower())}">
      {anterior}
      <span class="numeros">{numeros}</span>
      {proxima}
    </nav>"""


def pagina_artigo(a):
    titulo = html.escape(a["titulo"])
    descricao = html.escape(a["descricao"])
    url = SITE + a["url"]
    ld = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": a["titulo"],
        "description": a["descricao"],
        "datePublished": a["data"].isoformat(),
        "dateModified": a["atualizado"].isoformat(),
        "inLanguage": "pt-BR",
        "mainEntityOfPage": url,
        "image": SITE + "/assets/foto_ricardo.jpeg",
        "author": {"@type": "Person", "name": AUTOR, "url": SITE + "/sobre.html"},
        "publisher": {"@type": "LegalService", "name": "Pacheco Freitas Advocacia",
                      "url": SITE + "/", "logo": SITE + "/assets/logo.png"},
    }
    whats = link_whatsapp(f"Olá, Dr. Ricardo. Li o artigo \"{a['titulo']}\" e queria conversar sobre um caso.")
    atualizado = ""
    if a["atualizado"] != a["data"]:
        atualizado = f" · atualizado em {data_extenso(a['atualizado'])}"
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
{CABECA_COMUM}
<title>{titulo} | Pacheco Freitas Advocacia</title>
<meta name="description" content="{descricao}">
<meta name="author" content="{AUTOR}">
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="canonical" href="{url}">
<meta property="og:locale" content="pt_BR">
<meta property="og:type" content="article">
<meta property="og:title" content="{titulo}">
<meta property="og:description" content="{descricao}">
<meta property="og:url" content="{url}">
<meta property="og:site_name" content="Pacheco Freitas Advocacia">
<meta property="og:image" content="{SITE}/assets/foto_ricardo.jpeg">
<meta property="article:published_time" content="{a['data'].isoformat()}">
<meta property="article:section" content="{html.escape(a['area'])}">
<script type="application/ld+json">
{json.dumps(ld, ensure_ascii=False, indent=2)}
</script>
</head>
<body>

{NAV_ABRE}{MENU}{NAV_FECHA}

<main>

<section class="page-hero bg-navy artigo-hero">
  <div class="container-sm">
    <span class="eyebrow dark">{html.escape(a['area'])}</span>
    <h1>{titulo}</h1>
    <p class="lead">{descricao}</p>
    <p class="artigo-meta">{AUTOR} · {data_extenso(a['data'])}{atualizado} · {a['minutos']} min de leitura</p>
  </div>
</section>

<article class="section-pad bg-paper">
  <div class="container-sm artigo-corpo">
{md_para_html(a['corpo_md'])}
  </div>
</article>

<section class="section-pad-sm bg-cream">
  <div class="container-sm autor-box">
    <img src="/assets/foto_ricardo.jpeg" alt="{AUTOR}" width="96" height="96" loading="lazy">
    <div>
      <strong>{AUTOR}</strong>
      <p>Advogado em Brasília, OAB/DF 44.412 e OAB/MG 145.814. Mestre em Direito Constitucional pelo UniCEUB. Trabalha em parceria com escritórios de todo o país na fase recursal dos tribunais superiores e em causas complexas e urgentes. <a href="/sobre.html">Trajetória</a> · <a href="/artigos/">Outros artigos</a></p>
    </div>
  </div>
</section>

<section class="cta-strip bg-navy">
  <div class="container-sm">
    <span class="eyebrow dark">Para advogados</span>
    <h2 style="margin-top: 18px;">Esse tema apareceu num processo <em>do seu escritório?</em></h2>
    <p>Mande a decisão e a data da publicação. Dizemos o que vemos e como podemos entrar no caso com você.</p>
    <div class="cta-acoes">
      <a href="{whats}" class="btn light" target="_blank" rel="noopener noreferrer">Conversar no WhatsApp <span class="arrow">→</span></a>
      <a href="mailto:{EMAIL}" class="btn light">{EMAIL}</a>
    </div>
  </div>
</section>

</main>

<!-- rodape -->
{RODAPE}
<!-- /rodape -->

<script src="/assets/navbar.js" defer></script>

</body>
</html>
"""


def pagina_lista(caminho, titulo, descricao, hero, corpo):
    """Molde comum do índice de artigos e das páginas de área."""
    url = SITE + caminho
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
{CABECA_COMUM}
<title>{html.escape(titulo)} | Pacheco Freitas Advocacia</title>
<meta name="description" content="{html.escape(descricao)}">
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="canonical" href="{url}">
<meta property="og:locale" content="pt_BR">
<meta property="og:type" content="website">
<meta property="og:title" content="{html.escape(titulo)} · Pacheco Freitas Advocacia">
<meta property="og:description" content="{html.escape(descricao)}">
<meta property="og:url" content="{url}">
<meta property="og:site_name" content="Pacheco Freitas Advocacia">
<meta property="og:image" content="{SITE}/assets/foto_ricardo.jpeg">
</head>
<body>

{NAV_ABRE}{MENU}{NAV_FECHA}

<main>

<section class="page-hero bg-navy">
  <div class="container-sm">
{hero}
  </div>
</section>

<section class="section-pad bg-paper">
  <div class="container-sm">
{corpo}
  </div>
</section>

</main>

<!-- rodape -->
{RODAPE}
<!-- /rodape -->

<script src="/assets/navbar.js" defer></script>

</body>
</html>
"""


def pagina_indice(artigos):
    grupos = por_area(artigos)
    indice = "".join(
        f'<a href="{url_area(area)}">{html.escape(area)} <span>({len(lista)})</span></a>'
        for area, lista in grupos)
    blocos = "\n      ".join(bloco_area(area, lista, limite=INDICE_POR_AREA) for area, lista in grupos)
    hero = """    <span class="eyebrow dark">Artigos</span>
    <h1>O que estudamos <em>nos processos.</em></h1>
    <p class="lead">Escrito para quem advoga. Cada artigo nasce de uma questão que apareceu num caso do escritório, e responde com a lei e com os precedentes, lidos no inteiro teor.</p>"""
    corpo = f"""    <nav class="sumario-indice" aria-label="Áreas">{indice}</nav>
    <div class="sumario">
      {blocos}
    </div>"""
    return pagina_lista("/artigos/", "Artigos",
                        "Artigos técnicos para advogados: admissibilidade de recursos no STJ e no STF, "
                        "saúde suplementar, fraude bancária, responsabilidade civil e processo civil.",
                        hero, corpo)


def pagina_area(area, lista, pagina, total):
    trecho = lista[(pagina - 1) * POR_PAGINA:pagina * POR_PAGINA]
    sufixo = f" · página {pagina} de {total}" if total > 1 else ""
    hero = f"""    <span class="eyebrow dark"><a href="/artigos/" style="color: inherit;">Artigos</a></span>
    <h1>{html.escape(area)}</h1>
    <p class="lead">{len(lista)} artigo{"s" if len(lista) != 1 else ""}{sufixo}.</p>"""
    corpo = f"""    <p class="voltar"><a href="/artigos/">← Todas as áreas</a></p>
    <section class="sumario-area">
        <ul>
{itens_lista(trecho)}
        </ul>
    </section>{paginacao(area, pagina, total)}"""
    return pagina_lista(url_area(area, pagina), f"{area}{sufixo}",
                        f"Artigos para advogados sobre {area.lower()}.", hero, corpo)


def sitemap(artigos, extras=()):
    hoje = dt.date.today().isoformat()
    linhas = ['<?xml version="1.0" encoding="UTF-8"?>',
              '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for p in PAGINAS:
        linhas.append(f"  <url>\n    <loc>{SITE}{p}</loc>\n    <lastmod>{hoje}</lastmod>\n  </url>")
    for a in artigos:
        linhas.append(f"  <url>\n    <loc>{SITE}{a['url']}</loc>\n    <lastmod>{a['atualizado'].isoformat()}</lastmod>\n  </url>")
    for caminho in extras:
        linhas.append(f"  <url>\n    <loc>{SITE}{caminho}</loc>\n    <lastmod>{hoje}</lastmod>\n  </url>")
    linhas.append("</urlset>")
    return "\n".join(linhas) + "\n"


def feed(artigos):
    def data_rfc(d):
        return format_datetime(dt.datetime(d.year, d.month, d.day, 9, 0, tzinfo=dt.timezone(dt.timedelta(hours=-3))))
    itens = []
    for a in artigos:
        itens.append(f"""    <item>
      <title>{html.escape(a['titulo'])}</title>
      <link>{SITE}{a['url']}</link>
      <guid isPermaLink="true">{SITE}{a['url']}</guid>
      <pubDate>{data_rfc(a['data'])}</pubDate>
      <category>{html.escape(a['area'])}</category>
      <description>{html.escape(a['descricao'])}</description>
    </item>""")
    ultima = data_rfc(artigos[0]["atualizado"]) if artigos else data_rfc(dt.date.today())
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>Artigos · Pacheco Freitas Advocacia</title>
    <link>{SITE}/artigos/</link>
    <atom:link href="{SITE}/feed.xml" rel="self" type="application/rss+xml"/>
    <description>Artigos técnicos para advogados, escritos a partir dos processos que o escritório conduz.</description>
    <language>pt-BR</language>
    <lastBuildDate>{ultima}</lastBuildDate>
{chr(10).join(itens)}
  </channel>
</rss>
"""


def gerar_artigos(pasta):
    artigos = [a for a in (ler_artigo(p) for p in sorted(Path(pasta).glob("*.md"))) if a]
    slugs = [a["slug"] for a in artigos]
    repetidos = {s for s in slugs if slugs.count(s) > 1}
    if repetidos:
        sys.exit(f"slug repetido: {', '.join(sorted(repetidos))}")
    artigos.sort(key=lambda a: (a["data"], a["titulo"]), reverse=True)

    destino = RAIZ / "artigos"
    destino.mkdir(exist_ok=True)
    esperados = {f"{a['slug']}.html" for a in artigos} | {"index.html"}
    for velho in destino.glob("*.html"):
        if velho.name not in esperados:
            velho.unlink()
            print(f"  removido {velho.relative_to(RAIZ)} (não está mais publicado)")
    for a in artigos:
        (destino / f"{a['slug']}.html").write_text(pagina_artigo(a), encoding="utf-8")
        print(f"  artigos/{a['slug']}.html  ←  {a['origem']}  ({a['palavras']} palavras)")
    (destino / "index.html").write_text(pagina_indice(artigos), encoding="utf-8")

    # Páginas de área. As subpastas de artigos/ são todas geradas aqui: a que
    # não corresponde a área publicada é apagada.
    paginas_area = []
    pastas = {ancora(area) for area, _ in por_area(artigos)}
    for velha in destino.iterdir():
        if velha.is_dir() and velha.name not in pastas:
            shutil.rmtree(velha)
            print(f"  removida a pasta {velha.relative_to(RAIZ)} (área sem artigo publicado)")
    for area, lista in por_area(artigos):
        pasta = destino / ancora(area)
        if pasta.exists():
            shutil.rmtree(pasta)
        total = max(1, -(-len(lista) // POR_PAGINA))
        for n in range(1, total + 1):
            arquivo = RAIZ / url_area(area, n).strip("/") / "index.html"
            arquivo.parent.mkdir(parents=True, exist_ok=True)
            arquivo.write_text(pagina_area(area, lista, n, total), encoding="utf-8")
            paginas_area.append(url_area(area, n))
        print(f"  {url_area(area)}  ({len(lista)} artigo(s), {total} página(s))")
    (RAIZ / "sitemap.xml").write_text(sitemap(artigos, paginas_area), encoding="utf-8")
    (RAIZ / "feed.xml").write_text(feed(artigos), encoding="utf-8")

    home = RAIZ / "index.html"
    vitrine = "\n      ".join(bloco_area(area, lista, limite=HOME_POR_AREA, nivel="h3")
                               for area, lista in por_area(artigos)[:HOME_AREAS]) or "<p>Em breve.</p>"
    texto, achou = trocar_marcado(home.read_text(encoding="utf-8"), "artigos-recentes",
                                  f"      {vitrine}")
    if achou:
        home.write_text(texto, encoding="utf-8")
    print(f"{len(artigos)} artigo(s) publicados; índice, sumário da home, sitemap e feed refeitos.")


def conferir_links():
    """Avisa de link interno que aponta para arquivo inexistente (ex.: artigo despublicado)."""
    quebrados = []
    for pagina in [*sorted(RAIZ.glob("*.html")), *sorted((RAIZ / "artigos").rglob("*.html"))]:
        for alvo in re.findall(r'(?:href|src)="(/[^"#?]*)', pagina.read_text(encoding="utf-8")):
            caminho = RAIZ / alvo.lstrip("/")
            if alvo.endswith("/"):
                caminho = caminho / "index.html"
            if not caminho.exists():
                quebrados.append(f"{pagina.relative_to(RAIZ)} → {alvo}")
    for q in quebrados:
        print(f"  AVISO: link quebrado: {q}")
    return quebrados


def main(argv):
    if len(argv) < 2 or argv[1] not in ("sincronizar", "artigos", "tudo"):
        sys.exit(__doc__)
    pasta = Path(argv[2]) if len(argv) > 2 else PASTA_ARTIGOS
    if argv[1] in ("artigos", "tudo"):
        gerar_artigos(pasta)
    if argv[1] in ("sincronizar", "tudo"):
        for p in sincronizar():
            print(f"  sincronizado {p}")
    conferir_links()


if __name__ == "__main__":
    main(sys.argv)
