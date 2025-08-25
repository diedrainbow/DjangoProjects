

		document.addEventListener('DOMContentLoaded', function() {
            // Обработка клика по ячейке для редактирования
            document.body.addEventListener('click', function(e) {
                const cell = e.target.closest('.cell');
                if (cell && !cell.classList.contains('header') && !cell.classList.contains('row-header')) {
                    const matches = cell.id.match(/cell-(\d+)-(\d+)/);
                    if (matches) {
                        const row = matches[1];
                        const col = matches[2];
                        htmx.trigger(cell, 'editCell');
                    }
                }
            });

            // Сохранение по нажатию Enter и отмена по Escape
            document.body.addEventListener('keydown', function(e) {
                if (e.target.classList.contains('cell-input')) {
                    if (e.key === 'Enter') {
                        e.preventDefault();
                        htmx.trigger(e.target.closest('form'), 'submit');
                    } else if (e.key === 'Escape') {
                        htmx.trigger(e.target.closest('form'), 'cancel');
                    }
                }
            });
        });

        // Кастомные события для HTMX
        htmx.defineExtension('cell-events', {
            onEvent: function(name, event) {
                if (name === 'htmx:afterProcessNode') {
                    const form = event.detail.elt;
                    if (form.classList.contains('cell-form')) {
                        const input = form.querySelector('input');
                        if (input) {
                            input.focus();
                            input.select();
                        }
                    }
                }
            }
        });