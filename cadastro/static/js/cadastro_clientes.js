document.addEventListener("DOMContentLoaded", () => {
    ClientePage.init();
});

const ClientePage = (() => {

    // ==========================
    // ELEMENTOS
    // ==========================

    const elements = {
        modal: document.getElementById("deleteModal"),
        modalNome: document.getElementById("modalNome"),
        deleteForm: document.getElementById("deleteForm"),
        closeBtn: document.querySelector(".close"),
        cancelModalBtn: document.querySelector(".cancel-modal"),
        deleteButtons: document.querySelectorAll(".delete-btn"),

        editButtons: document.querySelectorAll(".edit-btn"),
        idField: document.getElementById("cliente_id"),
        codField: document.getElementById("id_codigo"),
        nomeField: document.getElementById("id_nome"),
        submitBtn: document.getElementById("submitBtn"),
        btnCancelar: document.getElementById("btnCancelar"),

        mensagemErro: document.querySelector(".erro-msg")
    };


    // ==========================
    // MODAL
    // ==========================

    function initModal() {
        if (!elements.modal) return;

        elements.deleteButtons.forEach(btn => {
            btn.addEventListener("click", e => {
                e.preventDefault();

                const { id, nome } = btn.dataset;

                elements.modalNome.textContent = nome;
                elements.deleteForm.action = `/cadastro/cliente/excluir/${id}/`;

                elements.modal.style.display = "block";
            });
        });

        if (elements.closeBtn) {
            elements.closeBtn.onclick = closeModal;
        }

        if (elements.cancelModalBtn) {
            elements.cancelModalBtn.onclick = closeModal;
        }

        window.addEventListener("click", e => {
            if (e.target === elements.modal) closeModal();
        });
    }

    function closeModal() {
        elements.modal.style.display = "none";
    }


    // ==========================
    // EDITAR CLIENTE
    // ==========================

    function initEdit() {
        elements.editButtons.forEach(btn => {
            btn.addEventListener("click", e => {
                e.preventDefault();

                const { id, codigo, nome } = btn.dataset;

                elements.idField.value = id;
                elements.codField.value = codigo;
                elements.nomeField.value = nome;

                elements.submitBtn.textContent = "Salvar Alterações";
                elements.btnCancelar.style.display = "flex";

                elements.nomeField.focus();
            });
        });
    }


    // ==========================
    // RESET FORM
    // ==========================

    function initFormReset() {
        if (!elements.btnCancelar) return;

        elements.btnCancelar.addEventListener("click", () => {
            resetForm();
        });

        if (!elements.idField.value) {
            elements.btnCancelar.style.display = "none";
        }
    }

    function resetForm() {
        elements.idField.value = "";
        elements.codField.value = "";
        elements.nomeField.value = "";

        elements.submitBtn.textContent = "Salvar";
        elements.btnCancelar.style.display = "none";

        if (elements.mensagemErro) {
            elements.mensagemErro.style.display = "none";
            elements.mensagemErro.textContent = "";
        }
    }


    // ==========================
    // MENSAGEM DE ERRO
    // ==========================

    function initErrorMessage() {
        if (!elements.mensagemErro) return;

        const hasMessage = elements.mensagemErro.textContent.trim() !== "";

        if (!hasMessage) {
            elements.mensagemErro.style.display = "none";
            return;
        }

        elements.mensagemErro.style.display = "block";

        setTimeout(() => {
            elements.mensagemErro.style.display = "none";
        }, 8000);
    }


    // ==========================
    // INIT GERAL
    // ==========================

    function init() {
        initModal();
        initEdit();
        initFormReset();
        initErrorMessage();
    }

    return { init };

})();
