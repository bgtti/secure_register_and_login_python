import { Helmet } from "react-helmet-async";
function UserSettings() {

    return (
        <div>
            <Helmet>
                <title>Error Page</title>
                <meta name="robots" content="noindex, nofollow" />
            </Helmet>
            <h2>User settings!</h2>
            <p>UserSettings</p>
        </div>

    )
}
export default UserSettings