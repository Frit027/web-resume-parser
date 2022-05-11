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
        let ul = '';

        if (Object.keys(info).some((key) => info[key])) {
            ul = `
                <ul>
                  ${info.name       ? `<li>Имя: ${info.name}</li>` : ''}
                  ${info.age        ? `<li>Возраст: ${info.age} ${plural(info.age)}</li>` : ''}
                  ${info.email      ? `<li>Email: ${info.email}</li>` : ''}
                  ${info.phone      ? `<li>Телефон: ${info.phone}</li>` : ''}
                  ${info.academies  ? `<li>Оконченные учебные заведения:</li>
                                       <ul>${info.academies.reduce((str, academy) => str + `<li>${academy}</li>`, '')}</ul>`
                                    : ''
                  }
                  ${info.experience ? `<li>Опыт работы: ${info.experience} ${plural(parseInt(info.experience))}</li>` : ''}
                </ul>
            `;
        }
        $('#resumes').append(`
            <li><b>${response.filenames[i]}</b></li>
            ${ul}
        `);
        i += 1;
    })
};

plural = (number) => {
    const words = ['год', 'года', 'лет'];
    const cases = [2, 0, 1, 1, 1, 2];
    return words[(number % 100 > 4 && number % 100 < 20) ? 2 : cases[(number % 10 < 5) ? number % 10 : 5]];
};
