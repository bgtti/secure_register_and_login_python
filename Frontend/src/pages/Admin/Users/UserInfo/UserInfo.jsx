import { useState, useEffect } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import useIsComponentMounted from "../../../../hooks/useIsComponentMounted.js";
import { setLoader } from "../../../../redux/loader/loaderSlice";
import { getUserInfo } from "../../../../config/apiHandler/admin/userInfo.js";
import { PATH_TO } from "../../../../router/routePaths.js";
import { USER_ACCESS_DIC } from "../../../../utils/constants.js"
import Modal from "../../../../components/Modal/Modal";
import ModalUserAction from "../ModalUserAction/ModalUserAction";
import Flag from "../../../../components/Flag/Flag.jsx";
import iconUserIsBlocked from "../../../../assets/icon_user_status_blocked.svg";
import iconUserIsNotBlocked from "../../../../assets/icon_user_status_unblocked.svg";
import iconUserTypeAdmin from "../../../../assets/icon_user_type_admin.svg";
import iconUserTypeUser from "../../../../assets/icon_user_type_user.svg";
import "./userInfo.css"
/**
 * Component returns HTML div with user base information
 * 
 * Should be passed a location state when navigated to: the selected user's id.
 * 
 * @param {number} state //userId as int, navigate("userInfo", { state: userId }) 
 * @returns {React.ReactElement}
 */
