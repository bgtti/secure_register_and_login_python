import axios from 'axios';
import { useNavigate } from "react-router-dom";

/**
 * API calls in this application use the Axios library
 * @see {@link https://axios-http.com/docs/intro}
 */
const api = axios.create({
    baseURL: 'http://127.0.0.1:5000',
    withCredentials: true,
    // headers: {
    //     'Accept': 'application/json',
    //     'Content-Type': 'application/json'
    // }
});

// const navigate = useNavigate();

//interceptor: ignore 401 for login or signup -- should be handled differently
// how to do it: https://stackoverflow.com/questions/63423209/how-to-ignore-interceptors-in-axios-as-a-parameter
// or create new instance: https://github.com/axios/axios/issues/108

//uncomment the code bellow when login solved.

// api.interceptors.response.use(
//     function (response) {
//         return response;
//     },
//     function (error) {
//         let res = error.response;
//         if (res.status == 401) { //401 = Unauthorized (lacks valid authentication)
//             navigate("/login");
//         } else if (res.status == 429) { // 429 = Too Many Requests
//             console.log("too many requests") // handle properly
//         } else {
//             console.log("some other issue") //handle - display error page
//         }
//         console.error("Looks like there was a problem. Status Code:" + res.status);
//         return Promise.reject(error);
//     }
// )

export default api