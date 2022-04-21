import React from 'react';
import logo from './logo.svg';
import './App.css';
import UsersList from './components/Users';
import ProjectList from './components/Projects';
import ToDoList from './components/ToDo';
import ProjectToDoList from './components/ToDoList';
import LoginForm from './components/Auth';
import ProjectForm from './components/ProjectForm';
import ToDoForm from './components/ToDoForm';
import axios from 'axios';
import {HashRouter, Route, Router, Routes, Link, Switch, Redirect, BrowserRouter} from 'react-router-dom';
import Cookies from 'universal-cookie';



const NotFound404 = ({ location }) => {
  return (
    <div>
      <h1>Страница по адресу '{location.pathname}' не найдена</h1>
    </div>
  )
} 

const login = ({ location }) => {
  return (
    <div>
      <h1>Для </h1>
    </div>
  )
} 


class App extends React.Component {
  constructor(props) {
    super(props)
    this.url_source = 'http://127.0.0.1:8000' 
    this.url_api = {
      'get_token': this.url_source + '/api-token-auth/',
      'users': this.url_source + '/api/users/',
      'projects': this.url_source + '/api/projects/',
      'todo': this.url_source + '/api/todo/',
      'todo_base': this.url_source + '/api/todo/base/',
    }
      
    this.state = {
      'users': [],
      'projects':[],
      'todo_items':[],
      'token': '',
      'username': '',
    }
  }

  set_token(token, username) {
    const cookies = new Cookies()
    cookies.set('token', token)
    cookies.set('username', username)
    this.setState({
      'token': token,
      'username': username,
    }, () => this.load_data())
  }

  is_authenticated() {
    return this.state.token != ''
  }

  logout() {
    this.set_token('')
  }

  get_token_from_storage() {
    const cookies = new Cookies()
    const token = cookies.get('token')
    const username = cookies.get('username')
    this.setState({
      'token': token,
      'username': username,
    }, () => this.load_data() )
  }

  get_token(username, password) {
    axios.post(this.url_api['get_token'], {username: username, password: password})
    .then(response => {this.set_token(response.data['token'], username)})
    .catch(error => alert('Неверный логин или пароль'))
  }

  get_headers() {
    let headers = {
      'Content-Type': 'application/json'
    }
    if (this.is_authenticated()) {
      headers['Authorization'] = 'Token ' + this.state.token
    }
    return headers
  }

  load_data() {
    const headers = this.get_headers()
    // UsersList
    axios.get(this.url_api['users'], {headers})
    .then(response => {
      this.setState(
        {
          'users': response.data.results
        }
      ) 
    }).catch(error => {
      console.log(error)
      this.setState({'users': []})
    })

    // ProjectList
    axios.get(this.url_api['projects'], {headers})
    .then(
      response => {
        console.log(response.data.results)
        this.setState({
          'projects': response.data.results
        }
      ) 
    }).catch(error => {
      console.log(error)
      this.setState({'projects': []})
    })

    // ToDOList
    axios.get(this.url_api['todo'], {headers})
    .then(response => {
    this.setState(
      {
        'todo_items': response.data.results
      }
    )
    console.log(this.state.todo_items)
    }).catch(error => {
      console.log(error)
      this.setState({'todo_items': []})
    })
  }

  // --- Проекты
  // Удаление проекта по нажатию кнопки
  deleteProject(id) {
    const headers = this.get_headers()
    axios.delete(`${this.url_api['projects']}${id}/`, {headers})
      .then(response => {
        console.log(response.data)
        this.setState({projects: this.state.projects.filter((item) => item.id !== id)})
        }
    ).catch(error => console.log(error))
  }

  // Создание проекта
  createProject(data) {
    const headers = this.get_headers()
    axios.post(`${this.url_api['projects']}`, data, {headers, headers})
      .then(response => {
        console.log('сработал')
        let newProject = response.data;
        this.setState ({projects: [...this.state.projects, newProject]})})
        .catch(error => console.log(error))
  }

  // Редактирование проекта
  editProject(id, data) {
    const headers = this.get_headers()
    axios.put(`${this.url_api['projects']}${id}/`, data, {headers, headers})
      .then(response => {
        //let newProject = response.data;
        //this.setState ({projects: this.state.projects})
        this.load_data();
      })
        .catch(error => console.log(error))
  }

