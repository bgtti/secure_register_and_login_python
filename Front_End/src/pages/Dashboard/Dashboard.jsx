import { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";
import { setLoader } from "../../redux/loader/loaderSlice"
import { setUser } from "../../redux/user/userSlice";
import api from "../../config/axios"
import APIURL from "../../config/apiUrls";

function Dashboard() {
    const user = useSelector((state) => state.user);
    const dispatch = useDispatch();
    const navigate = useNavigate();

    useEffect(() => {
        if (user.id === "") {
            dispatch(setLoader(true));
            const getUserData = async () => {
                try {
                    const response = await api.get(APIURL.GET_USER);
                    if (response.status !== 200) {
                        console.log("oops")
                    } else {
                        const userData = {
                            id: response.data.user.id,
                            email: response.data.user.email,
                            name: response.data.user.name
                        }
                        dispatch(setUser(userData))
                    }
                } catch (error) {
                    console.log("oops")
                }
                dispatch(setLoader(false));
            }
            getUserData();
        }
    }, [])

    return (
        <p>Dashboard from {user.name}</p>
    )
}
export default Dashboard