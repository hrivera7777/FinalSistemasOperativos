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

    var continar=document.getElementById("continue").value;

    $('#PaP').submit(function (e) {
        e.preventDefault();
        
        $.ajax({
            url: $(this).attr('action'),
            type: $(this).attr('method'),
            data: $(this).serialize(),

            success: function(json){
                console.log(json)
                
               if(continar == 'True'){

                $('#ModalPaP').modal('show');
                document.write(json);

               }

               else{
                document.write(json);

               }
               /*document.write(json);

               console.log(json.actiModal)*/
              
               
               //if(json.){

               //}

                //console.log('hi');
            }
        });
    });


    
    

    $('#formPaP').submit(function (e) {
        e.preventDefault();
        $('#modaLPaP').modal('hide');    
        $.ajax({
            url: $(this).attr('action'),
            type: $(this).attr('method'),
            data: $(this).serialize(),

            success: function(json){
                if (continar == 'True'){
                $('#ModalparaLeer').modal('show');
                document.write(json);
               }
               else{
                $('#ModalparaLeer').modal('hide'); 
                document.write(json);
               }
               
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
               if (continar == 'True'){
                $('#ModalparaLeer').modal('show');
               }
               else{
                $('#ModalparaLeer').modal('hide'); 
               }
               
                
                //console.log('hi');
            }
        });
    });
    */

});
