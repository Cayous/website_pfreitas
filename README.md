# Pacheco Freitas Advocacia · Site Institucional

Site estático em HTML/CSS/JS puro. Sem build, sem dependências, sem servidor de aplicação. Hospede em qualquer servidor estático (Hostinger, Netlify, Vercel, GitHub Pages, AWS S3, etc.) ou abra `index.html` localmente.

## Estrutura de arquivos

```
pacheco-freitas-site/
├── index.html              ← Home (página inicial)
├── escritorio.html         ← O Escritório
├── empresarial.html        ← Vertical I — Família Empresária e Patrimônio
├── medico.html             ← Vertical II — Direito Médico e da Saúde
├── equipe.html             ← Equipe (Ricardo + Martim)
├── contato.html            ← Contato
└── assets/
    ├── styles.css          ← TODO o CSS está aqui (sistema de design)
    ├── logotipo.png
    ├── logotipo2.png
    ├── logotipo_transparente.png
    ├── foto_ricardo.jpeg
    └── foto_martim.jpeg
```

## Como editar

**Mudar texto:** abra o `.html` e edite. As páginas são autocontidas — alterar uma não afeta as outras.

**Mudar cores, fontes, espaçamentos:** edite `assets/styles.css`. As variáveis principais estão no topo do arquivo, dentro de `:root { ... }`. As cores-chave:

```
--navy:      #0B1A3F   (azul-marinho dominante)
--gold:      #B89968   (dourado champagne)
--paper:     #FBFAF6   (off-white de fundo)
```

**Trocar fotos:** substitua os arquivos em `assets/` mantendo os nomes (`foto_ricardo.jpeg`, `foto_martim.jpeg`).

**Trocar dados de contato:** os dados aparecem no rodapé de TODAS as páginas e na página `contato.html`. Use Ctrl+F para encontrar o número, e-mail ou endereço e substituir em cada arquivo.

**Adicionar página nova:** copie qualquer `.html` existente, troque o conteúdo do meio (entre `<nav>` e `<footer>`), e adicione um link no menu (`<ul class="navbar-menu">`) de TODAS as páginas.

## Alinhamento com o folder

O site é o lastro institucional do folder PDF entregue à holding familiar:

- **Home + Escritório** estabelecem o posicionamento boutique e a divisão em duas verticais (afasta a impressão de "escritório só de Direito Médico" que o site anterior dava).
- **Empresarial & Patrimônio** confirma e aprofunda o que o folder ofereceu — empresarial, sucessório, imobiliário, tributário, família patrimonial, contencioso cível.
- **Equipe** apresenta o Martim como **Advogado Consultor** (parceria permanente). Coerente com o folder, em que ele assume a posição de sócio para o projeto específico de assessoria continuada — figura comum em projetos boutique.

## Domínio

Conteúdo migrado de `rfreitas.adv.br` provisoriamente, até ativação de `pachecofreitas.adv.br`. Recomenda-se redirecionar 301 do domínio antigo para o novo após a transição.

## Notas técnicas

- Fontes via Google Fonts (Cormorant Garamond + Lora + Montserrat).
- Mapa do Google Maps na página `contato.html` usa `<iframe>` com endereço já preenchido — funciona automaticamente quando hospedado.
- Mobile-first responsivo. Navbar vira hamburger abaixo de 980px.
- Sem JavaScript pesado: apenas toggle de menu mobile e highlight de página ativa.
- Formulário de contato em `contato.html` é puramente cosmético na entrega — para funcionar de verdade é necessário um backend (ex: Formspree, Netlify Forms, ou integração com WhatsApp).

## OAB

O número da inscrição OAB do(s) sócio(s) ainda precisa ser inserido no rodapé. Procure por `OAB/DF` em todos os arquivos `.html` e substitua pelo número correto (ex: `OAB/DF nº 12.345`).
