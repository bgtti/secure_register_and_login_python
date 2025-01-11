import { api } from "../../axios";
import apiEndpoints from "../../apiEndpoints.js";
import { FLAG_TYPES, USER_TYPE_REQUEST } from "../../../utils/constants";

// In this file: API Handlers to change user type, change user flag, delete user, and block/unblock user

/**
 * Function makes api call to change flag of a particular user.
 * 
 * @param { number } userId
 * @param {string} flagColour enum: ["red", "yellow", "purple", "blue"]
 * @returns { Promise<object> } success as a boolean
 * @example
 * Example return if response 200:
 * { success: true }
    * Example return if response not 200:
 * { success: false }
 */
export function changeUserFlag(userId, flagColour) {
    let theId = (userId && (typeof userId === "number")) ? userId : "";
    let theFlag = (flagColour && FLAG_TYPES.includes(flagColour)) ? flagColour : "";

    if (theId === "" || theFlag === "") {
        console.warn("Invalid input. Cannot change user flag.")
        return Promise.resolve({ success: false })
    }

    let requestData = {
        "user_id": theId,
        "new_flag_colour": theFlag
    }

    const getData = async () => {
        try {
            const response = await api.post(apiEndpoints.adminChangeUserFlag, requestData)
            if (response.status === 200) {
                return Promise.resolve({ success: true })
            } else {
                return Promise.resolve({ success: false })
            }
        }
        catch (error) {
            console.error("Error changing user flag:", error);
            return Promise.resolve({ success: false })
        }
    }

    return getData();
};

/**
 * Function makes api call to change access type of a particular user.
 * 
 * @param { number } userId
 * @param {string} accessType enum: ["user", "admin"]
 * @returns { Promise<object> } success as a boolean
 * @example
 * Example return if response 200:
 * { success: true }
    * Example return if response not 200:
 * { success: false }
 */
export function changeUserType(userId, accessType) {
    let allowed_types = Object.keys(USER_TYPE_REQUEST);
    let the_id = (userId && (typeof userId === "number")) ? userId : "";
    let the_type = (accessType && allowed_types.includes(accessType)) ? accessType : "";

    if (the_id === "" || the_type === "") {
        console.warn("Invalid input. Cannot change user access type.")
        return Promise.resolve({ success: false })
    }

    let requestData = {
        "user_id": the_id,
        "new_type": the_type
    }

    const getData = async () => {
        try {
            const response = await api.post(apiEndpoints.adminChangeUserAccessType, requestData)
            if (response.status === 200) {
                return Promise.resolve({ success: true })
            } else {
                return Promise.resolve({ success: false })
            }
        }
        catch (error) {
            console.error("Error changing user access type:", error);
            return Promise.resolve({ success: false })
        }
    }

    return getData();
};

/**
 * Function makes api call to block or unblock a particular user.
 * 
 * @param { number } userId
 * @param { boolean } block false to unblock & true to block
 * @returns { Promise<object> } success as a boolean
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
        console.warn("Invalid input. Cannot block or unblock user.")
        return Promise.resolve({ success: false })
    }

    let requestData = {
        "user_id": the_id,
        "block": is_block
    }

    const getData = async () => {
        try {
            const response = await api.post(apiEndpoints.adminBlockUnblockUser, requestData)
            if (response.status === 200) {
                return Promise.resolve({ success: true })
            } else {
                return Promise.resolve({ success: false })
            }
        }
        catch (error) {
            console.error("Error blocking/unblocking user:", error);
            return Promise.resolve({ success: false })
        }
    }

    return getData();
};

/**
 * Function makes api call to delete a particular user.
 * 
 * @param {number} userId 
 * @returns {Promise<object>} success as a boolean
 * @example
 * Example return if response 200:
 * {success: true}
 * Example return if response not 200:
 * {success: false}
 */
export function deleteUser(userId) {
    let the_id = (userId && (typeof userId === "number")) ? userId : "";

    if (the_id === "") {
        console.warn("Invalid input. Cannot delete user.")
        return Promise.resolve({ success: false })
    }

    let requestData = {
        "user_id": the_id
    }

    const getData = async () => {
        try {
            const response = await api.post(apiEndpoints.adminDeleteUser, requestData)
            if (response.status === 200) {
                return Promise.resolve({ success: true })
            } else {
                return Promise.resolve({ success: false })
            }
        }
        catch (error) {
            console.error('Error deleting user:', error);
            return Promise.resolve({ success: false })
        }
    }

    return getData();
};