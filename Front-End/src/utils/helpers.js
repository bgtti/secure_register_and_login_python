export function capitalizeFirstLetter(string) {
    const stringCapitalized = string
        .split(' ')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
        .join(' ');

    return stringCapitalized;
}
// example usage:
// capitalizeFirstLetter("hello wOrld") -> "Hello World"