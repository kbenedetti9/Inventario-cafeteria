function obtenerValoresusuario(e) {
    var fila = e.target.parentNode;
    let idUsuario = fila.children[0].innerHTML
    let nombreUsuario = fila.children[1].innerHTML
    let correoUsuario = fila.children[2].innerHTML
    let Usuario = fila.children[3].innerHTML
    cargarValoresusuario(idUsuario,nombreUsuario,correoUsuario,Usuario);
    let id = document.getElementById("ID_usuario");
    id.readOnly = true;
}

function cargarValoresusuario(idValor,nombreValor,correoValor,usuarioValor) {
    let id = document.getElementById("ID_usuario");
    let nombre = document.getElementById("nombre_usuario");
    let correo = document.getElementById("correo_electronico");
    let usuario = document.getElementById("Usuario");
    id.value = parseInt(idValor);
    nombre.value = nombreValor;
    correo.value = correoValor;
    usuario.value = usuarioValor;
}