
// Modal
const modal = document.getElementById("deleteModal");
const modalNome = document.getElementById("modalNome");
const deleteForm = document.getElementById("deleteForm");

document.querySelectorAll(".delete-btn").forEach(btn => {
    btn.addEventListener("click", e => {
        e.preventDefault();

        modalNome.textContent = btn.dataset.nome;
        deleteForm.action = btn.dataset.url;

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
