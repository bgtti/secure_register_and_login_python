import api from "../axios";
import apiEndpoints from "../apiEndPoints";
import { INPUT_LENGTH } from "../../utils/constants";

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

/**
 * Function makes api call to retrieve an array of logs for a particular user.
 * 
 * Pagination is expected to handle the returned data.
 * 
 * Given an invalid uuid or error response, will return an empty object.
 * 
 * Sends the key 'data' as a boolean to indicate whether there is response data or not.
 * 
 * @param {number} PageNr integer, must be positive
 * @param {string} uuid 
 * @returns {object}
 * 
 * @example
 * //Usage:
 * getUserLogs(1, "6f93fab8681a435a96794cfd69170cfd")
 * 
 * //Original API response:
 * {
 *    "current_page": 1,
 *    "logs": [
 *        {
 *            "activity": "signup",
 *            "created_at": "Tue, 09 Jan 2024 21:07:38 GMT",
 *            "message": "successful signup.",
 *            "type": "INFO",
 *            "user_uuid": "6f93fab8681a435a96794cfd69170cfd"
 *        },
 *        ...
 *    ],
 *    "query": {
 *        "items_per_page": 25,
 *        "order_sort": "descending",
 *        "ordered_by": "created_at",
 *        "page_nr": 1
 *    },
 *    "response": "success",
 *    "total_pages": 1
 * }
 * 
 * //Response from getUserLogs:
 * {
 *  currentPage: 1,
 *  totalPages: 1,
 *  data: true,
 *  logs: [
 *       {
 *            "activity": "signup",
 *            "createdAt": "09 Jan 2024",
 *            "message": "successful signup.",
 *            "type": "INFO",
 *            "userUuid": "6f93fab8681a435a96794cfd69170cfd"
 *        },
 *        ...
 *  ]
 * }
 */
export function getUserLogs(pageNr, userUuid) {
    let thePageNum = parseInt(pageNr);
    thePageNum = (pageNr && Number.isInteger(thePageNum) && thePageNum >= 1) ? thePageNum : 1;
    let theUuid = (userUuid && (typeof userUuid === "string") && userUuid.length === 32) ? userUuid : "";

    const emptyObj = {
        logs: [],
        totalPages: 1,
        currentPage: 1,
        data: false
    }

    if (theUuid === "") {
        console.warn("No uuid provided to get user logs.")
        return emptyObj
    }

    let requestData = {
        "page_nr": thePageNum,
        "user_uuid": theUuid,
    }

    const getData = async () => {
        try {
            const response = await api.post(apiEndpoints.adminGetUserLogs, requestData)
            if (response.status === 200 && response.data.logs.length > 0) {
                const javaScriptifiedUserFields = response.data.logs.map(log => {
                    const { user_uuid: userUuid, created_at: createdAt, ...rest } = log;
                    // Format lastSeen date
                    const formattedCreatedAt = new Date(createdAt).toLocaleDateString('en-GB', {
                        day: 'numeric',
                        month: 'short',
                        year: 'numeric',
                    });
                    return {
                        ...rest,
                        createdAt: formattedCreatedAt,
                        userUuid,
                    };
                });
                return {
                    logs: javaScriptifiedUserFields,
                    totalPages: response.data.total_pages,
                    currentPage: response.data.current_page,
                    data: true,
                }
            } else {
                return emptyObj
            }
        }
        catch (error) {
            console.error('Error fetching logs:', error);
            return emptyObj
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