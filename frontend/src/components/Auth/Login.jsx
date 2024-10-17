// src/components/Login.js

import React, { useState } from 'react';
import axios from 'axios';

const Login = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [role, setRole] = useState('ADMIN'); // Default to Admin, can be changed

    const handleLogin = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post(`http://localhost:8000/api/${role.toLowerCase()}/login/`, {
                email,
                password,
            });
            console.log('Login successful:', response.data);
            // Store tokens and redirect or display a success message
        } catch (error) {
            console.error('Login error:', error.response.data);
        }
    };

    return (
        <form onSubmit={handleLogin}>
            <h2>Login</h2>
            <div>
                <label>Email:</label>
                <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
            </div>
            <div>
                <label>Password:</label>
                <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
            </div>
            <div>
                <label>Role:</label>
                <select value={role} onChange={(e) => setRole(e.target.value)}>
                    <option value="ADMIN">Admin</option>
                    <option value="HOD">HOD</option>
                    <option value="PRINCIPAL">Principal</option>
                    <option value="STUDENT">Student</option>
                </select>
            </div>
            <button type="submit">Login</button>
        </form>
    );
};

export default Login;
