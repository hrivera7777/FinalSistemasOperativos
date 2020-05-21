$(document).ready(function () {
    console.log('terminó de cargar');
    this.subir = function () {
        $('#btnAbrir').addClass('displayNone');
        console.log('here');

        //logica

        $('#btnUp').removeClass('displayNone');
    };

    $('#myModal').on('shown.bs.modal', function () { /*scrip para la ventada modal */
        $('#myInput').trigger('focus')
    });
    let i = document.getElementById('contadorPasos').value; // se trae el contador de pasos para saber si está en la primera linea del programa con paso a paso
    if (i == 0) {
        console.log(i)
        let a = document.getElementById('sgtpaso');
        a.value = 'sgtpaso';
        $('#btnPaso').addClass('hidden');
        $('#instrSgtPaso').addClass('hidden');
    }

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
            //console.log(archivo);
            if (archivo !== '') {

                //console.log('entro al if' + document.getElementById('subirArchivoCh').value);
                a.style = 'display : none;';
                document.getElementById('btnUp').style = 'display : block;'; /*este es el que envia el formulario*/
                //console.log('entro al click' + document.getElementById('subirArchivoCh').value);
            }
            else {
                //console.log('entro al else' + document.getElementById('subirArchivoCh').value);
                a.style = 'display : block;';
            }
        });


        //a.style = 'display : none;'; 





        return true;
    };

    actionEjc = function () {
        document.getElementById('ejecutar').click();

        return true;
    };


    actionPaP = function () {
        document.getElementById('subPaP').click();
        //$('#btnsgtePaso').removeClass('hidden');
        //document.getElementById('btnsgtePaso').style = 'display : block;';

        return true;
    };
    actionMostrarBtnPaP = function () {

        $('#btnsgtePaso').removeClass('hidden');
        //document.getElementById('btnsgtePaso').style = 'display : block;';

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

