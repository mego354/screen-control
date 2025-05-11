document.querySelectorAll('.attend_record_li').forEach((item) => {
    item.addEventListener('click', () => {
        var div = document.querySelector(`#${item.dataset.divid}`);
        var span = document.querySelector(`#${item.dataset.divid}_span`);
        if (div.classList.contains('hidden')) {
            div.classList.remove('hidden');
            div.classList.add('visible');
            span.innerHTML = 'Hide';
        } else {
            div.classList.remove('visible');
            div.classList.add('hidden');
            span.innerHTML = 'Review';
        }
    });
});
