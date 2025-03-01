import React from 'react'
import ReactDOM from 'react-dom/client'
import Router from './router/Router'
import { Provider } from 'react-redux';
import { store } from './redux/store';
import { HelmetProvider } from "react-helmet-async";
import './styles/cssReset.css'
import './styles/fonts.css'
import './styles/global.css'
import './main.css'

ReactDOM.createRoot(document.getElementById('root')).render(
    <React.StrictMode>
        <Provider store={store}>
            <HelmetProvider>
                <Router />
            </HelmetProvider>
        </Provider>
    </React.StrictMode>,
)
