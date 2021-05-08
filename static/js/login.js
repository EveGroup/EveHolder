function setFormMessage(formElement, type, message) {
    const messageElement = formElement.querySelector(".form__message");

    messageElement.textContent = message;
    messageElement.classList.remove("form__message--success", "form__message--error");
    messageElement.classList.add(`form__message--${type}`);
}

let result;

async function loginData(email, password) {
    await fetch('http://158.108.182.10:3000/login_post', {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            email: email,
            password: password
        })
    })
        .then((response) => response.json())
        .then(value => {
            result = value.result
            console.log("result", result)
        })
        .catch(reason => console.log("error", reason));
}

document.addEventListener("DOMContentLoaded", () => {
    const loginForm = document.querySelector("#login");

    loginForm.addEventListener("submit", evt => {
        evt.preventDefault();
        let email = document.getElementById("email").value
        let password = document.getElementById("password").value
        loginData(email, password).then(r => {
            if (result === "Check your login details and try again." || result === "Wrong password")
                setFormMessage(loginForm, "error", result);
            if (result === "login successfully") {
                setFormMessage(loginForm, "success", result);
                document.getElementById("password").value = "";
                window.location.href = "../templates/info.html?email=" + email;
                document.getElementById("email").value = "";
            }
            result = "";
        });
    });

    // let submitLogin = document.getElementById('submitLogin')
    // let url = new URL('https://')
    // let params = new URLSearchParams(url.search.slice(1))
    //
    // submitLogin.onclick = function (click) {
    //     params.append("email", "email from form")
    // }
    //
    // loginForm
})
