import { useLocation, Link } from "react-router-dom";
import { Helmet } from "react-helmet-async";
import "./errorPage.css"

/**
 * Component returns error page according to props or state passed, or default error if none is specified.
 * 
 * Defining the error can be done in two ways: passing the error number as a string via state (in useNavigate) or via props. See examples bellow for more information.
 * 
 * @summary Error page component: error number can be passed to this component via prop or state
 * @returns {React.ReactElement}
 * 
 * @example
 * //Using useNavigate:
 * import { useNavigate } from "react-router-dom";
 * let navigate = useNavigate();
 * 
 * let myOnClickFunc = () => {
        navigate("/errorPage", { state: "429" });
    } // will return the page for the 429 error
 * 
 * let myOnClickFunc = () => {
        navigate("/errorPage");
    } // will return the default error page
 * 
 * //Using props to define the error page:
 * 
 * <Route exact path="*" element={<ErrorPage errorNum="404" />} /> // defining page not found route
 * 
 * <ErrorPage /> // will lead to default/general error page
 * 
 * <ErrorPage errorNum="409"/> // will lead to 409 error page
 */
function ErrorPage(props) {
    const { errorNum } = props;

    const location = useLocation();
    const errorCodeState = location.state;

    let errorCode = (errorNum && errorNum !== "") ? errorNum : errorCodeState;

    let meaning = "";
    let reason = "";
    let solution = "";

    switch (errorCode) {
        case "400":
            meaning = "Bad request"
            reason = "An invalid request was sent to the server and it returned an error."
            solution = "Re-submit your input, checking the syntax and make sure it is valid."
            break
        case "401":
            meaning = "Unauthorized access"
            reason = "You may have submitted invalid credentials or the account might not exist."
            solution = "Make sure you are authorized to access the resource and input valid credentials."
            break
        case "403":
            meaning = "Unauthorized access"
            reason = "You may have your accessed blocked temporarily (due to multiple failed log in attempts), or your account might have been blocked by an admin, or you may not have the required authorization to access this resource."
            solution = "Make sure you are authorized to access the resource and have not been blocked by a site admin."
            break
        case "404":
            meaning = "Page not found"
            reason = "This URL does not exist or could not be found."
            solution = "Check the URL and try again."
            break
        case "409":
            meaning = "Conflict"
            reason = "The request sent caused a conflict, possibly because the resource already exists. "
            solution = "Make sure you were not trying to create something that already exists in the database."
            break
        case "429":
            meaning = "Too many requests"
            reason = "This error typically occurs when too many requests are sent to the server in a short amount of time. The rate limit has been surpassed."
            solution = "Rate limits are used to stop bots and malicious actors. Please wait a couple of minutes before trying again - this error usually resolves itself. Note that some actions have stricter limits. Multiple failed log in attempts may lead to longer time blockages. Multiple sign up attempts may lead you to be blocked for requesting a new registration for up to 24 hours. If abuse is perceived, you may be blocked for longer periods or indefinitely from accessing this site. Should you see this error page frequently and this is impacting your usability, please let us know - and give us information about what you were trying to do when the error occured."
            break
        case "500":
            meaning = "Internal server error"
            reason = "The server is currently unresponsive."
            solution = "Reload the page to check if the problem can be resolved."
            break
        case "502":
            meaning = "Bag gateway"
            reason = "The server may have received an invalid response from another server, and it is taking longer than expected to complete your request."
            solution = "Thy refreshing the browser or clearing the browser cache."
            break
        case "503":
            meaning = "Service unavailable"
            reason = "The server is running, but likely currently overloaded."
            solution = "The site could be under maintenance or the issue should temporarily be resolved. Please come back later and reload the page."
            break
        default:
            meaning = "An error ocurred"
            reason = "No further information about the error was provided."
            solution = "Please try to refresh the page to see if the error is resolved."
    }


    return (
        <div id="error-page" className="ErrorPage">
            <Helmet>
                <title>Error Page</title>
                <meta name="robots" content="noindex, nofollow" />
            </Helmet>
            <h2>Oops!</h2>
            <p>something went wrong...</p>
            <section className="ErrorPage-Section1">
                <h3>Error {errorCode}</h3>
                <p>{meaning}</p>
            </section>
            <section className="ErrorPage-Section2">
                <h3>About this error</h3>
                <p>{reason}</p>
                <p>{solution}</p>
                <br />
                <p>If the error persists, please inform the site admins: <Link to="/contact">contact form</Link>.</p>
            </section>
        </div>
    );
}

export default ErrorPage;