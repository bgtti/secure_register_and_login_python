import { BrowserRouter, Routes, Route } from "react-router-dom";
import { useSelector } from "react-redux";
import AxiosApiInterceptor from "../config/AxiosApiInterceptor";
import Loader from "../components/Loader";
//Layout
import NavBar from "../layout/NavBar";
import Footer from "../layout/Footer";
//Pages: open website pages
import Home from '../pages/Home/Home';
import LogIn from "../pages/Login/LogIn";
import SignUp from "../pages/SignUp/SignUp";
import Contact from "../pages/Contact/Contact";
//Pages: protected route (registered users)
import Dashboard from "../pages/Dashboard/Dashboard";
import UserSettings from "../pages/UserSettings/UserSettings";
//Pages: admin protected
import AdminArea from "../pages/Admin/AdminArea";
import AdminDashboard from "../pages/Admin/Dashboard/AdminDashboard";
import Users from "../pages/Admin/Users/Users";
import UserInfo from "../pages/Admin/Users/UserInfo/UserInfo";
import UserLogs from "../pages/Admin/Users/UserLogs/UserLogs";
import UsersTable from "../pages/Admin/Users/UsersTable/UsersTable";
import AdminSettings from "../pages/Admin/Settings/AdminSettings";
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
                <Route exact path="login" element={<LogIn />} />
                <Route exact path="signup" element={<SignUp />} />
                <Route exact path="contact" element={<Contact />} />
                <Route exact path="errorPage" element={<ErrorPage />} />
                <Route exact path="botError" element={<BotError />} />
                <Route exact path="*" element={<ErrorPage errorNum="404" />} />
                <Route element={<ProtectedUserRoute />}>
                    <Route exact path="dashboard" element={<Dashboard />} />
                    <Route exact path="userSettings" element={<UserSettings />} />
                </Route>
                {/* <Route exact path="adminLogin" element={<AdminLogIn />} /> */}
                <Route element={<ProtectedAdminRoute />}>
                    <Route path="adminArea" element={<AdminArea />}>
                        <Route index element={<AdminDashboard />} />
                        <Route path="admindashboard" element={<AdminDashboard />} />
                        <Route path="users" element={<Users />}>
                            <Route index element={<UsersTable />} />
                            <Route path="usersTable" element={<UsersTable />} />
                            <Route path="userInfo" element={<UserInfo />} />
                            <Route path="userLogs" element={<UserLogs />} />
                        </Route>
                        <Route path="adminSettings" element={<AdminSettings />} />
                    </Route>
                </Route>
                {/* <Route exact path="terms" element={<Terms />} /> */}
            </Routes>
            <Footer />
        </BrowserRouter>
    )
}
export default Router