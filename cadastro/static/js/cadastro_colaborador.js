
// Modal
const modal = document.getElementById("statusModel");
const modalNome = document.getElementById("modalNome");
const modalAcao = document.getElementById("modalAcao");
const statusForm = document.getElementById("statusForm");
const confirmarAcaoBtn = document.getElementById("confirmarAcaoBtn");

document.querySelectorAll(".status-btn").forEach(btn => {
    btn.addEventListener("click", e => {
        e.preventDefault();

        const acao = btn.dataset.acao;

        modalNome.textContent = btn.dataset.nome;
        modalAcao.textContent = acao;
        statusForm.action = btn.dataset.url;
        confirmarAcaoBtn.textContent = acao.charAt(0).toUpperCase() + acao.slice(1);

        modal.style.display = "block";
    });
});

document.querySelectorAll(".close").forEach(btn => {
    btn.addEventListener("click", () => {
        modal.style.display = "none";
    });
});

window.addEventListener("click", e => {
    if (e.target === modal) {
        modal.style.display = "none";
    }
});


// Mostrar/ocultar horários personalizados dependendo do turno
const turnoSelect = document.getElementById('id_turno');
const horariosDiv = document.getElementById('horarios-personalizados');

function toggleHorarios() {
    if (turnoSelect.value === 'OUTROS') {
        horariosDiv.style.display = 'flex';
    } else {
        horariosDiv.style.display = 'none';
    }
}

turnoSelect.addEventListener('change', toggleHorarios);
toggleHorarios(); // inicializa no carregamento
