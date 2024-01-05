import { useState } from 'react'
import PropTypes from 'prop-types'
import { nameValidation, emailValidation } from "../../../../utils/validation"
import "../usersTable.css"

/*******************  CONSTANTS  ********************/

/** 
 * Constants array for defining selection of filter options
 * @constant
 * @type {string[]}
 * @default 
 * ["name", "email"]
*/
const SEARCH_BY = ["name", "email"];

/*******************  THE COMPONENT  ********************/

/**
 * Component that enables searching for a user
 * 
 * @param {object} props
 * @param {func} props.somefunc //DEFINE
 * @returns {React.ReactElement}
 */
function SearchUser(props) {
    //import function to query results

    const [showOptions, setShowOptions] = useState(false);
    const [formData, setFormData] = useState({
        searchBy: "name",
        searchInput: "",
        errorMessage: ""
    });
    function toggleShowOptions() {
        setShowOptions(!showOptions);
        if (formData.message !== "") {
            setFormData((prevData) => ({
                ...prevData,
                errorMessage: "",
            }));
        }
    }
    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData((prevData) => ({
            ...prevData,
            [name]: value,
        }));
        if (formData.message !== "") {
            setFormData((prevData) => ({
                ...prevData,
                errorMessage: "",
            }));
        }
    };
    const handleSubmit = (e) => {
        e.preventDefault();
        let searchBy = (formData.searchBy && SEARCH_BY.includes(formData.searchBy)) ? formData.searchBy : false;
        let searchInput;
        if (searchBy) {
            searchBy === "email" ? searchInput = emailValidation(formData.searchInput) : searchInput = nameValidation(formData.searchInput);
        }

        let formIsValid = searchBy && searchInput.response;

        if (formIsValid) {
            // query results
            setShowOptions(false);
        } else {
            setFormData((prevData) => ({
                ...prevData,
                errorMessage: (formData.searchBy === "email" ? "Invalid email input." : "Invalid name input.")
            }));
            console.warn("You are trying to submit invalid data.");
        }
    };

    return (
        <div>
            <button className={`UsersTableFilters-btn ${showOptions ? "UsersTableFilters-btn-selected" : ""}`} onClick={toggleShowOptions}>
                {showOptions ? "Hide search ↓" : "Search user ->"}
            </button>
            {
                showOptions && (
                    <form action="" className="MAIN-form UsersTableFilters-form" onSubmit={handleSubmit}>
                        <div className="MAIN-form-display-table">
                            <label htmlFor="searchBy">Search by:</label>
                            <select name="searchBy" id="searchBy" defaultValue={formData.searchBy} onChange={handleChange}>
                                {
                                    SEARCH_BY.map((item, index) => (
                                        <option value={item} key={index}>{item}</option>
                                    ))
                                }
                            </select>
                        </div>
                        <div className="MAIN-form-display-table">
                            <label htmlFor="searchInput">Filter:</label>
                            <input type="text" name="searchInput" id="searchInput" onChange={handleChange} />
                        </div>
                        {
                            formData.errorMessage !== "" && (
                                <p className="MAIN-error-message">
                                    <i>{formData.errorMessage}</i>
                                </p>
                            )
                        }
                        <button type="submit">Search</button>
                    </form>
                )
            }
        </div>
    )
}

SearchUser.propTypes = {}

export default SearchUser
