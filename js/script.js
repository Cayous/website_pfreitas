// Smooth scroll para navegação
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            const headerOffset = 80; // Altura do header fixo
            const elementPosition = target.getBoundingClientRect().top;
            const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

            window.scrollTo({
                top: offsetPosition,
                behavior: 'smooth'
            });
        }
    });
});

// Adiciona classe 'scrolled' ao header quando rolar a página
window.addEventListener('scroll', () => {
    const header = document.querySelector('header');
    if (window.scrollY > 50) {
        header.classList.add('scrolled');
    } else {
        header.classList.remove('scrolled');
    }
});

// Animação de fade-in para os elementos quando entram na viewport
const observerOptions = {
    root: null,
    rootMargin: '0px',
    threshold: 0.1
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('fade-in');
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

// Observa os elementos que devem ter animação
document.querySelectorAll('.profile-card, .service-card, .contact-form').forEach(element => {
    element.classList.add('fade-out');
    observer.observe(element);
});

// Função para exibir o modal de confirmação
function showConfirmationModal() {
    const modal = document.getElementById('confirmation-modal');
    modal.style.display = 'flex'; // Exibe o modal
}

// Função para fechar o modal
function closeConfirmationModal() {
    const modal = document.getElementById('confirmation-modal');
    modal.style.display = 'none'; // Oculta o modal
}

// Fechar o modal ao clicar no "X"
document.querySelector('.close-modal').addEventListener('click', closeConfirmationModal);

// Fechar o modal ao clicar fora dele
window.addEventListener('click', (event) => {
    const modal = document.getElementById('confirmation-modal');
    if (event.target === modal) {
        closeConfirmationModal();
    }
});

// Adicionar evento de envio do formulário
document.querySelector('form').addEventListener('submit', function (e) {
    e.preventDefault(); // Impede o envio padrão do formulário

    // Simula o envio do formulário (substitua pelo envio real via FormSubmit)
    setTimeout(() => {
        showConfirmationModal(); // Exibe o modal de confirmação
        this.reset(); // Limpa o formulário após o envio
    }, 1000); // Simula um atraso de 1 segundo para o envio
});

document.querySelector('form').addEventListener('submit', function (e) {
    const nome = document.getElementById('nome').value.trim();
    const email = document.getElementById('email').value.trim();
    const telefone = document.getElementById('telefone').value.trim();
    const mensagem = document.getElementById('mensagem').value.trim();

    if (!nome || !email || !telefone || !mensagem) {
        e.preventDefault();
        alert('Por favor, preencha todos os campos.');
    }
});

document.querySelectorAll('section').forEach(section => {
    section.classList.add('fade-out');
    observer.observe(section);
});