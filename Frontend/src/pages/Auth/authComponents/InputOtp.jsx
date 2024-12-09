import { useEffect, useState } from "react";
import { PropTypes } from "prop-types";
import { otpValidation } from "../../../utils/validation";
import { INPUT_LENGTH } from "../../../utils/constants";
import RequiredFieldStar from "../../../components/RequiredFieldStar/RequiredFieldStar";
import ErrorMessage from "../../../components/ErrorMessage/ErrorMessage";

/**
 * Component returns InputOtp that should be the child component of a form
 * 
 * The form requires two states to be set on the parent: otp and otpIsValid. 
 * This component will use "otp" and set the state of the parent. It will also set the state of otpIsValid.
 * 
 * @visibleName Input OTP
 * 
 * @param {object} props
 * @param {string} props.email
 * @param {func} props.setOtp
 * @param {func} props.setOtpIsValid 
 * @returns {React.ReactElement}
 * 
 */
function InputOtp(props) {
    const { otp, setOtp, setOtpIsValid } = props;

    const [errorMessage, setErrorMessage] = useState("");

    const handleChange = (e) => {
        setOtp(e.target.value);
        if (errorMessage !== "") { setErrorMessage("") }
    };

    const handleBlur = (e) => {
        let validation = otpValidation(e.target.value);
        setErrorMessage(validation.message);
        setOtpIsValid(validation.response);
    };

    //useEffect used to enable button (is password is indeed valid) as user is typing the otp: smoother mouseless navigation
    useEffect(() => {
        if (otp.length === INPUT_LENGTH.otp.minValue) {
            let validation = otpValidation(otp);
            setOtpIsValid(validation.response);
        }
    }, [otp])

    return (
        <>
            <div className="MAIN-form-display-table">
                <label htmlFor="otp">OTP:<RequiredFieldStar /></label>
                <input
                    aria-invalid={errorMessage === "" ? "false" : "true"}
                    aria-describedby="otp-error"
                    autoComplete="one-time-code"
                    id="otp"
                    maxLength={`${INPUT_LENGTH.otp.maxValue}`}
                    minLength={`${INPUT_LENGTH.otp.minValue}`}
                    name="otp"
                    onBlur={handleBlur}
                    onChange={handleChange}
                    required
                    type="text"
                    value={otp}
                />
            </div>
            {
                errorMessage !== "" && (
                    <ErrorMessage message={errorMessage} ariaDescribedby="otp-error" />
                )
            }
        </>
    );
};
InputOtp.propTypes = {
    otp: PropTypes.string.isRequired,
    setOtp: PropTypes.func.isRequired,
    setOtpIsValid: PropTypes.func.isRequired,
};

export default InputOtp;