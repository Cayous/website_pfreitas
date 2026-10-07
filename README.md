# Pacheco Freitas Advocacia · Site Institucional

Site estático em HTML/CSS/JS puro. Sem build, sem dependências, sem servidor de aplicação. Hospede em qualquer servidor estático (Hostinger, Netlify, Vercel, GitHub Pages, AWS S3, etc.) ou abra `index.html` localmente.

## Estrutura de arquivos

```
├── index.html                  ← Início: posicionamento, análise de admissibilidade, frentes, artigos
├── tribunais-superiores.html   ← REsp, RE, agravos, admissibilidade, presença em Brasília
├── causas-complexas.html       ← copatrocínio em causa complexa ou urgente
├── retaguarda.html             ← produção de peças para escritórios (CSS e JS próprios)
├── sobre.html                  ← trajetória do Ricardo e método do escritório
├── contato.html                ← canais; seção #parte para quem não é advogado
├── privacidade.html
├── artigos/                    ← GERADO: um .html por artigo + index.html
├── feed.xml, sitemap.xml       ← GERADOS
├── escritorio.html, equipe.html, empresarial.html,
│   plano-de-saude.html, medico.html,
│   golpe-falso-funcionario-banco.html   ← GERADOS: redirecionam os endereços antigos
├── _ferramentas/site.py        ← menu, rodapé, artigos, sitemap, feed, redirecionamentos
└── assets/
    ├── styles.css              ← CSS do site (componentes novos no fim, "REPOSICIONAMENTO")
    ├── navbar.css, navbar.js   ← cabeçalho de todas as páginas
    ├── retaguarda.css, retaguarda.js
    └── foto_ricardo.jpeg, logo*.png
```

Pasta com `_` na frente não é publicada pelo GitHub Pages (Jekyll a ignora).

## Como editar

**Texto de uma página:** abra o `.html` e edite. Os links internos são
absolutos (`/sobre.html`); para ver no computador, sirva a pasta em vez de
abrir o arquivo:

```bash
python3 -m http.server 8811 --bind 127.0.0.1    # e abra http://127.0.0.1:8811
```

**Menu e rodapé:** não se editam nas páginas. Ficam em `_ferramentas/site.py`
(`MENU` e `RODAPE`) e são copiados para todas as páginas entre os marcadores
`<!-- menu -->` e `<!-- rodape -->`. A Retaguarda recebe só o menu; o rodapé
dela é próprio.

**Artigos:** o `.md` mora no repositório do escritório
(`~/Documentos/Advocacia/4-escritorio/marketing/artigos/`), que é privado.
Este repositório é público, então só o HTML vem para cá, e do cabeçalho do
`.md` só se leem `titulo`, `descricao`, `data`, `atualizado`, `area`, `slug` e
`publicar`. Vai ao site o artigo com `publicar: sim`. Depois de escrever ou
mudar um artigo, ou o menu, ou o rodapé:

```bash
python3 _ferramentas/site.py tudo
```

Isso refaz `artigos/`, o sumário da página inicial, o `sitemap.xml`, o
`feed.xml`, o menu e o rodapé de todas as páginas e os redirecionamentos
(`REDIRECIONAMENTOS` no script).

Os artigos aparecem em **sumário por área**, uma linha por título, para
escalar: o índice (`/artigos/`) lista todos, com atalhos para cada área no
topo; a página inicial mostra no máximo `HOME_AREAS` áreas (6) com os
`HOME_POR_AREA` artigos mais recentes de cada (2) e um link "Mais N". A ordem
das áreas está em `AREAS_ORDEM`; área nova entra depois, em ordem alfabética.
Cada área tem página própria, `/artigos/<área>/`, com `POR_PAGINA` (25)
artigos por página e paginação em `/artigos/<área>/2/`, `/3/`…; o índice
mostra os `INDICE_POR_AREA` (8) mais recentes de cada área e leva à página
dela. As subpastas de `artigos/` são todas geradas: não ponha nada à mão lá.
Ao fim de cada geração, o script avisa de link interno quebrado (por exemplo,
um redirecionamento que aponta para artigo despublicado).

