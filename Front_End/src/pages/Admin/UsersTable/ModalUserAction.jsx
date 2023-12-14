// import { useState } from "react";
import { PropTypes } from "prop-types";
import "./modalUserAction.css"

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