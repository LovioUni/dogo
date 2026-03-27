document.getElementById("btn-signin").addEventListener("click", login);

function login(){
    const email = document.getElementById("user-email").value;
    const password = document.getElementById("user-password").value;

    if(email === "") {
        Swal.fire({
            title: 'Correo no ingresado',
            text: 'Debe ingresar un correo.',
            icon: 'warning',
            confirmButtonText: 'Aceptar'
        });
        return;
        //TO DO: Ponerlo con sweet alert como en signup.js
    }

    if(password === "") {
        Swal.fire({
            title: 'Contraseña no ingresada',
            text: 'Debe ingresar una contraseña.',
            icon: 'warning',
            confirmButtonText: 'Aceptar'
        });
        return;
        //TO DO: Ponerlo con sweet alert como en signup.js
    }

    const data = {
        email: email,
        password: password
    }

    fetch('api/login', {
        method:"POST",
        headers: { "Content-Type": "application/json"},
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        if(result.success){
            window.location.href = "/welcome";
        } else {
            alert("sus datos no son correctos")
        }
    })
    .catch(error => {
        console.error(error);
    });
}