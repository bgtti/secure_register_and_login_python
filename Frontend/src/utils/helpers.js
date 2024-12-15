// ABOUT THIS FILE
// Helper functions that can be used in components, utils, apiHandlers, etc


/**
  * Converts a string or boolean to a boolean value.
 * - If a boolean is passed, it is returned as-is.
 * - If the string "true" or "false" is passed, it is converted to a boolean.
 * - Logs an error and returns null if the input cannot be processed.
 * 
 * @param {string|boolean} input
 * @returns {bool | null}
 * @example
 * stringToBool("true"); // -> true
 * stringToBool("false"); // -> false
 * stringToBool(true);    // -> true
 * stringToBool(false);   // -> false
 * stringToBool("hello"); // -> null (logs error)
 */
export function stringToBool(input) {
    if (typeof input === "boolean") { return input }
    if (input === "true") { return true }
    if (input === "false") { return false }
    console.error("Input cannot be transformed into boolean. Check utils > helpers > stringToBool input: ", input)
    return null;
}


/**
 * Function that capitalizes the first letter of each word in a string.
 * 
 * It will return the string with each first word capitalized
 * 
 * @param {string} string 
 * @returns {string}
 * @example
 * capitalizeFirstLetter("hello wOrld") -> "Hello World"
 */
export function capitalizeFirstLetter(string) {
    const stringCapitalized = string
        .split(' ')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
        .join(' ');

    return stringCapitalized;
}

/**
 * Function that returns a date 30 days in the past in the format YYYY-MM-DD
 * 
 * @returns {string}
 * @example
 * console.log(getLastMonthDate()); -> "2024-02-23"
 */
export function getLastMonthDate() {
    const today = new Date();
    const thirtyDaysAgo = new Date(today);
    thirtyDaysAgo.setDate(today.getDate() - 30);

    // Format the date as YYYY-MM-DD
    const formattedDate = `${thirtyDaysAgo.getFullYear()}-${(thirtyDaysAgo.getMonth() + 1).toString().padStart(2, '0')}-${thirtyDaysAgo.getDate().toString().padStart(2, '0')}`;

    return formattedDate;
}

/**
 * Function that returns today's date in the format YYYY-MM-DD
 * 
 * @returns {string}
 * @example
 * console.log(getTodaysDate()); -> "2024-02-23"
 */
export function getTodaysDate() {
    const today = new Date();

    // Format the date as YYYY-MM-DD
    const formattedDate = `${today.getFullYear()}-${(today.getMonth() + 1).toString().padStart(2, '0')}-${today.getDate().toString().padStart(2, '0')}`;

    return formattedDate;
}

/**
 * Function that returns a date in the format YYYY-MM-DD
 * @param {string} dateString - a date in string format
 * @returns {string}
 * Note: this function will not validate the dateString input.
 * If you need date input validation see the {@link validateDate} function in utils helpers
 * @example
 * dateToYYYYMMDD(23 Feb 2024); -> "2024-02-23"
 */
export function dateToYYYYMMDD(dateString) {
    const date = new Date(dateString);

    // Format the date as YYYY-MM-DD
    const formattedDate = `${date.getFullYear()}-${(date.getMonth() + 1).toString().padStart(2, '0')}-${date.getDate().toString().padStart(2, '0')}`;

    return formattedDate;
}


//An alternative to the function bellow would have been to combine all regex cases into one for the case of "any" or "all":
// isValid = /^(?:\d{4}[-/.](?:0[1-9]|1[0-2])[-/.](?:0[1-9]|[12][0-9]|3[01])|(?:0[1-9]|[12][0-9]|3[01])[-/.](?:0[1-9]|1[0-2])[-/.]\d{4}|(?:0[1-9]|[12][0-9]|3[01]) (?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) \d{4}|(?:0[1-9]|[12][0-9]|3[01]) (?:January|February|March|April|May|June|July|August|September|October|November|December) \d{4}|(?:0[1-9]|1[0-2])[-/.](?:0[1-9]|[12][0-9]|3[01])[-/.]\d{4}|\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{3}Z|\d{2} (?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) \d{4}, \d{2}:\d{2} (?:GMT|UTC|[A-Z]{3})([+-]\d{2}))$/.test(dateString);


