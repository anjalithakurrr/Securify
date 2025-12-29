// navbar.js
export function createNavbar() {
    const navbar = document.createElement('div');
    navbar.className = 'navbar';
    navbar.innerHTML = `
        <h1>Securify Dashboard</h1>
    `;
    return navbar;
}
