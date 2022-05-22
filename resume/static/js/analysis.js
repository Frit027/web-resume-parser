const iconClasses = {
    caretUp: 'bi bi-caret-up-fill',
    caretDown: 'bi bi-caret-down-fill',
};

const SKILLS = [
    'Языки программирования', 'Языки описания внешнего вида страницы',
    'Языки разметки', 'СУБД', 'Операционные системы', 'Системы контроля версий',
    'Технологии IOS', 'Технологии Android', 'ML, Data Science/Analysis',
    'GameDev', 'Технологии и методы тестирования', 'Администрирование',
    'DevOps', 'Технологии Frontend-разработки', 'Технологии Backend-разработки'
];

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
    age:        $('#age').find(':selected').val(),
    levels:     $('#levels').val(),
    skills: {
        program_lang:     $('#program_lang').val(),
        stylesheet_lang:  $('#stylesheet_lang').val(),
        markup_lang:      $('#markup_lang').val(),
        db:               $('#db').val(),
        operating_system: $('#operating_system').val(),
        version_control:  $('#version_control').val(),
        ios:              $('#ios').val(),
        android:          $('#android').val(),
        ml:               $('#ml').val(),
        gamedev:          $('#gamedev').val(),
        testing:          $('#testing').val(),
        sys_admin:        $('#sys_admin').val(),
        devops:           $('#devops').val(),
        frontend:         $('#frontend').val(),
        backend:          $('#backend').val(),
    }}
);

insertInfo = (response) => {
    const resumesDiv = $('#resumes');

    resumesDiv.html('');
    if (!response.resumes.length) {
        resumesDiv.append('<p class="text-center mt-4 empty-result">Ничего не найдено</p>');
        return;
    }
    resumesDiv.append('<p class="mt-3 mb-3 relevance-text">Результаты показаны по убыванию релевантности резюме запросу</p>');

    response.resumes.forEach((resume, i) => {
        const generalInfo = {
            name:       resume.name,
            age:        resume.age,
            email:      resume.email,
            phone:      resume.phone,
            academies:  resume.education.academies,
            experience: resume.experience,
        };
        const skills = resume.skills;

        resumesDiv.append(`
          <div class="filename">${resume.filename}</div>
          <span class="detail" id="detail_button_${i}">Подробнее <i id="bi_${i}" class="${iconClasses.caretDown}"></i></span>
          <div class="resume-info" id="info_${i}">
            ${anyKey(generalInfo) ? getGeneralInfo(generalInfo) : ''}
            ${anyKey(skills) ? getSkills(skills, response.request_skills) : ''}
          </div>
        `);

        $(`#detail_button_${i}`).on('click', { i }, toggleInfo);
    })
};

toggleInfo = (event) => {
    const info = $(`#info_${event.data.i}`);
    if(info.is(':hidden')) {
        $(`#detail_button_${event.data.i}`).html(`Скрыть <i id="bi_${event.data.i}" class="${iconClasses.caretUp}"></i>`);
        info.show('slow');
    } else {
        $(`#detail_button_${event.data.i}`).html(`Подробнее <i id="bi_${event.data.i}" class="${iconClasses.caretDown}"></i>`);
        info.hide('slow');
    }
};

getGeneralInfo = (info) => {
    return `
      <div class="subtitle">Общая информация</div>
      <ul>
        ${info.name       ? `<li><span class="text-primary">Имя:</span> ${info.name}</li>` : ''}
        ${info.age        ? `<li><span class="text-primary">Возраст:</span> ${info.age} ${getWordByYear(info.age)}</li>` : ''}
        ${info.email      ? `<li><span class="text-primary">Email:</span> ${info.email}</li>` : ''}
        ${info.phone      ? `<li><span class="text-primary">Телефон:</span> ${info.phone}</li>` : ''}
        ${info.academies.length ? `<li><span class="text-primary">Оконченные учебные заведения:</span></li>
                                 <ul>${info.academies.reduce((str, academy) => str + `<li>${academy}</li>`, '')}</ul>`
                                : ''}
        ${info.experience ? `<li><span class="text-primary">Опыт работы:</span> ${info.experience} ${getWordByYear(parseInt(info.experience))}</li>` : ''}
      </ul>
    `;
};

getSkills = (obj, req_skills) => {
    const lis = Object.keys(obj).reduce((res, key, i) =>
        obj[key].length ? res + `<li><span class="text-primary">${SKILLS[i]}:</span> ${highlighting(obj[key], req_skills)}</li>`
                        : res + '', ''
    );
    return `
      <div class="subtitle">Информационные технологии</div>
      <ul>${lis}</ul>
    `;
};

anyKey = (info) => Object.keys(info).some(
    (key) => {
        if (Array.isArray(info[key])) return info[key].length;
        return info[key];
    });

highlighting = (skills, req_skills) => {
    skills = skills.map((skill) => {
        if (req_skills.includes(skill)) return `<span class="skill">${skill}</span>`;
        return skill;
    });
    return skills.join(', ');
};

getWordByYear = (number) => {
    const words = ['год', 'года', 'лет'];
    const cases = [2, 0, 1, 1, 1, 2];
    return words[(number % 100 > 4 && number % 100 < 20) ? 2 : cases[(number % 10 < 5) ? number % 10 : 5]];
};
