// NavbarComponent.js
import React from 'react';
import { Navbar, Nav, Container } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import LogoutButton from './Logout';
import './Navbar.css'

const NavbarComponent = (props) => (
  <Navbar bg="light-purple" expand="lg" fixed="top" style={{ backgroundColor: '#2C272E' }}>
    <Container>
      <Link to="/"  className="navbar-brand">
        Tarot Card Website!!
      </Link>
      <Navbar.Toggle aria-controls="basic-navbar-nav" />
      <Navbar.Collapse id="basic-navbar-nav">
        <Nav className="me-auto">
          {/* Use the Link component for navigation links */}
        </Nav>
        <Nav>
            <LogoutButton setIsLoggedIn={props.setIsLoggedIn}/>
        </Nav>
      </Navbar.Collapse>
    </Container>
  </Navbar>
);

export default NavbarComponent;
