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
        //console.log(window.location.href)
        $('#btnsgtePaso').removeClass('hidden');
        //$('#ModalPaP').modal('show');
        
        $.ajax({
            url: $(this).attr('action'),
            type: $(this).attr('method'),
            data: $(this).serialize(),

            success: function(json){
                //console.log(json)
                
               if(continar == "True"){
                   console.log('entre aqui if')

                document.write(json);
                $('#btnsgtePaso').removeClass('hidden');
               // $('#ModalPaP').modal('show');
                $('#btnsgtePaso').removeClass('hidden');

               }

               else{
                console.log('entre aqui else')
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

    /*
    $('#btnPaso').click(function (e) {
        e.preventDefault();
        document.getElementById("formPaP").submit();
        $('#btnsgtePaso').removeClass('hidden');
        $('#ModalPaP').modal('hide');  
        
        console.log('entre aqui funcion')  
        $.ajax({
            url: $(this).attr('action'),
            type: $(this).attr('method'),
            data: $(this).serialize(),

            success: function(json){
                $('#btnsgtePaso').removeClass('hidden');
                $('#ModalPaP').modal('show');
                if (continar == "True"){
                    console.log('entre aqui if formPaP')
                    
                   
                document.write(json);
                $('#btnsgtePaso').removeClass('hidden');
                $('#ModalPaP').modal('show');
                
                
               }
               else{
                console.log('entre aqui else')
                
                document.write(json);
                $('#ModalPaP').modal('hide'); 
               }
               
                //console.log('hi');
            }
        });
    });
    */
   
   var sgt= window.location.href;
    MostrarBtnPaP = function () {
    if (sgt == "http://127.0.0.1:8000/?sgtpaso=sgtpaso" ){
        console.log("entre aqui funcion monstrar")
        $('#btnsgtePaso').removeClass('hidden');

    }
    
    //document.getElementById('btnsgtePaso').style = 'display : block;';

    return true;
    };

    MostrarBtnPaP();


    //window.onload=MostrarBtnPaP;
    /*
    var formPaP=document.getElementById("formPaP")

    
    $(formPaP).submit(function (e) { //'#formPaP'
    //submitFormPaP = function (e){ //(e){
        console.log('entro al metodo')
        //e.preventDefault();
         //podria quitarse
        $('#btnsgtePaso').removeClass('hidden');
        $('#ModalPaP').modal('hide');  
        
        console.log('entre aqui funcion')  
        $.ajax({
            url: $(this).attr('action'),
            type: $(this).attr('method'),
            data: $(this).serialize(),

            success: function(json){
                $('#btnsgtePaso').removeClass('hidden');
                $('#ModalPaP').modal('show');
                if (continar == "True"){
                    console.log('entre aqui if formPaP')
                    
                   
                //document.write(json);
                $('#btnsgtePaso').removeClass('hidden');
                $('#ModalPaP').modal('show');
                
                
               }
               else{
                console.log('entre aqui else')
                
                //document.write(json);
                $('#ModalPaP').modal('hide'); 
               }
               $('#btnsgtePaso').removeClass('hidden');
               //document.getElementById("formPaP").submit();
               
                //console.log('hi');
            }
        });
    //};
     });
*/


    

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

