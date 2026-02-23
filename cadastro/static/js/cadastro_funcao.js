document.addEventListener("DOMContentLoaded", function () {

    const form = document.getElementById("funcaoForm");
    const inputId = document.getElementById("funcao_id");
    const inputDescricao = document.getElementById("id_descricao");
    const inputValor = document.getElementById("id_valor_hora");
    const submitBtn = document.getElementById("submitBtn");
    const btnCancelar = document.getElementById("btnCancelar");

    const deleteModal = document.getElementById("deleteModal");
    const deleteForm = document.getElementById("deleteForm");
    const modalNome = document.getElementById("modalNome");
    const closeModalBtn = document.querySelector(".close");

    /* =========================
       EDITAR
    ==========================*/
    document.querySelectorAll(".edit-btn").forEach(button => {
        button.addEventListener("click", function (e) {
            e.preventDefault();

            const id = this.dataset.id;
            const descricao = this.dataset.descricao;
            const valor = this.dataset.valor;
            const valorFormatado = valor.replace(",", ".");


            inputId.value = id;
            inputDescricao.value = descricao;
            inputValor.value = valorFormatado;

            submitBtn.textContent = "Atualizar";
        });
    });

    /* =========================
       CANCELAR EDIÇÃO
    ==========================*/
    btnCancelar.addEventListener("click", function () {
        form.reset();
        inputId.value = "";
        submitBtn.textContent = "Salvar";
    });

    /* =========================
       EXCLUIR
    ==========================*/
    document.querySelectorAll(".delete-btn").forEach(button => {
        button.addEventListener("click", function (e) {
            e.preventDefault();

            const id = this.dataset.id;
            const descricao = this.dataset.descricao;

            modalNome.textContent = descricao;
            deleteForm.action = this.dataset.url;

            deleteModal.style.display = "block";
        });
    });

    /* =========================
       FECHAR MODAL
    ==========================*/
    closeModalBtn.addEventListener("click", function () {
        deleteModal.style.display = "none";
    });

    window.addEventListener("click", function (e) {
        if (e.target === deleteModal) {
            deleteModal.style.display = "none";
        }
    });

});