//Test validation for validateDate function:
//'2011-10-05T14:48:00.000Z' should be valid
//'2018-11-10T11:22:33+00:00' should be valid
//'2011-10-05T14:99:00.000Z' should not be valid (time doesnt exist)
// "Sat Sep 13 275760 00:00:00 GMT+0000 (Coordinated Universal Time)" should be valid
// 8.64e15 + 1 should not be valid
// '10 Nov 2018, 12:22 GMT+1' should be valid
// "25 Jan 2024" should be valid
// "15 February 2024" should be valid
// "2024-04-16", "2024/04/16", or "2024.04.16" should be valid
// "16-04-2024", "16/04/2024", or "16.04.2024" should be valid dmy
// "04-16-2024", "04/16/2024", or "04.16.2024" should be valid mdy
// Check: https://stackoverflow.com/a/7445368/14517941



/**
 * Function checks whether a string represents a valid date
 * 
 * @param {string} dateString - a date in string format
 * @param {string} [format="any"] - if not given, defaults to "any"
 * @returns {boolean}
 * 
 * @example
 * validateDate("2024-04-16") //-> true
 * validateDate("2024-04-16") //-> true
 * validateDate("044475162024") //-> false
 * validateDate("04-16-2024", "MDY") //-> true
 * validateDate("04-16-2024", "DMY") //-> false
 * validateDate("10 Nov 2018, 12:22 GMT+1", "local") //-> true
 * 
 * //Accepted format parameter values: 
 * formats = [
    "yyyy-mm-dd",
    "yyyy/mm/dd",
    "yyyy.mm.dd",
    "YDM", // YMD checks for "yyyy-mm-dd", "yyyy/mm/dd", or "yyyy.mm.dd"
    "dd-mm-yyyy",
    "dd/mm/yyyy",
    "dd.mm.yyyy",
    "DMY", // DMY checks for "dd-mm-yyyy", "dd/mm/yyyy", or "dd.mm.yyyy"
    "dd mmm yyyy",
    "dd/mmm/yyyy",
    "dd mmmm yyyy",
    "mm-dd-yyyy",
    "mm/dd/yyyy",
    "mm.dd.yyyy",
    "MDY", // MDY checks for "mm-dd-yyyy", "mm/dd/yyyy", or "mm.dd.yyyy"
    "iso", // ISO standard: YYYY-MM-DDTHH:MN:SS.MSSZ
    "local", // local checks for "dd mmm yyyy, HH:MN Z", where Z is the shortOffset timeZoneName(ex: "GMT-8" or "UTC+1")
    "any", // will check all formats (not recommended)
    "all"// will check all formats (not recommended)
];
 * 
 */
