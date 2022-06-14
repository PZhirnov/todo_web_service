import React from 'react'
import { Link, button } from 'react-router-dom';

const DateFormat = {
    OnlyDate: function OnlyDate(props) {
        if (props.datetime) {
            let date = new Date(props.datetime);
            let result = date.toLocaleDateString();
            return <p>{result}</p>  
        } else {
            return <p>n/a</p>
        }
        
    },
    OnlyDateTime: function OnlyDateTime(props) {
        if (props.datetime) {
            let date = new Date(props.datetime);
            let result = date.toLocaleString();
            return <p>{result}</p>  
        } else {
            return <p>n/a</p>
        }
    }
}



const ToDoItem = ({todo, projects, deleteToDo}) => {

    function getProjectName(id) {
        console.log(todo)
        console.log(projects)
        let nameProject = projects.filter(project => project.id == id)[0];
        return nameProject.name
    }
    
    return (
            <tr>
                <td>
                    {todo.id}
                </td>
                <td>
                    {todo.projectId.name} ({todo.projectId.id})
                </td>
                <td>
                    {todo.title}
                </td>
                <td>
                    {todo.description}
                </td>
                <td>
                    {todo.isActive ? <p>да</p>: <p>нет</p>}
                </td>
                <td>
                    {todo.isClose ? <p>да</p>: <p>нет</p>}
                </td>
                <td>
                    <DateFormat.OnlyDateTime datetime={todo.scheduledDate} />
                </td>
                <td>
                    <DateFormat.OnlyDateTime datetime={todo.actualDate} />
                </td>
                <td>
                    <DateFormat.OnlyDate datetime={todo.addDate} />
                </td>
                <td>
                    <ul>
                      {todo.userOnTodo.map((user) => <li class="userSmall">{user.user.username}</li>)}  
                    </ul>
                    
                </td>
                <td>
                    <button type="button" onClick={() => deleteToDo(todo.id)} class='btn_action'>Удалить</button>
                    <Link to={`tasks/${todo.id}`} class="btn btn-dark">Редактировать</Link>
                </td>
            </tr>
    )
    }

const ToDoList = ({todo_items, projects, deleteToDo}) => {
    // console.log(todo_items)
    return (

        <div>
            <h1>Cписок заданий:</h1>
            <table>
                <th>
                    id
                </th>
                <th>
                    Наименование проекта (ID)
                </th>

                <th>
                    Заголовок
                </th>
                <th>
                    Описание
                </th>
                <th>
                    Активное
                </th>
                <th>
                    Закрыта
                </th>
                <th>
                    Плановая дата закрытия
                </th>
                <th>
                    Фактическая дата закрытия
                </th>
                <th>
                    Дата добавления
                </th>
                <th>
                    Исполнители
                </th>
                <th>
                    Действия
                </th>
                {todo_items.map((todo) => <ToDoItem todo={todo} projects={projects} deleteToDo={deleteToDo}/>)}
            </table>
        </div>
            
    )
 }
 
 
 export default ToDoList
 