import { apiHandle404 } from "../../axios";
import { apiEndpoints } from "../../apiEndpoints";
import { MESSAGES_TABLE_REQUEST } from "../../../utils/constants";

/**
 * Function makes api call to retrieve an array of messages sent by a particular user.
 * 
 * Pagination is expected to handle the returned data.
 * 
 * Given an invalid id or error response, will return an empty object.
 * 
 * Sends the key 'data' as a boolean to indicate whether there is response data or not.
 * @async
 * @param {object} data 
 * @param {number} [data.pageNr = 1] integer, must be positive
 * @param {number} [data.itemsPerPage = 25] integer between 5 and 50, must be multiple of 5
 * @param {string} [data.orderSort = "descending"] enum: ["descending", "ascending"]
 * @param {string} [data.filterBy = "all"] enum: ["answer_needed", "answer_not_needed", "all"]
 * @param {boolean} [data.includeSpam = false] 
 * @returns {Promise<object>}
 * 
 * @example
 * //Usage:
 * getAllMessages({pageNr: 1, itemsPerPage: 25})
 * 
 * //Response from getUserMessages:
 * {
 *  currentPage: 1,
 *  totalPages: 1,
 *  data: true,
 *  messages: [
 *       {
 *            "date": "Tue, 09 Jan 2024 21:07:38 GMT",
 *            "senderName": "John",
 *            "senderEmail": "john@example.com",
 *            "senderIsUser": true,
 *            "subject": "Login issue",
 *            "message": "Hi, I have a problem logging in.",
 *            "flagged": "blue",
 *            "isSpam": false,
 *            "answerNeeded": true,
 *            "wasAnswered": false,
 *            "answeredBy": "",
 *            "answerDate": "",
 *            "answer": ""
 *        },
 *        ...
 *  ]
 * }
 */
export function getAllMessages(data = {}) {
    const SORT = MESSAGES_TABLE_REQUEST.order_sort;
    const FILTER = MESSAGES_TABLE_REQUEST.filter_by;

    // validate data - if validation fails, defaults are set
    let pageNr = parseInt(data.pageNr);
    pageNr = (data.pageNr && Number.isInteger(pageNr) && pageNr >= 1) ? pageNr : 1;

    let itemsPerPage = parseInt(data.itemsPerPage);
    itemsPerPage = (data.itemsPerPage && Number.isInteger(itemsPerPage) && itemsPerPage >= 5 && itemsPerPage <= 50 && itemsPerPage % 5 === 0) ? itemsPerPage : 25;

    let orderSort = (data.orderSort && SORT.includes(data.orderSort)) ? data.orderSort : "descending";
    let filterBy = (data.filterBy && FILTER.includes(data.filterBy)) ? data.filterBy : "all";
    let includeSpam = (typeof data.includeSpam === "boolean") ? data.includeSpam : false;

    let requestData = {
        "page_nr": pageNr,
        "items_per_page": itemsPerPage,
        "order_sort": orderSort,
        "filter_by": filterBy,
        "include_spam": includeSpam
    }

    const emptyObj = {
        messages: [],
        totalPages: 1,
        currentPage: 1,
        data: false
    }

    const getData = async () => {
        try {
            const response = await apiHandle404.post(apiEndpoints.adminMessagesTable, requestData)
            if (response.status === 200 && response.data.messages.length > 0) {
                const javaScriptifiedMessageFields = response.data.messages.map(message => {
                    const { sender_name: senderName, sender_email: senderEmail, sender_is_user: senderIsUser, answer_needed: answerNeeded, was_answered: wasAnswered, answered_by: answeredBy, answer_date: answerDate, is_spam: isSpam, user_id: userId, ...rest } = message;
                    // Format date
                    const dateFormat = {
                        day: "numeric",
                        month: "short",
                        year: "numeric",
                        hour: "numeric",
                        minute: "numeric",
                        timeZoneName: "shortOffset"
                    }
                    const formattedDateMessage = new Date(message.date).toLocaleString("en-GB", dateFormat);
                    const formattedDateAnswer = new Date(answerDate).toLocaleString("en-GB", dateFormat);
                    return {
                        ...rest,
                        date: formattedDateMessage,
                        senderName,
                        senderEmail,
                        senderIsUser,
                        answerDate: formattedDateAnswer,
                        answerNeeded,
                        wasAnswered,
                        answeredBy,
                        userId,
                        isSpam
                    };
                });
                return {
                    messages: javaScriptifiedMessageFields,
                    totalPages: response.data.total_pages,
                    currentPage: response.data.current_page,
                    data: true,
                }
            } else {
                return Promise.resolve(emptyObj)
            }
        }
        catch (error) {
            console.error('Error fetching messages:', error);
            return Promise.resolve(emptyObj)
        }
    }

    return getData();
};