export function validateDate(dateString, format = "any") {

    if (typeof dateString !== "string" || dateString.trim() === "" || typeof format !== "string") {
        console.warn("Invalid date or date format input ")
        return false
    }

    let isValid = false;
    switch (format) {
        case "yyyy-mm-dd":
        case "yyyy/mm/dd":
        case "yyyy.mm.dd":
        case "YDM":
            isValid = /^\d{4}[-/.](?:0[1-9]|1[0-2])[-/.](?:0[1-9]|[12][0-9]|3[01])$/.test(dateString)
            break
        case "dd-mm-yyyy":
        case "dd/mm/yyyy":
        case "dd.mm.yyyy":
        case "DMY":
            isValid = /^(?:0[1-9]|[12][0-9]|3[01])[-/.](?:0[1-9]|1[0-2])[-/.]\d{4}$/.test(dateString)
            break
        case "dd mmm yyyy":
        case "dd/mmm/yyyy":
            isValid = /^(?:0[1-9]|[12][0-9]|3[01]) (?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) \d{4}$/.test(dateString)
            break
        case "dd mmmm yyyy":
            isValid = /^(?:0[1-9]|[12][0-9]|3[01]) (?:January|February|March|April|May|June|July|August|September|October|November|December) \d{4}$/.test(dateString)
            break
        case "mm-dd-yyyy":
        case "mm/dd/yyyy":
        case "mm.dd.yyyy":
        case "MDY":
            isValid = /^(?:0[1-9]|1[0-2])[-/.](?:0[1-9]|[12][0-9]|3[01])[-/.]\d{4}$/.test(dateString)
            break
        case "iso":
            isValid = /\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{3}Z/.test(dateString)
            break
        case "local":
            isValid = /^\d{2} (?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) \d{4}, \d{2}:\d{2} (?:GMT|UTC|[A-Z]{3})([+-]\d{2})$/.test(dateString)
            break
        case "any":
        case "all":
            if (isNaN(Date.parse(dateString))) { break }
            isValid = /^\d{4}[-/.](?:0[1-9]|1[0-2])[-/.](?:0[1-9]|[12][0-9]|3[01])$/.test(dateString)
            if (isValid) { break }
            isValid = /^(?:0[1-9]|[12][0-9]|3[01])[-/.](?:0[1-9]|1[0-2])[-/.]\d{4}$/.test(dateString)
            if (isValid) { break }
            isValid = /^(?:0[1-9]|[12][0-9]|3[01]) (?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) \d{4}$/.test(dateString)
            if (isValid) { break }
            isValid = /^(?:0[1-9]|[12][0-9]|3[01]) (?:January|February|March|April|May|June|July|August|September|October|November|December) \d{4}$/.test(dateString)
            if (isValid) { break }
            isValid = /^(?:0[1-9]|1[0-2])[-/.](?:0[1-9]|[12][0-9]|3[01])[-/.]\d{4}$/.test(dateString)
            if (isValid) { break }
            isValid = /\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{3}Z/.test(dateString)
            if (isValid) { break }
            isValid = /^\d{2} (?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) \d{4}, \d{2}:\d{2} (?:GMT|UTC|[A-Z]{3})([+-]\d{2})$/.test(dateString)
            break
        default:
            console.warn("Date format input not valid.")
            return false
    }
    if (!isValid && !isNaN(Date.parse(dateString))) {
        console.log("Date did not pass the validation test, but Date.parse indicates the input could be a date.")
        console.log(`Date input: ${dateString}. If input is a valid date, check format parameter.`)
    }
    return isValid;
}


/**
 * Function transforms a locale date into ISO format (UTC)
 * 
 * @param {string} dateString - a date in string format
 * @param {string} [format="any"] - if not given, defaults to "any"
 * @returns {string | boolean} - returns string or false (if fails to generate a UTC date)
 * 
 * Note: the date input will be validaded with the {@link validateDate} function
 * 
 * @example
 * getUTCString("2018-11-10"); -> "2018-11-10T00:00:00+00:00"
 * getUTCString("2018-11-10", "local"); -> false
 * 
 * //Accepted format parameter values: 
 * formats = [
    "yyyy-mm-dd",
    "yyyy/mm/dd",
    "yyyy.mm.dd",
    "YDM", // YMD checks for "yyyy-mm-dd", "yyyy/mm/dd", or "yyyy.mm.dd"
    "dd-mm-yyyy",
    "dd/mm/yyyy",
    "dd.mm.yyyy",
    "DMY", // DMY checks for "dd-mm-yyyy", "dd/mm/yyyy", or "dd.mm.yyyy"
    "dd mmm yyyy",
    "dd/mmm/yyyy",
    "dd mmmm yyyy",
    "mm-dd-yyyy",
    "mm/dd/yyyy",
    "mm.dd.yyyy",
    "MDY", // MDY checks for "mm-dd-yyyy", "mm/dd/yyyy", or "mm.dd.yyyy"
    "iso", // ISO standard: YYYY-MM-DDTHH:MN:SS.MSSZ
    "local", // local checks for "dd mmm yyyy, HH:MN Z", where Z is the shortOffset timeZoneName(ex: "GMT-8" or "UTC+1")
    "any", // will check all formats (not recommended)
    "all"// will check all formats (not recommended)
];
 */
export function getUTCString(dateString, format = "any") {

    if (validateDate(dateString, format)) {
        let date = new Date(dateString)
        return date.toISOString()
    } else {
        return false
    }
}