$(document).ready(() => {
    const MAIN_URL = "http://localhost:8000";

    if ($("#mode").length == 0) {
        $("#id_line").html('');
        $("#id_wells").html('');
    }

    $("#id_primary_watercourse").change(() => {
        var parentID = $("#id_primary_watercourse").find(":selected").val();

        $.ajax({
            type: "GET",
            url: `${MAIN_URL}/watercourses/children/${parentID}`,
            contentType: "application/json",
            success: (response) => {
                $("#id_secondary_watercourse_tempmain").html('');

                if ($("div[id^='newSelect_']").length > 0) {
                    for (var i=0; i < $("div[id^='newSelect_']").length; i++) {
                        $(`div[id^='newSelect_${i}']`).remove();
                    }
                }

                response.forEach(watercourse => {
                    $("#id_secondary_watercourse_tempmain").append(`<option value="${watercourse.id}">${watercourse.name}</option>`); 
                });
            },
            error: () => {
                // alert('Произошла ошибка!');
            }
        })
    });

    $("select[id^='id_secondary_watercourse_tempmain']").change(() => {
        // $(this).html('');
        var parentID = $("#id_secondary_watercourse_tempmain").find(":selected").val();

        $.ajax({
            type: "GET",
            url: `${MAIN_URL}/watercourses/children/${parentID}`,
            contentType: "application/json",
            success: (response) => {
                
                if ($("div[id^='newSelect_']").length > 0) {
                    for (var i=0; i < $("div[id^='newSelect_']").length; i++) {
                        $(`div[id^='newSelect_${i}']`).remove();
                    }
                }
                var newSelect = $(`<select class="form-control" multiple></select>`);
                newSelect.attr("id", `id_secondary_watercourse_temp_${$("select[id^='id_secondary_watercourse_temp_']").length}`);
                response.forEach(watercourse => {
                    newSelect.append(`<option value="${watercourse.id}">${watercourse.name}</option>`); 
                });
                var newDiv = $("<div>").attr('id', `newSelect_${$("select[id^='id_secondary_watercourse_temp_']").length}`);
                newDiv.append(newSelect);
                newDiv.append(`<button type="button" class="btn btn-info" data-target="${newSelect.attr('id')}">Выбрать выделенные</button>`)

                $("#temp_selects").append(newDiv);
            },
            error: () => {
                // alert('Произошла ошибка!');
            }
        })
    });

    $(document).on("change", "select[id^='id_secondary_watercourse_temp_']", (event) => {
        // $(this).html('');
        // var parentID = $("#id_secondary_watercourse_temp").find(":selected").val();
        var parentID = event.currentTarget.value;
        var elementID = event.target.id.split('temp_')[1];

        $.ajax({
            type: "GET",
            url: `${MAIN_URL}/watercourses/children/${parentID}`,
            contentType: "application/json",
            success: (response) => {
                if (response.length == 0)
                    return

                if ($("div[id^='newSelect_']").length > 0) {
                    for (var i=parseInt(elementID) + 1; i < $("div[id^='newSelect_']").length; i++) {
                        $(`div[id^='newSelect_${i}']`).remove();
                    }
                }

                var newSelect = $(`<select class="form-control" multiple></select>`);
                newSelect.attr("id", `id_secondary_watercourse_temp_${$("select[id^='id_secondary_watercourse_temp_']").length}`);
                response.forEach(watercourse => {
                    newSelect.append(`<option value="${watercourse.id}">${watercourse.name}</option>`); 
                });

                var newDiv = $("<div>").attr('id', `newSelect_${$("select[id^='id_secondary_watercourse_temp_']").length}`);
                newDiv.append(newSelect);
                newDiv.append(`<button type="button" class="btn btn-info" data-target="${newSelect.attr('id')}">Выбрать выделенные</button>`)
                $("#temp_selects").append(newDiv);
            },
            error: () => {
                // alert('Произошла ошибка!');
            }
        })
    });

    $("#id_license").change((event) => {
        $.ajax({
            url: `${MAIN_URL}/watercourses_by_license/${event.target.value}`,
            method: 'GET',
            success: (response) => {
                $("#id_watercourse").html('');
                $("#id_wells").html('');
                $("#id_line").html('');

                $("#id_watercourse").append(`
                    <option selected disabled>Выберите водоток</option>
                `);

                response.forEach((line) => {
                    $("#id_watercourse").append(`
                        <option value="${line.id}">${line.name}</option>
                    `);
                });
            },
            error: (e) => {
                console.log("Error: ", e);
            }
        })
    });

    $("#id_watercourse").change((event) => {
        $.ajax({
            url: `${MAIN_URL}/lines/${event.currentTarget.value}`,
            method: 'GET',
            success: (response) => {
                $("#id_line").html('');
                $("#id_wells").html('');

                $("#id_line").append(`
                    <option selected disabled>Выберите линию</option>
                `);

                response.forEach((line) => {
                    $("#id_line").append(`
                        <option value="${line.id}">${line.name}</option>
                    `);
                });
            },
            error: (e) => {
                console.log("Error: ", e);
            }
        })
    });

    $("#id_line").change((event) => {
        $.ajax({
            url: `${MAIN_URL}/wells_by_line/${event.currentTarget.value}`,
            method: 'GET',
            success: (response) => {
                $("#id_wells").html('');

                response.forEach((well) => {
                    $("#id_wells").append(`
                        <option value="${well.id}">${well.name}</option>
                    `);
                });


            },
            error: (e) => {
                console.log("Error: ", e);
            }
        })
    });
});
