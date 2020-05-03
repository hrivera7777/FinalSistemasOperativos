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
});

