
import './Logout.css';
import { logoutUser } from '../service/AuthService';
import React from 'react';


export default function LogoutButton(props){


    const handleLogout = () =>{

        logoutUser(props.setIsLoggedIn);
    }


    return(
        <div>
            
            <button className="logout-button" onClick={handleLogout}>
                Logout
            </button>
        </div>
    );

}
