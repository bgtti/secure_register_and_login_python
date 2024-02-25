import { useState, useEffect, lazy, Suspense, useRef } from "react";
import PropTypes from 'prop-types';
import { useDispatch, useSelector } from "react-redux";
import useIsComponentMounted from "../../../../hooks/useIsComponentMounted.js";
import { setLoader } from "../../../../redux/loader/loaderSlice"
import { getUserInfo } from "../../../../config/apiHandler/admin/userInfo.js"
import Pagination from "../Pagination/Pagination.jsx";
import "./userInformation.css"

/**
 * Component returns HTML div with user base information
 * 
 * Child component: UserLogRow
 * 
 * @visibleName Admin Area: Users' Table: User Information
 * @param {object} props
 * @param {number} props.userId
 * @param {func} props.setShowUserLogs
 * @param {func} props.setShowUserInfo  
 * @param {func} props.selectUserAction
 * @param {func} props.toggleModal 
 * @returns {React.ReactElement}
 */
function UserInformation(props) {
    const { userId, setShowUserInfo, setShowUserLogs, selectUserAction, toggleModal } = props;

    const dispatch = useDispatch();
    const isComponentMounted = useIsComponentMounted();

    const [user, setUser] = useState({});

    useEffect(() => {
        getInfo();
    }, [])

    function getInfo(id = userId) {
        if (id === 0) {
            return
        }
        // dispatch(setLoader(true))
        // getUserInfo(userId)
        //     .then(response => {
        //         if (isComponentMounted()) {
        //             if (response.data) {
        //                 setUser(response.user)
        //             } else {
        //                 setUser({})
        //             }
        //         }
        //     })
        //     .catch(error => {
        //         console.warn("getUserInfo (in UsersTable > UserInfo) encountered an error", error);
        //     })
        //     .finally(() => {
        //         dispatch(setLoader(false));
        //     })
    }

    //CHECK HERE
    function handleReturn() {
        selectUserAction("", "");
        setShowUserInfo(false);
    }
    function goToLogs() {
        selectUserAction(userId, "logs");
        setShowUserInfo(false);
        setShowUserLogs(true);
    }

    return (
        <>
            <div className="UserInformation">
                <button onClick={handleReturn}>Back to Users Table</button>
                <h3>User Information</h3>
                <div className="UserInformation-InfoGrid">
                    {
                        user && user.name && (
                            <>
                                <div>
                                    <p><b className="UserInformation-bold">User:</b></p>
                                    <p>{user.name}</p>
                                </div>
                                <div>
                                    <p><b className="UserInformation-bold">Email:</b></p>
                                    <p>{user.email}</p>
                                </div>
                                <div>
                                    <p><b className="UserInformation-bold">Flag:</b></p>
                                    <p>{user.flagged}</p>
                                </div>
                                <div>
                                    <p><b className="UserInformation-bold">Blocked:</b></p>
                                    <p>{user.isBlocked}</p>
                                </div>
                                <div>
                                    <p><b className="UserInformation-bold">User type:</b></p>
                                    <p>{user.access}</p>
                                </div>
                                <div>
                                    <p><b className="UserInformation-bold">Last seen:</b></p>
                                    <p>{user.lastSeen}</p>
                                </div>
                            </>
                        )
                    }
                </div>
                <hr className="UserInformation-hr" />
                <h3>Actions</h3>
                <div className="UserInformation-ActBtnContainer">
                    <button
                        className="UserInformation-ActBtn"
                        onClick={() => { selectUserAction(userId, "flag"); toggleModal() }}>
                        Change flag
                    </button>
                    <button
                        className="UserInformation-ActBtn"
                        onClick={() => { selectUserAction(userId, "type change"); toggleModal() }}>
                        Change user type
                    </button>
                    <button
                        className="UserInformation-ActBtn"
                        onClick={() => { selectUserAction(userId, (user.isBlocked === "false" ? "block" : "unblock")); toggleModal() }}>
                        Block user
                    </button>
                    <button
                        className="UserInformation-ActBtn"
                        onClick={() => { selectUserAction(userId, "delete"); toggleModal() }}>
                        Delete user
                    </button>
                </div>
                <hr className="UserInformation-hr" />
                <h3>Activity Logs</h3>
                <div>
                    <button
                        className="UserInformation-ActBtn"
                        onClick={goToLogs}
                    >Show Logs</button>
                </div>
                <hr className="UserInformation-hr" />
                <h3>Message</h3>
                <div>
                    <button
                        className="UserInformation-ActBtn">Show Messages</button>
                </div>

            </div>
        </>
    );
};

UserInformation.propTypes = {
    userId: PropTypes.number.isRequired,
    toggleModal: PropTypes.func.isRequired,
    setShowUserInfo: PropTypes.func.isRequired,
    setShowUserLogs: PropTypes.func.isRequired,
    selectUserAction: PropTypes.func.isRequired,
};

export default UserInformation;  