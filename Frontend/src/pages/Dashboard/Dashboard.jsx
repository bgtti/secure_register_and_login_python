import { useSelector } from "react-redux";
import { Helmet } from "react-helmet-async";

/**
 * Component for the User's Dashboard
 * 
 * 
 * @visibleName User Dashboard
 * @returns {React.ReactElement}
 * 
 */
function Dashboard() {
    const user = useSelector((state) => state.user);

    return (
        <div>
            <Helmet>
                <title>Dashboard</title>
                <meta name="robots" content="noindex, nofollow" />
            </Helmet>
            <div>
                <h2>User Dashboard</h2>
            </div>
            <p>Hello, {user.name}!</p>
            <br />
            <p>Set up the Dashboard with the content of your choice.</p>
        </div>
    )
};
export default Dashboard;