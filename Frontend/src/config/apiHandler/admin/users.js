import { apiHandle404 } from "../../axios";
import apiEndpoints from "../../apiEndpoints";
import { INPUT_LENGTH, USERS_TABLE_REQUEST } from "../../../utils/constants";
import { validateDateFormat } from "../../../utils/validation";
import { getLastMonthDate } from "../../../utils/helpers";

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
 * @param {string} [data.filterBy = "none"] enum: ["none", "is_blocked", "is_unblocked", "flag", "flag_not_blue", "is_admin", "is_user", "last_seen"]
 * @param {string} [data.filterByFlag = "blue"] enum: ["red", "yellow", "purple", "blue"]
 * @param {string} [data.filterByLastSeen = ""] date format YYYY-MM-DD
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
                {
                "id": 10
                "name": "Frank Torres",
                "email": "frank.torres@fakemail.com",
                "last_seen": "Thu, 25 Jan 2024 00:00:00 GMT",
                "access": "user",
                "flagged": "blue",
                "is_blocked": "false"
                }, 
                ...
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
 *        id: 10,
 *        name: "Frank Torres",
 *        email: "frank.torres@fakemail.com",
 *        lastSeen: "25 Jan 2024",
 *        access: "user",
 *        flagged: "blue",
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

    const ORDER = USERS_TABLE_REQUEST.order_by
    const SORT = USERS_TABLE_REQUEST.order_sort
    const FILTER = USERS_TABLE_REQUEST.filter_by
    const FLAG_FILTER = USERS_TABLE_REQUEST.filter_by_flag
    const SEARCH_BY = USERS_TABLE_REQUEST.search_by
    const SEARCH_WORD_MAX_LENGTH = INPUT_LENGTH.email.maxValue

    // validate data - if validation fails, defaults are set
    let pageNr = parseInt(data.pageNr);
    pageNr = (data.pageNr && Number.isInteger(pageNr) && pageNr >= 1) ? pageNr : 1;

    let itemsPerPage = parseInt(data.itemsPerPage);
    itemsPerPage = (data.itemsPerPage && Number.isInteger(itemsPerPage) && itemsPerPage >= 5 && itemsPerPage <= 50 && itemsPerPage % 5 === 0) ? itemsPerPage : 25;

    let orderBy = (data.orderBy && ORDER.includes(data.orderBy)) ? data.orderBy : "last_seen";
    let orderSort = (data.orderSort && SORT.includes(data.orderSort)) ? data.orderSort : "descending";
    let filterBy = (data.filterBy && FILTER.includes(data.filterBy)) ? data.filterBy : "none";
    let filterByFlag = (data.filterByFlag && FLAG_FILTER.includes(data.filterByFlag)) ? data.filterByFlag : "blue";
    let filterByLastSeen = (data.filterByLastSeen && validateDateFormat(data.filterByLastSeen)) ? data.filterByLastSeen : getLastMonthDate();
    let searchBy = (data.searchBy && SEARCH_BY.includes(data.searchBy)) ? data.searchBy : "none";
    let search_word = (data.searchWord && (typeof data.searchWord === "string") && data.searchWord.length <= SEARCH_WORD_MAX_LENGTH) ? data.searchWord : "";

    let requestData = {
        "page_nr": pageNr,
        "items_per_page": itemsPerPage,
        "order_by": orderBy,
        "order_sort": orderSort,
        "filter_by": filterBy,
        "filter_by_flag": filterByFlag,
        "filter_by_last_seen": filterByLastSeen,
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
            const response = await apiHandle404.post(apiEndpoints.adminGetUsersTable, requestData)
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