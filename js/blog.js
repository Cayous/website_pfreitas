// Função para carregar os posts do JSON
async function loadPosts() {
    try {
        const response = await fetch('data/posts.json'); // Caminho para o arquivo JSON
        const posts = await response.json();
        return posts;
    } catch (error) {
        console.error('Erro ao carregar os posts:', error);
        return [];
    }
}

// Função para renderizar os posts na página
function renderPosts(posts, containerId, limit = null) {
    const container = document.getElementById(containerId);
    if (!container) return;

    // Limita o número de posts se necessário
    const postsToRender = limit ? posts.slice(0, limit) : posts;

    // Cria o HTML para cada post
    const postsHTML = postsToRender.map(post => `
        <div class="blog-post">
            <img src="${post.image}" alt="${post.title}" class="blog-image">
            <div class="blog-content">
                <h3>${post.title}</h3>
                <p class="blog-date">${new Date(post.date).toLocaleDateString('pt-BR')}</p>
                <p class="blog-summary">${post.summary}</p>
                <a href="post.html?id=${post.id}" class="cta-button">Leia Mais</a>
            </div>
        </div>
    `).join('');

    // Insere os posts no container
    container.innerHTML = postsHTML;
}

// Carrega e renderiza os posts na página principal
document.addEventListener('DOMContentLoaded', async () => {
    let posts = await loadPosts();

    // Ordena os posts por data (do mais recente para o mais antigo)
    posts.sort((a, b) => new Date(b.date) - new Date(a.date));

    // Renderiza os últimos 3 posts na página principal
    if (document.getElementById('blog-posts')) {
        renderPosts(posts, 'blog-posts', 3); // Limite de 3 posts
    }

    // Renderiza todos os posts na página de blog
    if (document.getElementById('all-blog-posts')) {
        renderPosts(posts, 'all-blog-posts'); // Sem limite
    }
});