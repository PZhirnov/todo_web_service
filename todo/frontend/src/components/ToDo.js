import React from 'react'


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

const ToDoList = ({todo_items}) => {
    console.log(todo_items)
    return (

        <div>
            <h1>Cписок заданий:</h1>
            <table>
                <th>
                    id
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
                    Закрыто
                </th>
                {todo_items.map((todo) => <ToDoItem todo={todo} />)}
            </table>
        </div>
            
    )
 }
 
 
 export default ToDoList
 