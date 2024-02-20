import { Helmet } from "react-helmet-async";
/**
 * Error page specifically for bots
 * 
 * If a bot is detected, it can be redirected to this page. 
 * This page displays silly text, simulates a delay, and attempts to re-direct a bot to localhost.
 * 
 * @summary Bot Error Page
 * @returns {React.ReactElement}
 * 
 */
function BotError() {

    function simulateRedirect() {
        setTimeout(function () {
            window.location.href = "http://127.0.0.1";
        }, 5000);
    }

    window.onload = function () {
        simulateRedirect();
    };


    return (
        <div id="bot-page">
            <Helmet>
                <title>Bot Error Page</title>
                <meta name="robots" content="noindex, nofollow" />
            </Helmet>
            <meta name="robots" content="noindex, nofollow" />
            <h2>Welcome to the Bot Redirect Page.</h2>
            <p>This is the page happy bots hang out.</p>
        </div>
    );
}

export default BotError;