# 📌 Backlog do Sistema de OS

## 🔴 Bugs (Alta Prioridade)
- [ ] Exibir corretamente o número do código no campo da intervenção  
- [ ] Mensagens no dashboard não estão sumindo após exibição  

---

## 🟡 Melhorias (Média Prioridade)
- [ ] Incluir lista suspensa com todas as OS e horários trabalhados ao clicar no colaborador na aba de relatórios  
- [ ] Atualizar layout da tela de Finalizar OS  
- [ ] Atualizar impressão da OS para formato editável estilo Word (para envio digital e anotações)  
- [ ] Permitir adicionar imagem na OS puxando do SharePoint  

---

## 🟢 Concluído

### Melhorias Implementadas
- [x] Botão de voltar na `base.html` para retorno ao dashboard  
- [x] Estrutura de Função com valor/hora e vínculo ao colaborador  
- [x] Ajuste de Horas: campo para lançamento, seletor de mês (21/mes anterior → 20/mes atual), exclusão de registros  
- [x] Tela de login e grupos de acesso (ADM, PCM, SUPERVISOR, ALMOXARIFE, FABRICA)  
- [x] Layout atualizado do cadastro de Centros de Custos  

### Bugs Corrigidos
- [x] Orçamento Clientes puxando valor da função, total de horas por OS e função  
- [x] Correções em apontamento de horas, abertura de OS e layout  
- [x] Correções em edição de Centro de Custo, Clientes, Intervenção e Colaborador  
- [x] Separação correta de horas Normais, 50% e 100% nos relatórios  
- [x] Ajuste no orçamento de horas PDF (desconto do almoço)  
- [x] Tratamento de erros ao excluir Centro Pai com filhos e centros em uso em OS  
- [x] Alteração no colaborador: retirar exclusão e adicionar opção de desligar  

---

## 🆕 Novas Funcionalidades

### Tela de Finalização de OS
- [ ] Campos obrigatórios:  
  - Descrição Técnica da Avaria  
  - Descrição da Intervenção  
  - Descrição do Sintoma  
  - Causa  
  - Data/Hora de Início  
  - Data/Hora de Fim  
- [ ] Campos opcionais:  
  - Peças Aplicadas (Quantidade, Descrição)  
  - Observações  
- [ ] Todos os campos devem ser salvos em banco como registro  
- [ ] Alterar status da OS para **Finalizado** (já existente)  

### Cadastro de Centros de Custos
- [x] Campo "Centro de Custos Atual" renomeado para "Tag"  
- [x] Adicionar campo para centro de custo  
- [x] Alterar nome do card para "Cadastro de Ativos"  

---

## 📊 Arquitetura de Dados
- [x] Definição das tabelas Fato e Dimensão  



- verificar servidor da IMA
- verivicar disponibilidade de rodar local
- alinhamento nas sextas as 13:30
7