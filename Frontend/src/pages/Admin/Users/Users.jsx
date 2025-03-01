import { Outlet } from "react-router-dom"

/**
 * Outlet for user management page.
 * This component allows for nested routes to render their element content here.
 * It means the 'Users' menu may display the user's table or user information (if a user is selected) or another subpage, according to the user's interaction with the page.
 * By default, the adminArea/users will display the user's table, but the user's interaction with the page will display subpages here.
 * 
 * @visibleName Outlet for User Management Page
 * @returns {React.ReactElement}
 */
function Users(props) {
    let { children } = props

    return children ? children : <Outlet />;
}
export default Users;