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
                {todo.is_active}
            </td>
            <td>
                {todo.add_date}
            </td>
        </tr>
    )
 }

const ProjectToDoList = ({todo_items}) => {
    let {id} = useParams();
    let filtered_Items = todo_items.filter((todo) => todo.project_id == id)
    console.log(`данные - ${todo_items}`)
    return (
        <div>
            Задачи не проекте № {id}:
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