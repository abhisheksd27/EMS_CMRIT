// src/components/Register.js

import React, { useState } from 'react';
import axios from 'axios';

const Register = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [role, setRole] = useState('ADMIN'); // Default to Admin, can be changed

    const handleRegister = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post(`http://localhost:8000/api/${role.toLowerCase()}/register/`, {
                email,
                password,
            });
            console.log('Registration successful:', response.data);
            // Optionally redirect or display a success message
        } catch (error) {
            console.error('Registration error:', error.response.data);
        }
    };

    return (
        <form onSubmit={handleRegister}>
            <h2>Register</h2>
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
            <button type="submit">Register</button>
        </form>
    );
};

export default Register;
