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

    // Elementos para mensagens e spinner
    const msgStatus = document.getElementById("statusOS"); // div para mensagens
    const spinner = document.getElementById("spinnerOS"); // div com spinner CSS

    // =============================
    // Estado
    // =============================
    let ultimoNumeroBuscado = null;
    let controller = null;
    let debounceTimer;
    const cacheOS = {}; // cache de OS já buscadas

    // =============================
    // Funções utilitárias
    // =============================
    function limparCampos() {
        descricaoInput.value = "";
        situacaoInput.value = "";
        observacoesInput.value = "";
        hiddenInput.value = "";
    }

    function preencherCampos(data, numero) {
        descricaoInput.value = data.descricao ?? "";
        situacaoInput.value = data.situacao ?? "";
        observacoesInput.value = data.observacoes ?? "";
        hiddenInput.value = numero;
    }

    function mostrarMensagem(texto, tipo = "info") {
        if (!msgStatus) return;
        msgStatus.textContent = texto;
        msgStatus.className = tipo; // tipo pode ser: info, erro, sucesso
        msgStatus.style.display = texto ? "block" : "none";
    }

    function mostrarSpinner(ativar = true) {
        if (!spinner) return;
        spinner.style.display = ativar ? "inline-block" : "none";
    }

    // =============================
    // Buscar OS via fetch
    // =============================
    async function buscarOS(numero) {
        numero = numero.trim();

        if (!numero) {
            limparCampos();
            mostrarMensagem("");
            return;
        }

        // evita requisição duplicada
        if (numero === ultimoNumeroBuscado && cacheOS[numero]) {
            preencherCampos(cacheOS[numero], numero);
            mostrarMensagem("");
            return;
        }

        ultimoNumeroBuscado = numero;

        // cancela requisição anterior
        if (controller) controller.abort();
        controller = new AbortController();

        mostrarSpinner(true);
        mostrarMensagem("");

        try {
            const url = `/relatorio/buscar-os/${encodeURIComponent(numero)}/`;
            const response = await fetch(url, { signal: controller.signal });

            if (!response.ok) {
                limparCampos();
                mostrarMensagem("Erro ao conectar com o servidor.", "erro");
                mostrarSpinner(false);
                return;
            }

            const data = await response.json();

            if (data.erro) {
                limparCampos();
                mostrarMensagem(`OS ${numero} não encontrada.`, "erro");
                mostrarSpinner(false);
                return;
            }

            // salva no cache e preenche campos
            cacheOS[numero] = data;
            preencherCampos(data, numero);

            mostrarMensagem("OS carregada com sucesso.", "sucesso");

        } catch (err) {
            if (err.name === "AbortError") return; // cancelamento normal
            console.error("Erro ao buscar OS:", err);
            limparCampos();
            mostrarMensagem("Erro de rede. Tente novamente.", "erro");
        } finally {
            mostrarSpinner(false);
        }
    }

    // =============================
    // Auto buscar ao digitar (debounce)
    // =============================
    numeroInput.addEventListener("input", () => {
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(() => buscarOS(numeroInput.value), 400);
    });

    // =============================
    // Preencher ao clicar na tabela
    // =============================
    document.querySelectorAll(".linha-os").forEach(row => {
        row.addEventListener("click", function () {
            const numero = this.dataset.numero;
            const data = {
                descricao: this.dataset.descricao,
                situacao: this.dataset.situacao,
                observacoes: this.dataset.observacoes ?? ""
            };

            numeroInput.value = numero;
            preencherCampos(data, numero);

            // salva no cache para não buscar novamente
            cacheOS[numero] = data;
            mostrarMensagem("OS carregada da tabela.", "sucesso");
        });
    });

    // =============================
    // Validação de Observações no submit
    // =============================
    form.addEventListener("submit", (e) => {
        if (observacoesInput.value.trim() === "") {
            e.preventDefault();
            erroObs.style.display = "block";
            observacoesInput.focus();
        } else {
            erroObs.style.display = "none";
        }
    });

    // =============================
    // Filtro da tabela
    // =============================
    buscarTabela.addEventListener("input", function () {
        const filtro = this.value.toLowerCase();
        document.querySelectorAll("#tabelaOs tbody tr").forEach(linha => {
            const texto = linha.innerText.toLowerCase();
            linha.style.display = texto.includes(filtro) ? "" : "none";
        });
    });

});