// Most common password list based on: https://nordpass.com/most-common-passwords-list/
// IMPORTANT:
// The name of the app in question is commonly used in passwords. 
// Substitute the first value of the list with the name of your app if you are using this template.
// Use lower case letters only, as a string will be compared to a value in this list in lower case.

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

//INPUT LENGTH REQUIREMENTS
//Email length set according to OWASP recommendations: https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html
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
    contactMessage: {
        minValue: 1,
        maxValue: 300
    }
})

export const USER_ACCESS_TYPES = [
    "user",
    "admin",
    "super_admin"
]

export const FLAG_TYPES = [
    "red",
    "yellow",
    "purple",
    "blue"
]

export const IS_BLOCKED_TYPES = [
    "true",
    "false"
]

export const USERS_TABLE_REQUEST = {
    order_by: ["last_seen", "name", "email", "created_at"],
    order_sort: ["descending", "ascending"],
    filter_by: ["none", "is_blocked", "is_unblocked", "flag", "flag_not_blue", "is_admin", "is_user", "last_seen"],
    filter_by_flag: [...FLAG_TYPES],
    search_by: ["none", "name", "email"]
}