document.addEventListener('DOMContentLoaded', () => {

  const form = document.querySelector('.abrir-os form');
  const numeroOS = document.getElementById('numero_os');
  const saveBtn = document.querySelector('.save-btn');
  const cancelBtn = document.querySelector('.cancel-btn');
  const deleteBtn = document.querySelector('.delete-btn');

  const dropdown = {
    selected: document.getElementById('dropdownSelected'),
    list: document.getElementById('dropdownList'),
    hidden: document.getElementById('centro_custo'),

    set(cod, label) {
      this.hidden.value = cod || '';
      this.selected.textContent = label || 'Selecione um centro de custo';
    },

    toggle() {
      this.list.classList.toggle('hidden');
    },

    close() {
      this.list.classList.add('hidden');
    }
  };

  dropdown.selected.addEventListener('click', e => {
    e.stopPropagation();
    dropdown.toggle();
  });

  document.addEventListener('click', e => {
    if (!e.target.closest('.dropdown-container')) {
      dropdown.close();
    }
  });

  dropdown.list.addEventListener('click', e => {
    const parent = e.target.closest('.parent');
    const child = e.target.closest('.child');
    const arrow = parent?.querySelector('.arrow');

    if (parent && e.target.classList.contains('arrow')) {
      const children = document.getElementById(`children-${parent.dataset.cod}`);
      children.classList.toggle('hidden');
      arrow.textContent = children.classList.contains('hidden') ? '▶' : '▼';
      return;
    }

    if (child) {
      dropdown.set(child.dataset.cod, child.dataset.label);
      dropdown.close();
    } else if (parent && !e.target.classList.contains('arrow')) {
      dropdown.set(parent.dataset.cod, parent.dataset.label);
      dropdown.close();
    }
  });

  // Preencher formulário para edição
  function setFormValue(name, value) {
    const input = form.querySelector(`[name="${name}"]`);
    if (!input) return;
    if (input.tagName === 'SELECT' || input.tagName === 'INPUT') {
      input.value = value ?? '';
    }
  }

  function preencherFormulario(data) {
    numeroOS.value = data.numero;
    dropdown.set(data.centroCod, data.centroLabel);

    form.action = `/abertura_os/editar_os/${data.id}/`;
    saveBtn.textContent = '💾 Salvar Alterações';
    cancelBtn.style.display = 'inline-block';
    deleteBtn.style.display = 'inline-block';
    deleteBtn.href = `/abertura_os/excluir_os/${data.id}/`;

    Object.entries(data.campos).forEach(([k, v]) => setFormValue(k, v));
  }

  function resetForm() {
    form.reset();
    dropdown.set('', '');
    saveBtn.textContent = '💾 Abrir OS';
    cancelBtn.style.display = 'none';
    deleteBtn.style.display = 'none';
    form.action = window.URL_ABRIR_OS;
    numeroOS.value = window.PROXIMO_NUMERO_OS;
  }

  cancelBtn.addEventListener('click', resetForm);

  // Botão editar
  document.querySelectorAll('.edit-btn').forEach(btn => {
    btn.addEventListener('click', e => {
      const tr = e.target.closest('tr');
      preencherFormulario({
        id: tr.dataset.osId,
        numero: tr.dataset.numeroOs,
        centroCod: tr.dataset.centroCusto,
        centroLabel: tr.dataset.centroLabel,
        campos: {
          descricao_os: tr.dataset.descricaoOs,
          cliente: tr.dataset.cliente,
          motivo_intervencao: tr.dataset.motivoIntervencao,
          ssm: tr.dataset.ssm
        }
      });
    });
  });

  deleteBtn.addEventListener('click', e => {
    e.preventDefault();
    if (confirm('Deseja excluir esta OS?')) window.location.href = deleteBtn.href;
  });
});
