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
const SEARCH_BY = ["name", "email", "none"];

/*******************  THE COMPONENT  ********************/

/**
 * Component that enables searching for a user
 * 
 * @param {object} props
 * @param {function} props.setSearchOptions updates props.tableOptions
 * @param {object} props.searchOptions state in parent
 * @param {string} props.searchOptions.searchBy string 
 * @param {string} props.searchOptions.searchWord string 
 * @returns {React.ReactElement}
 */
function SearchUser(props) {
    const { searchOptions, setSearchOptions } = props

    const [showOptions, setShowOptions] = useState(false);
    const [errorMessage, setErrorMessage] = useState("");

    const [formData, setFormData] = useState({
        searchBy: searchOptions.searchBy,
        searchWord: searchOptions.searchWord
    });

    function toggleShowOptions() {
        setShowOptions(!showOptions);
    }
    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData((prevData) => ({
            ...prevData,
            [name]: value,
        }));
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        let searchBy = (formData.searchBy && SEARCH_BY.includes(formData.searchBy)) ? formData.searchBy : false;
        let searchWord;
        let formIsValid;
        let currentForm = { ...formData };

        if (searchBy && searchBy !== "none") {
            searchBy === "email" ? searchWord = emailValidation(formData.searchWord) : searchWord = nameValidation(formData.searchWord);
            formIsValid = searchBy && searchWord.response;
        } else if (searchBy && searchBy === "none") {
            if (formData.searchWord !== "") {
                currentForm = {
                    searchBy: "none",
                    searchWord: ""
                };
                setFormData({ ...currentForm });
            };
            formIsValid = true;
        } else {
            formIsValid = false;
        }

        let stateChanged = JSON.stringify(searchOptions) !== JSON.stringify(currentForm)

        if (formIsValid && stateChanged) {
            setErrorMessage("")
            setSearchOptions({ ...currentForm })
            setShowOptions(false);
        } else {
            (formIsValid && !stateChanged) ?
                setErrorMessage("Oops, no changes detected. Check your input and try again.") :
                setErrorMessage((formData.searchBy === "email" ? "Invalid email input." : "Invalid name input."))
        }
    };

    return (
        <div>
            <button className={`UsersTableFilters-btn ${showOptions ? "UsersTableFilters-btn-selected" : ""}`} onClick={toggleShowOptions}>
                {showOptions ? "Hide search ↓" : "Search user ->"}
            </button>
            {
                showOptions && (
                    <form className="MAIN-form UsersTableFilters-form" onSubmit={handleSubmit}>
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
                            <label htmlFor="searchWord">Search word:</label>
                            <input type="text" name="searchWord" id="searchWord" onChange={handleChange} value={formData.searchWord} />
                        </div>
                        {
                            errorMessage !== "" && (
                                <p className="MAIN-error-message">
                                    <i>{errorMessage}</i>
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

SearchUser.propTypes = {
    setSearchOptions: PropTypes.func.isRequired,
    searchOptions: PropTypes.shape({
        searchBy: PropTypes.string,
        searchWord: PropTypes.string
    })
};

export default SearchUser;
