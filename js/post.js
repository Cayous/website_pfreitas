// Função para carregar o post específico
async function loadPost(postId) {
    try {
        const response = await fetch('data/posts.json');
        const posts = await response.json();
        return posts.find(post => post.id === postId);
    } catch (error) {
        console.error('Erro ao carregar o post:', error);
        return null;
    }
}

// Função para renderizar o post na página
function renderPost(post) {
    const container = document.getElementById('post-content');
    if (!container || !post) return;

    container.innerHTML = `
        <h2>${post.title}</h2>
        <p class="blog-date">${new Date(post.date).toLocaleDateString('pt-BR')}</p>
        <img src="${post.image}" alt="${post.title}" class="blog-image">
        <div class="blog-content">
            <p>${post.content}</p>
        </div>
    `;
}

// Carrega e renderiza o post na página
document.addEventListener('DOMContentLoaded', async () => {
    const urlParams = new URLSearchParams(window.location.search);
    const postId = parseInt(urlParams.get('id'));

    if (postId) {
        const post = await loadPost(postId);
        renderPost(post);
    }
});