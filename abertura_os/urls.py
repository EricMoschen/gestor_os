from django.urls import path
from config.access_control import ROLE_ADM, ROLE_ALMOXARIFE, ROLE_PCM, role_required
from . import views

urlpatterns = [
    path("abertura_os/",role_required([ROLE_ADM, ROLE_PCM, ROLE_ALMOXARIFE]) (views.abrir_os), name="abrir_os"),
    path('imprimir_os/<int:pk>/', role_required([ROLE_ADM, ROLE_PCM, ROLE_ALMOXARIFE]) (views.imprimir_os), name='imprimir_os'),
    path("editar/<int:pk>/", role_required([ROLE_ADM, ROLE_PCM, ROLE_ALMOXARIFE]) (views.editar_os), name="editar_os"),
    path("excluir/<int:pk>/",role_required([ROLE_ADM, ROLE_PCM, ROLE_ALMOXARIFE]) (views.excluir_os), name="excluir_os"),
    path("ajax/subcentros/",role_required([ROLE_ADM, ROLE_PCM, ROLE_ALMOXARIFE]) (views.get_subcentros_ajax), name="get_subcentros"),
    path("finalizar_os/",role_required([ROLE_ADM, ROLE_PCM, ROLE_ALMOXARIFE]) (views.finalizar_os_view), name="finalizar_os"),
    
]

