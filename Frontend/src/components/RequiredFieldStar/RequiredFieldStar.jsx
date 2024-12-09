import "./requiredFieldStar.css"

/**
 * Component returns span tag with a star
 * 
 * Can be placed inside label in a form to indicate a required form field.
 * Make sure to add the 'required' attribute to your field. 
 * 
 * This may seem like a silly component, but since this simple star may be used in many form fields, it may be easier to maintain as the app grows.
 * Keeping this component separate helps making sure the style is the same everywhere, as well as makes it easier to change the style whenever needed.
 * 
 * @visibleName Required Field
 * 
 * @returns {React.ReactElement}
 * 
 * @example
 *  // before:
 *  <label htmlFor="email">Email:<span className="MAIN-form-star"> *</span></label>
    <input  required  {...etc}  />
    // after:
    import RequiredFieldStar from "../../../components/RequiredFieldStar/RequiredFieldStar";
    //...
    <label htmlFor="email">Email:<RequiredFieldStar /></label>
    <input  required  {...etc}  />
 */
function RequiredFieldStar() {

    return (
        <span className="RequiredFieldStar"> *</span>
    );
};

export default RequiredFieldStar;