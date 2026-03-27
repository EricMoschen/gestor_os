document.addEventListener("DOMContentLoaded", () => {
    const numeroInput = document.getElementById("numero_os");
    const descricaoInput = document.getElementById("descricao_os");
    const situacaoInput = document.getElementById("situacao_os");
    const hiddenInput = document.getElementById("numero_os_hidden");
    const observacoesInput = document.getElementById("observacoes");
    const contadorObservacoes = document.getElementById("contadorObservacoes");
    const erroObs = document.getElementById("erroObservacoes");
    const form = document.getElementById("finalizarForm");
    const buscarTabela = document.getElementById("buscarTabela");
    const msgStatus = document.getElementById("statusOS");
    const totalAbertas = document.getElementById("totalAbertas");
    const totalFinalizadas = document.getElementById("totalFinalizadas");

    const cacheOS = {};
    const linhas = document.querySelectorAll(".linha-os");

    function limparSelecaoTabela() {
        document.querySelectorAll(".linha-os.is-selected").forEach((row) => {
            row.classList.remove("is-selected");
        });
    }

    function selecionarLinha(numero) {
        limparSelecaoTabela();

        const linhaSelecionada = document.querySelector(`.linha-os[data-numero="${CSS.escape(numero)}"]`);

        if (linhaSelecionada) {
            linhaSelecionada.classList.add("is-selected");
            linhaSelecionada.scrollIntoView({ behavior: "smooth", block: "nearest" });
        }
    }

    function limparCampos() {
        descricaoInput.value = "";
        situacaoInput.value = "";
        observacoesInput.value = "";
        hiddenInput.value = "";
        limparSelecaoTabela();
        atualizarContadorObservacoes();
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
        atualizarContadorObservacoes();
        selecionarLinha(numero);
    }

    function atualizarContadoresResumo() {
        let abertas = 0;
        let finalizadas = 0;

        Object.values(cacheOS).forEach((os) => {
            if (os.situacaoCodigo === "FI") {
                finalizadas += 1;
            } else {
                abertas += 1;
            }
        });

        if (totalAbertas) totalAbertas.textContent = abertas;
        if (totalFinalizadas) totalFinalizadas.textContent = finalizadas;
    }

    function atualizarContadorObservacoes() {
        if (!contadorObservacoes || !observacoesInput) return;

        const quantidade = observacoesInput.value.trim().length;
        contadorObservacoes.textContent = `${quantidade} caractere${quantidade === 1 ? "" : "s"}`;
    }

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

        mostrarMensagem("OS carregada. Revise os dados e finalize quando estiver pronto.", "sucesso");
    }

    linhas.forEach((row) => {
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

    atualizarContadoresResumo();
    atualizarContadorObservacoes();

    numeroInput.addEventListener("input", () => {
        const numero = numeroInput.value.trim();
        carregarDaTabela(numero);
    });

    observacoesInput.addEventListener("input", () => {
        atualizarContadorObservacoes();

        if (observacoesInput.value.trim()) {
            erroObs.style.display = "none";
        }
    });

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

    buscarTabela.addEventListener("input", function () {
        const filtro = this.value.toLowerCase();
        let linhasVisiveis = 0;

        document.querySelectorAll("#tabelaOs tbody tr").forEach((linha) => {
            const texto = linha.innerText.toLowerCase();
            const visivel = texto.includes(filtro);

            linha.style.display = visivel ? "" : "none";

            if (visivel) {
                linhasVisiveis += 1;
            }
        });

        if (filtro && linhasVisiveis === 0) {
            mostrarMensagem("Nenhuma OS corresponde ao filtro informado.", "aviso");
            return;
        }

        if (filtro && linhasVisiveis > 0) {
            mostrarMensagem(`${linhasVisiveis} OS encontradas com o filtro aplicado.`, "info");
            return;
        }

        mostrarMensagem("");
    });
});



