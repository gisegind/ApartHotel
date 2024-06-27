$(document).ready(function(){

    $('#login-btn').click(function(){
        $('.login-form').toggleClass('active');
        $('#menu-btn').removeClass('fa-times');
        $('.navbar').removeClass('active');
    });

    $('#menu-btn').click(function(){
        $(this).toggleClass('fa-times');
        $('.navbar').toggleClass('active');
        $('.login-form').removeClass('active');
    })

    $(window).on('scroll load', function(){

        $('#menu-btn').removeClass('fa-times');
        $('.navbar').removeClass('active');
        $('.login-form').removeClass('active');

        $('section').each(function(){

            let top = $(window).scrollTop();
            let height = $(this).height();
            let offset = $(this).offset().top - 200;
            let id = $(this).attr('id');
    
            if(top >= offset && top < offset + height){
                $('.navbar a').removeClass('active');
                $('.navbar').find(`[href="#${id}"]`).addClass('active');
            }
    
        });

    });

});


// --------------------------------------------------------
// Formulario Contacto
// --------------------------------------------------------

    //getElementByID selecciona el elemento del formulario con el id "formulario-consulta" y añade un event listener que estará atento a cuando se envíe el formulario. 
    // Cuando se envíe el formulario, se ejecutará la función validarFormulario
    //La llamada a event.preventDefault() evita que el formulario se envíe de forma convencional y permite que la validación se realice mediante JavaScript.
    //Creo una expresión para poder validar que los caracteres de nombre sean correctos
    const expresiones = {
        nombre: /^[a-zA-ZÀ-ÿ\s]{1,40}$/ // Letras y espacios, pueden llevar acentos.
    }
    

    document.getElementById("formulario-consulta").addEventListener("submit", function(event) {
        event.preventDefault();
        validarFormulario();
    });

  
    function validarFormulario() {
        let nameInput = document.getElementById("contact-name").value;
        let emailInput = document.getElementById("contact-email").vale;
        let validacionElement = document.getElementById("validacion");   
         //VALIDA QUE CARACTERES DE NOMBRE SEAN CORRECTOS Y TANTO NOMBRE COMO CORREO NO PUEDEN SER CAMPOS VACIOS
         if ( (!expresiones.nombre.test(nameInput) || nameInput === '' ) ||  emailInput === '' ){
            validacionElement.textContent = "Nombre incorrecto o incompleto";  
            validacionElement.classList.remove("validacionCorrecta");
            validacionElement.classList.add("validacionError");     
        } else {
            validacionElement.textContent = "Formulario enviado correctamente";
            validacionElement.classList.remove("validacionError");
            validacionElement.classList.add("validacionCorrecta");
        }
        // Voy a limpiar el span para cargar otra vez los datos si me equivoque
    var limpiarBoton = document.getElementById("orderButton1");

    // Agregar un event listener al botón "Limpiar Formulario" para ocultar el span cuando se haga clic en él
    limpiarBoton.addEventListener("click", function () {
        // Selecciono el span por su ID
        var spanValidacion = document.getElementById("validacion");

        // Ocultar el span si el mensaje es de datos incorrectos
        if ((validacionElement.textContent == "Nombre incorrecto o incompleto") || (validacionElement.textContent == "Email incompleto")) {
            spanValidacion.style.display = "none";
        }
        location.reload();
    });
    }

//----- VALIDA CONDICIONES PARA SUBIR IMAGEN
document.getElementById('formularioImagen').addEventListener('submit', function(event) {
    event.preventDefault(); // Evitar el envío predeterminado del formulario

    var imagen = document.getElementById('imagen').value;
    var opcion1 = document.getElementById('opcion1').checked;
    var opcion2 = document.getElementById('opcion2').checked;
    var opcion3 = document.getElementById('opcion3').checked;
    var acepto = document.getElementById('terminos').checked;

    if (imagen === '') {
        alert('Por favor, selecciona una imagen.');
        return false;
    }

    if (!opcion1 && !opcion2 && !opcion3) {
        alert('Por favor, selecciona una red social.');
        return false;
    }

    if (!acepto) {
        alert('Por favor, acepta los términos y condiciones.');
        return false;
    }

    mostrarMensajeExito();
});

function mostrarMensajeExito() {
    document.getElementById('formularioImagen').reset();
    document.getElementById('mensajeExito').style.display = 'block';
}




    