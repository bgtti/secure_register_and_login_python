import { api } from "../../axios";
import apiEndpoints from "../../apiEndPoints";

// In this file: API Handlers to delete user and block/unblock user

/**
 * Function makes api call to block or unblock a particular user.
 * 
 * @param { number } userId
 * @param { boolean } block false to unblock & true to block
 * @returns { object } success as a boolean
 * @example
 * Example return if response 200:
 * { success: true }
    * Example return if response not 200:
 * { success: false }
 */
export function blockOrUnblockUser(userId, block) {
    let the_id = (userId && (typeof userId === "number")) ? userId : "";
    let is_block = (typeof block === "boolean") ? block : "";

    if (the_id === "" || is_block === "") {
        return console.warn("Invalid input. Cannot block or unblock user.")
    }

    let requestData = {
        "user_id": the_id,
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
 * @param {number} userId 
 * @returns {object} success as a boolean
 * @example
 * Example return if response 200:
 * {success: true}
 * Example return if response not 200:
 * {success: false}
 */
export function deleteUser(userId) {
    let the_id = (userId && (typeof userId === "number")) ? userId : "";

    if (the_id === "") {
        return console.warn("Invalid input. Cannot delete user.")
    }

    let requestData = {
        "user_id": the_id
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