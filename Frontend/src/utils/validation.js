import { MOST_COMMON_PASSWORDS, RESERVED_NAMES, INPUT_LENGTH } from "./constants"

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
        return { response: false, message: "Name must be a string." };
    }

    const trimmedName = name.trim();

    if (
        trimmedName.length < INPUT_LENGTH.name.minValue ||
        trimmedName.length > INPUT_LENGTH.name.maxValue
    ) {
        return {
            response: false,
            message: `Name must have between ${INPUT_LENGTH.name.minValue} and ${INPUT_LENGTH.name.maxValue} characters.`
        };
    }

    const lowerCaseName = trimmedName.toLowerCase();

    for (const reserved of RESERVED_NAMES) {
        if (lowerCaseName.includes(reserved.toLowerCase())) {
            return {
                response: false,
                message: `Name must not contain '${reserved}' because this is a reserved word.`
            };
        }
    }

    return { response: true, message: "" };
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
    // Validate type
    if (typeof email !== "string") {
        return { response: false, message: "Email must be a string." }
    }
    // Validate length
    const trimmedEmail = email.trim();
    if (trimmedEmail.length < INPUT_LENGTH.email.minValue || trimmedEmail.length > INPUT_LENGTH.email.maxValue) {
        return { response: false, message: `An email should be between ${INPUT_LENGTH.email.minValue} and ${INPUT_LENGTH.email.maxValue} characters.` }
    }
    // Validate format with regex
    const emailRegex = /^[^@]+@[^@]+$/; // Ensures at least one character before and after @
    if (!emailRegex.test(trimmedEmail)) {
        return { response: false, message: "Email format is not valid." };
    }
    return { response: true, message: "" }
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
 * passwordValidationSimplified("password!") => { response: true, message: "" }
 * passwordValidationSimplified(123) => { response: false, message: "Password must be a string." }
 */
export function passwordValidationSimplified(password) {
    if (typeof password !== "string") {
        return { response: false, message: "Password must be a string." }
    } else if (password.trim().length < INPUT_LENGTH.password.minValue || password.trim().length > INPUT_LENGTH.password.maxValue) {
        return { response: false, message: `Passwords should have between ${INPUT_LENGTH.password.minValue} and ${INPUT_LENGTH.password.maxValue} characters.` }
    } else {
        return { response: true, message: "" }
    }
}

/**
 * Function that validates a user's otp input for login
 * 
 * @param {string} otp
 * @returns {object}
 * Returns an object:
 * obj.response {bool} will be false if otp is invalid and true otherwise
 * obj.message {string} will document the problem in case otp is invalid
 * @example
 * otpValidation("523694") => { response: true, message: "" }
 * otpValidation(123) => { response: false, message: "Check OTP format." }
 */
export function otpValidation(otp) {
    if (typeof otp !== "string") {
        return { response: false, message: "Check OTP format." }
    } else if (/\s/.test(otp)) {
        return { response: false, message: "OTP should not contain spaces." };
    } else if (otp.length < INPUT_LENGTH.otp.minValue || otp.length > INPUT_LENGTH.otp.maxValue) {
        return { response: false, message: `OTP does not meet length standards.` }
    } else if (!/^[a-zA-Z0-9]+$/.test(otp)) {
        return { response: false, message: `OTP contains invalid characters` }
    } else {
        return { response: true, message: "" }
    }
}

/**
 * Function that validates a date in string format to make sure it complies with the format "YYYY-MM-DD".
 * 
 * It will return true if the date format is valid, and false otherwise
 * 
 * @param {string} dateString // format "YYYY-MM-DD"
 * @returns {boolean}
 * @example
 * console.log(isValidDateFormat("2022-02-23")); // Output: true
 * console.log(isValidDateFormat("2022-0223")); // Output: false
 */
export function validateDateFormat(dateString) {
    if (typeof dateString !== "string") {
        return false;
    }
    const dateFormatRegex = /^\d{4}-\d{2}-\d{2}$/;
    return dateFormatRegex.test(dateString);
}

/**
 * Function that sanitizes userAgent
 * 
 * It will return either return an empty string or the sanitized value.
 * 
 * If no argument is given or the wrong variable type is given: returns empty string
 * If string is given, the function will:
 * 1) strip certain characters according to /[^a-zA-Z0-9 .,/();:+_-]/g 
 *      allowed: a-zA-Z 0-9 . , / ( ) ; : + _ - and spaces
 * 2) if the string is greater than the maximum character length for user agent, the string will be cut accordingly.
 * 
 * @param {string} userAgent
 * @returns {string}
 * 
 * @example
 * 
 * // The same string may be returned:
 * let uA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
 * sanitizedUserAgent(uA) //=> returns "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
 * 
 * // The string may be sanitized:
 * let uA = "Mozilla/5.0 <script>alert('XSS')</script> (Windows NT 10.0; Win64; x64)"
 * sanitizedUserAgent(uA) //=> returns "Mozilla/5.0 scriptalertXSSscript (Windows NT 10.0; Win64; x64)"
 * 
 */
export function sanitizedUserAgent(userAgent = "") {
    if (!userAgent || userAgent === "" || typeof userAgent !== "string") { return "" };
    //replace certain characters
    let sanitizedUA = userAgent.replace(/[^a-zA-Z0-9 .,/();:+_-]/g, "")
    //diminish size of string if too long
    const maxLength = INPUT_LENGTH.userAgent.maxValue
    if (sanitizedUA.length > maxLength) {
        sanitizedUA = sanitizedUA.substring(0, maxLength);
    }
    return sanitizedUA
}

/**
 * Function that checks if token passes basic regex.
 * 
 * It will return true if the token format is valid, and false otherwise
 * 
 * @todo use ajv for js validation
 * 
 * @param {string} token 
 * @returns {boolean}
 * @example
 * let token = "sb5oALqhJsT5rUZ9H9XgUHcIWkVgaqiIiqVjvfgX-5Q"
 * validateTokenFormat(token) // Output: true
 * validateTokenFormat("") // Output: false
 */
export function tokenFormatIsValid(token) {
    // check for type
    if (typeof token !== "string" || token.trim() === "") { return false }

    const trimmedToken = token.trim()

    //check for length
    if (trimmedToken.length < INPUT_LENGTH.signedToken.minValue || trimmedToken.length > INPUT_LENGTH.signedToken.maxValue) {
        return false;
    }
    // token should contain only: alphanumeric, period, dash, and underscore
    const tokenRegex = /^[a-zA-Z0-9._-]+$/;
    if (!tokenRegex.test(trimmedToken)) { return false; }

    // next may be a silly black list check, but why not...
    const noGoInput = ["document", "href", "html", "http", "select", "script", "where", "www."]
    if (noGoInput.some(weirdInput => trimmedToken.toLowerCase().includes(weirdInput))) { return false }

    return true
}

