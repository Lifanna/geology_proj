$(document).ready(() => {
    const MAIN_URL = "http://localhost:8000";

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
});
