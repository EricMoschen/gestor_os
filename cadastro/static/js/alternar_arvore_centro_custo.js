document.addEventListener('DOMContentLoaded', function() {
    const toggles = document.querySelectorAll('.tree-toggle');

    toggles.forEach(toggle => {
        toggle.addEventListener('click', () => {
            toggle.classList.toggle('active');
            const nested = toggle.nextElementSibling;
            if (nested) {
                nested.style.display = nested.style.display === 'block' ? 'none' : 'block';
            }
        });
    });
});



document.addEventListener("DOMContentLoaded", function () {

    const form = document.querySelector("form");
    const inputId = document.getElementById("centro_id");
    const inputCod = document.getElementById("id_cod_centro");
    const inputDescricao = document.getElementById("id_descricao");
    const inputPai = document.getElementById("id_centro_pai");
    const submitBtn = document.getElementById("submitBtn");
    const btnCancelar = document.getElementById("btnCancelar");

    document.querySelectorAll(".editable").forEach(span => {
        span.addEventListener("click", function () {
            const id = this.dataset.id;
            const cod = this.dataset.cod;
            const descricao = this.dataset.descricao;

            inputId.value = id;
            inputCod.value = cod;
            inputDescricao.value = descricao;

            submitBtn.textContent = "Atualizar";
        });
    });

    btnCancelar.addEventListener("click", function () {
        form.reset();
        inputId.value = "";
        submitBtn.textContent = "Cadastrar";
    });

});