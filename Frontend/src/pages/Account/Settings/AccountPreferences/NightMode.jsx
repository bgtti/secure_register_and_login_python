import { useState } from "react";
import { useDispatch } from "react-redux";
import { PropTypes } from "prop-types";
import { setNightMode } from "../../../../config/apiHandler/userSettings/setNightMode.js"
import { setLoader } from "../../../../redux/loader/loaderSlice.js"
import useIsComponentMounted from "../../../../hooks/useIsComponentMounted.js";
import ErrorMessage from "../../../../components/ErrorMessage/ErrorMessage";
/**
 * Component returns section with UI to change user's night mode's preferences
 * 
 * @returns {React.ReactElement}
 * 
 */
function NightMode(props) {
    const { preferences } = props;

    const userAgent = navigator.userAgent; //info to be passed on to BE

    const dispatch = useDispatch();
    const isComponentMounted = useIsComponentMounted();

    //State of night mode
    const [nightModeEnabled, setNightModeEnabled] = useState(preferences.nightMode)

    // State set by api call
    const [infoMessage, setInfoMessage] = useState("");

    // Submit
    const handleSubmit = (e) => {
        e.preventDefault();

        const requestData = {
            nightMode: !nightModeEnabled,
            userAgent: userAgent
        }

        setNightModeEnabled(!nightModeEnabled)

        dispatch(setLoader(true));

        setNightMode(requestData)
            .then(res => {
                if (isComponentMounted()) {
                    if (!res.response) { setNightModeEnabled(!nightModeEnabled); }//Revert state if API call fails
                    setInfoMessage(res.message);
                }
            })
            .catch(error => { console.warn("clickHandler in modal encountered an error", error) })
            .finally(dispatch(setLoader(false)));
    };


    return (
        <>
            <div>
                <p>Night mode</p>
                <div>
                    <label className="toggleBtn">
                        <input
                            checked={nightModeEnabled}
                            onChange={handleSubmit}
                            type="checkbox" />
                        <span className="slider round"></span>
                    </label>
                </div>
            </div>
            {
                infoMessage !== "" && (
                    <>
                        <div className="AccountSettings-Preferences-InfoMessage">
                            < ErrorMessage message={infoMessage} ariaDescribedby="api-response-error" />
                        </div>
                    </>
                )
            }

        </>
    );
};
NightMode.propTypes = {
    preferences: PropTypes.shape({
        nightMode: PropTypes.bool.isRequired
    }).isRequired,
};

export default NightMode;