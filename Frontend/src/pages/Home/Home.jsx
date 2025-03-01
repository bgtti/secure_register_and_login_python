import { Helmet } from "react-helmet-async";
import "./home.css"

function Home() {
    return (
        <div className="Home">
            <Helmet>
                <title>Home Page</title>
            </Helmet>
            <section className="Home-Section1">
                <div className="Home-Section1-text">
                    <h1>a secure</h1>
                    <p>registration and log-in template</p>
                    <p><span>with Flask, React & SQL</span></p>
                </div>
                <div className="Home-Section1-triangleStyle">
                </div>
            </section>
            <section>
                <h2>Replace this content</h2>
                <p>include information here about what your app does</p>
            </section>
        </div>
    )
}

export default Home