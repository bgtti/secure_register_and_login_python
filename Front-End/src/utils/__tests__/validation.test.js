import { nameValidation, passwordValidation, emailValidation, passwordValidationForLogin } from "../validation"
import { INPUT_LENGTH } from "../constants"

test('Name input validation test', () => {
    expect(nameValidation(0)).toStrictEqual({ response: false, message: "Name must be a string." });
    expect(nameValidation("")).toStrictEqual({ response: false, message: `Name must have between ${INPUT_LENGTH.name.minValue} and ${INPUT_LENGTH.name.maxValue} characters.` });
    expect(nameValidation("maria")).toStrictEqual({ response: true, message: "" });
});

test('Email input validation test', () => {
    expect(emailValidation(5)).toStrictEqual({ response: false, message: "Email must be a string." });
    expect(emailValidation(" fgt")).toStrictEqual({ response: false, message: "Email format is not valid." });
    expect(emailValidation("d@to")).toStrictEqual({ response: true, message: "" });
});

test('Password input validation test', () => {
    expect(passwordValidation(5)).toStrictEqual({ response: false, message: "Password must be a string." });
    expect(passwordValidation(" e356jhl")).toStrictEqual({ response: false, message: `Password must have between ${INPUT_LENGTH.password.minValue} and ${INPUT_LENGTH.password.maxValue} characters.` });
    expect(passwordValidation("kung12345")).toStrictEqual({ response: false, message: "Password provided in the list of most common passwords used." });
    expect(passwordValidation("waZerTy1")).toStrictEqual({ response: false, message: "Password provided in the list of most common passwords used." });
    expect(passwordValidation("jjjjbghj")).toStrictEqual({ response: false, message: "Password cannot contain the same character 4 or more times consecutively." });
    expect(passwordValidation("dfrgt0000")).toStrictEqual({ response: false, message: "Password cannot contain the same character 4 or more times consecutively." });
    expect(passwordValidation("mkh*****")).toStrictEqual({ response: false, message: "Password cannot contain the same character 4 or more times consecutively." });
    expect(passwordValidation("xyzu//////")).toStrictEqual({ response: false, message: "Password cannot contain the same character 4 or more times consecutively." });
    expect(passwordValidation("$gtd23?)(")).toStrictEqual({ response: true, message: "" });
    expect(passwordValidation("000xxxazerty***")).toStrictEqual({ response: true, message: "" });
});

test('Login password validation test', () => {
    expect(passwordValidationForLogin(8)).toStrictEqual({ response: false, message: "Password must be a string." });
    expect(passwordValidationForLogin(" e356jhl")).toStrictEqual({ response: false, message: `Passwords should have between ${INPUT_LENGTH.password.minValue} and ${INPUT_LENGTH.password.maxValue} characters. Please check your input.` });
    expect(passwordValidationForLogin("kung12345")).toStrictEqual({ response: true, message: "" });
    expect(passwordValidationForLogin("mkh*****")).toStrictEqual({ response: true, message: "" });
});

