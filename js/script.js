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

// Função para criar e exibir o modal de confirmação
function showConfirmationModal() {
    const modal = document.createElement('div');
    modal.id = 'confirmation-modal';
    modal.className = 'modal';
    modal.innerHTML = `
        <div class="modal-content">
            <span class="close-modal">&times;</span>
            <h3>Mensagem Enviada!</h3>
            <p>Obrigado pelo seu contato. Entraremos em contato assim que possível.</p>
        </div>
    `;
    document.body.appendChild(modal);

    // Exibe o modal
    modal.style.display = 'flex';

    // Fechar o modal ao clicar no "X"
    modal.querySelector('.close-modal').addEventListener('click', () => {
        modal.style.display = 'none';
        document.body.removeChild(modal);
    });

    // Fechar o modal ao clicar fora dele
    window.addEventListener('click', (event) => {
        if (event.target === modal) {
            modal.style.display = 'none';
            document.body.removeChild(modal);
        }
    });
}

// Envio do formulário via AJAX
document.querySelector('form').addEventListener('submit', function (e) {
    e.preventDefault(); // Impede o envio padrão do formulário

    const formData = new FormData(this);

    fetch(this.action, {
        method: 'POST',
        body: formData,
        headers: {
            'Accept': 'application/json'
        }
    })
    .then(response => {
        if (response.ok) {
            showConfirmationModal(); // Exibe o modal de confirmação
            this.reset(); // Limpa o formulário após o envio
        } else {
            alert('Ocorreu um erro ao enviar a mensagem. Por favor, tente novamente.');
        }
    })
    .catch(error => {
        alert('Ocorreu um erro ao enviar a mensagem. Por favor, tente novamente.');
    });
});