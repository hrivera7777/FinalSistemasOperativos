$(document).ready(function () {

    //funciones para ejecución normal 

    $('#eject').submit(function (e) {
        e.preventDefault();

        $.ajax({
            url: $(this).attr('action'),
            type: $(this).attr('method'),
            data: $(this).serialize(),

            success: function (json) {
                //console.log(json);
                /*
               if(json.actiModal){

                $('#ModalparaLeer').modal('show');
                
                //json.actiModal = false;

               }

               else{
                document.write(json);

               }*/
                document.write(json);
                //$('#ingresarValorTeclado').addClass('hidden');
                $('#btnPaso').addClass('hidden');
                $('#instrSgtPaso').addClass('hidden');

                //console.log(json.actiModal);


                //if(json.){

                //}

                //console.log('hi');
            }
        });
    });



    //funciones para paso a paso


    $('#PaP').submit(function (e) {
        e.preventDefault();
        //console.log(window.location.href)
        // mientras $('#btnsgtePaso').removeClass('hidden');
        //$('#ModalPaP').modal('show');

        $.ajax({
            url: $(this).attr('action'),
            type: $(this).attr('method'),
            data: $(this).serialize(),

            success: function (json) {
                //console.log(json)
                var continar = document.getElementById("continue").value;
                console.log(continar);
                if (continar === "True") {
                    console.log('entre aqui if');
                    document.write(json);
                    $('#btnPaso').removeClass('hidden');
                    $('#instrSgtPaso').removeClass('hidden');



                    
                    //$('#btnsgtePaso').removeClass('hidden');
                    //$('#ModalPaP').modal('show');
                    //$('#myModal').on('shown.bs.modal', function () { /*scrip para la ventada modal */
                        //$('#myInput').trigger('focus')
                        
                            //$('#ModalPaP').modal('show');
                      
                        //document.getElementById('btnSgte').click();
                    //});

                    //$('#btnsgtePaso').removeClass('hidden');

                }

                else {
                    console.log('entre aqui else');
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

    /*20-05-2020
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
     20-05-2020
     */

    //window.onload=MostrarBtnPaP;


    //var formPaP=document.getElementById("formPaP")

    
     nombreFuncion = function () { //'#formPaP' //formPaP
     //submitFormPaP = function (e){ //(e){
         $('#ModalPaP').modal('hide'); 
         console.log('entro al metodo');
         //e.preventDefault();
         console.log('entre aqui funcion');
          //podria quitarse
        // $('#btnsgtePaso').removeClass('hidden');
         //$('#ModalPaP').modal('hide');  
         /*
         var continar = document.getElementById("continue").value;
                 if (continar == "True"){
                     console.log('entre aqui if formPaP');
                     
                    
                 //document.write(json);
                 //$('#btnsgtePaso').removeClass('hidden');
                 $('#ModalPaP').modal('show');
                 //nombreFuncion();
                 setTimeout(() => {
                //    nombreFuncion();
                 }, 2000);
                
                 
                 
                }
                else{
                 console.log('entre aqui else');
                 
                 //document.write(json);
                 $('#ModalPaP').modal('hide'); 
                }
                */
 
 
 
 
         
         $.ajax({
             url: $(this).attr('action'),
             type: $(this).attr('method'),
             data: $(this).serialize(),
 
             success: function(json){
                 //$('#btnsgtePaso').removeClass('hidden');
                 //$('#ModalPaP').modal('show'); 
                 var continar = document.getElementById("continue").value;
                 //
                 //document.getElementById('cual').innerHTML = json;
                 
                 //$('#ModalPaP').modal('show');
                 //setTimeout(() => {
                   //  document.write(json);
                     
                 //}, 500);
                 
                 if (continar == "True"){
                     console.log('entre aqui if formPaP');
                     
                    
                 //$('#btnsgtePaso').removeClass('hidden');
                 
                 
                 
                }
                else{
                 console.log('entre aqui else');
                 
                
                // $('#ModalPaP').modal('hide'); 
                }
                
                //$('#btnsgtePaso').removeClass('hidden');
                //document.getElementById("formPaP").submit();
                
                 //console.log('hi');
             }
         });
     //};
      };

 /////////////////////////////////////////////////////estamos aquí ///////////////////

    $('#formPaP').submit(function (e) { //'#formPaP' //formPaP
    //submitFormPaP = function (e){ //(e){
       // $('#ModalPaP').modal('hide'); 
        console.log('entro al metodo');
        e.preventDefault();
        console.log('entre aqui funcion');
       
        $.ajax({
            url: $(this).attr('action'),
            type: $(this).attr('method'),
            data: $(this).serialize(),

            success: function(json){
                var continar = document.getElementById("continue").value;
                document.write(json);

                if (continar == "True"){
                    console.log('entre aqui if formPaP');
                    
                    
                   
                //$('#btnsgtePaso').removeClass('hidden');
                
                
                
               }
               else{
                console.log('entre aqui else');
                
               
                //$('#ModalPaP').modal('hide'); 
               }
               
               //$('#btnsgtePaso').removeClass('hidden');
               //document.getElementById("formPaP").submit();
               
                //console.log('hi');
            }
        });
    //};
     });


     
     /*
     $('#leerTeclado').submit(function (e) { 
    //submitFormPaP = function (e){ //(e){
       // $('#ModalPaP').modal('hide'); 
        console.log('entro al metodo');
        e.preventDefault();
        console.log('entre aqui funcion');

        let l = document.getElementById('activarLeer').value;
                if (l == "True") {
                    console.log(l + "esto es L en if")
                    $('#ingresarValorTeclado').removeClass('hidden');
                // i++;
                }else if (l=="False"){
                    console.log(l + "esto es L en elif")
                    $('#ingresarValorTeclado').addClass('hidden');
                }
                else{
                    console.log(l + "esto es L en else")
                    $('#ingresarValorTeclado').removeClass('hidden');
                }


        
        $.ajax({
            url: $(this).attr('action'),
            type: $(this).attr('method'),
            data: $(this).serialize(),

            success: function(json){
                var continar = document.getElementById("continue").value;
                document.write(json);

                
               
               //$('#btnsgtePaso').removeClass('hidden');
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

