/**
 * @param {any} inputElement The input element that need to set as error.
 * @param {string} message Text about error information.
 */
function setInputError(inputElement, message) {
    console.log('inputElement:', inputElement);
    inputElement.classList.add("form__input--error");
    inputElement.parentElement.querySelector(".form__input-error-message").textContent = message;
}

/**
 * @param {Element} inputElement The input element that need to clear error.
 */
function clearInputError(inputElement) {
    inputElement.classList.remove("form__input--error");
    inputElement.parentElement.querySelector(".form__input-error-message").textContent = "";
}

let result;

function successfullySignup() {
    document.getElementById("email").value = "";
    document.getElementById("first_name").value = "";
    document.getElementById("last_name").value = "";
    document.getElementById("password1").value = "";
    document.getElementById("password2").value = "";
    document.getElementById("blood type").value = "";
    document.getElementById("jobs").value = "";
    document.getElementById("cyberWareSN").value = "";

    window.location.href = "../templates/login.html";
}

document.addEventListener("DOMContentLoaded", () => {

    const createAccountForm = document.querySelector("#createAccount")
    const accountInfo = document.querySelector("#accountInfo")
    const moreInfo = document.querySelector("#moreInfo")

    createAccountForm.addEventListener("submit", evt => {
        evt.preventDefault();
        let username = document.getElementById("username").value;
        let email = document.getElementById("email").value;
        let first_name = document.getElementById("first_name").value;
        let last_name = document.getElementById("last_name").value;
        let password = document.getElementById("password1").value;
        let bloodType = document.getElementById("blood type").value;
        let job = document.getElementById("jobs").value;
        let sn = document.getElementById("cyberWareSN").value;
        signupData(username, email, first_name, last_name, password, job, bloodType, sn).then(() => {
            if (result === "This serial number is not exist!" || result === "This serial number is already signed up!")
                setInputError(document.getElementById("cyberWareSN"), result);
            else if (result === "This email is already signed up!") {
                accountInfo.classList.remove("form--hidden");
                moreInfo.classList.add("form--hidden");
                setInputError(document.getElementById("email"), result)
            } else if (result === "signup successful")
                successfullySignup()
            result = "";
        });
    })

    createAccountForm.addEventListener("submit", evt => {
        evt.preventDefault()
    })

    document.querySelectorAll(".form__input").forEach(inputElement => {

        document.querySelector("#nextToMoreInfo").addEventListener("click", e => {
            e.preventDefault();
            accountInfo.classList.add("form--hidden");
            moreInfo.classList.remove("form--hidden");
        });

        document.querySelector("#backToSignup").addEventListener("click", e => {
            e.preventDefault();
            accountInfo.classList.remove("form--hidden");
            moreInfo.classList.add("form--hidden");
        });

        inputElement.addEventListener("blur", evt => {
            if (evt.target.id === "email" && !(/^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/.test(evt.target.value))) {
                setInputError(inputElement, "You have entered an invalid email address!");
            }
            let password1 = document.getElementById("password1");
            let password2 = document.getElementById("password2");
            if (evt.target.id === "password2" && password1.value !== password2.value) {
                setInputError(inputElement, "Password does not match")
            }
        });

        inputElement.addEventListener("input", () => {
            clearInputError(inputElement);
        })
    });

})
