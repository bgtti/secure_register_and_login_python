import { MOST_COMMON_PASSWORDS, INPUT_LENGTH } from "./constants"

export function nameValidation(name) {
    if (typeof name !== 'string') {
        return { response: false, message: "Name must be a string." }
    } else if (name.trim().length < INPUT_LENGTH.name.minValue || name.trim().length > INPUT_LENGTH.name.maxValue) {
        return { response: false, message: `Name must have between ${INPUT_LENGTH.name.minValue} and ${INPUT_LENGTH.name.maxValue} characters.` }
    } else {
        return { response: true, message: "" }
    }
}

export function emailValidation(email) {
    if (typeof email !== 'string') {
        return { response: false, message: "Email must be a string." }
    } else if (email.trim().length < INPUT_LENGTH.email.minValue || email.trim().length > INPUT_LENGTH.email.maxValue || !email.includes("@")) {
        return { response: false, message: "Email format is not valid." }
    } else {
        return { response: true, message: "" }
    }
}

export function passwordValidation(password) {
    if (typeof password !== 'string') {
        return { response: false, message: "Password must be a string." }
    } else if (password.trim().length < INPUT_LENGTH.password.minValue || password.trim().length > INPUT_LENGTH.password.maxValue) {
        return { response: false, message: `Password must have between ${INPUT_LENGTH.password.minValue} and ${INPUT_LENGTH.password.maxValue} characters.` }
    } else if (/(\S)\1{3,}/.test(password)) {
        // Check if the password contains the same character 4 or more times
        return { response: false, message: "Password cannot contain the same character 4 or more times consecutively." };
    } else {
        if (password.trim().length < 15 && MOST_COMMON_PASSWORDS.some(commonPwd => password.toLowerCase().includes(commonPwd))) {
            return { response: false, message: "Password provided in the list of most common passwords used." }
        } else {
            return { response: true, message: "" }
        }
    }
}

//A simpler version of the passwordValidation function.
//Used for log-in - so new password rules do not need to be checked
export function passwordValidationForLogin(password) {
    if (typeof password !== 'string') {
        return { response: false, message: "Password must be a string." }
    } else if (password.trim().length < INPUT_LENGTH.password.minValue || password.trim().length > INPUT_LENGTH.password.maxValue) {
        return { response: false, message: `Passwords should have between ${INPUT_LENGTH.password.minValue} and ${INPUT_LENGTH.password.maxValue} characters. Please check your input.` }
    } else {
        return { response: true, message: "" }
    }
}