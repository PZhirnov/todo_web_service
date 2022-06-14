import React from "react";
import axios from "axios";
import Cookies from 'universal-cookie';
import { toHaveDisplayValue } from "@testing-library/jest-dom/dist/matchers";

// Функция получает индексы выбранных проектов из массива select
function getSelectedIndexes (oListbox)
{
  var arrIndexes = new Array;
  for (var i=0; i < oListbox.options.length; i++)
  {
      if (oListbox.options[i].selected) arrIndexes.push(i);
  }
  return arrIndexes;
};

// Функция получает id выбранных проектов из select
function getSelectedId (oListbox)
{
  var arrId = new Array;
  for (var i=0; i < oListbox.options.length; i++)
  {
      if (oListbox.options[i].selected) arrId.push(
          {id: oListbox.options[i].value, username: oListbox.options[i].innerHTML}
          );
  }
  return arrId;
};


class ToDoForm extends React.Component {

    constructor (props) {
        super(props)
        this.cookies = new Cookies()
        this.token = this.cookies.get('token')
        this.username = this.cookies.get('username')
        this.url_source = 'http://127.0.0.1:8000' 
        this.url_api = {
        'availableUsers': this.url_source + '/api/available/?project_id=',
        }
        this.otherData = {
            'projectInfo': {},
            'usersOnProject': [],
        }

        console.log(props);
        if (props.edit) {
            let id_todo = document.location.pathname.replaceAll('/tasks', '').replaceAll('/', '').trim();
            let todo = props.todo.filter((item) => item.id == id_todo)[0]
            let project = props.projects.filter((project) => project.id == todo.projectId['id'])[0]
            // console.log(todo)
            this.state = todo
            this.otherData['projectInfo'] = project
            // this.userOnTodoId = todo.userOnTodo.map((user) => user.id)
            this.state['usersOnProject'] = []

        } else {
            let id_project = document.location.pathname.replaceAll('projects/', '').replaceAll('/', '').replaceAll('taskscreate', '').trim()
            let project = props.projects.filter((item) => item.id == id_project)[0]
            this.otherData['projectInfo'] = project
            this.state = {  'actualDate': '',
                            'addDate': '', 
                            'description': '', 
                            'isActive': true, 
                            'isClose': false, 
                            'lastModified': '', 
                            'projectId': {'id':project.id, 'name': project.name}, 
                            'scheduledDate': '', 
                            'title': '', 
                            'userOnTodo': [],
                            'usersOnProject': []
                        }
        }    
    }

    is_authenticated() {
        return this.token != ''
    }

    get_headers() {
        let headers = {
          'Content-Type': 'application/json'
        }
        if (this.is_authenticated()) {
          headers['Authorization'] = 'Token ' + this.token
        }
        return headers
    }

    load_data() {
        const headers = this.get_headers()
        let availableUsers = `${this.url_api['availableUsers']}${this.state.projectId.id}`
        axios.get(availableUsers, {headers})
        .then(response => {
            console.log('данные')
            console.log(response.data)
            this.setState({
                    'usersOnProject': response.data
                }
            ) 
            console.log('данные load')
            console.log(this.state) 
        }).catch(error => {
            console.log(error)
            this.setState({
                'usersOnProject': []
            }
            ) 
        })
    }

    handleChange(event) {
        console.log(event.target.value)
        let value = event.target.value;
        if (event.target.type == 'checkbox') {
            value = event.target.checked;
        }

        this.setState(
            {
                [event.target.name]: value,
            }
        );
        console.log(this.state);

    }

    // Функция проверяет наличие элемента в массиве
    containsEl(arr, elem, from=null) {
        return arr.indexOf(elem, from) != -1;
    }


    checkOnToDo () {
        let usersInput = document.querySelector('.userLi')
        let allInput = usersInput.getElementsByTagName('input')
        console.log(allInput)
        //allInput.map((el) => {this.containsEl(this.state.userOnTodo, el.id) ? el.setAttribute("checked", "checked") : ''})
    }


