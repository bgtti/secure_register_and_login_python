import { api } from "../../axios";
import apiEndpoints from "../../apiEndPoints";

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
 * @param {number} userId 
 * @returns {object}
 * 
 * @example
 * //Usage:
 * getUserLogs(1, 1234)
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
 *            "user_id": 1234
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
 *            "userId": 1234
 *        },
 *        ...
 *  ]
 * }
 */
export function getUserLogs(pageNr, userId) {
    let thePageNum = parseInt(pageNr);
    thePageNum = (pageNr && Number.isInteger(thePageNum) && thePageNum >= 1) ? thePageNum : 1;
    let theId = parseInt(userId);
    theId = (userId && Number.isInteger(userId) && userId >= 1) ? userId : "";

    const emptyObj = {
        logs: [],
        totalPages: 1,
        currentPage: 1,
        data: false
    }

    if (theId === "") {
        console.warn("No user id provided to get user logs.")
        return emptyObj
    }

    let requestData = {
        "page_nr": thePageNum,
        "user_id": theId,
    }

    const getData = async () => {
        try {
            const response = await api.post(apiEndpoints.adminGetUserLogs, requestData)
            if (response.status === 200 && response.data.logs.length > 0) {
                const javaScriptifiedUserFields = response.data.logs.map(log => {
                    const { user_id: userId, created_at: createdAt, ...rest } = log;
                    // Format lastSeen date
                    const formattedCreatedAt = new Date(createdAt).toLocaleDateString('en-GB', {
                        day: 'numeric',
                        month: 'short',
                        year: 'numeric',
                    });
                    return {
                        ...rest,
                        createdAt: formattedCreatedAt,
                        userId,
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