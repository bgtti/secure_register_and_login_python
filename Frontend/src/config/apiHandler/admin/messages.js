import { apiHandle404 } from "../../axios";
import apiEndpoints from "../../apiEndpoints";
import { MESSAGES_TABLE_REQUEST } from "../../../utils/constants";

/**
 * Function makes api call to retrieve an array of messages sent by a particular user.
 * 
 * Pagination is expected to handle the returned data.
 * 
 * Given an invalid id or error response, will return an empty object.
 * 
 * Sends the key 'data' as a boolean to indicate whether there is response data or not.
 * 
 * @param {object} data 
 * @param {number} [data.pageNr = 1] integer, must be positive
 * @param {number} [data.itemsPerPage = 25] integer between 5 and 50, must be multiple of 5
 * @param {string} [data.orderSort = "descending"] enum: ["descending", "ascending"]
 * @param {string} [data.filterBy = "all"] enum: ["answer_needed", "answer_not_needed", "all"]
 * @param {string} [data.includeSpam = "false"] enum: ["true", "false"]
 * @returns {object}
 * 
 * @example
 * //Usage:
 * getAllMessages({pageNr: 1, itemsPerPage: 25})
 * 
 * //Original API response:
 * {
 *    "current_page": 1,
 *    "messages": [
 *        {
 *            "id": 1,
 *            "date": "Tue, 09 Jan 2024 21:07:38 GMT",
 *            "sender_name": "John",
 *            "sender_email": "john@example.com",
 *            "sender_is_user": true,
 *            "subject": "Login issue",
 *            "message": "Hi, I have a problem logging in.",
 *            "flagged": "blue",
 *            "is_spam": false,
 *            "answer_needed": "true",
 *            "was_answered": "false",
 *            "answered_by": "",
 *            "answer_date": "",
 *            "answer": ""
 *        },
 *        ...
 *    ],
 *    "query": {
 *        "items_per_page": 25,
 *        "order_sort": "descending",
 *        "filter_by": "answer_needed",
 *        "page_nr": 1
 *    },
 *    "response": "success",
 *    "total_pages": 1,
 *    "current_page": 1,
 * }
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
    const SPAM = MESSAGES_TABLE_REQUEST.include_spam;

    // validate data - if validation fails, defaults are set
    let pageNr = parseInt(data.pageNr);
    pageNr = (data.pageNr && Number.isInteger(pageNr) && pageNr >= 1) ? pageNr : 1;

    let itemsPerPage = parseInt(data.itemsPerPage);
    itemsPerPage = (data.itemsPerPage && Number.isInteger(itemsPerPage) && itemsPerPage >= 5 && itemsPerPage <= 50 && itemsPerPage % 5 === 0) ? itemsPerPage : 25;

    let orderSort = (data.orderSort && SORT.includes(data.orderSort)) ? data.orderSort : "descending";
    let filterBy = (data.filterBy && FILTER.includes(data.filterBy)) ? data.filterBy : "answer_needed";
    let includeSpam = (data.includeSpam && SPAM.includes(data.includeSpam)) ? data.includeSpam : "false";

    let requestData = {
        "page_nr": pageNr,
        "items_per_page": itemsPerPage,
        "order_sort": orderSort,
        "filter_by": filterBy,
        "includeSpam": includeSpam
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
                    const { sender_name: senderName, sender_email: senderEmail, sender_is_user: senderIsUser, answer_needed: answerNeeded, was_answered: wasAnswered, answered_by: answeredBy, answer_date: answerDate, is_spam: isSpam, ...rest } = message;
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
                        answerNeeded: answerNeeded === "false" ? false : true,
                        wasAnswered: wasAnswered === "false" ? false : true,
                        answeredBy,
                        isSpam
                    };
                });
                return {
                    message: javaScriptifiedMessageFields,
                    totalPages: response.data.total_pages,
                    currentPage: response.data.current_page,
                    data: true,
                }
            } else {
                return emptyObj
            }
        }
        catch (error) {
            console.error('Error fetching messages:', error);
            return emptyObj
        }
    }

    return getData();
};