    selectExecutor(event) {
        console.log(event.target.id)
        // Выбираем элемент списка li, чтобы в нем изменить класс для подсветки выбранного пользователя
        let curUser = document.querySelector('.u' + event.target.id)
        let input = curUser.getElementsByTagName('input')[0]
        console.log(input)
        let userCheckedCss = input.checked ? " userChecked" : ""
        //input.checked ? input.removeAttribute("checked") : input.setAttribute("checked", "checked")
        curUser.setAttribute("class", "userLi u" + event.target.id + userCheckedCss)
        // Обновляем данные в параметре userOnTodo
        let UsersTodo = document.querySelectorAll('.userLi')
        //console.log(UsersTodo)
        this.state.userOnTodo = []
        // this.userOnTodoId = [] // this.state.userOnTodo.map((user) => user.id)
        let s = UsersTodo.forEach((element) => element.childNodes[1].checked ? this.state.userOnTodo.push({id: element.childNodes[1].id, username: element.childNodes[0].data}) : null)
        console.log(this.state.userOnTodo)
        this.checkOnToDo()
    }

    handleSubmit(event) {
        // Тут сделал в 'лоб' нужные данные для отправки, т.к. не успевал
        console.log(this.state.userOnTodo)
        let arrayData = {   'actualDate': this.state.actualDate,
                            'addDate': this.state.addDate, 
                            'description': this.state.description, 
                            'isActive': this.state.isActive, 
                            'isClose': this.state.isClose, 
                            'projectId': this.state.projectId.id, 
                            'scheduledDate': this.state.scheduledDate, 
                            'title': this.state.title, 
                            'userOnTodo': this.state.userOnTodo,
                        }    

        if (!this.props.edit) {
            this.props.createToDo(arrayData)
        } else {
            console.log(this.state.id)
            this.props.editToDo(this.state.id, arrayData)
        }
        event.preventDefault()
    }

    componentDidMount() {
        this.load_data()
        // this.checkOnToDo()
    }

    render() {
        console.log('render');
        console.log(this.state);
        console.log(this.otherData)
        return(
            <form onSubmit={(event) => this.handleSubmit(event)}>
                <div>
                    <h2>{this.props.edit ? 'Редактирование задачи' : 'Создание новой задачи'} для проекта: {this.otherData.projectInfo.name} ({this.otherData.projectInfo.id})</h2>
                    
                </div>
                <div>
                    <label for='name'>Заголовок задачи:</label>
                    <input type='text' className="form-control" name="title" value={this.state.title} onChange={(event) => this.handleChange(event)}/> 
                </div>
                <div>
                    <label for='description'>Описание задачи:</label>
                    <textarea rows="4" cols="120" className="form-control" name='description' value={this.state.description} onChange={(event) => this.handleChange(event)}>

                    </textarea>
                </div>
                <div>
                    <label for='scheduledDate'>Ожидаемая дата завершения:</label>
                    <input type='datetime-local' className="form-control" name="scheduledDate" value={this.state.scheduledDate} onChange={(event) => this.handleChange(event)}/> 
                </div>
                <div>
                    <label for='actualDate'>Дата завершения работ по факту:</label>
                    <input type='datetime-local' className="form-control" name="actualDate" value={this.state.actualDate} onChange={(event) => this.handleChange(event)}/> 
                </div>
                <div>
                    <label for='addDate'>Дата и время добавления задачи:</label>
                    <input type='datetime-local' className="form-control" name="addDate" value={this.state.addDate} onChange={(event) => this.handleChange(event)}/> 
                </div>
                <div>
                    <label for='isActive'>Задача на исполнении</label>
                    <input type='checkbox' className="form-control" name="isActive" value={this.state.isActive} 
                    defaultChecked={this.state.isActive} onClick={(event) => this.handleChange(event)}/> 
                </div>
                <div>
                    <label for='isClose'>Задача завершена</label>
                    <input type='checkbox' className="form-control" name="isClose" value={this.state.isClose} 
                    defaultChecked={this.state.isClose} onClick={(event) => this.handleChange(event)}/> 
                </div>
                <div>
                    {/* {this.otherData.usersOnProject[0].id} */}
                    <label>Доступные пользователи на проекте:</label>
                    <ul>
                        {this.state.usersOnProject.map(
                            (curUser) => (
                                <>  
                                    <li className={'userLi u' + curUser.id + (this.containsEl(this.state.userOnTodo.map((el) => el.id), curUser.id) ? ' userChecked' : '')}>{curUser.user.username}
                                        <input type='checkbox' id={curUser.id} onChange={(event) => this.selectExecutor(event)} class='inputUser' 
                                         defaultChecked={(this.containsEl(this.state.userOnTodo.map((el) => el.id), curUser.id) ? true : false)}>
                                        </input>
                                    </li> 
                                </>
                                )
                            )}
                    </ul>
                </div>
                
                <h2>Дата последнего изменения: {this.state.lastModified}</h2>
                <button type="submit" className="btn_action_large">Сохранить</button>
            </form>   
        )
    }
}

export default ToDoForm