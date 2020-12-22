function obtenerValores(e) {
    var fila = e.target.parentNode;
    let idValor = fila.children[0].innerHTML
    let nombreValor = fila.children[1].innerHTML
    let precioValor = fila.children[2].innerHTML
    let cantidadValor = fila.children[3].innerHTML
    let imagenValor = fila.children[4].innerHTML
    cargarValores(idValor, nombreValor, precioValor, cantidadValor, imagenValor);
    id.readOnly = true;
}

function cargarValores(idValor, nombreValor, precioValor, cantidadValor, imagenValor) {
    let id = document.getElementById("id");
    let nombre = document.getElementById("nombre");
    let precio = document.getElementById("precio");
    let cantidad = document.getElementById("cantidad");
    let imagen = document.getElementById("img");
    id.value = idValor.toString()
    nombre.value = nombreValor;
    precio.value = parseInt(precioValor);
    cantidad.value = parseInt(cantidadValor);
    imagen.src = "../static/Imagenes/" + imagenValor
}

function mostrarImagen() {
    let image = document.getElementById("img");
    var num = Math.floor(Math.random() * 3) + 1
    console.log(num);
    if (num == 1) {
        image.src = "../static/Imagenes/papitas.png"

    } else if (num == 2) {
        image.src = "../static/Imagenes/chocolate.png"
    } else if (num == 3) {
        image.src = "../static/Imagenes/gaseosa.png"
    }
}


