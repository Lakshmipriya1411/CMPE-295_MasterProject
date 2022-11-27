import React, {Component} from 'react';
import axios from 'axios';
import {Navigate} from 'react-router-dom';

export default class Login extends Component {

    state = {
        email: '',
        password: '',
        redirect: false,
        authError: false,
        isLoading: false,
        location: {},
    };

    handleEmailChange = event => {
        this.setState({email: event.target.value});
    };
    handlePwdChange = event => {
        this.setState({password: event.target.value});
    };

    handleSubmit = event => {
        event.preventDefault();
        this.setState({isLoading: true});
        const url = 'http://ec2-54-153-46-53.us-west-1.compute.amazonaws.com:5000/api/auth/signin';
        const email = this.state.email;
        const password = this.state.password;
        const bodyFormData = {"user_email": email, "user_password": password}
        axios.post(url, bodyFormData)
            .then(result => {
                if (result.data.token) {
                    localStorage.setItem('isLoggedIn', true);
                    localStorage.setItem('token', result.data.token);
                    this.setState({redirect: true, isLoading: false});
                    if (localStorage.getItem('redirect')) {
                        localStorage.removeItem('redirect')
                        window.location.href = '/recipe-details'
                    } else {
                        window.location.href = '/home'
                    }
                }
            })
            .catch(error => {
                console.log(error);
                this.setState({authError: true, isLoading: false});
            });
    };


    renderRedirect = () => {
        if (this.state.redirect) {
            return <Navigate to='/home'/>
        }
    };

    render() {
        return (
            <div className="row pt-10">
                <div className="col-md-4"></div>
                <div className="col-md-4">
                    <div className="card card-primary">
                        <div className="card-header">
                            <h3 className="card-title">Login </h3>
                        </div>
                        <form onSubmit={this.handleSubmit}>
                            <div className="card-body">
                                <div className="form-group">
                                    <label htmlFor="exampleInputEmail1">Email address</label>
                                    <input type="email" className="form-control" id="exampleInputEmail1" placeholder="Enter email" id="inputEmail" placeholder="Email address" type="text" name="email" onChange={this.handleEmailChange} autoFocus required/>
                                </div>
                                <div className="form-group">
                                    <label htmlFor="exampleInputPassword1">Password</label>
                                    <input type="password" className="form-control" id="exampleInputPassword1" placeholder="Password" id="inputPassword" placeholder="******" name="password" onChange={this.handlePwdChange} required/>
                                </div>

                                <div className="form-check">
                                    <input type="checkbox" className="form-check-input" id="exampleCheck1"/>
                                    <label className="form-check-label" htmlFor="exampleCheck1">Check me out</label>
                                </div>
                            </div>

                            <div className="card-footer">
                                <button type="submit" className="btn btn-primary">Submit</button>
                            </div>
                        </form>
                    </div>
                </div>
                {this.renderRedirect()}
            </div>
        )
    }
}