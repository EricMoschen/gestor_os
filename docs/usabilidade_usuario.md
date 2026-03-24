# Manual de Usabilidade do Usuário — Gestor OS

## 1) Objetivo do sistema
O **Gestor OS** é uma plataforma de gestão operacional para:
- abrir e controlar Ordens de Serviço (OS);
- registrar horas de execução por colaborador;
- ajustar apontamentos com governança;
- gerar relatórios de horas e orçamento em PDF.

Este guia foi feito para uso diário, com linguagem simples e fluxo prático.

---

## 2) Perfis de acesso e responsabilidades
O sistema controla as telas por perfil. Em termos práticos:

- **Administrador (ADM):** acesso completo.
- **PCM / Almoxarife:** forte atuação em abertura/finalização de OS e cadastros.
- **Supervisor:** foco em apontamento, ajuste de horas e relatórios.
- **Fábrica:** foco em apontamento de horas.

> Dica de governança SaaS: mantenha cada usuário com o menor nível de privilégio necessário (princípio do menor privilégio).

---

## 3) Primeiros passos (onboarding rápido)

### Passo 1 — Login
1. Acesse a tela de login.
2. Preencha **Usuário** e **Senha**.
3. Clique em **Entrar**.

### Passo 2 — Dashboard
Após login, você verá o **Painel de Gestão** com cards por categoria:
- **Ordens de Serviço**
- **Cadastros**
- **Relatórios**

> Se um card não aparecer, significa que seu perfil não possui permissão para aquela função.

---

## 4) Fluxo operacional recomendado (padrão de alta eficiência)

Use esta sequência para reduzir erros e retrabalho:

1. **Cadastros base** (uma vez e manutenção contínua)
2. **Abrir OS**
3. **Apontar Horas**
4. **Ajustar Horas** (quando necessário)
5. **Finalizar OS**
6. **Emitir relatórios/PDF**

---

## 5) Cadastros (base de dados confiável)

### 5.1 Cadastro de Centro de Custo
**Quando usar:** estrutura de centros e subcentros.

**Como fazer:**
1. Acesse **Cadastros > Centro de Custos**.
2. Preencha código e descrição.
3. (Opcional) selecione **Centro Pai** para criar hierarquia.
4. Clique em **Cadastrar**.
5. Para editar, clique no item da árvore à direita.

**Boas práticas:**
- use padrão de nomenclatura por área/unidade;
- evite duplicidades de código.

### 5.2 Cadastro de Clientes
1. Acesse **Cadastros > Clientes**.
2. Informe **Código do Cliente** e **Nome do Cliente**.
3. Clique em **Salvar**.
4. Use ✏️ para editar.
5. Exclua apenas clientes sem vínculo de OS.

### 5.3 Cadastro de Intervenção
1. Acesse **Cadastros > Intervenção**.
2. Preencha a descrição.
3. Clique em **Cadastrar**.
4. Use ✏️ para editar e 🗑️ para excluir quando não estiver em uso.

### 5.4 Cadastro de Função
1. Acesse **Cadastros > Função**.
2. Informe a descrição da função e valor/hora.
3. Salve o registro.
4. Edite quando houver reajuste de custos.

### 5.5 Cadastro de Colaborador
1. Acesse **Cadastros > Colaborador**.
2. Preencha matrícula, nome, função e turno.
3. Configure horários personalizados (se necessário).
4. Clique em **Cadastrar**.
5. Em edição, ajuste status (ativo/desligado).

---

## 6) Ordens de Serviço (ciclo de vida completo)

### 6.1 Abrir OS
1. Acesse **Ordens de Serviço > Abrir OS**.
2. Confira o número de OS gerado automaticamente.
3. Selecione o **Centro de Custo**.
4. Preencha os campos obrigatórios do formulário.
5. Clique em **Abrir OS**.

**Recursos úteis na tela:**
- tabela com OS já cadastradas;
- atalho ✏️ para edição;
- atalho 🖨️ para impressão da OS.

### 6.2 Apontar Horas (início/fim da execução)
1. Acesse **Ordens de Serviço > Apontar Horas**.
2. Digite a **Matrícula do Colaborador**.
3. Informe o **Número da OS**.
4. Clique em:
   - **▶️ Iniciar OS** para abrir o apontamento;
   - **⏹️ Finalizar OS** para encerrar o apontamento.

**Observação:** a tela já traz lista de OS e filtro rápido para consulta.

### 6.3 Ajustar Horas (supervisão e correção)
1. Acesse **Ordens de Serviço > Ajustar Horas**.
2. Filtre por competência, colaborador, OS ou status.
3. Clique em **Ajustar** no registro desejado.
4. Altere data/hora início/fim e salve.
5. Se necessário, exclua o apontamento indevido.
6. Para lançamento retroativo, use **+ Incluir Lançamento**.

**Governança recomendada:**
- ajuste somente com justificativa interna;
- prefira manter trilha de auditoria do processo.

### 6.4 Finalizar OS
1. Acesse **Ordens de Serviço > Finalizar OS**.
2. Digite o número da OS ou selecione na tabela de OS em aberto.
3. Revise os dados carregados automaticamente.
4. Preencha **Observações** (obrigatório).
5. Clique em **Finalizar OS**.

---

## 7) Relatórios e PDFs (decisão e prestação de contas)

### Relatório por OS
1. Acesse **Relatórios > Relatórios**.
2. Informe número da OS e período (início/fim).
3. Clique em **Buscar**.
4. Analise horas normais, 50%, 100% e total geral por colaborador.

### Exportações
Com uma OS válida em tela, use:
- **Orçamento Horas (PDF)**
- **Orçamento Cliente (PDF)**

---

## 8) Rotina operacional diária (modelo pronto)

### Início do turno
- validar colaboradores ativos;
- confirmar OS abertas do dia;
- orientar equipe sobre matrícula e OS correta no apontamento.

### Durante o turno
- monitorar apontamentos em aberto;
- corrigir inconsistências em **Ajustar Horas**;
- registrar desvios e justificativas internas.

### Encerramento do turno
- garantir encerramento de apontamentos;
- finalizar OS concluídas;
- emitir relatório das OS críticas/estratégicas.

---

## 9) Erros comuns e prevenção

- **Matrícula inválida:** confira se colaborador está cadastrado e ativo.
- **OS não encontrada:** valide o número e situação da OS.
- **Impossibilidade de exclusão em cadastro:** item está em uso por outros registros.
- **Card ausente no dashboard:** perfil sem permissão.

---

## 10) Padrão de qualidade SaaS (nível profissional)

Para operação madura e escalável:
- mantenha cadastros limpos e padronizados;
- adote rotina diária de fechamento operacional;
- use relatórios como base para decisão (não percepção);
- formalize responsáveis por abertura, ajustes e finalização;
- revise perfis e acessos periodicamente.

---

## 11) Checklist rápido (1 minuto)

Antes de encerrar o dia, confirme:
- [ ] não há apontamentos críticos em aberto;
- [ ] OS concluídas foram finalizadas com observação;
- [ ] ajustes foram realizados apenas quando necessários;
- [ ] relatório das OS prioritárias foi emitido.

---

## 12) Resumo executivo
Se sua equipe seguir este fluxo:
**Cadastrar base → Abrir OS → Apontar/Encerrar horas → Ajustar quando necessário → Finalizar OS → Emitir relatório**,
você terá operação mais previsível, rastreável e com qualidade de dados para gestão.
