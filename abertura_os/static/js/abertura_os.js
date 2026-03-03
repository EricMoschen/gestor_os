document.addEventListener('DOMContentLoaded', () => {
  const dropdown = {
    wrapper: document.querySelector('.dropdown'),
    selected: document.getElementById('dropdownSelected'),
    list: document.getElementById('dropdownList'),
    hidden: document.getElementById('centro_custo'),

    set(cod, label) {
      if (this.hidden) this.hidden.value = cod || '';
      if (this.selected) {
        this.selected.textContent = label || 'Selecione...';
      }
    },

    toggle() {
      this.list?.classList.toggle('hidden');
    },

    close() {
      this.list?.classList.add('hidden');
    }
  };

  if (!dropdown.wrapper || !dropdown.selected || !dropdown.list || !dropdown.hidden) {
    return;
  }

  dropdown.selected.addEventListener('click', (e) => {
    e.stopPropagation();
    dropdown.toggle();
  })


  dropdown.selected.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      dropdown.toggle();
    }

    if (e.key === 'Escape') {
      dropdown.close();
    }
  });

  document.addEventListener('click', (e) => {
    if (!e.target.closest('dropdown')) {
      dropdown.close();
    }
  });

  dropdown.list.addEventListener('click', (e) => {
    const parent = e.target.closest('.dropdown__item--parent');
    const chield = e.target.closest('.dropdown__item--child');

    if (!parent && !chield) return;
    const targetItem = child || parent;
    const arrow = parent?.querySelector('.arrow');

    if (parent && e.target.classList.contains('.arrow')) {
      const chieldren = document.getElementById(`children-${parent.dataset.cod}`);

      if (!children) return;

      children.classList.toggle('hidden');
      if (arrow) {
        arrow.textContent = chieldren.classList.contains('hidden') ? '▶' : '▼'; // colocar indicadores
      }
      return;
    }
    dropdown.set(targetItem.dataset.cod, targetItem.dataset.label);
    dropdown.close();
  });
});

