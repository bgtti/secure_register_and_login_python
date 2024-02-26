import { useRef } from "react";
import { useDispatch, useSelector } from "react-redux";
import { Navigate, Outlet } from 'react-router-dom';
import { setLoader } from "../redux/loader/loaderSlice";
import { getUserData } from "../config/apiHandler/getUser";

/**
 * Component returns a wrapper for protected routes only logged in users may access
 * 
 * The function should be used to wrap around protected route elements in Router.jsx
 * 
 * @visibleName ProtectedUserRoute
 * @returns {React.ReactElement}
 * 
 */
function ProtectedUserRoute(props) {
    let { children } = props
    const dispatch = useDispatch();

    const triedLogIn = useRef(false);

    const user = useSelector((state) => state.user);

    if (!user.loggedIn && !triedLogIn) {
        triedLogIn.current = true;
        dispatch(setLoader(true));
        getUserData()
            .then(res => {
                // If user couldn't belogged in from the request's cookie...
                if (!res.response) {
                    return <Navigate to={"/login"} replace />;
                }
            })
            .catch(error => {
                console.error("Error in protected route:", error);
            })
            .finally(() => {
                dispatch(setLoader(false));
            });
    }
    if (!user.loggedIn && triedLogIn) {
        return <Navigate to={"/login"} replace />;
    }

    return children ? children : <Outlet />;
}

export default ProtectedUserRoute;