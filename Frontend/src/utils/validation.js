import { MOST_COMMON_PASSWORDS, INPUT_LENGTH } from "./constants"

/**
 * Function that validates a user's name input
 * 
 * It will check whether the param is a string and whether the trimmed input is within the minimum and maximum length input, according to the constants set in utils/constants.js
 * 
 * @param {string} name 
 * @returns {object}
 * Returns an object:
 * obj.response {bool} will be false if name is invalid and true otherwise
 * obj.message {string} will document the problem in case name is invalid
 * @example
 * nameValidation("John") => { response: true, message: "" }
 */
export function nameValidation(name) {
    if (typeof name !== "string") {
        return { response: false, message: "Name must be a string." }
    } else if (name.trim().length < INPUT_LENGTH.name.minValue || name.trim().length > INPUT_LENGTH.name.maxValue) {
        return { response: false, message: `Name must have between ${INPUT_LENGTH.name.minValue} and ${INPUT_LENGTH.name.maxValue} characters.` }
    } else {
        return { response: true, message: "" }
    }
}

/**
 * Function that validates a user's email input
 * 
 * It will check whether the param is a string and whether the trimmed input is within the minimum and maximum length input, according to the constants set in utils/constants.js
 * It will also check whether the input contains an @ character.
 * 
 * @param {string} email 
 * @returns {object}
 * Returns an object:
 * obj.response {bool} will be false if email is invalid and true otherwise
 * obj.message {string} will document the problem in case email is invalid
 * @example
 * emailValidation("John@example.com") => { response: true, message: "" }
 * emailValidation("hello") => { response: false, message: "Email format is not valid." }
 */
export function emailValidation(email) {
    if (typeof email !== "string") {
        return { response: false, message: "Email must be a string." }
    } else if (email.trim().length < INPUT_LENGTH.email.minValue || email.trim().length > INPUT_LENGTH.email.maxValue || !email.includes("@")) {
        return { response: false, message: "Email format is not valid." }
    } else {
        return { response: true, message: "" }
    }
}

/**
 * Function that validates a user's password input for signups
 * 
 * It will check whether the param is a string and whether the trimmed input is within the minimum and maximum length input, according to the constants set in utils/constants.js
 * It will also check whether the password contains 4 or more consecutive characters.
 * If the password has less than 15 characters, it will also check it against the most common passwords array defined in utils/constants.js
 * 
 * @param {string} password 
 * @returns {object}
 * Returns an object:
 * obj.response {bool} will be false if password is invalid and true otherwise
 * obj.message {string} will document the problem in case password is invalid
 * @example
 * passwordValidation("hiMyNameIsJohnAndImFromAlaska55") => { response: true, message: "" }
 * passwordValidation("password!") => { response: false, message: "Password provided in the list of most common passwords used." }
 */
export function passwordValidation(password) {
    if (typeof password !== "string") {
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

/**
 * Function that validates a user's password input for login
 * 
 * This is a simpler version than the passwordValidation function
 * Since it is assumed the user already has an account, new password rules such as checking for consecutive characters or validating against most common passwords are not used here.
 * 
 * It will check whether the param is a string and whether the trimmed input is within the minimum and maximum length input, according to the constants set in utils/constants.js
 * 
 * @param {string} password 
 * @returns {object}
 * Returns an object:
 * obj.response {bool} will be false if password is invalid and true otherwise
 * obj.message {string} will document the problem in case password is invalid
 * @example
 * passwordValidation("hiMyNameIsJohnAndImFromAlaska55") => { response: true, message: "" }
 * passwordValidationForLogin("password!") => { response: true, message: "" }
 * passwordValidationForLogin(123) => { response: false, message: "Password must be a string." }
 */
export function passwordValidationForLogin(password) {
    if (typeof password !== "string") {
        return { response: false, message: "Password must be a string." }
    } else if (password.trim().length < INPUT_LENGTH.password.minValue || password.trim().length > INPUT_LENGTH.password.maxValue) {
        return { response: false, message: `Passwords should have between ${INPUT_LENGTH.password.minValue} and ${INPUT_LENGTH.password.maxValue} characters. Please check your input.` }
    } else {
        return { response: true, message: "" }
    }
}