Testado em 07.10.2026 com 130 artigos fictícios em seis áreas (uma delas com
três páginas), em 1366 e 375 px. Precisa de `markdown_it` e
`yaml` no Python do sistema.

**Cores e fontes:** variáveis no topo de `assets/styles.css`
(`--navy #0B1A3F`, `--gold #B89968`, `--paper #FBFAF6`).

## Posicionamento do site (desde 07.10.2026)

O site fala com **advogados** de qualquer estado: o escritório que eles
chamam quando a causa fica complexa, urgente ou sobe para Brasília. Três
frentes: Tribunais Superiores (a principal, centrada na admissibilidade),
Causas complexas e urgentes (copatrocínio) e Retaguarda (peças). A parte que
chega direto também é atendida (`contato.html#parte`). O site não fala em
preço. As antigas páginas de produto viraram artigos técnicos, e os
endereços antigos redirecionam para eles.

A prospecção (`~/Documentos/Advocacia/_prospeccao/ABORDAGENS.md`) aponta
para `tribunais-superiores.html`.

## Como publicar (medido em 21.09.2026)

O site é **GitHub Pages**, servindo a branch `main` na raiz — confirmado pelos
IPs (185.199.108–111.153) e pelo cabeçalho `server: GitHub.com`. Push em `main`
publica; a compilação leva cerca de um minuto.

**Armadilha:** o `git push`/`git fetch` por SSH **não funciona nesta máquina** —
a chave pede passphrase e não há `ssh-askpass` instalado. O sintoma engana: o
`origin/main` local fica congelado e o `git status` anuncia "ahead 8" mesmo
quando o GitHub já está em dia. Não acredite nesse número sem um fetch que
tenha funcionado.

Publicar por HTTPS, usando a credencial do `gh`:

```bash
gh auth setup-git
git push https://github.com/Cayous/website_pfreitas.git main
```

Conferir de fato no ar:

```bash
gh api repos/Cayous/website_pfreitas/pages/builds --jq '.[0].status'
curl -sI https://rfreitas.adv.br/<pagina>.html | head -1
```

## Telefone

Desde 26.09.2026 **todas** as páginas usam o celular profissional do
Ricardo, (61) 99679-8902; o celular do escritório, (61) 99641-9368, foi
cancelado. O perfil "Pacheco Freitas Advocacia" no Google Maps já mostra o
número novo.

## Domínio

O domínio canônico configurado no site é `https://rfreitas.adv.br/`. Se o domínio mudar, atualize os links canônicos, Open Graph, JSON-LD, `robots.txt` e `sitemap.xml`, além de configurar redirecionamentos HTTP 301.

## Notas técnicas

- Fontes via Google Fonts (Cormorant Garamond + Lora + Montserrat).
- Mobile-first responsivo. O cabeçalho (`assets/navbar.css` + `navbar.js`) é o mesmo em todas as páginas: Tribunais Superiores · Causas Complexas · Retaguarda · Artigos · Sobre, mais o botão "Fale Conosco". O `navbar.js` mede o cabeçalho e recolhe em estágios para nunca alargar a página (Sobre é o item `navbar-secondary`); abaixo de 1076 px vai tudo para o hambúrguer, com "Contato" como item. Conferido em 07.10.2026 em 1366, 1100, 820 e 375 px, em todas as páginas.
- Sem JavaScript pesado: menu, página ativa (um artigo marca "Artigos"), filtro de áreas no índice de artigos. Desde 07.10.2026 não há Google Ads nem medição de nenhum tipo; o único serviço externo é o Google Fonts.
- O contato institucional direciona para telefone, e-mail e WhatsApp; o site não coleta prontuários ou dados médicos por formulário.
- As páginas principais possuem títulos e descrições exclusivos, URLs canônicas, Open Graph, HTML semântico e dados estruturados Schema.org.
- `robots.txt` permite Googlebot, Bingbot e OAI-SearchBot e informa a localização do sitemap.

## Dados profissionais

Ricardo Pacheco Mesquita de Freitas · OAB/DF 44.412 · OAB/MG 145.814. Mantenha nome, inscrição, telefone e endereço consistentes no site, no Perfil da Empresa no Google e nos demais perfis públicos do escritório.
