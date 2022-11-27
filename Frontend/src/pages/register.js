import React, {Component} from 'react';
import axios from 'axios';
import {Navigate} from 'react-router-dom';

export default class Register extends Component {

    state = {
        email: '',
        password: '',
        userName: '',
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

    handlePUseNameChange = event => {
        this.setState({userName: event.target.value});
    };

    handleSubmit = event => {
        event.preventDefault();
        this.setState({isLoading: true});
        const url = 'http://ec2-54-153-46-53.us-west-1.compute.amazonaws.com:5000/api/auth/signup';
        const user_email = this.state.email;
        const user_password = this.state.password;
        const user_name = this.state.userName;
        const bodyFormData = {user_email, user_password, user_name}
        axios.post(url, bodyFormData)
            .then(result => {
                console.info(result)
                if (result.data) {
                    localStorage.setItem('token', result.data.token);
                    window.location.href = '/login'
                    this.setState({redirect: true, isLoading: false});
                    localStorage.setItem('isLoggedIn', true);
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
                            <h3 className="card-title">Sign Up </h3>
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

                                 <div className="form-group">
                                    <label htmlFor="exampleInputUserName">User Name</label>
                                    <input type="text" className="form-control" id="exampleInputUserName" placeholder="Password" id="inputPassword" placeholder="User Name" name="userName" onChange={this.handlePUseNameChange} required/>
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