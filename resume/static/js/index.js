$("#apply_button").click(function() {
    const data = {
        experience: $("#experience").find(":selected").val(),
        age: $("#age").find(":selected").val(),
        levels: $("#levels").val(),
        skills: {
            program_lang: $("#program_lang").val(),
            stylesheet_lang: $("#stylesheet_lang").val(),
            markup_lang: $("#markup_lang").val(),
            db: $("#db").val(),
            operating_system: $("#operating_system").val(),
            version_control: $("#version_control").val(),
            ios: $("#ios").val(),
            android: $("#android").val(),
            ml: $("#ml").val(),
            gamedev: $("#gamedev").val(),
            testing: $("#testing").val(),
            sys_admin: $("#sys_admin").val(),
            devops: $("#devops").val(),
            frontend: $("#frontend").val(),
            backend: $("#backend").val(),
        }
    };
    $.ajax({
        type: "POST",
        headers: { "X-CSRFToken": Cookies.get('csrftoken') },
        url: /analysis/,
        data: data,
        success: (data) => {
            $("#resumes").html('');
            data.resumes.forEach((file) => {
                $("#resumes").append(`<li>${file}</li>`)
            })
        }
    });
});
