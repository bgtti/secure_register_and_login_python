import { api } from "../../axios";
import apiEndpoints from "../../apiEndPoints";
import { INPUT_LENGTH } from "../../../utils/constants";

/**
 * Function makes api call to retrieve an array of users (number of users retrieved = itemsPerPage).
 * 
 * Pagination is expected to handle the returned data.
 * 
 * Given wrong parameters defaults will be used (it will not return an error).
 * 
 * Sends the key 'data' as a boolean to indicate whether there is response data or not.
 * 
 * @param {object} data 
 * @param {number} [data.pageNr = 1] integer, must be positive
 * @param {number} [data.itemsPerPage = 25] integer between 5 and 50, must be multiple of 5
 * @param {string} [data.orderBy = "last_seen"] enum: ["last_seen", "name", "email", "created_at"]
 * @param {string} [data.orderSort = "descending"] enum: ["descending", "ascending"]
 * @param {string} [data.filterBy = "none"] enum: ["none", "is_blocked"]
 * @param {string} [data.searchBy = "none"] enum: ["none", "name", "email"]
 * @param {string} [data.searchWord  = ""] no longer than maximum email length
 * @returns {object}
 * 
 * @example
 * //Input example:
 * const data = {
 *     page_nr: 1,
 *     order_by: "name"
 * }
 * 
 * //Original API response:
 * {
 *  "response": "success"
 *  "users": [
 *      {
 *        uuid: "3f61108854cd4b5886401080d681dd96",
 *        name: "Josy",
 *        email: "josy@example.com",
 *        last_seen: "Thu, 25 Jan 2024 00:00:00 GMT",
 *        is_blocked: "false"
 *      },
 *      ...
 *  ]
 *  "total_pages": 3,
 *  "current_page": 1,
 *  "query": {...}
 * }
 * 
 * // Response from getAllUsers:
 * {
 *  users: [
 *      {
 *        uuid: "3f61108854cd4b5886401080d681dd96",
 *        name: "Josy",
 *        email: "josy@example.com",
 *        lastSeen: "25 Jan 2024",
 *        isBlocked: "false"
 *      },
 *      ...
 *  ]
 *  totalPages: 3,
 *  currentPage: 1,
 *  data: true
 * }
 */
export function getAllUsers(data = {}) {

    const ORDER = ["last_seen", "name", "email", "created_at"]
    const SORT = ["descending", "ascending"]
    const FILTER = ["none", "is_blocked"]
    const SEARCH_BY = ["none", "name", "email"]
    const SEARCH_WORD_MAX_LENGTH = INPUT_LENGTH.email.maxValue

    // validate data - if validation fails, defaults are set
    let pageNr = parseInt(data.pageNr);
    pageNr = (data.pageNr && Number.isInteger(pageNr) && pageNr >= 1) ? pageNr : 1;

    let itemsPerPage = parseInt(data.itemsPerPage);
    itemsPerPage = (data.itemsPerPage && Number.isInteger(itemsPerPage) && itemsPerPage >= 5 && itemsPerPage <= 50 && itemsPerPage % 5 === 0) ? itemsPerPage : 25;

    let orderBy = (data.orderBy && ORDER.includes(data.orderBy)) ? data.orderBy : "last_seen";
    let orderSort = (data.orderSort && SORT.includes(data.orderSort)) ? data.orderSort : "descending";
    let filterBy = (data.filterBy && FILTER.includes(data.filterBy)) ? data.filterBy : "none";
    let searchBy = (data.searchBy && SEARCH_BY.includes(data.searchBy)) ? data.searchBy : "none";
    let search_word = (data.searchWord && (typeof data.searchWord === "string") && data.searchWord.length <= SEARCH_WORD_MAX_LENGTH) ? data.searchWord : "";

    let requestData = {
        "page_nr": pageNr,
        "items_per_page": itemsPerPage,
        "order_by": orderBy,
        "order_sort": orderSort,
        "filter_by": filterBy,
        "search_by": searchBy,
        "search_word": search_word
    }

    const emptyObj = {
        users: [],
        totalPages: 1,
        currentPage: 1,
        data: false
    }

    const getData = async () => {
        try {
            const response = await api.post(apiEndpoints.adminGetUsersTable, requestData)
            if (response.status === 200 && response.data.users.length > 0) {
                const javaScriptifiedUserFields = response.data.users.map(user => {
                    const { last_seen: lastSeen, is_blocked: isBlocked, ...rest } = user;
                    // Format lastSeen date
                    const formattedLastSeen = new Date(lastSeen).toLocaleDateString('en-GB', {
                        day: 'numeric',
                        month: 'short',
                        year: 'numeric',
                    });
                    return {
                        ...rest,
                        lastSeen: formattedLastSeen,
                        isBlocked,
                    };
                });
                return {
                    users: javaScriptifiedUserFields,
                    totalPages: response.data.total_pages,
                    currentPage: response.data.current_page,
                    data: true,
                }
            } else {
                return emptyObj
            }
        }
        catch (error) {
            console.error('Error fetching users:', error);
            return emptyObj
        }
    }

    return getData();
};