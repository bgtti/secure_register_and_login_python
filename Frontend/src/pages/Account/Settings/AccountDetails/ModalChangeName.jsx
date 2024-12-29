import { useState, useEffect } from "react";
import { useDispatch } from "react-redux";
import { PropTypes } from "prop-types";
import useIsComponentMounted from "../../../../hooks/useIsComponentMounted.js";
import { setLoader } from "../../../../redux/loader/loaderSlice.js"
import { acctNameChange } from "../../../../config/apiHandler/authProfile/changeName.js"
import InputName from "../../../../components/Auth/InputName.jsx"
import ErrorMessage from "../../../../components/ErrorMessage/ErrorMessage.jsx"
import "./modalAccountDetailChange.css"

/**
 * This component is a modal used to change the user's name.
 * 
 * @param {object} props
 * @param {func} props.modalToggler opens/closes modal
 * @param {object} props.user 
 * @param {string} props.user.name
 * @returns {React.ReactElement}
 */
function ModalChangeName(props) {
    const { modalToggler, user } = props;

    const userAgent = navigator.userAgent; //info to be passed on to BE

    const isComponentMounted = useIsComponentMounted();
    const dispatch = useDispatch();

    // State set by input field component
    const [name, setName] = useState("");
    const [nameIsValid, setNameIsValid] = useState(false);

    // State set by api call
    const [infoMessage, setInfoMessage] = useState("");
    const [formSubmitted, setFormSubmitted] = useState(false);

    //if a form error was shown, hide it when the user starts to correct the input
    useEffect(() => {
        if (infoMessage !== "") {
            setInfoMessage("");
            setFormSubmitted(false);
        }
    }, [name]);

    const handleSubmit = (e) => {
        e.preventDefault();

        let oldName = user.name
        let dataChanged = oldName.localeCompare(name) !== 0

        if (!dataChanged) {
            console.log("No changes detected: new name is the same as old name.");
            setFormSubmitted(true);
            setInfoMessage("Submission failed: no changes detected to name.");
            return
        }

        dispatch(setLoader(true));

        const errorMsg = "An error occurred. Please close modal and try again."
        const successMsg = "Name changed successfully!"

        const handleResponse = (response) => {
            if (isComponentMounted()) {
                setInfoMessage(response.success ? successMsg : errorMsg);
            }
        };
        const handleError = (error) => {
            console.warn("clickHandler in modal encountered an error", error);
        };

        const handleFinally = () => {
            setFormSubmitted(true);
            dispatch(setLoader(false));
        };

        acctNameChange(name, userAgent)
            .then(response => handleResponse(response))
            .catch(error => handleError(error))
            .finally(handleFinally);

    }


    return (
        <>
            <form onSubmit={handleSubmit} className="ModalChangeName MAIN-form">

                <p >
                    Current name: {user.name}
                </p>

                <InputName
                    name={name}
                    setName={setName}
                    setNameIsValid={setNameIsValid}
                />
                {
                    infoMessage !== "" && (
                        < ErrorMessage message={infoMessage} ariaDescribedby="api-response-error" />
                    )
                }
                {
                    infoMessage === "" && (
                        <br />
                    )
                }

                <div className="Modal-BtnContainer">
                    <button disabled={formSubmitted || !nameIsValid} type="submit" className="Modal-ActionBtn">Save</button>
                    <button onClick={modalToggler}>{formSubmitted ? "Close" : "Cancel"}</button>
                </div>
            </form>
        </>
    );
};

ModalChangeName.propTypes = {
    modalToggler: PropTypes.func.isRequired,
    user: PropTypes.shape({
        name: PropTypes.string.isRequired,
    }).isRequired,
};

export default ModalChangeName;