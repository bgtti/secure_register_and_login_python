import { BrowserRouter, Routes, Route } from "react-router-dom";
import NavBar from "../layout/NavBar";
import Home from '../pages/Home/Home';
import LogIn from "../pages/Login/Login";
import SignUp from "../pages/SignUp/SignUp";
import Dashboard from "../pages/Dashboard/Dashboard";
import UserSettings from "../pages/UserSettings/UserSettings";
import Footer from "../layout/Footer";
import ErrorPage from '../pages/ErrorPage/ErrorPage';

const Router = () => {
    return (
        <BrowserRouter>
            <NavBar />
            <Routes>
                <Route exact path="/" element={<Home />} />
                <Route exact path="/login" element={<LogIn />} />
                <Route exact path="/signup" element={<SignUp />} />
                <Route exact path="/dashboard" element={<Dashboard />} />
                <Route exact path="/usersettings" element={<UserSettings />} />
                <Route exact path="*" element={<ErrorPage />} />
            </Routes>
            <Footer />
        </BrowserRouter>
    )
}
export default Router