$(document).ready(function () {
    console.log('termino de cargar');
    this.subir = function () {
        $('#btnAbrir').addClass('displayNone');
        console.log('here');

        //logica

        $('#btnUp').removeClass('displayNone');
    };

    $('#myModal').on('shown.bs.modal', function () {
        $('#myInput').trigger('focus')
    });
    let bandera = false;
    this.showHidden=function (){
        if (bandera) {
     $('#grande3').removeClass('hidden');

     } else {
        $('#grande3').addClass('hidden');
     }
        bandera = !bandera;
   };
});