  searchProject(searchChar) {
    const headers = this.get_headers()
    axios.get(`${this.url_api["projects"]}?search=${searchChar}`, {headers})
     .then(
       response => {
         console.log(response.data.results)
         this.setState({
           'projects': response.data.results
         }
       ) 
     }).catch(error => {
       alert('запрос на сработал')
       
     })
    }

  // --- ToDo ---
  deleteToDo(id) {
    const headers = this.get_headers();
    console.log(`будет удален ${id}`)
    axios.delete(`${this.url_api['todo_base']}${id}/`, {headers})
      .then(response => {
        console.log(response.data)
        this.setState({todo_items: this.state.todo_items.filter((item) => item.id !== id)})
        }
    ).catch(error => console.log(error))

  }

  createToDo(data) {
    const headers = this.get_headers();
    console.log(`создание todo ${data}`)
    axios.post(`${this.url_api['todo']}`, data, {headers, headers})
      .then(response => {
        let newToDo = response.data;
        console.log(response.data)
        this.setState ({todo_items: [...this.state.todo_items, newToDo]})})
        .catch(error => console.log(error))
    console.log(this.state.todo_items)
  }

  editToDo(id, data) {
    const headers = this.get_headers();
    console.log(`создание todo ${data}`)
    console.log(data)
    // ДОПИСАТЬ КОД ОТПРАВКИ ЗАПРОСА
    axios.put(`${this.url_api['todo']}${id}/`, data, {headers, headers})
      .then(response => {
        //this.load_data();
      })
      .catch(error => console.log(error))
    console.log(this.state.todo_items)
  }


  componentDidMount() {
    this.get_token_from_storage()
    this.load_data()
  }

  render() {
    return (
      
      <div className='App'>
          Приложение ToDo:       
          <BrowserRouter>
            <nav class="navbar navbar-expand-lg navbar-light bg-light">
              
              {this.is_authenticated() ? <button onClick={ () => this.logout()}>Выход</button> : <Link to='/login'>Вход</Link>}              
              {this.is_authenticated() ? 
              <ul>
                <h1>Пользователь: {this.state.username}</h1>
                <li><Link to='/users'>Пользователи</Link></li> 
                <li><Link to='/projects'>Проекты</Link></li>
                <li><Link to='/tasks'>Задачи</Link></li>
              </ul>
              : ''}  
            </nav>
            <Switch>
              <Route exact path='/' component={() => <UsersList users={this.state.users} />} />
              <Route exact path='/users' component={() => <UsersList users={this.state.users} />} />
              
              <Route exact path='/projects' component={
                () => <ProjectList 
                        projects={this.state.projects} 
                        deleteProject={(id) => this.deleteProject(id)}
                        searchProject={(searchChar) => this.searchProject(searchChar)}  
                      />
                } />
              
              <Route exact path='/projects/create' component={() => <ProjectForm createProject={(data) => this.createProject(data)} users={this.state.users}/>}/>
              
              <Route exact path='/projects/:id/' component={() => <ProjectForm editProject={
                (id, data) => this.editProject(id, data)} users={this.state.users} edit={true} projects={this.state.projects}/> 
                } />

              <Route exact path='/tasks' component={() => <ToDoList todo_items={this.state.todo_items} 
                                                            projects={this.state.projects} deleteToDo={(id) => this.deleteToDo(id)}/>} />
              
              <Route exact path='/projects/:id/tasks/create' component={
                () => <ToDoForm 
                        createToDo={(data) => this.createToDo(data)}
                        editToDo={(id, data) => this.editToDo(id, data)} 
                        usersOnProject = {this.state.userOnProject}
                        projects={this.state.projects}
                        edit={false}
                      />
                      } 
              />

              <Route exact path='/tasks/:id' component={
                () => <ToDoForm
                        createToDo={(data) => this.createToDo(data)} 
                        editToDo={(id, data) => this.editToDo(id, data)} 
                        usersOnProject = {this.state.userOnProject}
                        todo = {this.state.todo_items}
                        projects={this.state.projects}
                        edit={true}
                      />
                      } 
              />
                
              <Route exact path='/projects/tasks/:id/:title/' component={() => <ProjectToDoList todo_items={this.state.todo_items}/>}/>

              { this.is_authenticated() == '' ? <Route exact path='/login' 
              component={() => <LoginForm get_token={(username, password) => this.get_token(username, password)} />} /> : ''}
              
              
              <Route component={NotFound404} />
            </Switch>
          </BrowserRouter>
        </div>
    )
  }
}

export default App;
