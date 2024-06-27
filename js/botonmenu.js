//--------ACTIVO BOTON EN MENU DE RESTAURANTE--------------//

   
// Seleccionar el botón "Mostrar Botón" por su ID
var botonMostrar = document.getElementById("menu-1");
// Seleccionar el botón que se mostrará por su ID
var boton = document.getElementById("aparezco");
// Agregar un evento de clic al botón "Mostrar Botón"
botonMostrar.addEventListener("click", function() {
    // Si el botón está oculto, mostrarlo; de lo contrario, ocultarlo
    if (boton.style.display === "none") {
        boton.style.display = "block";
    } else {
        boton.style.display = "none";
    }
});

//-----------------
var botonMostrar2 = document.getElementById("menu-2");
var boton2 = document.getElementById("aparezco2");
botonMostrar2.addEventListener("click", function() {
    if (boton2.style.display === "none") {
        boton2.style.display = "block";
    } else {
        boton2.style.display = "none";
    }});

//-----------------
var botonMostrar3 = document.getElementById("menu-3");
var boton3 = document.getElementById("aparezco3");
botonMostrar3.addEventListener("click", function() {
    if (boton3.style.display === "none") {
        boton3.style.display = "block";
    } else {
        boton3.style.display = "none";
    }});

    //-----------------
var botonMostrar4 = document.getElementById("menu-4");
var boton4 = document.getElementById("aparezco4");
botonMostrar4.addEventListener("click", function() {
    if (boton4.style.display === "none") {
        boton4.style.display = "block";
    } else {
        boton4.style.display = "none";
    } });

   
//-----------------
var botonMostrar5 = document.getElementById("menu-5");
var boton5 = document.getElementById("aparezco5");
botonMostrar5.addEventListener("click", function() { 
    if (boton5.style.display === "none") {
    boton5.style.display = "block";
} else {
    boton5.style.display = "none";
} });

    //-----------------
var botonMostrar6 = document.getElementById("menu-6");
var boton6 = document.getElementById("aparezco6");
botonMostrar6.addEventListener("click", function() { 
    if (boton6.style.display === "none") {
    boton6.style.display = "block";
} else {
    boton6.style.display = "none";
} });