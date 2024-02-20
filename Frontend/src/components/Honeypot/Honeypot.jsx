import { useState, useEffect } from "react";
import { PropTypes } from "prop-types";
/**
 * Component returns Honeypot form elements to detect bots
 * 
 * Form elements that will be hidden from human interaction to serve as bot bait.
 * 
 * @visibleName Honeypot form fields
 * @param {object} props
 * @param {func} props.setHoneypotValue should be part of the parent's state
 * @returns {React.ReactElement}
 * 
 * If not familiar with Honeypots:
 * @see https://www.araweb.co.uk/Safe_Contact_Form_with_Honeypot_840
 * @example
 * //In the parent component, be sure to include:
 * const [honeypotValue, setHoneypotValue] = useState("");
 * 
 * // then pass setHoneypotValue as a prop:
 * <Honeypot setHoneypotValue={setHoneypotValue}/>
 * 
 * // send the honeypot value along the rest to enable BE handling
 * // a human using the form will cause honeypotValue === "". If a bot is caught, honeypotValue === "got honey!"
 * 
 */
function Honeypot(props) {
    const { setHoneypotValue } = props;

    const [honeypot1, setHoneypot1] = useState("");
    const [honeypot2, setHoneypot2] = useState(false);

    useEffect(() => {
        if (honeypot1 !== "" || honeypot2 === true) {
            setHoneypotValue("got honey!")
        }
    }, [honeypot1, honeypot2]);

    const onHoneypotChange = (value) => {
        setHoneypot1(value);
    };
    const onRobotCheckboxChange = (isChecked) => {
        setHoneypot2(isChecked);
    };

    return (
        <>
            <div className="MAIN-NO-HUN">
                <label htmlFor="fullName" aria-hidden="true">Leave this field empty:</label>
                <input
                    aria-hidden="true"
                    type="text"
                    id="fullName"
                    name="fullName"
                    autoComplete="off"
                    tabIndex="-1"
                    value={honeypot1}
                    onChange={(e) => onHoneypotChange(e.target.value)}
                />
            </div>

            <div className="MAIN-NO-HUN">
                <input
                    aria-hidden="true"
                    type="checkbox"
                    id="amIHuman"
                    tabIndex="-1"
                    checked={honeypot2}
                    onChange={(e) => onRobotCheckboxChange(e.target.checked)}
                />
                <label htmlFor="amIHuman">am I human?</label>
            </div>
        </>
    );
};

Honeypot.propTypes = {
    setHoneypotValue: PropTypes.func.isRequired
};

export default Honeypot;