import { useEffect, useState } from "react";
import { PropTypes } from "prop-types";
import { nameValidation } from "../../utils/validation";
import { INPUT_LENGTH } from "../../utils/constants";
import RequiredFieldStar from "../RequiredFieldStar/RequiredFieldStar";
import ErrorMessage from "../ErrorMessage/ErrorMessage";

/**
 * Component returns InputName that should be the child component of a form
 * 
 * The form requires two states to be set on the parent: name and nameIsValid. 
 * This component will use "name" and set the state of the parent. It will also set the state of nameIsValid.
 * 
 * @visibleName Input Name
 * 
 * @param {object} props
 * @param {string} [props.cssClass] //=> optional: defaults to "MAIN-form-display-table Auth-displayTable"
 * @param {string} [props.labelText] //=> optional: defaults to "Name"
 * @param {string} props.name 
 * @param {func} props.setName
 * @param {func} props.setNameIsValid 
 * @returns {React.ReactElement}
 * 
 */
function InputName(props) {
    const { name, setName, setNameIsValid, labelText = "Name", cssClass = "" } = props;

    // If this component is part of a form with many label/input pairs, it is recommended that only 
    // "MAIN-form-display-table" is passed as the argument to cssClass. Example: Signup form.
    const styleClass = cssClass === "" ? "MAIN-form-display-table Auth-displayTable" : cssClass;

    const [errorMessage, setErrorMessage] = useState("");

    const handleChange = (e) => {
        setName(e.target.value);
        if (errorMessage !== "") { setErrorMessage("") }
    };

    const handleBlur = (e) => {
        let validation = nameValidation(e.target.value);
        setErrorMessage(validation.message);
        setNameIsValid(validation.response);
    };

    //useEffect used to enable button (is name is indeed valid) as user is typing the name: smoother mouseless navigation
    useEffect(() => {
        if (name.length === INPUT_LENGTH.name.minValue) {
            let validation = nameValidation(name);
            setNameIsValid(validation.response);
        }
    }, [name])

    return (
        <>
            <div className={`${styleClass}`}>
                <label htmlFor="name">{labelText}:<RequiredFieldStar /></label>
                <input
                    aria-invalid={errorMessage === "" ? "false" : "true"}
                    aria-describedby="name-error"
                    autoComplete="name"
                    id="name"
                    maxLength={`${INPUT_LENGTH.name.maxValue}`}
                    minLength={`${INPUT_LENGTH.name.minValue}`}
                    name="name"
                    onBlur={handleBlur}
                    onChange={handleChange}
                    required
                    type="text"
                    value={name}
                />
            </div>
            {
                errorMessage !== "" && (
                    <ErrorMessage message={errorMessage} ariaDescribedby="name-error" />
                )
            }
        </>
    );
};
InputName.propTypes = {
    labelText: PropTypes.string,
    name: PropTypes.string.isRequired,
    setName: PropTypes.func.isRequired,
    setNameIsValid: PropTypes.func.isRequired,
};

export default InputName;