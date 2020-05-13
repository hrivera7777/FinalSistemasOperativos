$(document).ready(function () {

    $('#eject').submit(function (e) {
        e.preventDefault();

        $.ajax({
            url: $(this).attr('action'),
            type: $(this).attr('method'),
            data: $(this).serialize(),

            success: function(json){
               
               document.write(json);

                //console.log('hi');
            }
        });
    });


});