function UserInfo() {
    const location = useLocation();
    const userId = location.state;

    const dispatch = useDispatch();
    const navigate = useNavigate();

    // Only set state if component is mounted
    const isComponentMounted = useIsComponentMounted();

    // Some actions can only be performed by the super admin (deleting another admin)
    const adminUser = useSelector((state) => state.user);
    const isSuperAdmin = (adminUser.access === USER_ACCESS_DIC.super_admin);

    // User to be displayed in component
    const [user, setUser] = useState({});

    // Action selected through action buttons
    const [userAction, setUserAction] = useState("")

    //Actions allowed from this component (to be sent to modalUserAction)
    const ACTIONS = {
        block: "block",
        unblock: "unblock",
        delete: "delete",
        flag: "flag",
        typeChange: "type change",
    }

    //If a user is modified, request updated data
    const [updateData, setUpdateData] = useState(false)

    //Modal will open to perform selected action modal is displayed
    const [displayModal, setDisplayModal] = useState(false)

    //Modal setup: used in modal wrapper
    displayModal ? document.body.classList.add("Modal-active") : document.body.classList.remove("Modal-active");
    const modalContent = displayModal && userAction !== "" && (
        <ModalUserAction user={user} action={userAction} modalToggler={toggleModal} setUpdateData={setUpdateData} />
    );

    // Request user info upon component mount and if data is updated through an action
    useEffect(() => {
        getInfo();
    }, [])

    useEffect(() => {
        if (updateData) {
            setUserAction("");
            getInfo();
            setUpdateData(false);
        }
    }, [updateData])

    /**
     * Toggles modalUserAction display
     */
    function toggleModal() {
        setDisplayModal(!displayModal);
    }

    /**
     * Gets user object to pass on as props to children
     */
    function getUserObj() {
        let userObj = {
            name: user.name,
            email: user.email,
            id: user.id
        }
        return userObj;
    }

    /**
     * Fetch user data
     * 
     * @param {number} [id = userId] integer, must be positive
     * @returns {void} 
     */
    function getInfo(id = userId) {
        if (id === 0) {
            return
        }
        dispatch(setLoader(true))
        getUserInfo(userId)
            .then(response => {
                if (isComponentMounted()) {
                    if (response.data) {
                        setUser(response.user)
                    } else {
                        setUser({})
                    }
                }
            })
            .catch(error => {
                console.warn("getUserInfo (in UsersTable > UserInfo) encountered an error", error);
            })
            .finally(() => {
                dispatch(setLoader(false));
            })
    }


    return (
        <div className="Users UserInfo">
            {
                displayModal && userAction !== "" && (
                    <Modal
                        title={`${userAction} user`}
                        content={modalContent}
                        modalStatus={displayModal}
                        setModalStatus={setDisplayModal} ></Modal>
                )
            }

            <h3>User Info</h3>

            <button onClick={() => { navigate(PATH_TO.adminArea_usersTable) }}>Back to Users Table</button>

            <h4>Selected User</h4>
            {
                user && user.name && (
                    <>
                        <div className="UserInfo-InfoGrid">
                            <div>
                                <p><b>User:</b></p>
                                <p>{user.name}</p>
                            </div>
                            <div>
                                <p><b>Email:</b></p>
                                <p>{user.email}</p>
                            </div>
                            <div>
                                <p><b>Flag:</b></p>
                                <span className="UserInfo-iconContainer">
                                    <div className="MAIN-iconContainerCircle">
                                        <Flag flag={user.flagged} />
                                    </div>
                                    <p>({user.flagged})</p>
                                </span>
                            </div>
                            <div>
                                <p><b>Blocked:</b></p>
                                <span className="UserInfo-iconContainer">
                                    <div className="MAIN-iconContainerCircle">
                                        <img
                                            alt={`User is ${user.isBlocked === "false" ? "unblocked" : "blocked"}`}
                                            role="img"
                                            className={`${user.isBlocked === "false" ? "" : "MAIN-iconUserBlocked"}`}
                                            title={`User is ${user.isBlocked === "false" ? "unblocked" : "blocked"}`}
                                            src={user.isBlocked === "false" ? iconUserIsNotBlocked : iconUserIsBlocked}
                                        />
                                    </div>
                                    <p>({user.isBlocked})</p>
                                </span>
                            </div>
                            <div>
                                <p><b>User type:</b></p>
                                <span className="UserInfo-iconContainer">
                                    <div className="MAIN-iconContainerCircle">
                                        <img
                                            alt={`User is ${user.access === "user" ? "not" : ""} admin`}
                                            className="MAIN-iconUserType"
                                            role="img"
                                            title={`User is ${user.access === "user" ? "not" : ""} admin`}
                                            src={user.access === "user" ? iconUserTypeUser : iconUserTypeAdmin}
                                        />
                                    </div>
                                    <p>({user.access})</p>
                                </span>
                            </div>
                            <div>
                                <p><b>Last seen:</b></p>
                                <p>{user.lastSeen}</p>
                            </div>
                            <div>
                                <p><b>User since:</b></p>
                                <p>{user.createdAt}</p>
                            </div>
                        </div>

                        <hr className="UserInfo-hr" />

                        <h4>Actions</h4>
                        <div className="UserInfo-ActBtnContainer">
                            <button
                                className="UserInfo-ActBtn"
                                onClick={() => { setUserAction(ACTIONS.flag); toggleModal() }}>
                                Change flag
                            </button>
                            <button
                                className="UserInfo-ActBtn"
                                onClick={() => { setUserAction(ACTIONS.typeChange); toggleModal() }}>
                                Change user type
                            </button>
                            <button
                                className="UserInfo-ActBtn"
                                onClick={() => { setUserAction((user.isBlocked === "false" ? ACTIONS.block : ACTIONS.unblock)); toggleModal() }}>
                                {user.isBlocked === "false" ? "Block" : "Unblock"} user
                            </button>
                            {
                                ((user.access === USER_ACCESS_DIC.user) || (user.access === USER_ACCESS_DIC.admin && isSuperAdmin)) && (
                                    <button
                                        className="UserInfo-ActBtn UserInfo-DeleteBtn"
                                        onClick={() => { setUserAction(ACTIONS.delete); toggleModal() }}>
                                        Delete user
                                    </button>
                                )
                            }
                        </div>

                        <hr className="UserInfo-hr" />

                        <h4>Activity Logs</h4>
                        <div>
                            <button
                                className="UserInfo-ActBtn"
                                onClick={() => {
                                    let userObj = getUserObj();
                                    navigate(PATH_TO.adminArea_userLogs, { state: userObj })
                                }}>
                                Show Logs
                            </button>
                        </div>

                        <hr className="UserInfo-hr" />

                        <h4>Message</h4>
                        <div>
                            <button
                                className="UserInfo-ActBtn"
                                onClick={() => {
                                    let userObj = getUserObj();
                                    navigate(PATH_TO.adminArea_userMessages, { state: userObj })
                                }}>
                                Show Messages
                            </button>
                        </div>
                    </>
                )
            }
            {
                !user && !user.name && (
                    <p>An error occurred. Please reload the page and try again.</p>
                )
            }
        </div>
    );
};
export default UserInfo;