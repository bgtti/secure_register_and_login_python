import { useRef } from "react";
import { useDispatch, useSelector } from "react-redux";
import { Navigate, Outlet } from 'react-router-dom';
import { setLoader } from "../redux/loader/loaderSlice";
import { getUserData } from "../config/apiHandler/authMain/getUser";

/**
 * Component returns a wrapper for protected routes only logged in users of access level "admin" may access
 * 
 * The function should be used to wrap around admin-protected route elements in Router.jsx
 * 
 * @visibleName ProtectedAdminRoute
 * @returns {React.ReactElement}
 * 
 */
function ProtectedAdminRoute(props) {
    let { children } = props
    const dispatch = useDispatch();

    const triedLogIn = useRef(false);

    const user = useSelector((state) => state.user);

    if (user.loggedIn && !(user.access !== "admin" || user.access !== "super_admin")) {
        return <Navigate to={"/errorPage"} state={"401"} replace />;
    }

    if (!user.loggedIn && !triedLogIn.current) {
        triedLogIn.current = true;
        dispatch(setLoader(true));
        getUserData()
            .then(res => {
                // If user couldn't be logged in from the request's cookie or does not have the right access...
                if (!res.response) {
                    return <Navigate to={"/login"} replace />;
                }
                if (!(user.access !== "admin" || user.access !== "super_admin")) {
                    return <Navigate to={"/errorPage"} state={"401"} replace />;
                }
            })
            .catch(error => {
                console.error("Error in protected route:", error);
            })
            .finally(() => {
                dispatch(setLoader(false));
            });
    }

    if (!user.loggedIn && triedLogIn.current) {
        return <Navigate to={"/login"} replace />;
    }

    return children ? children : <Outlet />;
}

export default ProtectedAdminRoute;