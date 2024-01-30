import { jwtDecode } from "jwt-decode";

export function loginUser (setIsLoggedIn, setFname, setLname, setEmail, token) {

    setIsLoggedIn(true);
    let x = jwtDecode(token);
    setFname(x.fname);
    setLname(x.lname);
    setEmail(x.email);

    localStorage.setItem("loggedIn",true);
    localStorage.setItem("fName",x.fname);
    localStorage.setItem("lName",x.lname);
    localStorage.setItem("email",x.email)

}

export function checkUserLogin(setIsLoggedIn, setFname, setLname, setEmail){

    if(localStorage.getItem("loggedIn") !== null && localStorage.getItem("fName")!== null && localStorage.getItem("lName") !== null && localStorage.getItem("email")!==null){
        setFname(localStorage.getItem("fName"));
        setLname(localStorage.getItem("LName"));
        setEmail(localStorage.getItem("email"));
        setIsLoggedIn(localStorage.getItem("loggedIn"));
        return true;
    }
    return false;
}

export function logoutUser(setIsLoggedIn){
    setIsLoggedIn(false);

    if(localStorage.getItem("loggedIn") !== null){
        localStorage.removeItem("loggedIn");
    }

    if(localStorage.getItem("fName") !== null){
        localStorage.removeItem("fName")
    }

    if(localStorage.getItem("lName") !== null){
        localStorage.removeItem("lName")
    }

    if(localStorage.getItem("email") !== null){
        localStorage.removeItem("email")
    }
}


// export const AuthService = {


//     const login : (email, password) => {
//       const user = { email };
//       localStorage.setItem('user', JSON.stringify(user));
//     },
    
//     logout: () => {
//       localStorage.removeItem('user');
//     },
    
//     isAuthenticated: () => {
//       const user = localStorage.getItem('user');
//       return !!user;
//     }
//   };