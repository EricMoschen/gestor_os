from src.cadastro.models import Cliente
from src.cadastro.validators.cliente_validator import validar_codigo_unico


def salvar_cliente(*, cliente_id=None, codigo, nome):

    validar_codigo_unico(codigo, cliente_id)

    if cliente_id:
        cliente = Cliente.objects.get(pk=cliente_id)
        cliente.codigo = codigo
        cliente.nome = nome
        cliente.save()
        return cliente

    return Cliente.objects.create(
        codigo=codigo,
        nome=nome
    )


def remover_cliente(cliente):
    cliente.delete()
