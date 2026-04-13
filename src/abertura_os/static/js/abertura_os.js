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
  const normalize = (value) => (
    (value || '')
      .toString()
      .normalize('NFD')
      .replace(/[\u0300-\u036f]/g, '')
      .toLowerCase()
      .trim()
  );

  const enableNativeSelectFilter = (select) => {
    const originalOptions = Array.from(select.options).map((option) => ({
      value: option.value,
      label: option.textContent,
      disabled: option.disabled
    }));

    let query = '';
    let resetTimer = null;

    const buildOption = (data) => {
      const option = document.createElement('option');
      option.value = data.value;
      option.textContent = data.label;
      option.disabled = Boolean(data.disabled);
      return option;
    };

    const renderOptions = (term) => {
      const currentValue = select.value;
      const normalizedTerm = normalize(term);

      const filtered = !normalizedTerm
        ? originalOptions
        : originalOptions.filter((option, index) => (
          index === 0 || normalize(option.label).includes(normalizedTerm)
        ));

      select.innerHTML = '';
      filtered.forEach((optionData) => {
        select.appendChild(buildOption(optionData));
      });

      const hasCurrentValue = filtered.some((option) => option.value === currentValue);
      if (hasCurrentValue) {
        select.value = currentValue;
      }
    };

    const clearFilter = () => {
      query = '';
      renderOptions('');
    };

    const scheduleClearQuery = () => {
      clearTimeout(resetTimer);
      resetTimer = setTimeout(() => {
        query = '';
      }, 1200);
    };

    select.addEventListener('keydown', (event) => {
      if (event.ctrlKey || event.metaKey || event.altKey) {
        return;
      }

      if (event.key === 'Escape') {
        clearFilter();
        return;
      }

      if (event.key === 'Backspace') {
        event.preventDefault();
        query = query.slice(0, -1);
        renderOptions(query);
        scheduleClearQuery();
        return;
      }

      if (event.key.length === 1) {
        event.preventDefault();
        query += event.key;
        renderOptions(query);
        scheduleClearQuery();
      }
    });

    select.addEventListener('blur', clearFilter);
    select.addEventListener('change', clearFilter);
  };

  document
    .querySelectorAll('.form select.form-control')
    .forEach(enableNativeSelectFilter);

  if (!dropdown.wrapper || !dropdown.selected || !dropdown.list || !dropdown.hidden) {
    return;
  }

  const centroGroups = Array.from(dropdown.list.querySelectorAll('.dropdown__group'));
  let centroQuery = '';
  let centroTimer = null;
  let centroSearchActive = false;

  const clearCentroFilter = () => {
    centroQuery = '';
    centroSearchActive = false;

    centroGroups.forEach((group) => {
      const childrenContainer = group.querySelector('.dropdown__children');
      const arrow = group.querySelector('.dropdown__toggle .arrow');

      group.style.display = '';

      group
        .querySelectorAll('.dropdown__item--child')
        .forEach((child) => {
          child.style.display = '';
        });

      if (childrenContainer) {
        const wasHidden = childrenContainer.dataset.preSearchHidden;

        if (wasHidden === 'true') {
          childrenContainer.classList.add('hidden');
        } else if (wasHidden === 'false') {
          childrenContainer.classList.remove('hidden');
        }

        delete childrenContainer.dataset.preSearchHidden;

        if (arrow) {
          arrow.textContent = childrenContainer.classList.contains('hidden') ? '▶' : '▼';
        }
      }
    });
  };

  const applyCentroFilter = (term) => {
    const normalizedTerm = normalize(term);

    if (!normalizedTerm) {
      clearCentroFilter();
      return;
    }

    if (!centroSearchActive) {
      centroGroups.forEach((group) => {
        const childrenContainer = group.querySelector('.dropdown__children');
        if (childrenContainer) {
          childrenContainer.dataset.preSearchHidden = String(childrenContainer.classList.contains('hidden'));
        }
      });
      centroSearchActive = true;
    }

    centroGroups.forEach((group) => {
      const parentItem = group.querySelector('.dropdown__item--parent');
      const childrenContainer = group.querySelector('.dropdown__children');
      const arrow = group.querySelector('.dropdown__toggle .arrow');
      const parentMatches = normalize(parentItem?.textContent || '').includes(normalizedTerm);

      let hasVisibleChild = false;

      group.querySelectorAll('.dropdown__item--child').forEach((child) => {
        const childMatches = parentMatches || normalize(child.textContent).includes(normalizedTerm);
        child.style.display = childMatches ? '' : 'none';
        if (childMatches) {
          hasVisibleChild = true;
        }
      });

      group.style.display = parentMatches || hasVisibleChild ? '' : 'none';

      if (childrenContainer && (parentMatches || hasVisibleChild)) {
        childrenContainer.classList.remove('hidden');
        if (arrow) {
          arrow.textContent = '▼';
        }
      }
    });
  };

  const scheduleCentroClear = () => {
    clearTimeout(centroTimer);
    centroTimer = setTimeout(() => {
      centroQuery = '';
    }, 1200);
  };

  dropdown.selected.addEventListener('click', (e) => {
    e.stopPropagation();
    dropdown.toggle();

    if (dropdown.list.classList.contains('hidden')) {
      clearCentroFilter();
    }
  });

  dropdown.selected.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      dropdown.toggle();
    

    if (dropdown.list.classList.contains('hidden')) {
      clearCentroFilter();
    }
    return;
  }

    if (e.key === 'Escape') {
      clearCentroFilter();
      dropdown.close();
      return;
    }

    if (e.key === 'Backspace') {
      e.preventDefault();
      centroQuery = centroQuery.slice(0, -1);
      dropdown.list.classList.remove('hidden');
      applyCentroFilter(centroQuery);
      scheduleCentroClear();
      return;
    }

    if (e.key.length === 1 && !e.ctrlKey && !e.metaKey && !e.altKey) {
      e.preventDefault();
      centroQuery += e.key;
      dropdown.list.classList.remove('hidden');
      applyCentroFilter(centroQuery);
      scheduleCentroClear();
    }
  });

  document.addEventListener('click', (e) => {
    if (!e.target.closest('.dropdown')) {
      clearCentroFilter();
      dropdown.close();
    }
  });

  dropdown.list.addEventListener('click', (e) => {
    const toggleButton = e.target.closest('.dropdown__toggle');
    const child = e.target.closest('.dropdown__item--child');

    // Abrir / fechar filhos
    if (toggleButton) {
      const children = document.getElementById(toggleButton.dataset.target);
      const arrow = toggleButton.querySelector('.arrow');

      if (!children) return;

      children.classList.toggle('hidden');

      if (arrow) {
        arrow.textContent = children.classList.contains('hidden') ? '▶' : '▼';
      }

      return;
    }

    // Selecionar item
    if (!child) return;

    dropdown.set(child.dataset.cod, child.textContent.trim());
    clearCentroFilter();
    dropdown.close();
  });
});

