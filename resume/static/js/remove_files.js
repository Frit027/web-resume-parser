$('#remove_button').click(() => {
    $.ajax({
        type: 'POST',
        headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
        url: '',
        data: { is_remove_files: true },
        success: (data) => {
            if (data.is_removed) {
                $('#ul_resumes').replaceWith('<p>Вы пока не загрузили резюме.</p>');
            }
        }
    });
});
