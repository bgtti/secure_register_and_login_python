import { PropTypes } from "prop-types";
import iconClose from "../../assets/icon_close.svg"
import { capitalizeFirstLetter } from "../../utils/helpers"
import "./modal.css"

// When using the Modal component, place the following in the parent:
// modalStatus ? document.body.classList.add("Modal-active") : document.body.classList.remove("Modal-active");
// (replacing "modalStatus" with whatever variable name used to keep track of modal state)


function Modal(props) {
    const { modalStatus, setModalStatus, title, content, capitalizeTitle } = props;

    //optional props capitalizeTitle will capitalize every first letter in string. Set to true by default.
    let displayTitle;
    !capitalizeTitle ? displayTitle = capitalizeFirstLetter(title) : displayTitle = title;

    const toggleModal = () => {
        setModalStatus(!modalStatus);
    }
    return (
        modalStatus && (
            <div className="Modal">
                <div className="Modal-Container">
                    <div className="Modal-Heading">
                        <h2>{displayTitle}</h2>
                        <div>
                            <img
                                alt="Close modal"
                                className="Modal-Heading-icon"
                                role="button"
                                title="Close modal"
                                src={iconClose}
                                onClick={toggleModal} />
                        </div>
                    </div>
                    {content}
                </div>
            </div>
        )
    );
};

Modal.propTypes = {
    modalStatus: PropTypes.bool.isRequired,
    setModalStatus: PropTypes.func.isRequired,
    title: PropTypes.string.isRequired,
    content: PropTypes.element.isRequired,
    capitalizeTitle: PropTypes.bool
};

export default Modal;