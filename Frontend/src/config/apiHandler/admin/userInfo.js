import { apiHandle404 } from "../../axios";
import apiEndpoints from "../../apiEndpoints";

/**
 * Function makes api call to retrieve base information for a particular user.
 * 
 * Pagination is expected to handle the returned data.
 * 
 * Given an invalid id or error 404 response, will return an empty object.
 * 
 * Sends the key 'data' as a boolean to indicate whether there is response data or not.
 * 
 * @param {number} userId integer, must be positive greater than 0
 * @returns {Promise<object>}
 * 
 * @example
 * //Usage:
 * getUserInfo(1234)
 *     .then(response => {
 *         console.log(response);
 *     });
 * 
 * //Response from getUserInfo:
 * {
 *  data: true,
 *  user: {
                "id": 1234
                "name": "Frank Torres",
                "email": "frank.torres@fakemail.com",
                "createdAt": "09 Jan 2024",
                "lastSeen": "09 Jan 2024",
                "access": "user",
                "flagged": "blue",
                "isBlocked": "false"
                },
 * }
 */
export function getUserInfo(userId) {
    let theId = parseInt(userId);
    theId = (userId && Number.isInteger(userId) && userId >= 1) ? userId : "";

    const emptyObj = {
        user: {},
        data: false
    }

    if (theId === "") {
        console.warn("No user id provided to get user logs.")
        return Promise.resolve(emptyObj)
    }

    let requestData = {
        "user_id": theId,
    }

    const getData = async () => {
        try {
            const response = await apiHandle404.post(apiEndpoints.adminGetUserInfo, requestData)
            if (response.status === 200) {
                const javaScriptifiedUserFields = {
                    ...response.data.user,
                    createdAt: new Date(response.data.user.created_at).toLocaleDateString('en-GB', {
                        day: 'numeric',
                        month: 'short',
                        year: 'numeric',
                    }),
                    lastSeen: new Date(response.data.user.last_seen).toLocaleDateString('en-GB', {
                        day: 'numeric',
                        month: 'short',
                        year: 'numeric',
                    }),
                    isBlocked: response.data.user.is_blocked,
                };
                return {
                    user: javaScriptifiedUserFields,
                    data: true,
                }
            } else {
                Promise.resolve(emptyObj)
            }
        }
        catch (error) {
            console.error('Error fetching logs:', error);
            Promise.resolve(emptyObj)
        }
    }

    return getData();
};