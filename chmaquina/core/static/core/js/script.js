$(document).ready(function () {
    console.log('terminó de cargar');

    this.subir = function () {
        $('#btnAbrir').addClass('displayNone');
        console.log('here');

        $('#btnUp').removeClass('displayNone');
    };


    $('#myModal').on('shown.bs.modal', function () { /*scrip para la ventada modal */
        $('#myInput').trigger('focus')
    });


    ///////////////////////////////////////////////////
    //activar la ventana para leer en ejecución normal
    let l = document.getElementById('activarLeer').value;
    if (l == "True") {
        console.log(l + "esto es L en if")
        $('#ingresarValorTeclado').removeClass('hidden');
        $('#ingresarValorTecladoPaP').addClass('hidden');

    }else if (l=="False"){
        console.log(l + "esto es L en elif")
        console.log(l=="True")
        $('#ingresarValorTeclado').addClass('hidden');
        $('#ingresarValorTecladoPaP').addClass('hidden');

    }

    else{
        console.log(l + "esto es L en else")
        $('#ingresarValorTeclado').removeClass('hidden');
        $('#ingresarValorTecladoPaP').addClass('hidden');
    }
    ///////////////////////////////////////////////////////// 
    ///////////////////////////////////////////////////////////////////////


    let i = document.getElementById('contadorPasos').value; // se trae el contador de pasos para saber si está en la primera linea del programa con paso a paso
    if (i == 0) {
        let a = document.getElementById('sgtpaso');
        a.value = 'sgtpaso';
        $('#btnPaso').addClass('hidden');
        $('#instrSgtPaso').addClass('hidden');
        $('#ingresarValorTecladoPaP').addClass('hidden');
    }

    

    ///////////////////////////////////////////////////
    //activar la ventana para leer en ejecución Paso a Paso
    let l2 = document.getElementById('activarLeerPaP').value;
    if (l2 == "True") {
        console.log(l + "esto es L2 en if")
        $('#ingresarValorTecladoPaP').removeClass('hidden');
        $('#btnPaso').removeClass('hidden');

    }else if (l2=="False" && i > 0 ){
        console.log(l + " - esto es L2 en elif")
        $('#ingresarValorTecladoPaP').addClass('hidden');
        
        let a = document.getElementById('sgtpaso');
        a.value = 'sgtpaso';
        $('#btnPaso').removeClass('hidden');
        $('#instrSgtPaso').removeClass('hidden');
    }
    else if (l2=="False"){
        console.log(l + " - esto es L2 en elif")
        $('#ingresarValorTecladoPaP').addClass('hidden');
        $('#btnPaso').addClass('hidden');
        $('#instrSgtPaso').addClass('hidden');
        $('#ingresarValorTecladoPaP').addClass('hidden');
     
    }
    else{
        console.log(l + " - esto es L2 en else")
        $('#ingresarValorTecladoPaP').addClass('hidden');
        $('#ingresarValorTecladoPaP').addClass('hidden');
    }




    let bandera = true;
    this.showHidden = function () {
        if (bandera) {
            $('#grande3').removeClass('hidden');

        } else {
            $('#grande3').addClass('hidden');
        }
        bandera = !bandera;
    };

    actionOpen = function () {
        document.getElementById('subirArchivoCh').click();
        let a = document.getElementById('btnAbrir');/*este abrir (muestra la ventana)*/
        $('input[type=file]').change(() => {
            let archivo = $('#subirArchivoCh').val();
            if (archivo !== '') {
                a.style = 'display : none;';
                document.getElementById('btnUp').style = 'display : block;'; /*este es el que envia el formulario*/
            }
            else {
                a.style = 'display : block;';
            }
        });
        return true;
    };



    actionEjc = function () {
        document.getElementById('ejecutar').click();

        return true;
    };


    actionPaP = function () {
        document.getElementById('subPaP').click();
        return true;
    };
    actionMostrarBtnPaP = function () {
        $('#btnsgtePaso').removeClass('hidden');

        return true;
    };



    modalparaPaP = function () {
        console.log('entro a la funcion');
        var continar = document.getElementById("continue").value;
        if (continar == "True") {
            console.log('entre aqui if modalparaPaP');
            $('#ModalPaP').modal('show');


        }
        else {
            console.log('entre aqui else');
            $('#ModalPaP').modal('hide');
        }
        return true;
    };


});

