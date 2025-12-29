// api.js
export async function getDashboardData() {
    try {
        const response = await fetch('http://localhost:5000/dashboard'); // replace with your backend endpoint
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching dashboard data:', error);
        return null;
    }
}
