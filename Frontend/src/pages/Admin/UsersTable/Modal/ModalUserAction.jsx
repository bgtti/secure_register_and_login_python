import { PropTypes } from "prop-types";
import "./modalUserAction.css"

/**
 * Component returns fragment with information about a user to be deleted or blocked.
 * 
 * This component should be included inside the modal wrapper found at src>components>Modal through props.
 * 
 * @visibleName Admin Area: Users' Table: Modal Block or Delete User
 * @param {object} props
 * @param {string} props.action accepts either "block" or "delete"
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

    const actionLowerCase = action.toLowerCase()
    const actionCapitalized = actionLowerCase.charAt(0).toUpperCase() + actionLowerCase.slice(1);

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
                <button className="ModalUserAction-ActionBtn">{actionCapitalized} User</button>
                <button onClick={modalToggler}>Cancel</button>
            </div>
        </>
    );
};

ModalUserAction.propTypes = {
    action: PropTypes.oneOf(['block', 'delete']),
    user: PropTypes.shape({
        name: PropTypes.string.isRequired,
        email: PropTypes.string.isRequired,
        uuid: PropTypes.string.isRequired
    }).isRequired,
    modalToggler: PropTypes.func.isRequired
};

export default ModalUserAction;