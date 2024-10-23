import { apiHandle404 } from "../../axios";
import apiEndpoints from "../../apiEndpoints";

/**
 * Function makes api call to retrieve an array of messages sent by a particular user.
 * 
 * Pagination is expected to handle the returned data.
 * 
 * Given an invalid id or error response, will return an empty object.
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
 *    "messages": [
 *        {
 *            "date": "Tue, 09 Jan 2024 21:07:38 GMT",
 *            "sender_name": "John",
 *            "sender_email": "john@example.com",
 *            "message": "Hi, I have a problem logging in.",
 *            "flagged": "blue",
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
 *        "ordered_by": "date",
 *        "page_nr": 1
 *    },
 *    "response": "success",
 *    "total_pages": 1
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
 *            "message": "Hi, I have a problem logging in.",
 *            "flagged": "blue",
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
export function getUserMessages(pageNr, userId) {
    let thePageNum = parseInt(pageNr);
    thePageNum = (pageNr && Number.isInteger(thePageNum) && thePageNum >= 1) ? thePageNum : 1;
    let theId = parseInt(userId);
    theId = (userId && Number.isInteger(userId) && userId >= 1) ? userId : "";

    const emptyObj = {
        messages: [],
        totalPages: 1,
        currentPage: 1,
        data: false
    }

    if (theId === "") {
        console.warn("No user id provided to get user messages.")
        return emptyObj
    }

    let requestData = {
        "page_nr": thePageNum,
        "user_id": theId,
    }

    const getData = async () => {
        try {
            const response = await apiHandle404.post(apiEndpoints.adminGetUserMessages, requestData)
            if (response.status === 200 && response.data.messages.length > 0) {
                const javaScriptifiedMessageFields = response.data.messages.map(message => {
                    const { sender_name: senderName, sender_email: senderEmail, answer_needed: answerNeeded, was_answered: wasAnswered, answered_by: answeredBy, answer_date: answerDate, ...rest } = message;
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
                        answerDate: formattedDateAnswer,
                        senderName,
                        senderEmail,
                        answerNeeded: answerNeeded === "false" ? false : true,
                        wasAnswered: wasAnswered === "false" ? false : true,
                        answeredBy
                    };
                });
                return {
                    messages: javaScriptifiedMessageFields,
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