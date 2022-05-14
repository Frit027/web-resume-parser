const PRELOADER = `
  <div class="preloader">
    <div class="preloader__image"></div>
  </div>`;

(() => {
    $('#remove_button').click(() => {
        $.ajax({
            type: 'POST',
            headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
            url: '',
            data: { is_remove_files: true },
            success: (data) => {
                if (data.is_removed) {
                    $('.ul_filenames').replaceWith('<p>Вы пока не загрузили резюме.</p>');
                    $('#remove_button').remove();
                    $('.detail').remove();
                }
            }
        });
    });

    $('.detail').click(() => {
        const ulFilenames = $('.ul_filenames');
        if(ulFilenames.is(':hidden')) {
            $('.detail').html('Скрыть <i class="bi bi-caret-up-fill"></i>');
            ulFilenames.show('slow');
        } else {
            $('.detail').html('Показать <i class="bi bi-caret-down-fill"></i>');
            ulFilenames.hide('slow');
        }
    });

    $('#files_form').on('submit', () => {
        $('body').prepend(PRELOADER);
    });
})();

document.onreadystatechange = () => {
    $('.preloader').remove();
};
