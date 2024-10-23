import { useState, useEffect } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { useDispatch } from "react-redux";
import useIsComponentMounted from "../../../../hooks/useIsComponentMounted.js";
import { setLoader } from "../../../../redux/loader/loaderSlice";
import { PATH_TO } from "../../../../router/routePaths.js";
import Pagination from "../../../../components/Pagination/Pagination.jsx";
import { getUserMessages } from "../../../../config/apiHandler/admin/userMessages.js"
import UserMessageContainer from "./UserMessageContainer.jsx";
import "./userMessages.css"

/**
 * Component returns HTML div with selected user's messages
 * 
 * Should be passed a location state when navigated to: the selected user's id, name, and email.
 * 
 * @param {object} state //selected user passed as location state
 * @param {string} state.name
 * @param {string} state.email
 * @param {number} state.id
 * @returns {React.ReactElement}
 * @example
 * navigate("userMessages", { state: user })
 */
function UserMessages() {
    const location = useLocation();
    const user = location.state;
    const { name, email, id } = user;

    if (!user || !user.name || !user.email || !user.id) {
        console.error("Missing location state in UserMessages.")
    }

    const dispatch = useDispatch();
    const navigate = useNavigate();

    // Only set state if component is mounted
    const isComponentMounted = useIsComponentMounted();

    // Store messages and pagination
    const [messages, setMessages] = useState([]);
    const [curPage, setCurPage] = useState([]);
    const [tPages, setTPages] = useState([]);

    // Request user info upon component mount
    useEffect(() => {
        getMessages();
    }, [])

    function getMessages(pageNr = 1) {
        if (id === 0) {
            return
        }
        dispatch(setLoader(true))
        getUserMessages(pageNr, id)
            .then(response => {
                if (isComponentMounted()) {
                    if (response.data) {
                        setMessages(response.messages);
                        setCurPage(response.currentPage);
                        setTPages(response.totalPages);
                    } else {
                        setMessages([]);
                        setCurPage(1);
                        setTPages(1);
                    }
                }
            })
            .catch(error => {
                console.warn("getUserMessages (in UserMessages) encountered an error", error);
            })
            .finally(() => {
                dispatch(setLoader(false));
            })
    }

    function handlePagination(newPage) {
        if (Number.isInteger(newPage) && newPage >= 1 && newPage <= totalPages) {
            getMessages(newPage);
        }
    }



    return (
        <div className="Users UserMessages">
            <h3>User Messages</h3>

            <div className="UserMessages-btnContainer">
                <button onClick={() => { navigate(PATH_TO.adminArea_userInfo, { state: id }) }}>Back to User's Info</button>
                <button onClick={() => { navigate(PATH_TO.adminArea_usersTable) }}>Back to Users Table</button>
            </div>

            <h4 >User</h4>

            <div>
                <p><b>User:</b> {name}</p>
                <p><b>Email:</b> {email}</p>
            </div>

            <h4>Messages</h4>

            {
                messages && messages.length > 0 && (
                    <>
                        {messages && (
                            messages.map((message, index) => (
                                <UserMessageContainer
                                    theMessage={message}
                                    key={index}
                                />
                            ))
                        )}
                    </>
                )
            }
            {
                ((messages && messages.length == 0) || (!messages)) && (
                    <p><b>No message found.</b></p>
                )
            }
            {
                tPages > 1 && (
                    <Pagination
                        currentPage={curPage}
                        totalPages={tPages}
                        handlePageChange={handlePagination}
                    />
                )
            }
        </div>
    );
}
export default UserMessages;