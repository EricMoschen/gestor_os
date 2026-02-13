(function () {

    const filtroGeral = document.getElementById('filtro-geral');
    const filtroStatus = document.getElementById('filtro-status');
    const linhas = Array.from(document.querySelectorAll('#lista-apontamentos tr[data-id]'));

    const modal = document.getElementById('modal-ajuste');
    const campoId = document.getElementById('apontamento-id');
    const campoInicio = document.getElementById('data-inicio');
    const campoFim = document.getElementById('data-fim');
    const btnCancelar = document.getElementById('cancelar-modal');

    function aplicarFiltro() {

        const termo = filtroGeral.value.toLowerCase();
        const status = filtroStatus.value;

        linhas.forEach(linha => {

            const texto = [
                linha.dataset.matricula,
                linha.dataset.colaborador,
                linha.dataset.os,
                linha.dataset.status
            ].join(' ');

            const okTermo = !termo || texto.includes(termo);
            const okStatus = !status || linha.dataset.status === status;

            linha.style.display = okTermo && okStatus ? '' : 'none';

        });

    }

    function abrirModal(linha) {

        campoId.value = linha.dataset.id;
        campoInicio.value = linha.dataset.inicio || '';
        campoFim.value = linha.dataset.fim || '';

        modal.classList.add('active');
    }

    function fecharModal() {
        modal.classList.remove('active');
    }

    filtroGeral?.addEventListener('input', aplicarFiltro);
    filtroStatus?.addEventListener('change', aplicarFiltro);

    document.querySelectorAll('[data-open-modal]').forEach(btn => {
        btn.addEventListener('click', () => abrirModal(btn.closest('tr')));
    });

    btnCancelar?.addEventListener('click', fecharModal);

    modal?.addEventListener('click', e => {
        if (e.target === modal) fecharModal();
    });

})();
