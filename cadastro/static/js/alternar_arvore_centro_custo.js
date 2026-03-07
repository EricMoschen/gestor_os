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


    const form = document.querySelector("form");
    const inputId = document.getElementById("centro_id");
    const inputCod = document.getElementById("id_cod_centro");
    const inputDescricao = document.getElementById("id_descricao");
    const inputPai = document.getElementById("id_centro_pai");
    const submitBtn = document.getElementById("submitBtn");
    const btnCancelarEdicao = document.getElementById('btnCancelarEdicao');
    const formTitel = document.getElementById('formTitle');
    const formTip = document.getElementById('formTip');


    if (!form || !inputId || !submitBtn || !btnCancelarEdicao) {
        return;
    }

    const editable = Array.from(document.querySelectorAll('.editable'));

    const limparDestaque = () => {
        editable.forEach((item) => item.classList.remove('is-editing'));
    };

    const ativarModoCadastro = () => {
        form.reset();
        inputId.value = '';
        submitBtn.textContent = 'Cadastrar';
        formTitel.textContent = 'Cadastrar Centro de Custo';
        formTip.textContent = 'Clique em um centro na árvore para editar.';
        btnCancelarEdicao.classList.add('hidden');
        limparDestaque();
    };

    editable.forEach((span) => {
        span.addEventListener('click', () => {
            inputId.value = span.dataset.id || '';
            inputCod.value = span.dataset.cod || '';
            inputDescricao.value = span.dataset.descricao || '';

            if (span.dataset.pai) {
                inputPai.value = span.dataset.pai;
            } else {
                inputPai.value = '';
            }

            submitBtn.textContent = 'Atualizar';
            formTitel.textContent = 'Editar Centro de Custo';
            formTip.textContent = 'Você está editando um centro selecionado na árvore.';
            btnCancelarEdicao.classList.remove('hidden');

            limparDestaque();
            span.classList.add('is-editing');
        });
    });
    btnCancelarEdicao.addEventListener('click', ativarModoCadastro);

});


