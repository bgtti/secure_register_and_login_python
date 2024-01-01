import { BrowserRouter, Routes, Route } from "react-router-dom";
import { useSelector } from "react-redux";
import Loader from "../components/Loader";
import NavBar from "../layout/NavBar";
import Home from '../pages/Home/Home';
import LogIn from "../pages/Login/LogIn";
import SignUp from "../pages/SignUp/SignUp";
import Dashboard from "../pages/Dashboard/Dashboard";
import UserSettings from "../pages/UserSettings/UserSettings";
import AdminLogIn from "../pages/Admin/AdminLogIn";
import AdminArea from "../pages/Admin/AdminArea";
import AdminDashboard from "../pages/Admin/Dashboard/AdminDashboard";
import UsersTable from "../pages/Admin/UsersTable/UsersTable";
import AdminSettings from "../pages/Admin/Settings/AdminSettings";
import Footer from "../layout/Footer";
import ErrorPage from '../pages/ErrorPage/ErrorPage';

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
            {loaderDisplay ? <Loader></Loader> : ""}
            <NavBar />
            <Routes>
                <Route exact path="/" element={<Home />} />
                <Route exact path="login" element={<LogIn />} />
                <Route exact path="signup" element={<SignUp />} />
                <Route exact path="dashboard" element={<Dashboard />} />
                <Route exact path="userSettings" element={<UserSettings />} />
                <Route exact path="*" element={<ErrorPage />} />
                <Route exact path="adminLogin" element={<AdminLogIn />} />
                <Route path="adminArea" element={<AdminArea />}>
                    <Route index element={<AdminDashboard />} />
                    <Route path="dashboard" element={<AdminDashboard />} />
                    <Route path="usersTable" element={<UsersTable />} />
                    <Route path="adminSettings" element={<AdminSettings />} />
                    <Route path="*" element={<ErrorPage />} />
                </Route>
            </Routes>
            <Footer />
        </BrowserRouter>
    )
}
export default Router