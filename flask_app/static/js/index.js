
// Estoy obteniendo el formulario de login 
var formlogin = document.getElementById('formlogin'); 
// Creao un lisener que me escuche que cuando alguien quiera ingresar el formulario se detenga
// haga algun preventing form (prevenir accion por defecto)
formlogin.onsubmit= function(event) {
    event.preventDefault(); /* previene el comportamiento por default de mi formulario */
    //creamos una variable con todos los datos del formulario 
    var formulario= new FormData(formlogin); 

    fetch("/login", {method: 'POST', body: formulario})
        //cuando tengas la respuesta solo necesito la respuesta en json 
        .then(response => response.json())
        // Una vez lo tengas esa rpta json obtenida yo la recibo y la pongo data
        .then(data => {
            //hago un console.log para ver mi data 
            console.log(data)
            //si acaso del la data que tengo el mensaje es igual a correcto
            //entonces redirigeme a dashboard
            if(data.message =="correcto"){
                window.location.href="/dashboard";
            }
            // en el html tenemos un id con mensajeAlerta
            var mensajeAlerta = document.getElementById('mensajeAlerta');
            mensajeAlerta.innerText=data.message;
            //poner las alertas de mensaje mas "bonitas"
            mensajeAlerta.classList.add('alert');
            mensajeAlerta.classList.add('alert-danger');
        });
         
    }