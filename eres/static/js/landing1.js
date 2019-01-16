$(document).ready(function(){

    var ancho = $(window).width(),
    noticias = $("#noticias"),
    boton = $("#boton"),
    icono = $('#icono');

    //calcular ancho

    if (ancho < 800){
        noticias.hide();
    }
    if (ancho > 800){
        icono.hide();
    }

    boton.on('click', function(e){
        noticias.slideToggle();
    });

    $(window).on('resize', function(){
        if($(this).width() > 800){
            noticias.show();
            icono.hide();
        }
        else{
            noticias.hide();
            icono.show();
        }
    });


    //modal
    var cerrar = $('#cerrar'),
    abrir = $('#abrir'),
    modal = $('.modal');

    abrir.on('click', function(e){
        abrirmodal();
    });

    cerrar.on('click', function(e){
        cerrarmodal();
    });

    function abrirmodal() {
        modal.slideDown();
    }

    function cerrarmodal() {
        modal.slideUp('fast');
    }

    //modal nueva publicacion

    var abrir1 = $('.nueva'),
    modal1 = $('.modal1'),
    cerrar1 = $('.cerrar1');

    function abrirmodal1() {
        modal1.slideDown();
    }

    function cerrarmodal1() {
        modal1.slideUp('fast');
    }


    abrir1.on('click', function(e){
        abrirmodal1();
    });

    cerrar1.on('click', function(e){
        cerrarmodal1();
    });
    
    //pestanias

    $(".tab1").addClass('activo');
    $(".secciones article").hide();
    $("#tab1").show();

    $("ul.tablas li a").click(function(){
        $("ul.tablas li a").removeClass('activo');
        $(this).addClass('activo');
        $(".secciones article").hide();

        var activeTab = $(this).attr('href');
        console.log(activeTab);
        $(activeTab).show();
        return false; 
    });


    // favorito
    /*var fl = true;

    $("#prueba").on('click',function(){
try {
    console.log("volvi a entrar");
    if(fl){
       console.log("entre cuando era verdadero");
        fl=false;
        $("#prueba").addClass('fas');
        $("#prueba").removeClass('far');
        console.log("sali ileso");
    }else{
        fl=true;
        console.log("entre cuando era falso");
        $("#prueba").addClass('far');
        $("#prueba").removeClass('fas');
    }
} catch (error) {
    console.log(error)
}

    
        console.log(fl);
    })*/

   /* var prueba = $('#prueba');
    var poner = false;
    var contador = 0;

    prueba.on('click', function(e){

        console.log("entre" + contador );
        contador ++;

        if(poner == false){
            prueba.toggleClass('fas');
            poner = true;
            console.log(poner);
        }

        else{
            prueba.toggleClass('far');
            poner = false;
            console.log(poner);
        }
        console.log("este es el final");
        console.log(poner);
    });*/


});