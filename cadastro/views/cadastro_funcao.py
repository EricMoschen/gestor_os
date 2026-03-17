from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from cadastro.models import Funcao_colab
from cadastro.selectors.colaborador_selector import listar_funcoes_com_colaboradores


def cadastro_funcao(request):
    mensagem_erro = None

    if request.method == "POST":
        descricao = request.POST.get("descricao")
        valor_hora = request.POST.get("valor_hora")
        funcao_id = request.POST.get("funcao_id")

        try:
            if funcao_id:  # EDITAR
                funcao = get_object_or_404(Funcao_colab, id=funcao_id)
                funcao.descricao = descricao
                funcao.valor_hora = valor_hora
                funcao.save()
            else:  # CRIAR
                Funcao_colab.objects.create(
                    descricao=descricao,
                    valor_hora=valor_hora
                )

            return redirect("cadastro_funcao")

        except Exception as e:
            mensagem_erro = f"Erro ao salvar função: {str(e)}"

    funcoes = listar_funcoes_com_colaboradores()

    return render(request, "cadastro_funcao/cadastro_funcao.html", {
        "funcoes": funcoes,
        "mensagem_erro": mensagem_erro
    })



def editar_funcao(request, id):
    funcao = get_object_or_404(Funcao_colab, id=id)

    if request.method == "POST":
        funcao.descricao = request.POST.get("descricao")
        funcao.valor_hora = request.POST.get("valor_hora")
        funcao.save()

        return redirect("cadastro_funcao")

    return render(request, "editar_funcao.html", {
        "funcao": funcao
    })



def excluir_funcao(request, id):
    funcao = get_object_or_404(Funcao_colab, id=id)

    if request.method == "POST":
        if funcao.Função_Colaborador.exists():
            messages.error(request, "Não é possível excluir uma função que já está em uso.")
            return redirect("cadastro_funcao")
        funcao.delete()
        messages.success(request, "Função removida com sucesso.")
        return redirect("cadastro_funcao")

    return redirect("cadastro_funcao")