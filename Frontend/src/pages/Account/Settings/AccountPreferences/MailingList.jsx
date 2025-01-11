import { useState } from "react";
import { useDispatch } from "react-redux";
import { PropTypes } from "prop-types";
import { setMailingList } from "../../../../config/apiHandler/userSettings/setMailingList.js"
import { setLoader } from "../../../../redux/loader/loaderSlice.js"
import useIsComponentMounted from "../../../../hooks/useIsComponentMounted.js";
import ErrorMessage from "../../../../components/ErrorMessage/ErrorMessage";
import Tooltip from "../../../../components/Tooltip/Tooltip"
/**
 * Component returns section with UI to change user's mailing list's preferences
 * 
 * @returns {React.ReactElement}
 * 
 */
function MailingList(props) {
    const { preferences } = props;

    const userAgent = navigator.userAgent; //info to be passed on to BE

    const dispatch = useDispatch();
    const isComponentMounted = useIsComponentMounted();

    //State of mailing list
    const [inMailingList, setInMailingList] = useState(preferences.mailingList)

    // State set by api call
    const [infoMessage, setInfoMessage] = useState("");

    // Submit

    const handleSubmit = (e) => {
        e.preventDefault();

        const requestData = {
            mailingList: !inMailingList,
            userAgent: userAgent
        }

        setInMailingList(!inMailingList);

        dispatch(setLoader(true));

        setMailingList(requestData)
            .then(res => {
                if (isComponentMounted()) {
                    if (!res.response) { setInMailingList(!inMailingList); }//Revert state if API call fails
                    setInfoMessage(res.message)
                }
            })
            .catch(error => { console.warn("clickHandler in modal encountered an error", error) })
            .finally(dispatch(setLoader(false)));
    };


    return (
        <>
            <div>
                <p><Tooltip text="Mailing List" message="Receive app news per email" /></p>
                <div>
                    <label className="toggleBtn">
                        <input
                            checked={inMailingList}
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
MailingList.propTypes = {
    preferences: PropTypes.shape({
        mailingList: PropTypes.bool.isRequired,
    }).isRequired,
};

export default MailingList;