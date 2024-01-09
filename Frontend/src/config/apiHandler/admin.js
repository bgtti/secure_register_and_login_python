import api from "../axios";
import apiEndpoints from "../apiEndPoints";
import { INPUT_LENGTH } from "../../utils/constants";

/**
 * Function makes api call to retrieve an array of users (number of users = items_per_page).
 * 
 * Pagination is expected to handle the returned data.
 * 
 * Given wrong parameters defaults will be used (it will not return an error).
 * 
 * Sends the key 'data' as a boolean to indicate whether there is response data or not.
 * 
 * @todo UPDATE THIS DOCSTRING
 * @param {object} data 
 * @param {number} [data.page_nr = 1] integer, must be positive
 * @param {number} [data.items_per_page = 25] integer between 5 and 50, must be multiple of 5
 * @param {string} [data.order_by = "last_seen"] enum: ["last_seen", "name", "email", "created_at"]
 * @param {string} [data.order_sort = "descending"] enum: ["descending", "ascending"]
 * @param {string} [data.filter_by = "none"] enum: ["none", "is_blocked"]
 * @param {string} [data.search_by = "none"] enum: ["none", "name", "email"]
 * @param {string} [data.search_word  = ""] no longer than maximum email length
 * @returns {object}
 * 
 * @example
 * //Input example:
 * const data = {
 *     page_nr: 1,
 *     order_by: "name"
 * }
 * 
 * //Response example:
 * {
 *  response: "success"
 *  users: [
 *      {
 *        uuid: "3f61108854cd4b5886401080d681dd96",
 *        name: "Josy",
 *        email: "josy@example.com",
 *        last_seen: "Thu, 25 Jan 2024 00:00:00 GMT",
 *        is_blocked: "false"
 *      },
 *      ...
 *  ]
 *  total_pages: 3,
 *  current_page: 1,
 *  data: true,
 * }
 */
export function getAllUsers(data = {}) {

    const ORDER = ["last_seen", "name", "email", "created_at"]
    const SORT = ["descending", "ascending"]
    const FILTER = ["none", "is_blocked"]
    const SEARCH_BY = ["none", "name", "email"]
    const SEARCH_WORD_MAX_LENGTH = INPUT_LENGTH.email.maxValue

    // validate data - if validation fails, defaults are set
    let pageNr = parseInt(data.page_nr);
    pageNr = (data.page_nr && Number.isInteger(pageNr) && pageNr >= 1) ? pageNr : 1;

    let itemsPerPage = parseInt(data.items_per_page);
    itemsPerPage = (data.items_per_page && Number.isInteger(itemsPerPage) && itemsPerPage >= 5 && itemsPerPage <= 50 && itemsPerPage % 5 === 0) ? itemsPerPage : 25;

    let orderBy = (data.order_by && ORDER.includes(data.order_by)) ? data.order_by : "last_seen";
    let orderSort = (data.order_sort && SORT.includes(data.order_sort)) ? data.order_sort : "descending";
    let filterBy = (data.filter_by && FILTER.includes(data.filter_by)) ? data.filter_by : "none";
    let search_by = (data.search_by && SEARCH_BY.includes(data.search_by)) ? data.search_by : "none";
    let search_word = (data.search_word && (typeof data.search_word === "string") && data.search_word.length <= SEARCH_WORD_MAX_LENGTH) ? data.search_word : "";

    let requestData = {
        "page_nr": pageNr,
        "items_per_page": itemsPerPage,
        "order_by": orderBy,
        "order_sort": orderSort,
        "filter_by": filterBy,
        "search_by": search_by,
        "search_word": search_word
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
                return {
                    users: [],
                    totalPages: 1,
                    currentPage: 1,
                    data: false
                }
            }
        }
        catch (error) {
            console.error('Error fetching users:', error);
            return {
                users: [],
                totalPages: 1,
                currentPage: 1,
                data: false
            }
        }
    }

    return getData();
};

/**
 * Function makes api call to block or unblock a particular user.
 * 
 * @param {string} uuid 
 * @param {boolean} block false to unblock & true to block
 * @returns {object} success as a boolean
 * @example
 * Example return if response 200:
 * {success: true}
 * Example return if response not 200:
 * {success: false}
 */
export function blockOrUnblockUser(uuid, block) {
    let the_uuid = (uuid && (typeof uuid === "string") && uuid.length === 32) ? uuid : "";
    let is_block = (typeof block === "boolean") ? block : "";

    if (the_uuid === "" || is_block === "") {
        return console.warn("Invalid input. Cannot block or unblock user.")
    }

    let requestData = {
        "user_uuid": the_uuid,
        "block": is_block
    }

    const getData = async () => {
        try {
            const response = await api.post(apiEndpoints.adminBlockUnblockUser, requestData)
            if (response.status === 200) {
                return {
                    success: true
                }
            } else {
                return {
                    success: false
                }
            }
        }
        catch (error) {
            console.error('Error blocking/unblocking user:', error);
            return {
                success: false
            }
        }
    }

    return getData();
};

/**
 * Function makes api call to delete a particular user.
 * 
 * @param {string} uuid 
 * @returns {object} success as a boolean
 * @example
 * Example return if response 200:
 * {success: true}
 * Example return if response not 200:
 * {success: false}
 */
export function deleteUser(uuid) {
    let the_uuid = (uuid && (typeof uuid === "string") && uuid.length === 32) ? uuid : "";

    if (the_uuid === "") {
        return console.warn("Invalid input. Cannot delete user.")
    }

    let requestData = {
        "user_uuid": the_uuid
    }

    const getData = async () => {
        try {
            const response = await api.post(apiEndpoints.adminDeleteUser, requestData)
            if (response.status === 200) {
                return {
                    success: true
                }
            } else {
                return {
                    success: false
                }
            }
        }
        catch (error) {
            console.error('Error deleting user:', error);
            return {
                success: false
            }
        }
    }

    return getData();
};