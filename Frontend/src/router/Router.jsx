import { BrowserRouter, Navigate, Routes, Route } from "react-router-dom";
import { useSelector } from "react-redux";
import AxiosApiInterceptor from "../config/AxiosApiInterceptor";
import Loader from "../components/Loader";
//Layout
import NavBar from "../layout/NavBar";
import Footer from "../layout/Footer";
//Pages: open website pages
import Home from '../pages/Home/Home';
import LogIn from "../pages/Login/LogIn";
import Login from "../pages/Auth/Login/Login";
import SignUp from "../pages/SignUp/SignUp";
import ResetPassword from "../pages/Auth/ResetPassword/ResetPassword";
import Contact from "../pages/Contact/Contact";
//Pages: unprotected but no-follow
import VerifyEmail from "../pages/Auth/VerifyEmail/VerifyEmail";
import ChangeEmail from "../pages/Auth/ChangeEmail/ChangeEmail"
//Pages: protected route (registered users)
import UserAccount from "../pages/Account/AccountMain"
import UserDashboard from "../pages/Account/Dashboard/Dashboard";
import AcctSettings from "../pages/Account/Settings/AccountSettings";
//Pages: admin protected (admin users only)
import AdminArea from "../pages/Admin/AdminArea";
import AdminDashboard from "../pages/Admin/Dashboard/AdminDashboard";
import Users from "../pages/Admin/Users/Users";
import UsersTable from "../pages/Admin/Users/UsersTable/UsersTable";
import UserInfo from "../pages/Admin/Users/UserInfo/UserInfo";
import UserLogs from "../pages/Admin/Users/UserLogs/UserLogs";
import UserMessages from "../pages/Admin/Users/UserMessages/UserMessages";
import Messages from "../pages/Admin/Messages/Messages";
//Pages: error pages
import ErrorPage from '../pages/ErrorPage/ErrorPage';
import BotError from "../pages/ErrorPage/BotError";
//Router: protected route wrappers
import ProtectedUserRoute from "./ProtectedUserRoute";
import ProtectedAdminRoute from "./ProtectedAdminRoute";

//include about page
//include contact page
//include privacy policy page
//include terms and conditions page
//include cookie policy page
//include FAQ page

// TODO: confirm email page
// TODO: change password page

// TODO: separation of user and admin logic
// TODO: urls and relative urls in shared files with BE

// FIXME: error occurs, page reloads, sends user to login but if I write the address on the browser, it will log the user in again. Not only annoying, but dangerous as user may thing its logged out...



const Router = () => {
    const loaderDisplay = useSelector((state) => state.loader.display);
    return (
        <BrowserRouter>
            {<AxiosApiInterceptor />}
            {loaderDisplay ? <Loader></Loader> : ""}
            <NavBar />
            <Routes>
                <Route index element={<Home />} />
                <Route exact path="/" element={<Home />} />
                {/* <Route exact path="login" element={<LogIn />} /> */}
                <Route exact path="login" element={<Login />} />
                <Route exact path="signup" element={<SignUp />} />
                <Route exact path="resetPassword" element={<ResetPassword />} />
                <Route exact path="contact" element={<Contact />} />
                <Route exact path="verifyEmail/:token" element={<VerifyEmail />} />
                <Route exact path="confirmEmailChange/:token" element={<ChangeEmail />} />
                <Route exact path="confirmNewEmail/:token" element={<ChangeEmail />} />
                <Route exact path="errorPage" element={<ErrorPage />} />
                <Route exact path="botError" element={<BotError />} />
                <Route exact path="*" element={<ErrorPage errorNum="404" />} />
                <Route element={<ProtectedUserRoute />}>
                    <Route path="userAccount" element={<UserAccount />}>
                        <Route index element={<Navigate to="userdashboard" replace />} />
                        <Route path="userdashboard" element={<UserDashboard />} />
                        <Route path="acctSettings" element={<AcctSettings />} />
                    </Route>
                </Route>
                <Route element={<ProtectedAdminRoute />}>
                    <Route path="adminArea" element={<AdminArea />}>
                        <Route index element={<Navigate to="adminDashboard" replace />} />
                        <Route path="adminDashboard" element={<AdminDashboard />} />
                        <Route path="users" element={<Users />}>
                            <Route index element={<UsersTable />} />
                            <Route path="usersTable" element={<UsersTable />} />
                            <Route path="userInfo" element={<UserInfo />} />
                            <Route path="userLogs" element={<UserLogs />} />
                            <Route path="userMessages" element={<UserMessages />} />
                        </Route>
                        <Route path="messages" element={<Messages />} />
                    </Route>
                </Route>
                {/* <Route exact path="terms" element={<Terms />} /> */}
            </Routes>
            <Footer />
        </BrowserRouter>
    )
}
export default Router