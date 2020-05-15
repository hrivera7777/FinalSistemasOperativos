$(document).ready(function () {
    console.log('termino de cargar');
    this.subir = function () {
        $('#btnAbrir').addClass('displayNone');
        console.log('here');

        //logica

        $('#btnUp').removeClass('displayNone');
    };

    $('#myModal').on('shown.bs.modal', function () { /*scrip para la ventada modal */
        $('#myInput').trigger('focus')
    });


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
});

