$(document).ready(() => {
    const URL = 'http://localhost:8000';

    $("#generateMineBtn").click(() => {
        var selectedWells = $('#id_wells').val();

        if (selectedWells == null){
            $("#errorModal").modal('show');
            return
        }

        // for (let i = 0; i < array.length; i++) {
        //     const element = array[i];
            
        // }

        var mineImageData = JSON.stringify({
            'wells': selectedWells.map(eachID => Number(eachID)),
        });

        $.ajax({
            url: 'http://localhost:8000/mine/images/add',
            method: "POST",
            dataType: 'json',
            contentType: "application/json",
            data: mineImageData,
            success: (response) => {
                $('#img').attr('src', `/${response.img}`);
            },
            error: (error) => {
                console.log("ERROR: ", error);
            }
        });
    });
});
