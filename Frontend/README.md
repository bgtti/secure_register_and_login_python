# Secure Register and Login: Frontend template

This is the font end folder of the "Secure Register and Login" application.
The front end uses React and Vite with HMR and some ESLint rules.

## Table of Contents
- [Goals](#goals)
- [How to use this template](#how-to-use-this-template)
- [Installation](#installation)
- [Run tests](#run-tests)
- [React extensions](#react-extensions)
- [Pages](#pages)
    - [Home page](#home-page)
    - [Contact page](#contact-page)
    - [Login and Signup](#login-and-signup)
    - [User Dashboard and Settings](#user-dashboard-and-settings)
    - [Admin Dashboard and other protected pages](#admin-dashboard-and-other-protected-pages)
    - [Error pages](#error-pages)
- [Folder structure](#folder-structure)
- [Styles](#styles)
    - [CSS](#css)
    - [Code style](#code-style)
    - [SEO](#seo)
- [React + Vite](#react-+-vite)
- [Other resources](#other-resources)

## Goals

This app was made to be used as a template for software that need basic functionality such as authentication, authorization, basic user settings, role-based user management, and basic dashboard.
The whole project was designed with the concearn for user privacy (not utilizing, to the author's best knowledge, any third-party dependency that may track users), security (taking care of how auth is managed), and trying to utilize best practices (code documentation, following react common standards as much as possible).

Some key elements kept in mind are OWASP's top 10 principles. You can read more about that using the link bellow.
Link: https://www.cloudflare.com/en-gb/learning/security/threats/owasp-top-10/

## How to use this template

After installation:

1. change the favicon
first delete the file named icon_lock.svg in the public folder and place the file of your desired favicon there.

then, in index.html you will see a link tag. Replace the name in the href with that of the svg of your desired favicon. If you are using another file format, you might want to change the type as well (eg: for a .ico file: type="image/png" href="/favicon.ico")

```
<link rel="icon" type="image/svg+xml" href="/icon_lock.svg" />
```

2. change the app name 
`layout` contains the navbar where you may change the app's name to the name of your liking

3. change the home page
`pages` contain the homepage element. You can wipe out the css and re-design the homepage to your liking.
You can then delete the image from the `assets/images` folder.

4. design the user's dashboard
`pages/Account/Dashboard` contains the user's dashboard page (the first page viewed after the user logs in).
Here, you can include the content of your choice. 
You may also add more functionality to the user's account under `pages/Account`

5. deploy and enjoy
You will be ready to deploy your app! 
You can continue to improve and build upon it as needed.

## Installation

Install packages and run the application with the following commands:

```pwsh
npm install
npm run dev
```

## Run tests

Run Jest tests with the following command:
```pwsh
npm run test
```

TODO: Note jest tests have not yet been written.

## React extensions

React was extended with a couple of useful libraries:
- Redux: used for state management
- Axios: used for http API requests
- Router: used for page navigation
- Prop-types: used for type-checking props passed to components
- React-helmet-async: used to manage and update the `<head>` section of the HTML document (to improve SEO, for instance)

Since the goal of this app is to be a template upon which a developer could build upon, the author tried to keep the use of external libraries to a minimum. 
This should allow for greater flexibility, as well as improve maintainability and reduce the risk of possible performance impacts.

## Pages 

This app has the main skeleton and of a software already built. The main features are:
- Home page
- Contact page
- Login and signup page
- User dashboard and settings
- Admin dashboard with user management 
- Error pages

### Home page
The homepage was kept simple. A developer can easily replace it's content.
As it is the case with other page components, it is placed between the layout components NavBar and Footer. The NavBar 'logo' is a place holder for the app's name.
The navigation also contains a button to switch between light and dark modes.

### Contact page
Any user may send a message to the site's administrators through the contact form. The developer can set the admin's email in the backend to receive a notification of a new message. Messages sent through the form will also appear for site admins (inside the admin protected pages).

### Login and Signup
A user can create an account and log in using a password or OTP. The logic for resetting a password has also been implemented. Furthermore, the user can set the account as such to enable multi-factor authentication (MFA), and the login logic was built as to accommodate for the input of both the password and the OTP in those cases.

### User Dashboard and Settings
When users log in, they are re-directed to their Account where they will see a sub navigation bar with the option Dashboard and Settings. By default, they will see the Dashboard page underneath. This page is a placeholder for any content the developer wishes to display (according to the app logic desired). 
If the user clicks on Settings, they will see an array of options they can set in their accounts. Here, the user may change account details (name, email, password), set preferences (be included in the mailing list or toggle the dark-mode), set an account recovery email, verify the account, enable MFA, or delete the account. All this logic has been implemented in the backend and is use-ready.

### Admin Dashboard and other protected pages
Users with an admin role also will be given access to the admin area.

Here, the admins may see three navigation options:
1. Dashboard
Here admins can see basic analytics such as the total registered users and things that require the admin's attention such as unanswered messages.
TODO: note the logic of this page has not yet been implemented (only the UI has been implemented so far).

2. Users
Admins can manage users, and the starting point is a table of all signed up users. This app has been seeded in the backend to enable testing and visualization. Admins may:
- filter the table and search users
- see a table of user with information such as name, email, last login date, user type (or role, such as 'regular user' or 'admin'), flag (user may be flagged by an admin for whatever app logic needed, example: cursing or using profanity), account status (whether the user's account is blocked or not). Admins may also click to see further user information, block a user (if it was flagged as a spammer, for instance), or delete a user.

A user's information can be retrieved such as basic information about the user and that account, activity logs, and messages sent to site admins.
Note that only the Super Admin (there will be only 1) can manage user roles (example: assign the role of admin to a regular user).

3. Messages
Admins can view a table of messages sent through the contact form. They may also respond to it (either by recording a reply already sent by email or by replying directly from inside the app, and the user will also receive an email with the content). The messages table can be filtered to show only unanswered messages, for instance.
An admin may also flag a message or mark it as spam.

### Error pages
Should the user navigate to a page that does not exist, an error page will appear.
Should the user land on the error page due to a server error response, some information about the specific error may also be displayed (example 429 will show up if the user's IP is blocked by the server's rate limiter).
Note that routing to such error pages can be handled by axios interceptors. Error handling may differ according to the type of request, and more than one interceptor was created to allow for differed required behaviours (the `config` folder contains the interceptors). Authentication-related requests take more care not to display detailed error information so as to not open the door to bad actors trying to access accounts or check if they exist. These cases (example: wrong login credentials) are handled from within the component instead of routed to the error page. 

## Folder structure

The folder structure was designed to make this template scalable, and the author hopes it should enable maintainability and easen collaboration (so as new developers could understand it faster).

Inside the src folder you will see:

`main.jsx` is the main entry to the app. At its core, one will see Router (from the `react-router` library). It is wrapped by the HelmetProvider (from the `react-helmet-async` library), which in turn is wrapped by the Provide (from the `redux` library).

- `assets` is the folder containing downloaded fonts, images, and icons used throughout the app.
- `components` is the folder containing react components which are commonly re-used throughout the app (consumed from components inside the `pages` folder). Examples: Modal, Loader (when page is waiting for an async function to finish), Pagination, among others.
- `config` contains the configuration to use the `axios` library, as well as the API handlers and end points. React components call on those functions to request resources from the backend or make changes to the redux store. The `apiHandler` folder is structured in a way as to match the backend's routes folder structure.
- `hooks` contains custom hooks such as `useIsComponentMounted`, which checks whether a component is mounted to decide whether API request returns should still be displayed.
- `layout`contains page layout components such as the navbar and footer.
- `pages` contain page components, such as the homepage, and follows the user-flow logic (components named after the website pages they create). These pages are often build using shared components from the `components` folder. Example: `Auth` is a folder containing authorization-related pages which do not require user signup, such as the Login and Signup pages. These are pages that make use of a password input field. There is also a page (technically a modal) which the user can only access when he/she is signed into the account, which is the `ModalChangePassword` (inside `Account/Settings/AccountDetails`). Well, since all these require a password input field and need the logic for checking whether the password respects the same standards, they can import the password input field from the `src/components/Auth` folder, so the logic for checking a password does not need to be re-written. If a component is only used inside the page, then it will be found inside that page's folder. Else, if it is shared by multiple pages, either it will be found inside the parent's folder (local use) or the `components` folder if it is used by multiple pages.
- `redux` contains the redux store logic. It mainly stores the loader state, user information state, and user preferences. It also contains a `utilsRedux` folder that contain the functions that make changes to the redux store. While the loader state is used by files inside `pages`, it is recommended that other states only be changed from inside the `config/apiHandler` folder. The reason is that most of the redux state is anyway derived from API calls. The few times that is not the case (example: night-mode can also be set without logging into the app), a function to change the redux state was still included inside the `config/apiHandler/userSettings/setNightMode.js` file. The reason for this is to try to keep redux state changes as locally contained as possible, and this way make it easier to make changes to the stores in the future (whithout the need to scan the whole app, which would make making store changes a nightmare). To sum up: a component will call an API-handler function, which will make a call to a redux utils function, which in turn will make changes to the redux state. The only exception to this rule is the loader slice (whose redux state can be changed from any component).
- `router` is the folder containing the react-router logic (the main file being `Router.jsx`). It uses components such as `ProtectedUserRoute.jsx` to filter the authorization to access certain resources (pages the users can access only after logging in). Note authentication and authorization is managed by the backend with the use of server-side cookies, and will not serve content when the cookie is not present in the request (the backend is the one to insert the cookie following a login, and the frontend does not interact with it). Only the routing logic is used in the frontend (storing the information of whether a user is logged in by checking the information in the redux store).
- `styles` is the folder containing global css logic: resetting brower standards, loading fonts, and setting app global styles. These files are imported in `main.jsx`
- `utils` is the folder containing utilily functions such as `capitalizeFirstLetter` (inside `helpers.js`), functions used for input validation such as `nameValidation` (inside `validation.js`), or contants such as the object `INPUT_LENGTH` (inside `constants.js`) where we can derive the maximum number of characters from an email input field as being 320 from INPUT_LENGTH.email.maxValue.

## Styles

### CSS

This application does not use any third-party library or framework for styling.
It was decided instead to use vanilla css to give developers a greater control of how styles are applied. This also frees the project from being dependent on libraries that may change or become outdated (easier to maintain), and avoids performance impacts that third-party solutions may bring with it.

CSS files are organized the following way:

1. the styles folder
Here you will find:
- cssReset.css is used to avoid unwanted styles and effects from standard browser styles
- fonts.css is used to implement the fonts downloaded and available inside src/assets/fonts
- global.css sets the base styles of html elements used throughout this document (example: h1, p, and button styling)

The above files are imported in src/main.jsx, which is the entry point of this application

2. the main.css file
This file contains classes that are used by multiple files throughout the application. This is used to maintain a similar style throughout the app while also speeding up development (these classes can be copied and pasted in several react elements, bringing the intended behaviour). All shared classes names begin with `.Main-`. Example: `.MAIN-DeleteBtn` is used to style a button meant to delete a resource (such as deleting the user's own account) and `.MAIN-display-none` can be used whenever an element should be hidden from the DOM (such as a modal, which can be 'opened' and 'closed' programatically).

3. module-specific files
Components and pages are react elements that may require styling specific to them. A css file may therefore acompany a jsx file of the same name. These use css classes specific to those elements - and are not used in other jsx files in the application. It is possible that a component uses classes starting with "MAIN" in the name, indicated a shared style is used, and another class starting with the element's name that indicates the style is specific to that element alone. For instance, to style the main navigation (whose coponent is named NavBar) a class named `NavBar` was given to an element, and child element names start with `NavBar-`, such as `.NavBar-logo`. The className contains therefore the name of the component, so one can easily spot the location of the css file specifying the style.

The CSS logic was implemented as mobile-first and adapted to big screens (using @media only screen and (min-width:600px) and in specific cases, larger screens when necessary).

The app was also first styled for dark-mode, and later adapted to include light-mode. Styles specific to light-mode contain the class `.light-mode` preceeding the element or it's given style class. Example:
while `.MAIN-table>thead>tr` is used to style the table row under the class MAIN-table, `.light-mode .MAIN-table>thead>tr` is it's light-mode style.

### Code style

Docstrings were used to document js functions and components. These are thought to contain a description of parameters (if any) and returned values, along with a short explanation of what it does or why it was written a certain way (give context to decisions). *JSDocs* are used to acomplish this, and you can read more about it here: https://jsdoc.app/ 

Short comments throughout the file may be obvious, but put in place to enable a quick visual scan of a file (useful when trying to find a particular part of the code).

Imports try to follow some base standard: react imports on the top-level, followed by third-party libraries, followed by folders higher-up in the hiearachy, with style sheets at the bottom.

The `prop-types` library was also used in components that receives props. This helps catching bugs early by enforcing props have the expected types.

As much as possible, the author tried to implement type-checking of function parameters and communicate unexpected errors in a way that makes debugging easier when developing. This is mostly used in util functions or async functions that make API requests.

### SEO
`react-helmet-async` is used to easily modify the following HTML tags from within components: `title`, `meta`, and `head`.
Search Engine Optimization (SEO) is made easier this way, and the developer may easily describe what pages should or not be tracked by search engine crawlers.


## React + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react/README.md) uses [Babel](https://babeljs.io/) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh


## Other resources

###  React Helmet Async
used to handle meta tags and other header elements.
if you have never used it before, check out the link bellow.
Link: https://www.youtube.com/watch?v=wWeG8rWkMsM

### Inspiration
Would like to improve upon the admin dashboard?
Check out the repo in the link bellow
Link: https://github.com/jonalxh/Flask-Admin-Dashboard

Would you like some design inspiration from a beautiful website?
Check out the website bellow.
Link: https://job-ish.com/

### json schema validation for the front end
Would like to implement json schema validation for the front end?
This app does not make use of it, but you can find out more in the link bellow
Link: https://ajv.js.org/

### gitlab flow
If you use gitlab or would like to know more about the differences between github and gitlab flow, check out the link bellow (with review info about release branches).
Link: [What Is GitLab Workflow](https://www.youtube.com/watch?v=7lgGEXpsflI)





