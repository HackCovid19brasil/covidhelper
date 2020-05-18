import React, { useEffect, useState } from 'react';
import { Link, useHistory } from 'react-router-dom';

import api from '../../services/api';

import './styles.css'
import logoImg from '../../assets/logo.png'

function UserGreeting(props) {
    return (
        <div className="header-container-item">
            <div className="header-link">
                <h1>Welcome back!</h1>
            </div>
        </div>
    )
}

function GuestGreeting(props) {
    return (
        <div className="header-container-item">
            <div className="header-link">
                <button className="button">
                    <Link to="/register" className="header-link">Cadastro</Link>
                </button>
            </div>
            <div className="header-link">
                <Link to="/login" className="header-link">Login</Link>
            </div>
        </div>
    )
}

function Greeting(props) {
    const loggedId = props.loggedId;
    if (loggedId) {
        return <UserGreeting />
    }
    return <GuestGreeting />
}

export default function Header() {
    const history = useHistory();
    const token = localStorage.getItem('token');

    const [id, setLogin] = useState([]);

    useEffect(() => {
        api.get('tokens', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        }).then(response => {
            setLogin(response.data.id);
        }).catch(error => {
            setLogin(false);
            history.push('/login');
        })
    }, [token, history]);
    return (
        <div className="header-container sticky lower-opacity">
            <div className="header-container-item">
                <div className="header-link">
                    <Link to="/dashboard" className="header-link">
                        <img src={logoImg} className="header-img" alt="indicAI" />
                    </Link>
                </div>                
            </div>
        </div>
    );
}