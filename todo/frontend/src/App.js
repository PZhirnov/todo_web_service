import React from 'react';
import logo from './logo.svg';
import './App.css';
import UsersList from './components/Users';
import ProjectList from './components/Projects';
import ToDoList from './components/ToDo';
import ProjectToDoList from './components/ToDoList';
import axios from 'axios';
import {HashRouter, Route, Router, Routes, Link, Switch, Redirect, BrowserRouter} from 'react-router-dom'


const NotFound404 = ({ location }) => {
  return (
    <div>
      <h1>Страница по адресу '{location.pathname}' не найдена</h1>
    </div>
  )
} 


class App extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
      'users': [],
      'projects':[],
      'todo_items':[]
    }
  }

  componentDidMount() {
    // UsersList
    axios.get('http://127.0.0.1:8000/api/users/')
      .then(response => {
        const users = response.data.results
        console.log(users)
        this.setState(
          {
            'users': users
          }
        ) 
      }).catch(error => console.log(error))
    
    // ProjectList
    axios.get('http://127.0.0.1:8000/api/projects/')
    .then(response => {
      const projects = response.data.results
      console.log(projects)
      this.setState(
        {
          'projects': projects
        }
      ) 
    }).catch(error => console.log(error))

    // ToDOList
    axios.get('http://127.0.0.1:8000/api/todo/')
    .then(response => {
      const todo_items = response.data.results
      console.log(todo_items)
      this.setState(
        {
          'todo_items': todo_items
        }
      ) 
    }).catch(error => console.log(error))
  }

  render() {
    return (
      
      <div className='App'>
          Приложение ToDo:
          <BrowserRouter>
            <nav class="navbar navbar-expand-lg navbar-light bg-light">
              <ul>
                <li>
                  <Link to='/'>Пользователи</Link>
                </li>
                <Link to='/projects'>Проекты</Link>
                <li>
                  <Link to='/tasks'>Задачи</Link>
                </li>
              </ul>
            </nav>
            <Switch>
              <Route exact path='/' component={() => <UsersList users={this.state.users} />} />
              <Route exact path='/projects' component={() => <ProjectList projects={this.state.projects} />} />
              <Route exact path='/tasks' component={() => <ToDoList todo_items={this.state.todo_items} />} />
              
              <Route path='/projects/:id/:title/' >
                <ProjectToDoList todo_items={this.state.todo_items} />
              </Route>
              <Route component={NotFound404} />
            </Switch>
          </BrowserRouter>
        </div>
    )
  }
}

export default App;
