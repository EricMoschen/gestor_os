(function () {
    const filtroGeral = document.getElementById('filtro-geral');
    const filtroStatus = document.getElementById('filtro-status');
    const linhas = Array.from(document.querySelectorAll('#lista-apontamentos tr[data-id]'));

    const modalAjuste = document.getElementById('modal-ajuste');
    const campoId = document.getElementById('apontamento-id');
    const campoInicio = document.getElementById('data-inicio');
    const campoFim = document.getElementById('data-fim');
    const btnCancelarAjuste = document.getElementById('cancelar-modal');

    const modalNovo = document.getElementById('modal-novo-lancamento');
    const btnAbrirNovo = document.getElementById('abrir-modal-novo');
    const btnCancelarNovo = document.getElementById('cancelar-modal-novo');

    const formNovo = document.getElementById('form-novo-lancamento');
    const matriculaInput = document.getElementById('nova-matricula');
    const nomeInput = document.getElementById('novo-nome-colaborador');
    const numeroOsInput = document.getElementById('novo-numero-os');
    const descricaoInput = document.getElementById('nova-descricao-os');

    function aplicarFiltro() {
        const termo = filtroGeral?.value.toLowerCase() || '';
        const status = filtroStatus?.value || '';

        linhas.forEach((linha) => {

            const texto = [
                linha.dataset.matricula,
                linha.dataset.colaborador,
                linha.dataset.os,
                linha.dataset.status,
            ].join(' ');

            const okTermo = !termo || texto.includes(termo);
            const okStatus = !status || linha.dataset.status === status;

            linha.style.display = okTermo && okStatus ? '' : 'none';

        });

    }

    function abrirModalAjuste(linha) {
        if (!linha || !modalAjuste) return;

        campoId.value = linha.dataset.id;
        campoInicio.value = linha.dataset.inicio || '';
        campoFim.value = linha.dataset.fim || '';

        modalAjuste.classList.add('active');
    }

    function fecharModalAjuste(){
        modalAjuste?.classList.remove('active');
    }

    function abrirModalNovo(){
        modalNovo?.classList.add('active');
    }

    function fecharModalNovo() {
        modalNovo?.classList.remove('active');
    }

    async function buscaColaborador() {
        const matricula = matriculaInput?.value.trim().toUpperCase();
        const baseUrl = formNovo?.dataset.colaboradorUrlBase;

        if (!matricula || !baseUrl || !nomeInput) {
            if (nomeInput) nomeInput.value = '';
            return;
        }

        nomeInput.value = 'Buscando...';

        try {
            const url = baseUrl.replace('__MATRICULA__', encodeURIComponent(matricula));
            const resp = await fetch(url);

            if (!resp.ok) throw new Error('Colaborador não encontrado');

            const data = await resp.json();

            nomeInput.value = data.nome || 'Colaborador não encontrado';
        } catch { 
            nomeInput.value = 'Erro ao buscar colaborador';
        }
    }

    async function buscarOS() {

        const numero = numeroOsInput?.value.trim().toUpperCase();
        const baseUrl = formNovo?.dataset.osUrlBase;

        if (!numero || !baseUrl || !descricaoInput) {
            if (descricaoInput) descricaoInput.value = '';
            return;
        }

        descricaoInput.value = 'Buscando...';

        try {
            const url = baseUrl.replace('__OS__', encodeURIComponent(numero));
            const resp = await fetch(url);

            if (!resp.ok) throw new Error('OS não encontrada');

            const data = await resp.json();
            descricaoInput.value = data.descricao || 'OS não encotrada';
        } catch {
            descricaoInput.value = 'Erro ao buscar OS'
        }
    }
 
    filtroGeral?.addEventListener('input', aplicarFiltro);
    filtroStatus?.addEventListener('change', aplicarFiltro);

    document.querySelectorAll('[data-open-modal]').forEach((btn) => {
        btn.addEventListener('click', () => abrirModalAjuste(btn.closest('tr')));
    });

    btnCancelarAjuste?.addEventListener('click', fecharModalAjuste);
    btnAbrirNovo?.addEventListener('click', abrirModalNovo);
    btnCancelarNovo?.addEventListener('click', fecharModalNovo);

    matriculaInput?.addEventListener('blur', buscaColaborador);
    numeroOsInput?.addEventListener('blur', buscarOS);

    modalAjuste?.addEventListener('click', (e) => {
        if  (e.target === modalAjuste) fecharModalAjuste();
        });

    modalNovo?.addEventListener('click', (e) => {
        if (e.target === modalNovo) fecharModalNovo();
    });

})();
