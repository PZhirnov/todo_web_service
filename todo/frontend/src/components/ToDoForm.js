import React from "react";
import axios from "axios";
import Cookies from 'universal-cookie';

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
            this.state['projectInfo'] = project
            this.state['usersOnProject'] = []
            // this.load_data()
            //console.log('данные:')
            //console.log(this.state)    
            // // Выделим пользователей в select
            // let usersOnProjectId = project['userOnProject']
            // //console.log(usersList)
            // //SelectUsersOnProject(usersList, usersOnProjectId)

        } else {
            let id_project = document.location.pathname.replaceAll('projects/', '').replaceAll('/', '').replaceAll('taskscreate', '').trim()
            let project = props.projects.filter((item) => item.id == id_project)[0]
            //console.log(project)
            //console.log(project.id)
            this.state = {  actualDate: '',
                            addDate: '', 
                            description: '', 
                            isActive: true, 
                            isClose: false, 
                            lastModified: '', 
                            projectId: {'id':project.id, 'name': project.name}, 
                            scheduledDate: '', 
                            title: '', 
                            userOnTodo: [],
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
            //console.log('данные')
            //console.log(response.data)
            this.otherData(
            {
                'usersOnProject': response.data
            }
            )
            console.log('данные load')
            console.log(this.state) 
        }).catch(error => {
          console.log(error)
          this.otherData({usersOnProject: []})
        })
        


    }

    handleChange(event) {
        console.log(event.target.value)
        // // Получим массив id выбранных пользователей, чтобы потом добавить их на проект
        // let selectedUsers = document.getElementById('usersOnProject')
        // let idUsers = getSelectedId(selectedUsers)
        //console.log(event.target.name);
        //console.log(event.target.value);
        let value = event.target.value;
        if (event.target.type == 'checkbox') {
            value = event.target.checked;
        }

        this.setState(
            {
                [event.target.name]: value,
                //userOnProject: idUsers,
            }
        );
        console.log(this.state);
        // alert(this.token)
        // console.log(this.state.userOnProject);
    }

    selectExecutor(event) {
        console.log(event.target.id)
        // Выбираем элемент списка li, чтобы в нем изменить класс для подсветки выбранного пользователя
        let curUser = document.querySelector('.u' + event.target.id)
        let input = curUser.getElementsByTagName('input')[0]
        let userCheckedCss = input.checked ? " userChecked" : ""
        curUser.setAttribute("class", "userLi u" + event.target.id + userCheckedCss)
        // Обновляем данные в параметре userOnTodo
        let UsersTodo = document.querySelectorAll('.userLi')
        //console.log(UsersTodo)
        this.state.userOnTodo = []
        let s = UsersTodo.forEach((element) => element.childNodes[1].checked ? this.state.userOnTodo.push({id: element.childNodes[1].id, username: element.childNodes[0].data}) : null)
        console.log(this.state.userOnTodo)
    }




    handleSubmit(event) {
        let arrayData = this.state
        //delete arrayData['lastModified']
        //delete arrayData['projectInfo']
        //delete arrayData['usersOnProject']
        // arrayData.projectId = this.state.projectInfo.id
        //console.log('Массив:')
        //console.log(arrayData);
        //this.props.createToDo(arrayData)
        //event.preventDefault()
        if (!this.props.edit) {
            this.props.createToDo(arrayData)
        } else {
            console.log(this.state.id)
            this.props.editToDo(arrayData.id, arrayData)
        }
        event.preventDefault()
    }

    componentDidMount() {
        this.load_data()
    }

    render() {
        console.log('render');
        console.log(this.state);
        return(
            <form onSubmit={(event) => this.handleSubmit(event)}>
                <div>
                    <h2>{this.props.edit ? 'Редактирование задачи' : 'Создание новой задачи'} для проекта: {this.otherData.projectInfo.name} ({this.state.projectId.id})</h2>
                    
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
                    <input type='checkbox' className="form-control" name="isActive" value={this.state.isActive} onClick={(event) => this.handleChange(event)}/> 
                </div>
                <div>
                    <label for='isClose'>Задача завершена</label>
                    <input type='checkbox' className="form-control" name="isClose" value={this.state.isClose} onClick={(event) => this.handleChange(event)}/> 
                </div>
                <div>
                    
                    <label>Доступные пользователи на проекте:</label>
                    <ul>
                        {this.otherData.usersOnProject.map(
                            (curUser) => (
                                <>  
                                <li class={'userLi u' + curUser.id}>{curUser.user.username}
                                        <input type='checkbox' id={curUser.id} onClick={(event) => this.selectExecutor(event)}></input>
                                    </li> </>
                                )
                            )}
                    </ul>
                </div>
                
                <h2>Дата последнего изменения: {this.state.lastModified}</h2>
                <input type="submit" className="btn btn-primary" value="Сохранить" />
            </form>   
        )
    }
}

export default ToDoForm