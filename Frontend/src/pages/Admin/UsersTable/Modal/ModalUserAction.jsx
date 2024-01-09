import { useState } from "react";
import { PropTypes } from "prop-types";
import { useDispatch, useSelector } from "react-redux";
import useIsComponentMounted from "../../../../hooks/useIsComponentMounted.js";
import { setLoader } from "../../../../redux/loader/loaderSlice"
import { blockOrUnblockUser, deleteUser } from "../../../../config/apiHandler/admin"
import "./modalUserAction.css"

/**
 * Component returns fragment with information about a user to be deleted or blocked.
 * 
 * This component should be included inside the modal wrapper found at src>components>Modal through props.
 * 
 * @visibleName Admin Area: Users' Table: Modal Block or Delete User
 * @param {object} props
 * @param {string} props.action accepts only one of ["block", "unblock","delete"]
 * @param {object} props.user
 * @param {string} props.user.name
 * @param {string} props.user.email
 * @param {string} props.user.uuid
 * @param {func} props.toggleModal 
 * @returns {React.ReactElement}
 * 
 * @example
 * import Modal from ".../components/Modal/Modal"
 * import { useState} from "react";
 * //inside the functional component:
 * const [showModal, setShowModal] = useState(false)
 * function toggleModal() { setShowModal(!showModal)}
 * const modalInfo = <ModalUserAction user={name: "Josy", email: "j@example", uuid: "12345"} action="block" modalToggler={toggleModal} /> //<- refers to this component!
 * return (
 * <Modal title="Block User" content={modalInfo} modalStatus={showModal} setModalStatus={setShowModal} ></Modal> //<-the modal wrapper component with this component passed as a prop
 * )
 */
function ModalUserAction(props) {
    const { action, user, modalToggler } = props;
    const { name, email, uuid } = user;

    const isComponentMounted = useIsComponentMounted();
    const dispatch = useDispatch();

    const [errorMessage, setErrroMessage] = useState("")


    const actionLowerCase = action.toLowerCase()
    const actionCapitalized = actionLowerCase.charAt(0).toUpperCase() + actionLowerCase.slice(1);

    function clickHandler() {
        dispatch(setLoader(true));

        const handleResponse = (response, successMessage) => {
            if (isComponentMounted()) {
                setErrroMessage(response.success ? successMessage : "An error occurred. Please reload the page and try again.");
            }
        };

        const handleError = (error) => {
            console.warn("clickHandler in modal encountered an error", error);
        };

        const handleFinally = () => {
            dispatch(setLoader(false));
        };

        if (actionLowerCase === "delete") {
            deleteUser(uuid)
                .then(response => handleResponse(response, "User deleted successfully! Close modal and reload the page to get an updated users table."))
                .catch(handleError)
                .finally(handleFinally);
        } else {
            const block = actionLowerCase === "block";
            blockOrUnblockUser(uuid, block)
                .then(response => handleResponse(response, `User ${actionLowerCase}ed successfully! Close modal and reload the page to get an updated users table.`))
                .catch(handleError)
                .finally(handleFinally);
        };
    }

    return (
        <>
            <p>You are about to {actionLowerCase} the following user:</p>
            <br />
            <p className="ModalUserAction-Bold">Name: {name}</p><b></b>
            <p className="ModalUserAction-Bold">Email: {email}</p>
            <br />
            <p>Are you sure you would like to proceed?</p>
            <br />
            <div className="ModalUserAction-BtnContainer">
                <button className="ModalUserAction-ActionBtn" disabled={(errorMessage !== "")} onClick={clickHandler}>{actionCapitalized} User</button>
                <button disabled={(errorMessage !== "")} onClick={modalToggler}>Cancel</button>
            </div>
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
    action: PropTypes.oneOf(["block", "unblock", "delete"]),
    user: PropTypes.shape({
        name: PropTypes.string.isRequired,
        email: PropTypes.string.isRequired,
        uuid: PropTypes.string.isRequired
    }).isRequired,
    modalToggler: PropTypes.func.isRequired
};

export default ModalUserAction;