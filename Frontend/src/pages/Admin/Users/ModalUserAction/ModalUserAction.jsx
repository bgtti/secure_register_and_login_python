import { useState } from "react";
import { PropTypes } from "prop-types";
import { useDispatch, useSelector } from "react-redux";
import useIsComponentMounted from "../../../../hooks/useIsComponentMounted.js";
import { setLoader } from "../../../../redux/loader/loaderSlice.js"
import { changeUserFlag, changeUserType, blockOrUnblockUser, deleteUser } from "../../../../config/apiHandler/admin/userActions.js"
import { USER_ACCESS_TYPES, FLAG_TYPES, IS_BLOCKED_TYPES, USER_TYPE_REQUEST } from "../../../../utils/constants.js";
import "./modalUserAction.css"

const CHANGE_USER_TYPE = {
    admin: "make this user admin",
    user: "remove this user's admin permissions"
}


/**
 * Component returns fragment with information about a user to be deleted or blocked.
 * 
 * This component should be included inside the modal wrapper found at src>components>Modal through props.
 * 
 * @visibleName Admin Area: Users' Table: Modal Block or Delete User
 * @param {object} props
 * @param {string} props.action accepts only one of ["block", "unblock","delete", "flag", "type change"]
 * @param {object} props.user
 * @param {string} props.user.name
 * @param {string} props.user.email
 * @param {string} props.user.access
 * @param {string} props.user.flagged
 * @param {number} props.user.id
 * @param {func} props.toggleModal 
 * @param {func} props.setUpdateData 
 * @returns {React.ReactElement}
 * 
 * @example
 * import Modal from ".../components/Modal/Modal"
 * import { useState} from "react";
 * //inside the functional component:
 * const [showModal, setShowModal] = useState(false)
 * function toggleModal() { setShowModal(!showModal)}
 * const modalInfo = <ModalUserAction user={name: "Josy", email: "j@example", id: 12345} action="block" modalToggler={toggleModal} setUpdateData={setUpdateData}/> //<- refers to this component!
 * return (
 * <Modal title="Block User" content={modalInfo} modalStatus={showModal} setModalStatus={setShowModal} ></Modal> //<-the modal wrapper component with this component passed as a prop
 * )
 */
