// Mostrar/ocultar horários personalizados dependendo do turno
const turnoSelect = document.getElementById('id_turno');
const horariosDiv = document.getElementById('horarios-personalizados');

if (turnoSelect && horariosDiv) {
    function toggleHorarios() {
        if (turnoSelect.value === 'OUTROS') {
            horariosDiv.style.display = 'flex';
        } else {
            horariosDiv.style.display = 'none';
        }
        turnoSelect.addEventListener('change', toggleHorarios);
        toggleHorarios(); // inicializa no carregamento
    }
}
