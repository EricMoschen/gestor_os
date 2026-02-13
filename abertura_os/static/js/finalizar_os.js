document.addEventListener("DOMContentLoaded", () => {

    const numeroInput = document.getElementById("numero_os");
    const descricaoInput = document.getElementById("descricao_os");
    const situacaoInput = document.getElementById("situacao_os");
    const hiddenInput = document.getElementById("numero_os_hidden");
    const observacoesInput = document.getElementById("observacoes");
    const erroObs = document.getElementById("erroObservacoes");
    const form = document.getElementById("finalizarForm");

    // =============================
    // Buscar OS via fetch
    // =============================
    function buscarOS(numero) {
        if (!numero) {
            descricaoInput.value = "";
            situacaoInput.value = "";
            observacoesInput.value = "";
            hiddenInput.value = "";
            return;
        }

        fetch(`/relatorio/buscar-os/${numero}/`)
            .then(res => res.json())
            .then(data => {
                if (data.erro) {
                    descricaoInput.value = "";
                    situacaoInput.value = "";
                    observacoesInput.value = "";
                    hiddenInput.value = "";
                    return;
                }
                descricaoInput.value = data.descricao || "";
                situacaoInput.value = data.situacao || "";
                observacoesInput.value = data.observacoes || "";
                hiddenInput.value = numero;
            })
            .catch(() => {
                descricaoInput.value = "";
                situacaoInput.value = "";
                observacoesInput.value = "";
                hiddenInput.value = "";
            });
    }

    // =============================
    // Auto buscar ao digitar
    // =============================
    numeroInput.addEventListener("keyup", () => buscarOS(numeroInput.value.trim()));
    numeroInput.addEventListener("change", () => buscarOS(numeroInput.value.trim()));
    numeroInput.addEventListener("blur", () => buscarOS(numeroInput.value.trim()));

    // =============================
    // Preencher ao clicar na tabela
    // =============================
    document.querySelectorAll(".linha-os").forEach(row => {
        row.addEventListener("click", function () {
            let numero = this.dataset.numero;
            numeroInput.value = numero;
            descricaoInput.value = this.dataset.descricao;
            situacaoInput.value = this.dataset.situacao;
            buscarOS(numero)
            hiddenInput.value = numero;
        });
    });

    // =============================
    // Validação de Observações
    // =============================
    form.addEventListener("submit", function (e) {
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
    const buscarTabela = document.getElementById("buscarTabela");
    buscarTabela.addEventListener("keyup", function () {
        let filtro = this.value.toLowerCase();
        document.querySelectorAll("#tabelaOs tbody tr").forEach(linha => {
            let texto = linha.innerText.toLowerCase();
            linha.style.display = texto.includes(filtro) ? "" : "none";
        });
    });

});