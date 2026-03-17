document.addEventListener('DOMContentLoaded', () => {
    const toggles = document.querySelectorAll('.tree-toggle');

    toggles.forEach((toggle) => {
        toggle.addEventListener('click', (event) => {
            if (event.target.closest('.editable')) {
                return;
            }

            toggle.classList.toggle('active');
            const nested = toggle.nextElementSibling;
            if (nested) {
                nested.style.display = nested.style.display === 'block' ? 'none' : 'block';
            }
        });
    });


    const form = document.getElementById('centroCustoForm');
    const inputId = document.getElementById('centro_id');
    const inputAcao = document.getElementById('acao');
    const inputConfirmarExclusaoFilhos = document.getElementById('confirmar_exclusao_filhos');
    const inputCod = document.getElementById('id_cod_centro');
    const inputDescricao = document.getElementById('id_descricao');
    const inputPai = document.getElementById('id_centro_pai');
    const submitBtn = document.getElementById('submitBtn');
    const btnExcluir = document.getElementById('btnExcluir');
    const btnCancelarEdicao = document.getElementById('btnCancelarEdicao');
    const formTitle = document.getElementById('formTitle');
    const formTip = document.getElementById('formTip');


    if (!form || !inputId || !submitBtn || !btnCancelarEdicao || !btnExcluir) {
        return;
    }

    const editable = Array.from(document.querySelectorAll('.editable'));

    const limparDestaque = () => {
        editable.forEach((item) => item.classList.remove('is-editing'));
    };

    const ativarModoCadastro = () => {
        form.reset();
        inputId.value = '';
        inputAcao.value = 'salvar';
        if (inputConfirmarExclusaoFilhos) {
            inputConfirmarExclusaoFilhos.value = '0';
        }
        submitBtn.textContent = 'Cadastrar';
        formTitle.textContent = 'Cadastrar Centro de Custo';
        formTip.textContent = 'Clique em um centro na árvore para editar.';
        btnCancelarEdicao.classList.add('hidden');
        btnExcluir.classList.add('hidden');
        limparDestaque();
    };

    editable.forEach((span) => {
        span.addEventListener('click', () => {
            inputId.value = span.dataset.id || '';
            inputCod.value = span.dataset.cod || '';
            inputDescricao.value = span.dataset.descricao || '';
            inputPai.value = span.dataset.pai || '';
            inputAcao.value = 'salvar';
            submitBtn.textContent = 'Atualizar';
            formTitle.textContent = 'Editar Centro de Custo';
            formTip.textContent = 'Você está editando um centro selecionado na árvore.';
            btnCancelarEdicao.classList.remove('hidden');
            btnExcluir.classList.remove('hidden');

            limparDestaque();
            span.classList.add('is-editing');
        });
    });

    form.addEventListener('submit', () => {
        if (inputAcao.value !== 'excluir') {
            inputAcao.value = 'salvar';
            if (inputConfirmarExclusaoFilhos) {
                inputConfirmarExclusaoFilhos.value = '0';
            }
        }
    });

    btnExcluir.addEventListener('click', (event) => {
        event.preventDefault();
        
        if (!inputId.value) {
            return;
        }

        const confirmou = window.confirm('Deseja realmente excluir este centro de custo?');
        if (!confirmou) {
            return;
        }

        const possuiFilhos = editable.some((item) => item.dataset.pai === inputId.value);
        if (possuiFilhos) {
            const confirmarTodos = window.confirm(
                'Este é um centro pai e possui centros filhos. Deseja excluir também todos os filhos?'
            );
            if (!confirmarTodos) {
                return;
            }

            if (inputConfirmarExclusaoFilhos) {
                inputConfirmarExclusaoFilhos.value = '1';
            }
        } else if (inputConfirmarExclusaoFilhos) {
            inputConfirmarExclusaoFilhos.value = '0';
        }

        inputAcao.value = 'excluir';
        form.submit();
    });

    btnCancelarEdicao.addEventListener('click', ativarModoCadastro);
});
