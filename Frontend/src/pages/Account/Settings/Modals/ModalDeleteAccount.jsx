import { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { PropTypes } from "prop-types";
import useIsComponentMounted from "../../../../hooks/useIsComponentMounted.js";
import { setLoader } from "../../../../redux/loader/loaderSlice.js"
import { acctRequestVerifyEmail } from "../../../../config/apiHandler/authRegistration/verifyEmail.js"
import { INPUT_LENGTH } from "../../../../utils/constants";
import { passwordValidationSimplified } from "../../../../utils/validation";

/**
 * This component is a modal used delete the user's account.
 * 
 * @todo functionality missing
 * 
 * @visibleName Modal Initiate Email Verification
 * @param {object} props
 * @param {func} props.modalToggler opens/closes modal
 * @returns {React.ReactElement}
 */
function ModalDeleteAccount(props) {
    const { modalToggler } = props;

    const user = useSelector((state) => state.user);
    const preferences = useSelector((state) => state.preferences);

    const userAgent = navigator.userAgent; //info to be passed on to BE

    const isComponentMounted = useIsComponentMounted();
    const dispatch = useDispatch();

    // if mfa is enabled, user must confirm account deletion per email 
    // if not, require user to type in password
    const [linkSent, setLinkSent] = useState(null);

    // Used for actual fields
    const [formData, setFormData] = useState({
        password: "",
        passwordIsValid: { response: false, message: "" },
    });
    const handleChange = (e) => {
        const { value } = e.target;
        setFormData((prevData) => ({
            ...prevData,
            password: value,
            passwordIsValid: passwordValidationSimplified(value),
        }));
        //Ensures that, if an error message had appeared before, that it disappears as user corrects input
        if (!formData.passwordIsValid.response) {
            setFormData((prevData) => ({
                ...prevData,
                passwordIsValid: { response: false, message: "" },
            }));
        }
    };

    const handleBlur = (e) => {
        setFormData((prevData) => ({
            ...prevData,
            passwordIsValid: passwordValidationForLogin(e.target.value),
        }));
    };


    const handleSubmit = (e) => {
        e.preventDefault();
        console.log("account deletion")

        // dispatch(setLoader(true));

        // const handleResponse = (response) => {
        //     if (isComponentMounted()) {
        //         if (response.success) { setLinkSent(true) }
        //         else { setLinkSent(false) }
        //     }
        // };

        // const handleError = (error) => {
        //     if (isComponentMounted()) {
        //         console.warn("clickHandler in modal encountered an error", error);
        //     }
        // };

        // const handleFinally = () => {
        //     dispatch(setLoader(false));
        // };

        // acctRequestVerifyEmail(userAgent)
        //     .then(response => handleResponse(response))
        //     .catch(error => { handleError(error) })
        //     .finally(handleFinally);
    };



    return (
        <>
            <form onSubmit={handleSubmit} className="MAIN-form">
                {
                    preferences.mfa === true ? (
                        <>
                            <p>Multi-factor authentication is enabled in your account.</p>
                            <p>For this reason, to delete your account you shall receive a link per email.</p>
                            <p>Clicking on the link will confirm your account deletion.</p>
                            <p>The link will be valid for one hour.</p>
                        </>
                    ) : (
                        <>
                            <p>Are you sure you want to delete your account?</p>
                            <p>Type your password bellow to proceed</p>
                        </>
                    )
                }
                {/* Hidden field for username: helps password managers associate info. (Avoids browser warning) */}

                {
                    preferences.mfa !== true && (
                        <div className="MAIN-display-none">
                            <label htmlFor="username">Username</label>
                            <input
                                autoComplete="username"
                                id="username"
                                name="username"
                                readOnly
                                type="text"
                                value={user.email}
                            />
                        </div>
                    )
                }
                <div className="MAIN-form-display-table">
                    <label htmlFor="password">Password:<span className="MAIN-form-star"> *</span></label>
                    <input
                        aria-invalid={formData.passwordIsValid.message === "" ? "false" : "true"}
                        aria-describedby="password-error"
                        autoComplete="current-password"
                        id="password"
                        maxLength={`${INPUT_LENGTH.password.maxValue}`}
                        minLength={`${INPUT_LENGTH.password.minValue}`}
                        name="password"
                        onBlur={handleBlur}
                        onChange={handleChange}
                        required
                        type="password"
                        value={formData.password}
                    />
                </div>
                {
                    formData.passwordIsValid.message !== "" && (
                        <p className="MAIN-error-message" id="password-error">
                            <i>{formData.passwordIsValid.message}</i>
                        </p>
                    )
                }
                <br />
                <div className="">
                    {/* <button disabled={formSubmitted} type="submit" className="MAIN-DeleteBtn">{preferences.mfa === true ? "Send link" : "Delete"}</button> */}
                    {/* <button onClick={modalToggler}>{formSubmitted ? "Close" : "Cancel"}</button> */}
                    <button type="submit" className="MAIN-DeleteBtn">{preferences.mfa === true ? "Send link" : "Delete account"}</button>
                    <button onClick={modalToggler}>Cancel</button>
                </div>
            </form>
        </>
    );
};

ModalDeleteAccount.propTypes = {
    modalToggler: PropTypes.func.isRequired
};

export default ModalDeleteAccount;