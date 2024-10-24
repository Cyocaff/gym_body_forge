import { useEffect } from "react";
import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
const navigate = useNavigate();
export function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();

    const data = {
      username: username,
      password: password
    };

    try {
      const response = await axios.post('http://localhost:8000/auth/login/', data, {
        headers: {
          'Content-Type': 'application/json'
        }
      });
	  localStorage.setItem('access_token', response.data.access);
      localStorage.setItem('refresh_token', response.data.refresh);
      console.log(response.data);  // Handle the response (e.g., JWT tokens)

    } catch (error) {
      console.error('There was an error!', error);
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button type="submit">Login</button>
      </form>
    </div>
  );
}


