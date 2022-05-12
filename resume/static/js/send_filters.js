const iconClasses = {
    caretUp: 'bi bi-caret-up-fill',
    caretDown: 'bi bi-caret-down-fill',
};

(() => {
    $('#apply_button').click(() => {
        $.ajax({
            type: 'POST',
            headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
            url: '/analysis/',
            data: getSelected(),
            success: (response) => insertInfo(response),
        });
    });
})();

getSelected = () => ({
    experience: $('#experience').find(':selected').val(),
    age: $('#age').find(':selected').val(),
    levels: $('#levels').val(),
    skills: {
        program_lang: $('#program_lang').val(),
        stylesheet_lang: $('#stylesheet_lang').val(),
        markup_lang: $('#markup_lang').val(),
        db: $('#db').val(),
        operating_system: $('#operating_system').val(),
        version_control: $('#version_control').val(),
        ios: $('#ios').val(),
        android: $('#android').val(),
        ml: $('#ml').val(),
        gamedev: $('#gamedev').val(),
        testing: $('#testing').val(),
        sys_admin: $('#sys_admin').val(),
        devops: $('#devops').val(),
        frontend: $('#frontend').val(),
        backend: $('#backend').val(),
    }}
);

insertInfo = (response) => {
    $('#resumes').html('');
    let i = 0;
    response.resumes.forEach((resume) => {
        const info = {
            name: resume.name,
            age: resume.age,
            email: resume.email,
            phone: resume.phone,
            academies: resume.education.academies,
            experience: resume.experience,
        };

        $('#resumes').append(`
            <div class="filename">${response.filenames[i]}</div>
            <span class="detail" id="detail_button_${i}">Подробнее <i id="bi_${i}" class="${iconClasses.caretDown}"></i></span>
            ${getUlInfo(info, i)}
        `);

        $(`#detail_button_${i}`).on('click', { i }, toggleInfo);
        i += 1;
    })
};

toggleInfo = (event) => {
    const info = $(`#info_${event.data.i}`);
    if(info.is(':hidden')) {
        $(`#bi_${event.data.i}`).replaceWith(`<i id="bi_${event.data.i}" class="${iconClasses.caretUp}"></i>`)
        info.show('slow');
    } else {
        $(`#bi_${event.data.i}`).replaceWith(`<i id="bi_${event.data.i}" class="${iconClasses.caretDown}"></i>`)
        info.hide('slow');
    }
};

getWordByYear = (number) => {
    const words = ['год', 'года', 'лет'];
    const cases = [2, 0, 1, 1, 1, 2];
    return words[(number % 100 > 4 && number % 100 < 20) ? 2 : cases[(number % 10 < 5) ? number % 10 : 5]];
};

getUlInfo = (info, i) => {
    if (!Object.keys(info).some((key) => info[key])) return '';
    return `
        <ul class="resume-info" id="info_${i}">
          ${info.name       ? `<li>Имя: ${info.name}</li>` : ''}
          ${info.age        ? `<li>Возраст: ${info.age} ${getWordByYear(info.age)}</li>` : ''}
          ${info.email      ? `<li>Email: ${info.email}</li>` : ''}
          ${info.phone      ? `<li>Телефон: ${info.phone}</li>` : ''}
          ${info.academies  ? `<li>Оконченные учебные заведения:</li>
                               <ul>${info.academies.reduce((str, academy) => str + `<li>${academy}</li>`, '')}</ul>`
                            : ''
          }
          ${info.experience ? `<li>Опыт работы: ${info.experience} ${getWordByYear(parseInt(info.experience))}</li>` : ''}
        </ul>
    `;
};

