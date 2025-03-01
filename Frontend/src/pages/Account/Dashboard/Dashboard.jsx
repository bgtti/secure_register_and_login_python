import { useSelector } from "react-redux";

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
        <div className="MAIN-subNav-page">
            <h3>{user.name}'s Dashboard</h3>
            <section>
                <p><b>Welcome back, {user.name}!</b></p>
            </section>
            <section>
                <p>Add to this Dashboard the content of your choice!</p>
            </section>
        </div>
    )
};
export default Dashboard;