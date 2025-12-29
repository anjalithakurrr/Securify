// auth.js

// Login function (if not already present)
export async function loginUser(credentials) {
    try {
        const response = await fetch('http://localhost:5000/login', { // backend login endpoint
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(credentials)
        });
        return await response.json();
    } catch (error) {
        console.error('Login error:', error);
        return { success: false };
    }
}

// Register function
export async function registerUser(credentials) {
    try {
        const response = await fetch('http://localhost:5000/register', { // backend register endpoint
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(credentials)
        });
        return await response.json();
    } catch (error) {
        console.error('Register error:', error);
        return { success: false };
    }
}