function ModalUserAction(props) {
    const { action, user, modalToggler, setUpdateData } = props;
    const { name, email, flagged, access, id } = user;

    const isComponentMounted = useIsComponentMounted();
    const dispatch = useDispatch();

    const [errorMessage, setErrroMessage] = useState("")
    const [changesWereMade, setChangesWereMade] = useState(false)

    const [userFlag, setUserFlag] = useState(flagged)//only used when changing flag color
    const userTypeIsAdmin = useState(access === USER_TYPE_REQUEST.admin)//only used when changing user type

    const actionLowerCase = action.toLowerCase()
    const actionCapitalized = actionLowerCase.charAt(0).toUpperCase() + actionLowerCase.slice(1);

    const userBaseInfo = <><p><b className="ModalUserAction-Bold" >Name: </b>{name}</p><p><b className="ModalUserAction-Bold">Email: </b>{email}</p></>

    function getSaveBtnText() {
        if (action === "flag") { return "Save changes" }
        if (action === "type change") { return "Change type" }
        return `${actionCapitalized} User`
    }
    const saveBtnText = getSaveBtnText()


    function clickHandler() {
        dispatch(setLoader(true));

        const handleResponse = (response, successMessage) => {
            if (isComponentMounted()) {
                setErrroMessage(response.success ? successMessage : "An error occurred. Please reload the page and try again.");
                if (response.success) {
                    setChangesWereMade(true);
                    setUpdateData(true);
                }
            }
        };

        const handleError = (error) => {
            console.warn("clickHandler in modal encountered an error", error);
        };

        const handleFinally = () => {
            dispatch(setLoader(false));
        };

        let requestAction;
        let responseActionMessage;

        switch (actionLowerCase) {
            case "flag":
                requestAction = function () { return changeUserFlag(id, userFlag) };
                responseActionMessage = "User flag changed successfully!";
                break
            case "block":
                const block = actionLowerCase === "block";
                requestAction = function () { return blockOrUnblockUser(id, block) };
                responseActionMessage = `User ${actionLowerCase}ed successfully!`;
                break
            case "type change":
                let newType = userTypeIsAdmin ? "user" : "admin";
                requestAction = function () { return changeUserType(id, newType) };
                responseActionMessage = "User type changed successfully!";
            case "delete":
                requestAction = function () { return deleteUser(id) };
                responseActionMessage = "User deleted successfully!";
                break
            default:
                return console.error("Wrong action input in ModalUserAction.")
        }
        try {
            requestAction()
                .then(response => handleResponse(response, responseActionMessage))
                .catch(handleError)
                .finally(handleFinally);
        } catch {
            console.error("Error in ModalUserAction", error);
            dispatch(setLoader(false));
        }
    }

    return (
        <>
            {
                !changesWereMade && action === "type change" && (
                    <>
                        <p>You are about to change the type the following user:</p>
                        <br />
                        {userBaseInfo}
                        <p><b className="ModalUserAction-Bold" >Type: </b> {access}</p>
                        <br />
                        <p><b className="ModalUserAction-Bold" >You are about to {access === USER_TYPE_REQUEST.admin ? CHANGE_USER_TYPE.user : CHANGE_USER_TYPE.admin}.</b></p>
                        <br />
                    </>
                )
            }
            {
                changesWereMade && action === "type change" && (
                    <>
                        <p>The type of the following user was changed:</p>
                        <br />
                        {userBaseInfo}
                        <br />
                        <p>User {userTypeIsAdmin ? "now has " : "no longer has "} admin access.</p>
                    </>
                )
            }
            {
                !changesWereMade && action === "flag" && (
                    <>
                        <p>Select the flag colour of the following user:</p>
                        <br />
                        {userBaseInfo}
                        <p><b className="ModalUserAction-Bold" >Flag: </b> {flagged}</p>
                        <br />
                        <div className="MAIN-form-display-table ModalUserAction-displayTable">
                            <label htmlFor="changeFlag">Select new flag colour:</label>
                            <select
                                className="ModalUserAction-Select"
                                name="changeFlag"
                                id="changeFlag"
                                defaultValue={userFlag}
                                onChange={(e) => { setUserFlag(e.target.value) }}>
                                {
                                    FLAG_TYPES.map((item, index) => (
                                        <option value={item} key={index}>{item}</option>
                                    ))
                                }
                            </select>
                        </div>
                    </>
                )
            }
            {
                changesWereMade && action === "flag" && (
                    <>
                        <p>The type of the following user was changed:</p>
                        <br />
                        {userBaseInfo}
                        <br />
                        <p>New flag colour: {userFlag}.</p>
                    </>
                )
            }
            {!changesWereMade && action !== "type change" && action !== "flag" && (
                <>
                    <p>You are about to {actionLowerCase} the following user:</p>
                    <br />{userBaseInfo} <br />
                </>
            )}
            {changesWereMade && action !== "type change" && action !== "flag" && (
                <>
                    <p>The following user was {actionLowerCase}{actionLowerCase === "delete" ? "d" : "ed"}:</p>
                    <br />{userBaseInfo} <br />
                </>
            )}
            {!changesWereMade && (
                <>
                    {
                        action !== "flag" && (
                            <>
                                {/* <br /> */}
                                <p>Are you sure you would like to proceed?</p>
                            </>
                        )
                    }
                    <br />
                    <div className="ModalUserAction-BtnContainer">
                        <button className="ModalUserAction-ActionBtn" disabled={(errorMessage !== "")} onClick={clickHandler}>{saveBtnText}
                        </button>
                        <button disabled={(errorMessage !== "")} onClick={modalToggler}>Cancel</button>
                    </div>
                </>
            )}
            {
                errorMessage !== "" && (
                    <>
                        <br />
                        <p className="MAIN-error-message">
                            <i>{errorMessage}</i>
                        </p>
                    </>
                )
            }
        </>
    );
};

ModalUserAction.propTypes = {
    action: PropTypes.oneOf(["block", "unblock", "delete", "flag", "type change"]),
    user: PropTypes.shape({
        name: PropTypes.string.isRequired,
        email: PropTypes.string.isRequired,
        access: PropTypes.string.isRequired,
        flagged: PropTypes.string.isRequired,
        id: PropTypes.number.isRequired
    }).isRequired,
    modalToggler: PropTypes.func.isRequired,
    setUpdateData: PropTypes.func.isRequired,
};

export default ModalUserAction;