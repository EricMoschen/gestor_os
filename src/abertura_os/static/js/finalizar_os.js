
document.addEventListener("DOMContentLoaded", () => {
    const numeroInput = document.getElementById("numero_os");
    const descricaoInput = document.getElementById("descricao_os");
    const situacaoInput = document.getElementById("situacao_os");
    const hiddenInput = document.getElementById("numero_os_hidden");
    const form = document.getElementById("finalizarForm");
    const msgStatus = document.getElementById("statusOS");
    const totalAbertas = document.getElementById("totalAbertas");
    const totalFinalizadas = document.getElementById("totalFinalizadas");

    const addPieceBtn = document.getElementById("addPieceBtn");
    const pecasContainer = document.getElementById("pecasContainer");
    const pecaEmptyTemplate = document.getElementById("pecaEmptyFormTemplate");
    const totalFormsInput = document.querySelector("#id_pecas-TOTAL_FORMS");

    const cacheOS = {};
    const cacheItems = document.querySelectorAll(".ordem-cache-item");

    function mostrarMensagem(texto, tipo = "info") {
        if (!msgStatus) return;

        msgStatus.textContent = texto;
        msgStatus.className = `status-message ${tipo}`;
        msgStatus.classList.toggle("hidden", !texto);
    }

    function limparCamposOS() {
        descricaoInput.value = "";
        situacaoInput.value = "";
        hiddenInput.value = "";
    }

    function atualizarResumo() {
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

    function carregarOS(numeroDigitado) {
        const numero = numeroDigitado.trim().toUpperCase();

        if (!numero) {
            limparCamposOS();
            mostrarMensagem("");
            return;
        }

        const os = cacheOS[numero];

        if (!os) {
            limparCamposOS();
            mostrarMensagem(`OS ${numero} não encontrada.`, "erro");
            return;
        }

        descricaoInput.value = os.descricao || "";
        situacaoInput.value = os.situacao || "";
        hiddenInput.value = numero;

        if (os.situacaoCodigo === "FI") {
            mostrarMensagem("Atenção: esta OS já está finalizada.", "aviso");
            return;
        }

        mostrarMensagem("OS carregada com sucesso. Continue o preenchimento.", "sucesso");
    }

    function marcarParaExcluir(item) {
        const deleteCheckbox = item.querySelector('input[type="checkbox"][name$="-DELETE"]');

        if (deleteCheckbox) {
            deleteCheckbox.checked = true;
            item.style.display = "none";
            return;
        }

        item.remove();
    }

    function vincularEventoRemover(botao) {
        botao.addEventListener("click", () => {
            const item = botao.closest(".peca-item");
            if (item) {
                marcarParaExcluir(item);
            }
        });
    }

    cacheItems.forEach((item) => {
        const numero = (item.dataset.numero || "").toUpperCase();

        cacheOS[numero] = {
            descricao: item.dataset.descricao || "",
            situacao: item.dataset.situacao || "",
            situacaoCodigo: item.dataset.situacaoCodigo || ""
        };
    });

    document.querySelectorAll(".remove-piece-btn").forEach(vincularEventoRemover);

    addPieceBtn?.addEventListener("click", () => {
        if (!pecaEmptyTemplate || !pecasContainer || !totalFormsInput) return;

        const index = Number(totalFormsInput.value);
        const html = pecaEmptyTemplate.innerHTML.replaceAll("__prefix__", String(index));
        pecasContainer.insertAdjacentHTML("beforeend", html);

        totalFormsInput.value = String(index + 1);

        const novoItem = pecasContainer.lastElementChild;
        const removeBtn = novoItem?.querySelector(".remove-piece-btn");
        if (removeBtn) {
            vincularEventoRemover(removeBtn);
        }
    });

    numeroInput?.addEventListener("input", () => {
        numeroInput.value = numeroInput.value.toUpperCase();
        carregarOS(numeroInput.value);
    });

    form?.addEventListener("submit", (event) => {
        const numero = (numeroInput?.value || "").trim().toUpperCase();

        if (!numero) {
            event.preventDefault();
            mostrarMensagem("Informe o número da OS para continuar.", "erro");
            numeroInput?.focus();
            return;
        }

        if (!cacheOS[numero]) {
            event.preventDefault();
            mostrarMensagem("Informe um número de OS válido.", "erro");
            numeroInput?.focus();
            return;
        }

        if (cacheOS[numero].situacaoCodigo === "FI") {
            event.preventDefault();
            mostrarMensagem("Não é possível finalizar uma OS que já está finalizada.", "erro");
            return;
        }

        hiddenInput.value = numero;
    });

    atualizarResumo();
});