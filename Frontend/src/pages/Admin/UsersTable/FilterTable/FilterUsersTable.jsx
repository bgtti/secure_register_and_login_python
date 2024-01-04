import { useState } from "react";

const ITEMS_PER_PAGE = ["5", "10", "25", "50"];
const ORDER_BY = {
    last_seen: "last seen",
    name: "name",
    email: "email",
    created_at: "created at"
}
const ORDER_SORT = ["descending", "ascending"];
const FILTER_BY = {
    none: "no filter",
    is_blocked: "blocked users"
}



function FilterUsersTable() {

    const [itemsPerPage, setItemsPerPage] = useState(25);
    const [orderBy, setOrderBy] = useState("last_seen");
    const [orderSort, setOrderSort] = useState("descending");
    const [filterBy, setFilterBy] = useState("none");


    const [showOptions, setShowOptions] = useState(false);

    function toggleShowOptions() {
        setShowOptions(!showOptions);
    }


    return (
        <>
            <button onClick={toggleShowOptions}>
                Show options
            </button>
            {
                showOptions && (
                    <form action="">
                        <div>
                            <label htmlFor="itemsPerPage">Items per page:</label>
                            <select name="itemsPerPage" id="itemsPerPage">
                                {
                                    ITEMS_PER_PAGE.map((item, index) => (
                                        <option value={item} key={index}>{item}</option>
                                    ))
                                }
                            </select>
                        </div>
                        <div>
                            <label htmlFor="itemsPerPage">Items per page:</label>
                            <select name="itemsPerPage" id="itemsPerPage">
                                {
                                    ORDER_SORT.map((item, index) => (
                                        <option value={item} key={index}>{item}</option>
                                    ))
                                }
                            </select>
                        </div>
                    </form>
                )
            }
        </>
    );
}
export default FilterUsersTable;