/**
 * A path to the route is needed when using React Router's useNavigate.
 * If paths change in Router.jsx, hardcoded routes must be changed in every file.
 * To simplify this process, use the routePathTo object and select the key to import paths.
 * 
 * @example
 * //Usage:
 * import { useNavigate } from "react-router-dom";
 * import { routePathTo } from ".../router/routePaths"
 * const navigate = useNavigate();
 * 
 * //...
 * <button onClick={() => { navigate(PATH_TO.adminArea_usersTable) }}>Back to Users Table</button>
 * //...
 * 
 */
export const PATH_TO = {
    //Unprotected routes
    login: "/login",
    contact: "/contact",
    signup: "/signup",
    forgotPassword: "/forgotPassword",
    resetPassword: "/resetPassword/token=",
    //Protected routes
    userAccount: "/userAccount",
    //Admin routes
    adminArea_usersTable: "/adminArea/users/usersTable",
    adminArea_userInfo: "/adminArea/users/userInfo",
    adminArea_userLogs: "/adminArea/users/userLogs",
    adminArea_userMessages: "/adminArea/users/userMessages",
}