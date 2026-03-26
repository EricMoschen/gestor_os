# 📌 Tickets do Sistema

# senhas e usuarios de testes
User:ADM  / Senha:ADM@123456
User:PCM  / Senha:PCM@123456
User:ALMOXARIFE  / Senha:ALM@123456
User:SUPERVISOR  / Senha:SUP@123456
User:FABRICA / Senha:FAB@123456


## 🔴 Bugs


- Verificar pq não esta exibindo o numero do cógigo no campo da intervenção 

* Resolvido parcialmente, ainda avaliar
- [/] mensages estao aparecendo no dashboard e não estão sumindo

## 🟡 Melhorias

- [ ] incluir uma lista suspensa onde mostra todas as OS e horarios trabalhados em cadas OS ao clicar no colaborador na aba de relatórios.

- [ ] Atualizar layout do finalizar OS.
- [ ] Atualizar impressão da OS para estilo a um Word edit
avel, para enviar por meio digital e poder efetuar as anotações.





## 🟢  Concluído

## Melhorias Implementadas
- [x] Adicionar botão de voltar na `base.html` com retorno ao dashboard
- [x] Alterar estrutura:
      - [x]Remover valor da hora do cadastro de colaborador
      - [x]Criar cadastro de Função com valor/hora
      - [x] Relacionar apenas a Função ao Colaborador
      - [x] Modificar o Orçamento Horas para o mesmo layout do Orçamento Cliente

- [x] Na funcionalidade de Ajuste de Horas, adicionar campo para incluir lançamento
- [x] criar tela de login 
- [x] criar os grupos de acessos ao sistema( permissões, PCM, ADM, SUPERVISOR, ALMOXARIFE)
- [x] no Ajuste de horas adicionar um seletor para selecionar o mes dos ajustes, começando do dia 21 do mes anterior até o dia 20 do mes atual, EX: Mes de Março Retorna o intervalo dos dias de (21/02 até 20/03).
- [X] incluir funcionalidade para poder excluir registro no ajuste de horas.
- [X] Atualizar layout do cadastro de centros de custos.





## Bugs Corrigidos
- [x] Corrigir o Orçamento Clientes para puxar:
      - Valor da função
      - Total de horas por OS
      - Total de horas por função
      - Manter os intervalos de horas

- [x] Virificar o apontamento de Horas.
- [x] Verificar a abertura de OS.
- [x] Virificar layout do apontamento de Horas.
- [x] Corrigir a opção de edição do app Cadastro:
      - [x] Centro de Custo.
      - [x] Clientes.
      - [x] Intervenção.
      - [x] Colaborador.

- [x] corrigir a separação das horas Normais,50% e 100% nos relatórios.
- [x] corrigir erro ao puchar campos no finalizar OS.
- [X] verificar o orçamento de horas PDF, as horas estão puchando 3 horas a frente do horario normal, adicionar desconto do almoço 
- [x] retorno das funções que já estão em uso igual ao dos clientes 
- [x] no colaborador retirar a função de excluir e add a opção de desligar o colaborador 
- [X] retorno das Intervenções que já estão em uso 
- [x] tratamento erro ao excluir um Centro Pai que possui centros Filhos.
- [x] tratamento de erro ao excluir quando o centro de custo já esta em uso em alguma OS .









## Novas funcionalidades

-> Tela de Finalização de OS:
   -> Incluir campos a baixo salvos em Banco de dados:
      -> Descrição Técnica da Avaria
      -> Descrição da Intervenção
      -> Peças Aplicadas
            -> Quantidade 
            -> Descrição
      -> Descrição do Sintoma
      -> Causa
      -> Data com Hora de Inicio 
      -> Data com Hora de Fim
      -> Observações 


-> Tela de Cadastro de Centros de Custos:
      -> Modificar o campo Centro de Custos Atual para "Tag"
      -> Adicionar o campo para o centro de Custo 
      -> Mudar o nome do card de "Centro de Custo" para "Cadastro de Ativos"

- verificar para colocar imagem na OS puchando do Sharepoint 



## Concluidos

-[x] definir as tabelas fatos e Dimensão 