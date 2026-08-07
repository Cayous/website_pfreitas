# Pacheco Freitas Advocacia · Site Institucional

Site estático em HTML/CSS/JS puro. Sem build, sem dependências, sem servidor de aplicação. Hospede em qualquer servidor estático (Hostinger, Netlify, Vercel, GitHub Pages, AWS S3, etc.) ou abra `index.html` localmente.

## Estrutura de arquivos

```
pacheco-freitas-site/
├── index.html              ← Home (página inicial)
├── escritorio.html         ← O Escritório
├── plano-de-saude.html     ← Planos de Saúde — página orgânica e de campanha
├── medico.html             ← Direito Médico para profissionais e instituições
├── empresarial.html        ← Redirecionamento legado para Planos de Saúde
├── equipe.html             ← Equipe (Ricardo + consultores e parceiros)
├── contato.html            ← Contato
├── privacidade.html        ← Política de privacidade
├── robots.txt              ← Regras de rastreamento e local do sitemap
├── sitemap.xml             ← URLs canônicas para indexação
└── assets/
    ├── styles.css          ← CSS do site institucional
    ├── plano-saude.css     ← CSS da página de Planos de Saúde
    ├── plano-saude.js      ← Conversões, consentimento e interações
    ├── logotipo.png
    ├── logotipo2.png
    ├── logotipo_transparente.png
    └── foto_ricardo.jpeg
```

## Como editar

**Mudar texto:** abra o `.html` e edite. As páginas são autocontidas — alterar uma não afeta as outras.

**Mudar cores, fontes, espaçamentos:** edite `assets/styles.css`. As variáveis principais estão no topo do arquivo, dentro de `:root { ... }`. As cores-chave:

```
--navy:      #0B1A3F   (azul-marinho dominante)
--gold:      #B89968   (dourado champagne)
--paper:     #FBFAF6   (off-white de fundo)
```

**Trocar foto:** substitua o arquivo `assets/foto_ricardo.jpeg`, mantendo o mesmo nome.

**Trocar dados de contato:** os dados aparecem no rodapé de TODAS as páginas e na página `contato.html`. Use Ctrl+F para encontrar o número, e-mail ou endereço e substituir em cada arquivo.

**Adicionar página nova:** copie qualquer `.html` existente, troque o conteúdo do meio (entre `<nav>` e `<footer>`), e adicione um link no menu (`<ul class="navbar-menu">`) de TODAS as páginas.

## Posicionamento do site

O site concentra a apresentação do escritório em duas frentes complementares:

- **Planos de Saúde** atende beneficiários em negativas de internação, cirurgia, medicamento, home care e outros tratamentos prescritos.
- **Direito Médico** atende médicos, dentistas, clínicas e hospitais em atuação preventiva, responsabilidade civil e processos ético-disciplinares.
- **Equipe** apresenta o sócio fundador Ricardo e informa que o escritório conta com uma equipe especializada de consultores e parceiros, formada conforme as necessidades de cada trabalho.

## Domínio

O domínio canônico configurado no site é `https://rfreitas.adv.br/`. Se o domínio mudar, atualize os links canônicos, Open Graph, JSON-LD, `robots.txt` e `sitemap.xml`, além de configurar redirecionamentos HTTP 301.

## Notas técnicas

- Fontes via Google Fonts (Cormorant Garamond + Lora + Montserrat).
- Mobile-first responsivo. Navbar vira hamburger abaixo de 980px.
- Sem JavaScript pesado: toggle de menu, highlight de página ativa, consentimento e medição de cliques da campanha.
- O contato institucional direciona para telefone, e-mail e WhatsApp; o site não coleta prontuários ou dados médicos por formulário.
- As páginas principais possuem títulos e descrições exclusivos, URLs canônicas, Open Graph, HTML semântico e dados estruturados Schema.org.
- `robots.txt` permite Googlebot, Bingbot e OAI-SearchBot e informa a localização do sitemap.

## Dados profissionais

Ricardo Pacheco Mesquita de Freitas · OAB/DF 44.412. Mantenha nome, inscrição, telefone e endereço consistentes no site, no Perfil da Empresa no Google e nos demais perfis públicos do escritório.
