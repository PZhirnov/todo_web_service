import React from "react";
import { useParams } from 'react-router-dom';


const ToDoItem = ({todo}) => {
    return (
        <tr>
            <td>
                {todo.id}
            </td>
            <td>
                {todo.title}
            </td>
            <td>
                {todo.description}
            </td>
            <td>
                {todo.isActive}
            </td>
            <td>
                {todo.isClose}
            </td>
            <td>
                {todo.addDate}
            </td>
        </tr>
    )
 }

const ProjectToDoList = ({todo_items}) => {
    let {id} = useParams();
    let {title} = useParams();
    let filtered_Items = todo_items.filter((todo) => todo.projectId.id == id)
    console.log(`данные - ${id} ${todo_items}`)
    return (
        <div>
            <h1>Задачи на проекте '{title}' :</h1>
            <table>
                <tr>
                    <th>id</th>
                    <th>Заголовок задачи</th>
                    <th>Описание задачи</th>
                    <th>Статус выполнения</th>
                    <th>Дата добавления</th>
                </tr>
                {filtered_Items.map((todo) => <ToDoItem todo={todo} />)}
            </table>   
        </div>
        
    )
}

export default ProjectToDoList