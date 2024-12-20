//Constants used throughout the document to validate input are in this file.

/**
 * Array of most common passwords
 * @readonly
 * @enum {string[]}
 * 
 * Note: The name of the app in question is commonly used by users in passwords.
 * @todo Substitute the first value of the array with the name of your app if you are using this template.
 * 
 * When addid/editing this array: Use lower case letters only, as a string will be compared to a value in this list in lower case.
 * 
 * @see {@link https://nordpass.com/most-common-passwords-list/} Most common password list based on that on NordPass' website.
 */
export const MOST_COMMON_PASSWORDS = [
    "safedev",
    "1q2w3",
    "102030",
    "112233",
    "445566",
    "12345",
    "54321",
    "abc123",
    "abcd",
    "admin",
    "asdfghjkl",
    "azerty",
    "demo",
    "eliska81",
    "iloveyou",
    "monkey",
    "p@ssw0rd",
    "pass@123",
    "password",
    "qwerty",
    "root",
    "superman",
    "ubnt",
    "unknown",
    "user",
    "qwerty",
    "yxcvbnm"
];

/**
 * Array of reserved names
 * @readonly
 * @enum {string[]}
 * 
 * Note: The name of the app should also not be used as a name
 * @todo Substitute the first value of the array with the name of your app if you are using this template.
 * 
 * @note When addid/editing this array: Use lower case letters only, as a string will be compared to a value in this list in lower case.
 * 
 */
export const RESERVED_NAMES = [
    "safedev",
    "admin",
    "administrator",
    "moderator",
];

/**
 * Input length requirements
 * @readonly
 * @enum {object}
 * 
 * @see {@link https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html} OWASP recommendation for email length
 */
export const INPUT_LENGTH = Object.freeze({
    name: {
        minValue: 1,
        maxValue: 200
    },
    email: {
        minValue: 3,
        maxValue: 320
    },
    password: {
        minValue: 8,
        maxValue: 60
    },
    otp: {
        minValue: 8,
        maxValue: 8
    },
    contactMessageSubject: {
        minValue: 1,
        maxValue: 45
    },
    contactMessageAnswerSubject: {
        minValue: 1,
        maxValue: 50
    },
    contactMessage: {
        minValue: 1,
        maxValue: 300
    },
    userAgent: {
        minValue: 0,
        maxValue: 255
    },
    signedToken: {
        minValue: 40,
        maxValue: 300
    }
})

/**
 * Acct verification status
 * @readonly
 * @enum {Array<boolean|string>}
 */
export const ACCT_VERIFICATION_STATUS = [
    true,
    false,
    "pending"
]

/**
 * User access types
 * @readonly
 * @enum {string[]}
 * @deprecated use dictionary version
 * See {@link USER_ACCESS_DIC} as it should contain the same values.
 */
export const USER_ACCESS_TYPES = [
    "user",
    "admin",
    "super_admin"
]

/**
 * Possible user access types in object format
 * @readonly
 * @enum {object}
 */
export const USER_ACCESS_DIC = {
    user: "user",
    admin: "admin",
    super_admin: "super_admin"
}

/**
 * Possible user access types that can be given a user
 * @readonly
 * @enum {object}
 * Note super admin access type cannot be given or taken away from a user
 */
export const USER_TYPE_REQUEST = {
    admin: "admin",
    user: "user"
}

/**
 * Array of available flag colors
 * @readonly
 * @enum {string[]}
 */
export const FLAG_TYPES = [
    "red",
    "yellow",
    "purple",
    "blue"
]

/**
 * Array of available blocked statuses
 * @readonly
 * @enum {string[]}
 */
export const IS_BLOCKED_TYPES = [
    "true",
    "false"
]

/**
 * Object of possibilities array to validate input for requests sent to get users' table
 * @readonly
 * @enum {object}
 */
export const USERS_TABLE_REQUEST = {
    order_by: ["last_seen", "name", "email", "created_at"],
    order_sort: ["descending", "ascending"],
    filter_by: ["none", "is_blocked", "is_unblocked", "flag", "flag_not_blue", "is_admin", "is_user", "last_seen"],
    filter_by_flag: [...FLAG_TYPES],
    search_by: ["none", "name", "email"]
}

/**
 * Object of possibilities array to validate input for requests sent to get messages' table
 * @readonly
 * @enum {object}
 * 
 * - order_sort: ["descending", "ascending"]
 * - filter_by: ["answer_needed", "answer_not_needed", "all"]
 * - include_spam: [true, false]
 */
export const MESSAGES_TABLE_REQUEST = {
    order_sort: ["descending", "ascending"],
    filter_by: ["answer_needed", "answer_not_needed", "all"],
    include_spam: [true, false],
}