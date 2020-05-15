$(document).ready(function () {

    $('#eject').submit(function (e) {
        e.preventDefault();
        
        $.ajax({
            url: $(this).attr('action'),
            type: $(this).attr('method'),
            data: $(this).serialize(),

            success: function(json){
                console.log(json)
                /*
               if(json.actiModal){

                $('#ModalparaLeer').modal('show');
                
                //json.actiModal = false;

               }

               else{
                document.write(json);

               }*/
               document.write(json);

               console.log(json.actiModal)
              
               
               //if(json.){

               //}

                //console.log('hi');
            }
        });
    });

    /*
    $('#modaLeer').submit(function (e) {
        e.preventDefault();
        $('#ModalparaLeer').modal('hide');    
        $.ajax({
            url: $(this).attr('action'),
            type: $(this).attr('method'),
            data: $(this).serialize(),

            success: function(json){
                //json.actiModal = false;
               //document.write(json);
                
                //console.log('hi');
            }
        });
    });*/


});
