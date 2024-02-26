import { Outlet } from "react-router-dom"
import "./users.css"

// *** COMPONENT ***

/**
 * Component for ...
 * 
 * @visibleName ....
 * @summary ....
 * @returns {React.ReactElement}
 */
function Users(props) {
    let { children } = props


    return children ? children : <Outlet />;
}
export default Users;