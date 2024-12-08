import { useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { PropTypes } from "prop-types";
import useIsComponentMounted from "../../../../hooks/useIsComponentMounted.js";
import { setLoader } from "../../../../redux/loader/loaderSlice.js"
import { acctRequestVerifyEmail } from "../../../../config/apiHandler/authAccount/verifyEmail.js"
import "./modalAccountDetailChange.css" // TODO

/**
 * This component is a modal used start the account verification process.
 * 
 * @visibleName Modal Initiate Email Verification
 * @param {object} props
 * @param {func} props.modalToggler opens/closes modal
 * @returns {React.ReactElement}
 */
function ModalAccountVerify(props) {
    const { modalToggler } = props;

    const userAgent = navigator.userAgent; //info to be passed on to BE

    const isComponentMounted = useIsComponentMounted();
    const dispatch = useDispatch();

    const [linkSent, setLinkSent] = useState(false);


    const handleSubmit = () => { //===> TODO: improve
        e.preventDefault();

        dispatch(setLoader(true));

        const handleResponse = (response) => {
            if (isComponentMounted()) {
                if (response.success) { setLinkSent(true) }
                else { setLinkSent(false) }
            }
        };

        const handleError = (error) => {
            console.warn("clickHandler in modal encountered an error", error);
        };

        const handleFinally = () => {
            dispatch(setLoader(false));
        };

        try {
            acctRequestVerifyEmail(userAgent)
                .then(response => handleResponse(response))
                .catch(error => { handleError(error) })
                .finally(handleFinally);
        } catch (error) {
            console.error("Error in ModalChangeAcct", error);
            dispatch(setLoader(false));
        }
    };

    // Make this request only once
    useEffect(() => {
        handleSubmit()
    }, []);

    return (
        <>
            {linkSent && (
                <>
                    <p>A link was sent to your email address.</p>
                    <p>Click on the link to verify your account.</p>
                    <p>The link will be valid for 1 hr.</p>
                </>
            )}
            {!linkSent && (
                <>
                    <p>We failed to send you a verification link to your email address.</p>
                    <p>Please check that your email address is correct and try again.</p>
                    <p>Contact us in case you believe your email address is correct but we are failing to verify it.</p>
                </>
            )}
            <div className="ModalAccountDetailChange-BtnContainer">
                <button onClick={modalToggler}>{formSubmitted ? "Close" : "Cancel"}</button>
            </div>
        </>
    );
};

ModalAccountVerify.propTypes = {
    modalToggler: PropTypes.func.isRequired
};

export default ModalAccountDetailChange;