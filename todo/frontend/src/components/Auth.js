import React from 'react'


class LoginForm extends React.Component {
    constructor(props) {
        super(props)
        this.state = {login: '', password: ''}
    }

    handleChange(event) {
        this.setState(
            {
                [event.target.name]: event.target.value
            });
    }
    
    handleSubmit(event) {
        this.props.get_token(this.state.login, this.state.password)
        event.preventDefault()
    }

    render () {
        return (
            <div>
                <form onSubmit={(event)=> this.handleSubmit(event)}>
                <input type="text" className="login" name="login" placeholder="login" value={this.state.login} 
                onChange={(event)=>this.handleChange(event)} />
                <input type="password" className="login" name="password" placeholder="password" value={this.state.password} 
                onChange={(event)=>this.handleChange(event)} />
                <button type="submit" className="btn_login">Login</button>
            </form>

            </div>
            
            );
    }
}

export default LoginForm
