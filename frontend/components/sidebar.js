// sidebar.js
export function createSidebar() {
    const sidebar = document.createElement('div');
    sidebar.className = 'sidebar';
    sidebar.innerHTML = `
        <a href="dashboard.html">Dashboard</a>
        <a href="verify.html">Verify</a>
        <a href="result.html">Results</a>
        <a href="login.html">Logout</a>
    `;
    return sidebar;
}
