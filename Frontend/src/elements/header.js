import React, {Component} from 'react';
import {Link} from 'react-router-dom';

export default class Header extends Component {
    render() {
        return (
            <nav className="main-header navbar navbar-expand navbar-white navbar-light">
                {/*<ul className="navbar-nav">*/}
                {/*    <li className="nav-item">*/}
                {/*        <a className="nav-link" data-widget="pushmenu" href="#" role="button"><i className="fas fa-bars"></i></a>*/}
                {/*    </li>*/}
                {/*</ul>*/}

                <ul className="navbar-nav ml-auto">

                    <li className="nav-item">
                        <a className="nav-link" data-widget="fullscreen" href="/register" role="button">
                            Register
                        </a>
                    </li>
                    <li className="nav-item">
                        <a className="nav-link" data-widget="control-sidebar" data-controlsidebar-slide="true" href="/login" role="button">
                            Login
                        </a>
                    </li>
                </ul>
            </nav>
        )
    }
}