document.addEventListener("DOMContentLoaded", () => {

    // =============================
    // Referências de elementos
    // =============================
    const numeroInput = document.getElementById("numero_os");
    const descricaoInput = document.getElementById("descricao_os");
    const situacaoInput = document.getElementById("situacao_os");
    const hiddenInput = document.getElementById("numero_os_hidden");
    const observacoesInput = document.getElementById("observacoes");
    const erroObs = document.getElementById("erroObservacoes");
    const form = document.getElementById("finalizarForm");
    const buscarTabela = document.getElementById("buscarTabela");
    const msgStatus = document.getElementById("statusOS");

    const cacheOS = {};

    // =============================
    // Funções utilitárias
    // =============================

    function limparCampos() {
        descricaoInput.value = "";
        situacaoInput.value = "";
        observacoesInput.value = "";
        hiddenInput.value = "";
    }

    function mostrarMensagem(texto, tipo = "info") {
        if (!msgStatus) return;

        msgStatus.textContent = texto;
        msgStatus.className = `status-message ${tipo}`;

        if (texto) {
            msgStatus.classList.remove("hidden");
        } else {
            msgStatus.classList.add("hidden");
        }
    }

    function preencherCampos(data, numero) {
        descricaoInput.value = data.descricao || "";
        situacaoInput.value = data.situacao || "";
        observacoesInput.value = data.observacoes || "";
        hiddenInput.value = numero;
    }

    // =============================
    // Carregar OS da tabela
    // =============================

    function carregarDaTabela(numero) {

        if (!numero) {
            limparCampos();
            mostrarMensagem("");
            return;
        }

        const os = cacheOS[numero];

        if (!os) {
            limparCampos();
            mostrarMensagem(`OS ${numero} não encontrada na lista de ordens`, "erro");
            return;
        }

        preencherCampos(os, numero);

        if (os.situacaoCodigo === "FI") {
            mostrarMensagem("Atenção: esta OS já está finalizada.", "aviso");
            return;
        }

        mostrarMensagem("");
    }

    // =============================
    // Carregar dados da tabela
    // =============================

    document.querySelectorAll(".linha-os").forEach((row) => {

        const numero = row.dataset.numero;

        cacheOS[numero] = {
            descricao: row.dataset.descricao || "",
            situacao: row.dataset.situacao || "",
            situacaoCodigo: row.dataset.situacaoCodigo || "",
            observacoes: row.dataset.observacoes || ""
        };

        row.addEventListener("click", () => {
            numeroInput.value = numero;
            carregarDaTabela(numero);
        });

    });

    // =============================
    // Buscar OS digitando número
    // =============================

    numeroInput.addEventListener("input", () => {
        const numero = numeroInput.value.trim();
        carregarDaTabela(numero);
    });

    // =============================
    // Validação do formulário
    // =============================

    form.addEventListener("submit", (e) => {

        const numero = numeroInput.value.trim();
        const observacoes = observacoesInput.value.trim();

        if (!numero) {
            e.preventDefault();
            mostrarMensagem("Informe o número da OS para finalizar.", "erro");
            numeroInput.focus();
            return;
        }

        if (!cacheOS[numero]) {
            e.preventDefault();
            mostrarMensagem("Selecione uma OS válida na tabela para finalizar.", "erro");
            numeroInput.focus();
            return;
        }

        if (cacheOS[numero].situacaoCodigo === "FI") {
            e.preventDefault();
            mostrarMensagem("Não é possível finalizar uma OS que já está finalizada.", "erro");
            return;
        }

        if (!observacoes) {
            e.preventDefault();
            erroObs.style.display = "block";
            mostrarMensagem("Preencha o campo de observações para continuar.", "erro");
            observacoesInput.focus();
            return;
        }

        erroObs.style.display = "none";
        hiddenInput.value = numero;

    });

    // =============================
    // Busca na tabela
    // =============================

    buscarTabela.addEventListener("input", function () {

        const filtro = this.value.toLowerCase();

        document.querySelectorAll("#tabelaOs tbody tr").forEach((linha) => {

            const texto = linha.innerText.toLowerCase();

            if (texto.includes(filtro)) {
                linha.style.display = "";
            } else {
                linha.style.display = "none";
            }

        });

    });

});