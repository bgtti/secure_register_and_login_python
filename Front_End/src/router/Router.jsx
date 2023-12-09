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
import AdminDashboard from "../pages/Admin/AdminDashboard";
import Footer from "../layout/Footer";
import ErrorPage from '../pages/ErrorPage/ErrorPage';

const Router = () => {
    const loaderDisplay = useSelector((state) => state.loader.display);
    return (
        <BrowserRouter>
            {loaderDisplay ? <Loader></Loader> : ""}
            <NavBar />
            <Routes>
                <Route exact path="/" element={<Home />} />
                <Route exact path="/login" element={<LogIn />} />
                <Route exact path="/signup" element={<SignUp />} />
                <Route exact path="/dashboard" element={<Dashboard />} />
                <Route exact path="/usersettings" element={<UserSettings />} />
                <Route exact path="*" element={<ErrorPage />} />
                <Route exact path="/admin_login" element={<AdminLogIn />} />
                <Route exact path="/admin_dashboard" element={<AdminDashboard />} />
            </Routes>
            <Footer />
        </BrowserRouter>
    )
}
export default Router