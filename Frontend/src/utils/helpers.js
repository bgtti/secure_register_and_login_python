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
